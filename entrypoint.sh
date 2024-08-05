#!/bin/bash

# Function to activate the virtual environment and run a Python script
run_python_script() {
    echo 'Activating virtual environment...'
    source /app/envsubtrans/bin/activate
    python3 "$1" "${@:2}"
    echo 'Deactivating virtual environment...'
    deactivate
}

# Check if the input is a directory or a file
if [ -d "$1" ]; then
    run_python_script /app/scripts/folder-subtrans.py "$@"
elif [ -f "$1" ]; then
    run_python_script /app/scripts/gpt-subtrans.py "$@"
else
    echo 'Invalid input. Please provide a file or directory.'
    exit 1
fi
