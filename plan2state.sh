#!/bin/sh
# This script converts output from FF planner into
# objects' current state as if the plan was executed successfuly

cat | egrep '^\s*[0-9]+:' | awk -F: '{print $2}' | sed 's/^ //' | \
  tr '[:upper:]' '[:lower:]' | \
  sed -e 's/create-/created-/' -e 's/attach-/attached-/' \
    -e 's/mount-/mounted-/' -e 's/install-/installed-/' \
    -e 's/start-/running-/' -e 's/created-dir/exists-dir/'
