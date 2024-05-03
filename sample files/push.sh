#!/bin/sh
eval `ssh-agent -s`
ssh-add ~/.ssh/rpi558010ed25519
git push origin main