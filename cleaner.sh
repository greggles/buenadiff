#!/bin/bash
set -uex

# Deletes out files that accumulate during normal operation of the tool.
# Useful to get back to a clean state.

# This required argument helps ensure the script is only run intentionally.
if [ $# -eq 0 ]; then
  echo "Usage: $0 deletemystuff"
  exit 1
fi

if [$1 != "deletemystuff"]; then
  echo "Since this script is destructive you have to type $0 deletemystuff"
  exit 1
fi

rm reference/*.html
rm reference/*.txt
rm working-copy/*.html
rm working-copy/*.txt
rm url_data.csv

echo "Deleted stuff to get back to a clean state."