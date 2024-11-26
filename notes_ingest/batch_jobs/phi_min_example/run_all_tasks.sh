#!/bin/bash
set -e
# Specify the directory containing the JSON files
FOLDER_PATH="/home/andrey239/batch_phi_min/small_job/jsons/"
JOB_ID="phi-min-small"

# Loop through all files in the specified folder
for file in "$FOLDER_PATH"/*; do
    if [[ -f $file ]]; then  # Check if it's a file (not a subdirectory)
        echo "Processing file: $file"
        
        # Run the az batch task create command
        az batch task create --job-id $JOB_ID --json-file "$file"
        
        # Check if the command was successful
        if [[ $? -eq 0 ]]; then
            echo "Successfully created task for $file"
        else
            echo "Failed to create task for $file"
        fi
    fi
done
