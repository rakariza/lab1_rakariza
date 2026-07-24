#!/usr/bin/env bash

# Archive grades.csv with a timestamp and prepare a new empty workspace file.

archive_directory="archive"
source_file="grades.csv"
log_file="organizer.log"

if [ ! -f "$source_file" ]; then
    echo "Error: $source_file was not found. Nothing was archived."
    exit 1
fi

timestamp=$(date +"%Y%m%d-%H%M%S")
archived_file="grades_${timestamp}.csv"

mkdir -p "$archive_directory"

if ! mv "$source_file" "$archive_directory/$archived_file"; then
    echo "Error: $source_file could not be archived."
    exit 1
fi

if ! touch "$source_file"; then
    echo "Error: A new $source_file could not be created."
    exit 1
fi

printf "%s | original: %s | archived: %s\n" \
    "$timestamp" "$source_file" "$archived_file" >> "$log_file"

echo "$source_file was archived as $archive_directory/$archived_file."
echo "A new empty $source_file was created."
echo "The operation was recorded in $log_file."
