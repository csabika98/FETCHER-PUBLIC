V2!!
![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/v2_1.png?raw=true)
![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/v2_2.png?raw=true)
![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/v2_3.png?raw=true)
![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/v2_4.png?raw=true)



![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/1.png?raw=true)
![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/2.png?raw=true)
![alt text](https://github.com/csabika98/FETCHER/blob/main/screenshots/3.png?raw=true)

# Real-Time SSH Event Fetcher

## Introduction
The Real-Time SSH Event Fetcher is a Python application that allows you to retrieve and filter logs from remote servers via SSH connections in real-time. It connects to one or more remote servers, executes custom commands, and continuously saves the logs to your local computer. This tool is useful for monitoring and analyzing logs from remote servers without the need to manually download them.

## Features
- Real-time log retrieval from remote servers.
- Customizable SSH connection parameters and remote commands.
- Concurrent execution of SSH connections using threads.
- Log filtering options for specific events or patterns.
- Easy configuration using a `.env` file.

## Installation

### Prerequisites
Before you can use the Real-Time SSH Event Fetcher, ensure that you have the following prerequisites installed on your system:

- Python 3.x
- Paramiko library (for SSH connections)
- getch library (for keyboard input)
- python-decouple library (for configuration management)

You can install the required Python libraries using pip:

```bash
pip install paramiko getch python-decouple
```
## Configuration
- Clone or download this repository to your local machine.
- Create a .env file in the project directory with the following format and fill in your SSH connection details and desired commands:

```# .env
SSH_HOST=your_remote_host
SSH_USERNAME=your_username
SSH_KEY_FILENAME=your_key_file_openssh
SSH_PORT=your_ssh_port
COMMAND1=your_command_1
COMMAND2=your_command_2
```
- Run the application:
```python FETCHER.py```


## License
This project is licensed under the MIT License - see the LICENSE file for details.
