#!/usr/bin/env python3
"""Nightly Looperman loop fetcher for Homeroom Studio.

What it does (owner spec, 2026-09-19):
  * Runs at 4 a.m. (launchd) - logs in to Looperman with the owner's account.
  * Picks tonight's theme from a 4-day rotation.
  * Downloads up to 45 NEW loops for that theme (Looperman blocks ~48/day).
  * Skips loops already in the library, noise/FX/riser loops, drums.
  * Files them in a REVIEW folder, never straight into the main library:
        <BOTC Sorted Loops>/_New Tonight/<date>/<Melody|Chords>/
  * Writes a short morning note to  Homeroom Studio/Nightly Loops/LATEST.txt

Standard library only. Python 3.9 compatible (macOS Command Line Tools python).

Modes:
  --check-login   log in, say whether it worked, download nothing
  --dry-run       log in, search, list what WOULD be downloaded, download nothing
  --count N       download N loops instead of 45 (use 5 for the first test)
  --respect-window  stop starting new downloads after 05:55 local time
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import html as htmllib
import http.cookiejar
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------- settings
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB_ROOT = os.environ.get(
    "LOOPS_LIB_ROOT", "/Volumes/TBOTC 3/Sample Packs/BOTC Sorted Loops")
REVIEW_NAME = "_New Tonight"
NOTES_DIR = os.path.join(PROJECT, "Nightly Loops")
STATE_PATH = os.path.join(NOTES_DIR, ".nightly_state.json")
ACCOUNT_PATH = os.path.join(NOTES_DIR, ".looperman_account")  # email only
KEYCHAIN_SERVICE = "HomeroomStudio Looperman"

BASE = "https://www.looperman.com"
USER_AGENT = "HomeroomStudio-NightlyLoops/1.0 (personal use, logged-in account)"
NIGHTLY_COUNT = 45          # site blocks around 48 per 24h
DOWNLOAD_DELAY = 12         # seconds between downloads
PAGE_DELAY = 3              # seconds between page fetches
MAX_PER_UPLOADER = 5        # variety, same habit as earlier batches
DEADLINE = (5, 55)          # with --respect-window
ROLE_FOLDERS = ["Melody", "Chords", "Bass", "Drums", "Vocals", "Guitars"]

# One theme per night, rotating. Drums are deliberately not fetched
# (ASSUMING, matches every earlier batch: "No Drums").
THEMES = [
    {"name": "Hip-hop / boom bap",
     "keywords": ["boom bap", "hip hop", "dusty", "jazzy"]},
    {"name": "Trap / drill",
     "keywords": ["trap", "drill", "dark", "plugg"]},
    {"name": "Lo-fi / chill",
     "keywords": ["lofi", "chill", "mellow", "dreamy"]},
    {"name": "Soul / R&B / gospel",
     "keywords": ["soul", "rnb", "gospel", "neo soul"]},
]
# Looperman category ids (from the owner's earlier sourcing notes):
# 3 Guitar Electric, 4 Synth, 10 Strings, 11 Pad, 21 Piano.
CATEGORIES = [4, 11, 21, 3, 10]

NOISE_RE = re.compile(
    r"\b(noise|rain|wind|fx|sfx|riser|risers|foley|whoosh|sweep|ambience)\b", re.I)
DRUM_RE = re.compile(r"\b(drums?|drum loops?|hi-?hats?|kick|snare|percussion)\b", re.I)
NONCOMMERCIAL_RE = re.compile(
    r"(non[- ]?commercial|no[- ]?deriv|CC[ -]BY[ -]?(NC|ND))", re.I)
ID_IN_NAME_RE = re.compile(r"looperman-l-\d+-(\d{7})-")


# ---------------------------------------------------------------- pure helpers
def theme_for(date):
    """Tonight's theme. Rotates daily, same answer for the same date."""
    return THEMES[date.toordinal() % len(THEMES)]


def norm_key(raw):
    """'D#' -> 'D#', 'fm' -> 'Fm', 'A minor' -> 'Am', 'Unknown' -> None."""
    if not raw:
        return None
    raw = raw.strip()
    if raw.lower() in ("unknown", "none", "n/a", "-", ""):
        return None
    m = re.fullmatch(r"([A-Ga-g])([#b♯♭]?)\s*(maj(?:or)?|min(?:or)?|m)?", raw)
    if not m:
        return None
    tone = m.group(1).upper()
    acc = {"♯": "#", "♭": "b"}.get(m.group(2), m.group(2))
    mode = (m.group(3) or "").lower()
    minor = mode.startswith("m") and not mode.startswith("maj")
    return tone + acc + ("m" if minor else "")


