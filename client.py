#!/usr/bin/env python3

import re
import subprocess
import sys
import time
from config import SSH_KEY_PATH, SSH_HOST, REMOTE_DIR

SSH_COMMAND = ['ssh', '-i', SSH_KEY_PATH, SSH_HOST]
POLL_INTERVAL = 1

def getFileNameFromUser():
    while True:
        filename = input("Enter the file name to monitor: ")
        if isValidFileName(filename):
            return filename
        print("Invalid file name. Use letters, numbers, underscores, or * for wildcards.")

def isValidFileName(filename):
    pattern = r'^[a-zA-Z0-9_*]+$'
    return bool(re.match(pattern, filename))


def getWaitTimeFromUser():
    while True:
        wait_time_input = input("How many seconds to wait? ")
        try:
            wait_time = int(wait_time_input)
            if 1 <= wait_time <= 6000:
                return wait_time
        except ValueError:
            pass
        print("Enter a number between 1 and 6000.")


def checkFileExists(filename):
    ssh_command = SSH_COMMAND + ['test -e ' + REMOTE_DIR + '/' + filename]
    try:
        result = subprocess.run(ssh_command, capture_output=True, check=False)
        if result.returncode == 0:
            return True, ""
        elif result.returncode == 1:
            return False, ""
        else:
            error_msg = result.stderr.decode().strip()
            return False, "SSH Error: " + error_msg
    except Exception as e:
        return False, "Connection Error: " + str(e)


def waitForFile(filename, max_seconds):
    elapsed_time = 0
    
    while elapsed_time < max_seconds:
        file_exists, error_message = checkFileExists(filename)
        
        if error_message:
            print(error_message)
            return False
            
        if file_exists:
            print("File " + filename + " arrived in server after " + str(elapsed_time) + " seconds")
            return True
            
        if elapsed_time < max_seconds - 1:
            time.sleep(POLL_INTERVAL)
        elapsed_time += 1
    
    print("Timeout")
    return False


def main():
    filename = getFileNameFromUser()
    max_wait_seconds = getWaitTimeFromUser()
    
    print("Monitoring for file '" + filename + "' on remote server...")
    print("Maximum wait time: " + str(max_wait_seconds) + " seconds")
    print("Checking every " + str(POLL_INTERVAL) + " second(s)")
    print()
    
    success = waitForFile(filename, max_wait_seconds)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()