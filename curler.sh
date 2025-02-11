#!/bin/bash
set -uex

# Check if a filename is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

filename=$1

# Loop through the CSV file
while IFS=, read -r url_col file_col xpath_col; do
  if [[ "${url_col}" != "URL" ]]; then
    # Use xargs as it cleans up the strings along the way.
    echo "${url_col} -o working-copy/${file_col}.html" | xargs curl
  fi
done < "$filename"