#!/bin/bash
cd /biomappings
git remote set-url origin git@github.com:$GITHUBUSER/biomappings.git
git checkout -b curation
biomappings web