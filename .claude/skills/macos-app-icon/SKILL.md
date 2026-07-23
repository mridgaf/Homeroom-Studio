---
name: macos-app-icon
description: Safely change the icon of a macOS .app (like the Beat Machine launcher) without breaking the app or scrambling its icon in Finder. Use whenever asked to set, change, restore, or fix an app icon, or when an app shows a blank/wrong icon or won't open after an icon change. The safe method swaps only icon.icns inside the bundle; the trap is the Finder "paste custom icon" trick, which confuses the LaunchServices/icon cache.
---

# macOS App Icon — the safe swap only

The owner's app (e.g. Beat Machine) is a tiny launcher whose only job is to
`open -a Terminal <…>.command`. Its program is trivial and must not be
touched. Icon changes have twice caused blank icons and "won't open"
confusion. This skill is the safe path.

## Do this

Replace the icon **file** inside the bundle, nothing else:
`<App>.app/Contents/Resources/icon.icns` (confirm the real name in
`Contents/Info.plist` under `CFBundleIconFile`). A plain file replacement
can't affect launching. Keep a byte-for-byte backup of the original `.icns`
first so you can restore it exactly.

## Never do this

The Finder **Get Info → paste custom icon** trick (which writes an `Icon\r`
resource + a custom-icon flag). That's what scrambled the bundle before: it
confuses macOS's **LaunchServices / icon cache**, giving a blank icon and a
Get Info window that shows stale, misleading state. Pasting then deleting the
custom icon is exactly the misstep that broke things — don't repeat it.

## If the icon is already confused

It's a cache problem, not damage to the app. In order of least disruption:
- `touch` the .app bundle and re-open, or
- `killall Finder`, or
- **restart / log out and back in** — the reliable fix; it rebuilds the icon
  cache and re-registers the app.
Then cancel any stray "Open" dialogs from background apps.

## Verify from the filesystem, not Get Info

Get Info can show stale cached state. Confirm the true state by reading the
bundle on disk: that `icon.icns` is the intended file (or byte-identical to
the backup), the launcher script is intact and executable, and no
`Icon\r`/custom-icon file remains. Trust the filesystem over the window.
