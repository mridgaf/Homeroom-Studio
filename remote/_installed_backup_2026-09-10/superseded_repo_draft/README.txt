The files that WERE in remote/ until 2026-09-10. Never installed successfully:
 - ReasonVoice.luacodec held remote_init (the logic), NOT remote_supported_control_surfaces
   (the manifest) -- Reason ignores such a codec silently.
 - ReasonVoice.remotemap declared File Format Version 1.3 and one document-wide scope using
   'Select Next Patch for Target Device', which the reason-remote-bridge skill records as
   NOT verified. The working map uses 1.0.0 and 13 per-device scopes.
Kept for reference only. Do not reinstall.
