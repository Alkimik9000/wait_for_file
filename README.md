# Wait for File
Python script that monitors a remote EC2 server for file creation via SSH.

## Setup

1. Copy the example configuration:
   ```bash
   cp config.py.example config.py
   ```

2. Edit `config.py` with your actual SSH credentials:
   - `SSH_KEY_PATH`: Path to your SSH private key
   - `SSH_HOST`: Username and server IP (e.g., 'ubuntu@51.20.1.114') 
   - `REMOTE_DIR`: Remote directory to monitor (e.g., '/home/ubuntu')

   Example final `config.py`:
   ```python
   SSH_KEY_PATH = '/home/user/.ssh/my-ec2-key.pem'
   SSH_HOST = 'ubuntu@51.20.1.114'
   REMOTE_DIR = '/home/ubuntu'
   ```

## Usage

```bash
python3 client.py
```

Follow the prompts to enter:
- File name to monitor (supports wildcards with *)
- Wait time in seconds (1-6000)

## Security

The `config.py` file is excluded from git to protect sensitive credentials.
