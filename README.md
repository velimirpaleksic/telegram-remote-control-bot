# LockFlowRC

LockFlowRC is a simple and lightweight Telegram bot for remotely controlling a Windows machine. It allows for secure and efficient remote access, providing an easy way to manage your PC from anywhere.

## **Features**
- Remote access and control of a Windows machine via Telegram
- Secure authentication using chat ID for authorized users only
- Perform system actions like blocking input, executing commands, and power operations

## **Installation**
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

## **Usage**
1. Run the bot:
    ```bash
    python bot.py
    ```
2. Interact with the bot via Telegram using your authorized chat ID.

## **TODO**
- Support for:
  - [x] ~~Windows~~
  - [ ] Linux

<br>

- Commands:
  - STATUS:
    - [x] /status: Provides the current status of the system (e.g., uptime, current user, etc.)

    - [x] /diskusage: Displays information about disk space usage on the machine

    - [x] /ramusage: Displays information about ram usage on the machine

    - [x] /getinfo: Provides detailed system information such as OS version, CPU usage, and memory usage

  - TASK MANAGER:
    - [ ] /processes: Lists currently running processes on the system with options to terminate them

    - [ ] /taskkill: Kills specified process

  - FILE EXPLORER:
    - [ ] /fileexplorer [path]: Opens a specific directory for browsing files and directories remotely

    - [ ] /upload [file] [path]: Allows users to upload files from their device to the remote machine

    - [ ] /download [file]: Enables downloading files from the remote machine to the user's device

    - [ ] /ftp [file] [server] [port] [username] [password]: Allows downloading files from the remote machine to the remote file server
      
  - NETWORK:
    - [ ] /networkinfo: Displays current network settings and status (e.g., IP address, network speed, latency)

  - REMOTE INTERACTION:
    - [ ] /message [text]: Sends a message to the local machine, which can be displayed as a notification or pop-up

## **Contributing**
Contributions are welcome! Please create a pull request or open an issue for any enhancements or bugs.

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## **Bugs & features** 🧩
- [Report bug](https://github.com/velimirpaleksic/portfolio/issues)
- [Request Feature](https://github.com/velimirpaleksic/portfolio/issues)

## **Contact** ✉
- E-mail: [velimir.paleksic@gmail.com](velimir.paleksic@gmail.com).
- VexSystems Github: [github.com/vexsystems](https://github.com/vexsystems).
- VexSystems Instagram: [@vex.systems](https://www.instagram.com/vex.systems/).