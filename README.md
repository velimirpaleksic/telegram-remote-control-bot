# LockFlowRC 💣
LockFlowRC is a simple and lightweight Telegram bot for remotely controlling a Windows machine. It allows for secure and efficient remote access, providing an easy way to manage your PC from anywhere.

![Logo](images/logo.png)

## **Features** ✨
- Remote access and control of a Windows machine via Telegram
- Secure authentication using chat ID for authorized users only
- Perform system actions like blocking input, executing commands, and power operations

## **Commands** 🤖
- Commands:
  - HELP:
    - [x] /help: Displays a list of available commands and their descriptions
    - [x] /ping: Checks if the bot is responsive
  
  - STATUS:
    - [x] /status: Provides the current status of the system (e.g., uptime, current user, etc.)
    - [x] /diskusage (/du): Displays information about disk space usage on the machine
    - [x] /ramusage (/ru): Displays information about ram usage on the machine
    - [x] /systeminfo (/si): Provides detailed system information such as OS version, CPU usage, and memory usage

  - TASK MANAGER:
    - [x] /processes: Lists currently running processes on the system with options to terminate them
    - [x] /taskkill [pid]: Terminates the specified process

  - FILE EXPLORER:
    - [ ] /fileexplorer [path]: Opens a specific directory for browsing files and directories remotely
    - [ ] /upload [file] [path]: Allows users to upload files from their device to the remote machine
    - [x] /download [file]: Enables downloading files from the remote machine to the user's device
    - [ ] /ftp [file] [server] [port] [username] [password]: Transfers files to/from a remote file server

  - NETWORK:
    - [x] /networkinfo: Displays current network settings and status (e.g., IP address, network speed, latency)

  - REMOTE CONTROL:
    - [x] /screenshot (/screen): Captures and sends a screenshot of the remote machine
    - [x] /blockinput (/bi): Blocks input on the remote machine
    - [x] /unblockinput (/ubi): Unblocks input on the remote machine
    - [ ] /message [text]: Sends a message to the local machine, displayed as a notification or pop-up
  
  - POWER:
    - [x] /lock: Locks the remote machine
    - [x] /sleep: Puts the remote machine to sleep
    - [x] /restart: Restarts the remote machine
    - [x] /hibernate: Hibernates the remote machine
    - [x] /shutdown: Shuts down the remote machine

  - REMOTE SCRIPTING:
    - [x] /cmd: Executes a specified command on the remote machine

  - OTHER:
    - [x] /exit: Stops the bot from running

## **Make a bot guide** 🤖
- Go to the [@BotFather](https://t.me/BotFather) bot and create your own bot. Save the token of the bot.
- Now you need to get your chat id, go to the [@WhatChatIDBot](https://t.me/WhatChatIDBot) bot and save the chat id.

## **Installation** 🔨
1. Clone the repository:
    ```bash
    git clone https://github.com/velimirpaleksic/telegram-remote-control-bot
    cd telegram-remote-control-bot
    ```
2. Install the required packages:
    ```bash
    pip install python-telegram-bot Pillow mss
    ```
3. Update the bot token and chat ID in the script.

## **Usage** ⌨
1. Run the bot:
    ```bash
    python main.py
    ```
2. Interact with the bot via Telegram.

## **Contributing** ⭐
Contributions are welcome! Please create a pull request or open an issue for any enhancements or bugs.

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## **Contact** ✉
- E-mail: [velimir.paleksic@gmail.com](velimir.paleksic@gmail.com).
- VexSystems Github: [github.com/vexsystems](https://github.com/vexsystems).
- VexSystems Instagram: [@vex.systems](https://www.instagram.com/vex.systems/).