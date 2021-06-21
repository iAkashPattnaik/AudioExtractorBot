r"""
    _                _  _        
   / \    _   _   __| |(_)  ___
  / _ \  | | | | / _` || | / _ \
 / ___ \ | |_| || (_| || || (_) |
/_/   \_\ \__,_| \__,_||_| \___/
     _____        _                       _
    | ____|__  __| |_  _ __   __ _   ___ | |_   ___   _ __
    |  _|  \ \/ /| __|| '__| / _` | / __|| __| / _ \ | '__|
    | |___  >  < | |_ | |   | (_| || (__ | |_ | (_) || |
    |_____|/_/\_\ \__||_|    \__,_| \___| \__| \___/ |_|
                 ____          _
                | __ )   ___  | |_
                |  _ \  / _ \ | __|
                | |_) || (_) || |_
                |____/  \___/  \__|

telegramChannel - t.me/IndianBots
initialRelease - 21/06/21
"""

# Inbuilt
from os import mkdir, system as spawn, path, remove
from threading import Thread

# sitePackages
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# selfMade
from config import Config


app = Client(
    "AudioExtractorBot",
    api_id=Config.apiId,
    api_hash=Config.apiHash,
    bot_token=Config.botToken,
)


def getFileSize(filePath: str):
    fileSize = path.getsize(filePath)
    if fileSize < 1024:
        return f"{fileSize}B"
    elif 1024 <= fileSize <= 1048576:
        return f"{round(fileSize / 1024, 2)} KB"
    elif 1048576 < fileSize < 1073741824:
        return f"{round(fileSize / 1048576, 2)} MB"
    elif 1073741824 < fileSize < 1073741824:
        return f"{round(fileSize / 1099511627776, 2)} GB"


def getThumbnail(thumbs: list):
    if not len(thumbs) >= 1:
        return f"./bot/defaultThumb.jpg"
    return app.download_media(thumbs[0].file_id)


def downloadProgress(current, total, message):
    del total
    app.edit_message_text(
        message.chat.id,
        message.message_id,
        f"Downloading - `{current}` **Bytes**",
        parse_mode="md",
    )


def uploadProgress(current, total, message):
    app.edit_message_text(
        message.chat.id,
        message.message_id,
        f"Uploading -\n"
        f"`{current}/{total}` **Bytes**\n"
        f"Progress - {current * 100 / total:.1f}%✅",
        parse_mode="md",
    )


def delMessage(message):
    try:
        app.delete_messages(
            message.chat.id,
            message.message_id,
        )
    except Exception as _:
        print(f"[Errno 0] Can't delete message: '{message.message_id}'")


def checkUserJoinStatus(user_id):
    try:
        channel = app.get_chat_member("IndianBots", user_id)
        group = app.get_chat_member("IndianBotsChat", user_id)
    except Exception as _:
        channel = False
        group = False
    if channel and group:
        return True
    return False


@app.on_message(filters.video or filters.video_note or filters.document)
def extractAudio(_, message):
    userjoinStatus = checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/IndianBots",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/IndianBotsChat",
                    ),
                ]
            ])
        )
    infoMessage = app.send_message(
        message.chat.id,
        "Downloading - 0%",
        reply_to_message_id=message.message_id,
    )
    try:
        _ = message.video
        filePath = app.download_media(
            message.video.file_id,
            progress=downloadProgress,
            progress_args=(infoMessage,),
        )
        resultFile = f"{message.from_user.id}-{message.message_id}"
        spawn(f"ffmpeg -i {filePath} -f mp3 -ab 192000 -vn -loglevel quiet ./extracted/{resultFile}.mp3")
        if not path.exists(f"./extracted/{resultFile}.mp3"):
            return app.send_message(message.chat.id, "Couldn't Extract The Audio From This File. Sorry!")
        fileSize = getFileSize(f"./extracted/{resultFile}.mp3")
        fileThumb = getThumbnail(message.video.thumbs)
        infoMessageUpload = app.send_message(
            message.chat.id,
            "Uploading - 0%",
            reply_to_message_id=message.message_id,
        )
        app.send_audio(
            message.chat.id,
            f"./extracted/{resultFile}.mp3",
            caption=f"{fileSize} | 192 kbps | @IndianBots",
            reply_to_message_id=message.message_id,
            file_name=f"{message.video.file_name.split('.')[0]}",
            thumb=fileThumb,
            progress=uploadProgress,
            progress_args=(infoMessageUpload,),
        )
        Thread(target=delMessage(infoMessage)).start()
        Thread(target=delMessage(infoMessageUpload)).start()
        remove(f"./extracted/{resultFile}.mp3")
        remove(f"{filePath}")
        remove(f"{fileThumb}")
    except Exception as error:
        print(error)
        app.send_message(message.chat.id, "Couldn't Extract The Audio From This File. Sorry!")
        Thread(target=delMessage(infoMessage)).start()
        Thread(target=delMessage(infoMessageUpload)).start()


@app.on_message(filters.command("start"))
def startCommand(_, message):
    userjoinStatus = checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/IndianBots",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/IndianBotsChat",
                    ),
                ]
            ])
        )
    app.send_message(
        message.chat.id,
        f"Hoi **{message.from_user.first_name}**!\n"
        f"I hope you are pushing healty through the `Covid19 Pandemic.`\n"
        f"I am a **Audio Extractor Bot** made by **@Akash_am1**, i extract audio from videos and send it to you.\n"
        f"For help - /commands\n"
        f"Acknowledgment -\n\n"
        f"[Pyrogram](https://github.com/pyrogram/pyrogram)\n"
        f"[FFmpeg](https://www.ffmpeg.org/)\n"
        f"[Python](https://www.python.org/)",
        disable_web_page_preview=True,
        parse_mode='md',
    )


@app.on_message(filters.command(["github", "source"]))
def source_or_github(_, message):
    userjoinStatus = checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/IndianBots",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/IndianBotsChat",
                    ),
                ]
            ])
        )
    app.send_message(
        message.chat.id,
        "My Source Code Can be Found On Github...\n"
        "https://github.com/BLUE-DEVIL1134/AudioExtractorBot"
    )


@app.on_message(filters.command("commands"))
def commands(_, message):
    userjoinStatus = checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/IndianBots",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/IndianBotsChat",
                    ),
                ]
            ])
        )
    app.send_message(
        message.chat.id,
        "List of all Commands are given below -\n"
        "\n"
        "/help - Show this message\n"
        "/commands - Show this message\n"
        "/start - Restart/Refresh the bot\n"
        "/help - Get help on how to use me.",
        parse_mode="md",
    )


@app.on_message(filters.command("help"))
def commands(_, message):
    userjoinStatus = checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/IndianBots",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/IndianBotsChat",
                    ),
                ]
            ])
        )
    app.send_message(
        message.chat.id,
        "It's real **easy** to use me.\n"
        "All you need to do is send me a **video file** and i will **extract the audio** "
        "and send it to you.",
        parse_mode="md",
    )


if __name__ == "__main__":
    print("Starting ...")
    if not path.exists("./extracted"):
        mkdir("./extracted")
    app.run()