def clean_slug(slug):
    """Drop tempo-looking tokens so the engine (which takes the FIRST bpm-like
    token in a filename) never reads a stray number as the tempo."""
    out = []
    for tok in [t for t in slug.lower().split("-") if t]:
        if re.fullmatch(r"\d+", tok) and 50 <= int(tok) <= 220:
            continue
        if re.fullmatch(r"\d{2,3}bpm", tok) or tok == "bpm":
            continue
        out.append(tok)
    return "-".join(out)[:60].strip("-") or "loop"


def make_filename(user, id7, slug, key, bpm):
    """looperman-l-<user>-<id7>-<slug>_<Key>[_nokey][_<BPM>bpm].wav"""
    parts = [key or "C"]
    if not key:
        parts.append("nokey")
    if bpm:
        parts.append("%dbpm" % bpm)
    return "looperman-l-%s-%s-%s_%s.wav" % (user, id7, clean_slug(slug), "_".join(parts))


def role_for(cid, title):
    t = title.lower()
    if re.search(r"\b(chords?|pads?|strings?|orchestra\w*)\b", t) or cid in (10, 11):
        return "Chords"
    return "Melody"


def skip_reason(title, tags_text, license_text):
    """Return a reason to skip, or None. Owner rules: no noise/FX/risers, no drums."""
    blob = title + " " + tags_text
    if NOISE_RE.search(blob):
        return "noise/fx/riser"
    if DRUM_RE.search(blob):
        return "drums"
    if NONCOMMERCIAL_RE.search(license_text):
        return "non-commercial or no-derivatives licence"
    return None


def ids_in_names(names):
    found = set()
    for n in names:
        m = ID_IN_NAME_RE.search(n)
        if m:
            found.add(m.group(1))
    return found


