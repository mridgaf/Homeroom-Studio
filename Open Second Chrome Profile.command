#!/bin/bash
# Opens Chrome in a NEW separate profile called "Secondary Loops".
# First time: Chrome creates the profile. After that: it just opens it.
# Your normal Chrome and its logins are not touched.
open -na "Google Chrome" --args --profile-directory="Secondary Loops" "https://www.looperman.com/account/login" "https://freesound.org/home/login/"
echo "Chrome is opening in the new profile. You can close this window."
