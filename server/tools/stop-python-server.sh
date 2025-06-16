#!/bin/bash

# Get the process PID file and Docker service names from the command line
currentDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
serverDir=$( cd -- "${currentDir}/../" &> /dev/null && pwd )
pidFile="$serverDir/process_pids.txt"


# Check if PID file exists
if [ ! -f "$pidFile" ]; then
    echo "PID file not found. Processes might not be running."
    exit 1
fi

# Read and kill processes
while read -r pid; do
    # Skip empty lines
    if [ -z "$pid" ]; then
        continue
    fi
    
    if kill -0 "$pid" 2>/dev/null; then
        echo "Stopping process with PID $pid..."
        kill "$pid"
    else
        echo "Process with PID $pid is not running."
    fi
done < "$pidFile"

# Remove the PID file
rm -f "$pidFile"
echo "All processes stopped and PID file removed."