# LockFlow 💣
LockFlow is a simple and lightweight Telegram RAT for remotely controlling a Windows machine. It allows for secure and efficient remote access, providing an easy way to manage your PC from anywhere.

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

  - FILE MANAGER:
    - [x] /ls [path]: Lists the contents of the specified directory (not finished)
    - [x] /cd [path]: Changes the current working directory to the specified path (not finished)
    - [x] /delete [path]: Deletes the specified file or directory. Use with caution as it may not be reversible
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

## **Disclaimer**
LockFlow is intended for educational and research purposes only. The author is not responsible for any misuse or damage caused by this software.

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## **Contact** ✉
- E-mail: [velimir.paleksic@gmail.com](velimir.paleksic@gmail.com).
- VexSystems Github: [github.com/vexsystems](https://github.com/vexsystems).
- VexSystems Instagram: [@vex.systems](https://www.instagram.com/vex.systems/).

<details>
<summary>Keywords (ignore):</summary>
Remote Access Tool, Telegram Bot, Telegram Remote Access Bot, Windows Remote Control, System Management Bot, Lightweight Remote Access Tool, Open-Source Remote Bot, Telegram RAT, RAT, LockFlow, Remote Access, Remote Control, Windows Remote Access Tool, Windows Remote Access, Windows Tool, Remote Desktop Tool, Telegram Remote Desktop Bot, PC Management Bot, Windows RAT, Secure Remote Control, Remote PC Manager, Telegram System Tool, Telegram Command Bot, Windows System Tool, Remote Admin Tool, Remote PC Access, Remote Command Execution, Windows Automation Bot, PC Control Bot, Remote Access Automation, Telegram-Controlled RAT, Admin Control Bot, Remote Monitoring Bot, PC Access Tool, Lightweight Admin Bot
</details>
