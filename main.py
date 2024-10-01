import os
import mss
import sys
import time
import ctypes
import subprocess
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot token variables
BOT_TOKEN = 'BOT_TOKEN_HERE'
CHAT_ID = 'YOUR_CHAT_ID_HERE'

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(
"""LOCK FLOW HELP\n
HELP:
/help - Lists all commands
/ping - Pong!

REMOTE CONTROL:
/screen [screenshot] - Takes screenshot of every monitor
/blockinput [bi] - Block input
/unblockinput [ubi] - Unblocks input

POWER:
/lock - Locks machine
/sleep - Put's machine to sleep
/restart - Restarts the machine
/hibernate - Triggers hibernation
/shutdown - Shut's down the machine

REMOTE SCRIPTING:
/cmd - Executed given command into command prompt

OTHER:
/exit - Exits the application""")
        except Exception as ex:
            await update.message.reply_text(f"Help Error: {ex}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Ping Info: Pong!")
        except Exception as ex:
            await update.message.reply_text(f"Ping Error: {ex}")

# SCREEN
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Screenshot Info: Wait...")

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
            await update.message.reply_text(f"Screenshot Error: {ex}")

async def blockinput(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            ctypes.windll.user32.BlockInput(True)
            await update.message.reply_text(f"Block Input Info: Success")
        except Exception as ex:
            await update.message.reply_text(f"Block Input Error: {ex}")

async def unblockinput(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            ctypes.windll.user32.BlockInput(False)
            await update.message.reply_text(f"Unblock Input Info: Success")
        except Exception as ex:
            await update.message.reply_text(f"Unblock Input Error: {ex}")

# POWER
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Lock Info: Success")
            ctypes.windll.user32.LockWorkStation()
        except Exception as ex:
            await update.message.reply_text(f"Lock Error: {ex}")

async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Sleep Info: Success")
            ctypes.windll.PowrProf.SetSuspendState(False, True, False)
        except Exception as ex:
            await update.message.reply_text(f"Sleep Error: {ex}")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Restart Info: Success")
            os.system("shutdown /r /t 0")
        except Exception as ex:
            await update.message.reply_text(f"Restart Error: {ex}")

async def hibernate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Hibernate Info: Success")
            ctypes.windll.PowrProf.SetSuspendState(True, True, False)
        except Exception as ex:
            await update.message.reply_text(f"Hibernate Error: {ex}")

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            await update.message.reply_text(f"Shutdown Info: Success")
            os.system("shutdown /s /t 0")
        except Exception as ex:
            await update.message.reply_text(f"Shutdown Error: {ex}")

# REMOTE SCRIPTING
async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            command = ' '.join(context.args)
            if command:
                try:
                    # Run the command in the system's Command Prompt
                    result = subprocess.run(command, capture_output=True, shell=True, text=True)
                    
                    # Send the output back to the user
                    if result.stdout:
                        await update.message.reply_text(f"CMD Output:\n{result.stdout}")
                    if result.stderr:
                        await update.message.reply_text(f"CMD Error:\n{result.stderr}")
                except Exception as e:
                    await update.message.reply_text(f"CMD Error: {e}")
            else:
                await update.message.reply_text("CMD Info: Please provide a command to execute. Usage: /cmd <args>")
        except Exception as ex:
            await update.message.reply_text(f"CMD Error: {ex}")

# OTHER
async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserAuthorized(update.message.chat_id):
        try:
            sys.exit(0)
        except Exception as ex:
            await update.message.reply_text(f"Exit Error: {ex}")

# Check if user is authorized
def UserAuthorized(chatID):
    if str(chatID) == CHAT_ID:
        return True
    else:
        return False

def main():
    # Create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    # HELP
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("ping", ping))
    
    # REMOTE CONTROL
    application.add_handler(CommandHandler("screenshot", screenshot))
    application.add_handler(CommandHandler("screen", screenshot))  # Alias of "screenshot"

    application.add_handler(CommandHandler("blockinput", blockinput))
    application.add_handler(CommandHandler("bi", blockinput))  # Alias of "blockinput"

    application.add_handler(CommandHandler("unblockinput", unblockinput))
    application.add_handler(CommandHandler("ubi", unblockinput))  # Alias of "unblockinput"

    # POWER
    application.add_handler(CommandHandler("lock", lock))
    application.add_handler(CommandHandler("sleep", sleep))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("hibernate", hibernate))
    application.add_handler(CommandHandler("shutdown", shutdown))

    # REMOTE SCRIPTING
    application.add_handler(CommandHandler("cmd", cmd))

    # OTHER
    application.add_handler(CommandHandler("exit", exit))

    # Run the bot with automatic reconnect
    while True:
        try:
            print("LockFlowRC Info: Starting...")
            application.run_polling()
        except Exception as ex:
            print(f"LockFlowRC Error: {ex}")
            time.sleep(5)

if __name__ == '__main__':
    # Hide's console window
    #ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    main()