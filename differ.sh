#!/bin/bash

# Check if a filename is provided as an argument.
if [ $# -eq 0 ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

filename=$1

# Loop through the CSV file and diff the text files.
while IFS=, read -r url_col file_col xpath_col; do
  if [[ "$url_col" != "URL" ]]; then
    echo "Finding differences for ${url_col}:"
    diff "reference/${file_col}.txt" "working-copy/${file_col}.txt" >> changedlines.txt
    diff -u "reference/${file_col}.txt" "working-copy/${file_col}.txt"
  fi
done < "$filename"

# Loop through the CSV file and diff the HTML files.
# This is not DRY, but makes the output easier to read.
while IFS=, read -r url_col file_col xpath_col; do
  if [[ "$url_col" != "URL" ]]; then
    echo "Finding differences for ${url_col}:"
    diff "reference/${file_col}-distilled.html" "working-copy/${file_col}-distilled.html" >> changedlines.txt
    diff -u "reference/${file_col}-distilled.html" "working-copy/${file_col}-distilled.html"
  fi
done < "$filename"

changed_lines=$(wc -l < changedlines.txt)
if (( changed_lines > 0 )); then
    echo "::notice ::There is a difference in the files."
    echo "ALERT: 🎉 🥳 There are some changed lines."
else
    echo "::notice ::The files are the same."
    echo "⛴️ There are zero changed lines. 0️⃣"
fi

rm changedlines.txt