def strip_tags(page):
    page = re.sub(r"(?is)<(script|style).*?</\1>", " ", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    return re.sub(r"\s+", " ", htmllib.unescape(page))


def parse_list(page):
    """Ordered unique [(id7digits, slug)] from a Looperman list page."""
    seen, out = set(), []
    for lid, slug in re.findall(r"/loops/detail/(\d+)/([a-z0-9\-]+)", page):
        if lid not in seen:
            seen.add(lid)
            out.append((lid, slug))
    return out


def parse_detail(page, slug):
    """Key, BPM, uploader, 7-digit id, download link from a loop's page."""
    text = strip_tags(page)
    key = None
    m = re.search(r"Key\s*:\s*([A-G][#b]?(?:maj(?:or)?|min(?:or)?|m)?)(?![A-Za-z0-9#])", text)
    if m:
        key = norm_key(m.group(1))
    bpm = None
    tags = ""
    mt = re.search(r"Tags\s*:(.{0,220})", text)
    if mt:
        tags = mt.group(1)
        mb = re.search(r"(\d{2,3})\s*bpm", tags, re.I)
        if mb:
            bpm = int(mb.group(1))
    user = id7 = None
    mm = re.search(r"/media/loops/(\d+)/looperman-l-(\d+)-(\d{7})-", page)
    if mm:
        user, id7 = mm.group(2), mm.group(3)
    href = None
    md = re.search(r'href=["\']([^"\']*getfiles/loops[^"\']*)["\']', page)
    if md:
        href = urllib.parse.urljoin(BASE + "/", htmllib.unescape(md.group(1)))
    return {"key": key, "bpm": bpm, "tags": tags, "user": user, "id7": id7,
            "href": href, "text": text}


def _attrs(tag):
    return {m.group(1).lower(): htmllib.unescape(m.group(3) if m.group(3) is not None else m.group(4))
            for m in re.finditer(r"([\w-]+)\s*=\s*(\"([^\"]*)\"|'([^']*)')", tag)}


def parse_login_form(page):
    """Hidden tokens + checkbox/button values from the login page."""
    hidden, checks, submit = {}, {}, ("submit", "Login")
    for tag in re.findall(r"<input\b[^>]*>", page):
        a = _attrs(tag)
        if a.get("type") == "hidden" and a.get("name"):
            hidden[a["name"]] = a.get("value", "")
        elif a.get("type") == "checkbox" and a.get("name"):
            checks[a["name"]] = a.get("value", "on")
    for tag in re.findall(r"<button\b[^>]*>", page):
        a = _attrs(tag)
        if a.get("type") == "submit" and a.get("name"):
            submit = (a["name"], a.get("value", "Login"))
    return hidden, checks, submit


def classify_download(status, body):
    """'ok' | 'cap' (daily limit) | 'wait' (1-minute throttle) | 'fail'."""
    head = body[:2000].decode("latin-1", "ignore").lower()
    if "24 hours" in head or (status == 429 and "24" in head):
        return "cap"
    if body[:4] == b"RIFF" and len(body) > 1000:
        return "ok"
    if len(body) < 1000 and "minute" in head:
        return "wait"
    return "fail"


# ---------------------------------------------------------------- network
class Session:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.opener.addheaders = [("User-Agent", USER_AGENT),
                                  ("Accept-Language", "en-US,en;q=0.9")]

    def _do(self, req):
        try:
            with self.opener.open(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except (urllib.error.URLError, OSError) as e:
            return 0, str(e).encode()

    def get(self, url, referer=None):
        req = urllib.request.Request(url)
        if referer:
            req.add_header("Referer", referer)
        return self._do(req)

    def post(self, url, fields, referer=None):
        req = urllib.request.Request(url, data=urllib.parse.urlencode(fields).encode())
        if referer:
            req.add_header("Referer", referer)
        return self._do(req)


def get_password(email):
    r = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE,
                        "-a", email, "-w"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def read_email():
    try:
        with open(ACCOUNT_PATH) as f:
            return f.read().strip() or None
    except OSError:
        return None


def login(sess):
    """Returns (ok, message)."""
    email = read_email()
    if not email:
        return False, "No saved Looperman email. Double-click 'Save Looperman Login.command'."
    password = get_password(email)
    if not password:
        return False, "Could not read the saved password from the Mac Keychain."
    login_url = BASE + "/account/login"
    status, body = sess.get(login_url)
    if status != 200:
        return False, "Login page did not load (status %s)." % status
    hidden, checks, submit = parse_login_form(body.decode("utf-8", "ignore"))
    if not hidden:
        return False, "Login page had no security tokens - the site layout may have changed."
    fields = dict(hidden)
    fields.update({"user_email": email, "upass": password})
    fields.update(checks)                     # terms + remember-me boxes ticked
    fields[submit[0]] = submit[1]
    status, _ = sess.post(login_url, fields, referer=login_url)
    status, body = sess.get(login_url)        # logged-in users don't get the form
    page = body.decode("utf-8", "ignore")
    if 'name="upass"' in page or "name='upass'" in page:
        return False, "Looperman did not accept the login (wrong password, or it blocks scripts)."
    return True, "Logged in."


# ---------------------------------------------------------------- state / drive
def load_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"seen": {}, "history": []}


def save_state(state):
    os.makedirs(NOTES_DIR, exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
    os.replace(tmp, STATE_PATH)


def drive_ok():
    return (os.path.isdir(LIB_ROOT)
            and os.path.isfile(os.path.join(LIB_ROOT, "READ ME.txt"))
            and os.path.isdir(os.path.join(LIB_ROOT, "Chords")))


def library_ids():
    names = []
    for role in ROLE_FOLDERS:
        p = os.path.join(LIB_ROOT, role)
        try:
            names.extend(os.listdir(p))
        except OSError:
            pass
    for root, _dirs, files in os.walk(os.path.join(LIB_ROOT, REVIEW_NAME)):
        names.extend(files)
    return ids_in_names(names)


def size_index():
    """size -> [paths] for existing looperman files (cheap duplicate check)."""
    idx = {}
    dirs = [os.path.join(LIB_ROOT, r) for r in ("Melody", "Chords", "Bass", "Vocals")]
    for root, _d, files in os.walk(os.path.join(LIB_ROOT, REVIEW_NAME)):
        dirs.append(root)
    for d in dirs:
        try:
            for n in os.listdir(d):
                if n.startswith("looperman-l-"):
                    p = os.path.join(d, n)
                    idx.setdefault(os.path.getsize(p), []).append(p)
        except OSError:
            pass
    return idx


def md5_of(path_or_bytes):
    h = hashlib.md5()
    if isinstance(path_or_bytes, bytes):
        h.update(path_or_bytes)
    else:
        with open(path_or_bytes, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- main run
def candidates(sess, theme):
    """Lazy stream of (id, slug, cid) - page 1 of everything first, then page 2..."""
    for page_no in (1, 2, 3):
        for kw in theme["keywords"]:
            for cid in CATEGORIES:
                url = "%s/loops?page=%d&cid=%d&order=3&keys=%s&dir=d" % (
                    BASE, page_no, cid, urllib.parse.quote(kw))
                time.sleep(PAGE_DELAY)
                status, body = sess.get(url)
                if status != 200:
                    continue
                for lid, slug in parse_list(body.decode("utf-8", "ignore")):
                    yield lid, slug, cid


def past_deadline():
    now = datetime.datetime.now()
    return (now.hour, now.minute) >= DEADLINE


def run(args):
    today = datetime.date.today()
    theme = theme_for(today)
    note = ["Nightly loops - %s" % today.isoformat(), "Theme: %s" % theme["name"]]
    filed, skipped, stop_reason = {}, {}, None

    def finish(code):
        total = sum(filed.values())
        note.append("Filed: %d (%s)" % (total, ", ".join("%s %d" % kv for kv in sorted(filed.items())) or "none"))
        if skipped:
            note.append("Skipped: " + ", ".join("%s %d" % kv for kv in sorted(skipped.items())))
        if stop_reason:
            note.append("Stopped: " + stop_reason)
        target = 0 if args.check_login else args.count
        if not args.dry_run and not args.check_login and total < target:
            note.append("Short of target by %d." % (target - total))
        text = "\n".join(note) + "\n"
        print(text)
        if not args.dry_run:
            os.makedirs(NOTES_DIR, exist_ok=True)
            for name in ("NIGHTLY-%s.txt" % today.isoformat(), "LATEST.txt"):
                with open(os.path.join(NOTES_DIR, name), "w") as f:
                    f.write(text)
        return code

    if not args.check_login and not drive_ok():
        stop_reason = ("The loop drive is not reachable at %s. Nothing was downloaded "
                       "and nothing was saved anywhere else." % LIB_ROOT)
        return finish(2)

    sess = Session()
    ok, msg = login(sess)
    note.append("Login: " + msg)
    if not ok:
        stop_reason = "login failed"
        return finish(1)
    if args.check_login:
        return finish(0)

    state = load_state()
    seen = set(state["seen"]) | library_ids()
    sizes = size_index()
    per_uploader = {}
    review_dir = os.path.join(LIB_ROOT, REVIEW_NAME, today.isoformat())
    target = args.count
    got = 0
    checked_link = False

    for lid, slug, cid in candidates(sess, theme):
        if got >= target:
            break
        if args.respect_window and past_deadline():
            stop_reason = "reached the 5:55 a.m. cutoff"
            break
        if lid in seen:
            continue
        seen.add(lid)
        time.sleep(PAGE_DELAY)
        status, body = sess.get("%s/loops/detail/%s/%s" % (BASE, lid, slug))
        if status != 200:
            continue
        d = parse_detail(body.decode("utf-8", "ignore"), slug)
        if not checked_link:
            checked_link = True
            if not d["href"]:
                stop_reason = "no download link on the loop page - login did not stick"
                break
        title = slug.replace("-", " ")
        reason = skip_reason(title, d["tags"], d["text"][:3000])
        if not reason and not (d["href"] and d["user"] and d["id7"]):
            reason = "page missing download link or ids"
        if not reason and per_uploader.get(d["user"], 0) >= MAX_PER_UPLOADER:
            reason = "uploader limit"
        if reason:
            skipped[reason] = skipped.get(reason, 0) + 1
            state["seen"][lid] = "skipped: " + reason
            continue
        role = role_for(cid, title)
        name = make_filename(d["user"], d["id7"], slug, d["key"], d["bpm"])
        if args.dry_run:
            print("WOULD FILE  %s/%s" % (role, name))
            got += 1
            filed[role] = filed.get(role, 0) + 1
            continue

        for attempt in range(2):
            time.sleep(DOWNLOAD_DELAY)
            status, data = sess.get(d["href"], referer="%s/loops/detail/%s/%s" % (BASE, lid, slug))
            verdict = classify_download(status, data)
            if verdict == "wait" and attempt == 0:
                time.sleep(68)
                continue
            break
        if verdict == "cap":
            stop_reason = ("Looperman's daily download limit was reached after %d loops. "
                           "If this says 0, other downloads today (e.g. a Chrome batch) "
                           "probably used it up. Try again tomorrow." % got)
            seen.discard(lid)
            break
        if verdict != "ok":
            skipped["download failed"] = skipped.get("download failed", 0) + 1
            continue
        dup = any(md5_of(p) == md5_of(data) for p in sizes.get(len(data), []))
        if dup:
            skipped["duplicate file"] = skipped.get("duplicate file", 0) + 1
            state["seen"][lid] = "skipped: duplicate file"
            continue
        os.makedirs(os.path.join(review_dir, role), exist_ok=True)
        dest = os.path.join(review_dir, role, name)
        with open(dest + ".part", "wb") as f:
            f.write(data)
        os.replace(dest + ".part", dest)
        sizes.setdefault(len(data), []).append(dest)
        per_uploader[d["user"]] = per_uploader.get(d["user"], 0) + 1
        state["seen"][lid] = "filed"
        filed[role] = filed.get(role, 0) + 1
        got += 1
        if not d["key"]:
            note.append("No key on Looperman, named C + nokey: %s" % name)
        save_state(state)

    if got < target and not stop_reason:
        stop_reason = "ran out of matching loops in the search results"
    if not args.dry_run:
        state["history"].append({"date": today.isoformat(), "theme": theme["name"],
                                 "filed": got, "stopped": stop_reason})
        state["history"] = state["history"][-60:]
        save_state(state)
    return finish(0)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check-login", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--count", type=int, default=NIGHTLY_COUNT)
    ap.add_argument("--respect-window", action="store_true")
    args = ap.parse_args(argv)
    args.count = max(1, min(args.count, NIGHTLY_COUNT))
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
