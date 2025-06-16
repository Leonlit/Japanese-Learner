#!/bin/bash

currentDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
serverDir=$( cd -- "${currentDir}/../" &> /dev/null && pwd )
logsDir="${serverDir}/debugLogs"

mkdir -p "$logsDir"

# Start the python server and save its PID
echo "Starting Python server from $serverDir..."
source "$serverDir/.venv/bin/activate" || { echo "Failed to activate virtual environment"; exit 1; }
nohup python -u "$serverDir/server.py" >> "$logsDir/pythonServer.log" 2>> "$logsDir/pythonError.log" &
pythonPid=$!
if [ $? -ne 0 ]; then
    echo "Failed to start the Python server."
    exit 1
fi
echo "Python server started with PID $pythonPid. Logs are in ${logsDir}."

# Save PIDs to a file in the initial directory
pidFile="$serverDir/process_pids.txt"
echo "$pythonPid" >> "$pidFile"
echo "Process started. PIDs saved to $pidFile."
