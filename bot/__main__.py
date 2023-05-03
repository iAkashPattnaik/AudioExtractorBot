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

telegramChannel - telegram.dog/PhantomProjects
initialRelease - 21/06/21
relaunchDate - 3/5/23
"""

# Inbuilt
from os import mkdir, system as spawn, path, remove
from typing import BinaryIO

# sitePackages
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# selfMade
from config import Config

app = Client(
    "AudioExtractorBot",
    api_id=Config.apiId, # type: ignore
    api_hash=Config.apiHash, # type: ignore
    bot_token=Config.botToken, # type: ignore
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


async def getThumbnail(thumbs: list) -> str | BinaryIO | None:
    if not len(thumbs) >= 1:
        return f"./bot/defaultThumb.jpg"
    return await app.download_media(thumbs[0].file_id)


async def downloadProgress(current, total, message):
    del total
    await app.edit_message_text(
        message.chat.id,
        message.id,
        f"Downloading - `{current}` **Bytes**",
        parse_mode=ParseMode.MARKDOWN,
    )


async def uploadProgress(current, total, message):
    await app.edit_message_text(
        message.chat.id,
        message.id,
        f"Uploading -\n"
        f"`{current}/{total}` **Bytes**\n"
        f"Progress - {current * 100 / total:.1f}%✅",
        parse_mode=ParseMode.MARKDOWN,
    )


async def delMessage(message):
    try:
        await app.delete_messages(
            message.chat.id,
            message.id,
        )
    except Exception as _:
        print(f"[Errno 0] Can't delete message: '{message.id}'")


async def checkUserJoinStatus(user_id):
    try:
        channel = await app.get_chat_member("PhantomProjects", user_id)
        group = await app.get_chat_member("PhantomProjectsGroup", user_id)
    except Exception as _:
        channel = False
        group = False
    if channel and group:
        return True
    return False


@app.on_message(filters.video or filters.video_note or filters.document)
async def extractAudio(_, message):
    userjoinStatus = await checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return await app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/PhantomProjects",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/PhantomProjectsGroup",
                    ),
                ]
            ])
        )
    infoMessage = await app.send_message(
        message.chat.id,
        "Downloading - 0%",
        reply_to_message_id=message.id,
    )
    try:
        _ = message.video
        filePath = await app.download_media(
            message.video.file_id,
            progress=downloadProgress,
            progress_args=(infoMessage,),
        )
        resultFile = f"{message.from_user.id}-{message.id}"
        spawn(f"ffmpeg -i {filePath} -f mp3 -b:a 320k -vn -loglevel quiet ./extracted/{resultFile}.mp3")
        if not path.exists(f"./extracted/{resultFile}.mp3"):
            return await app.send_message(message.chat.id, "Couldn't Extract The Audio From This File. Sorry!")
        fileSize = getFileSize(f"./extracted/{resultFile}.mp3")
        fileThumb = await getThumbnail(message.video.thumbs)
        infoMessageUpload = await app.send_message(
            message.chat.id,
            "Uploading - 0%",
            reply_to_message_id=message.id,
        )
        await app.send_audio(
            message.chat.id,
            f"./extracted/{resultFile}.mp3",
            caption=f"`{fileSize}` | 320 kbps | @PhantomProjects",
            reply_to_message_id=message.id,
            file_name=f"{message.video.file_name.split('.')[0]}",
            thumb=str(fileThumb),
            progress=uploadProgress,
            progress_args=(infoMessageUpload,),
            parse_mode=ParseMode.MARKDOWN,
        )
        await delMessage(infoMessage)
        await delMessage(infoMessageUpload)
        remove(f"./extracted/{resultFile}.mp3")
        remove(f"{filePath}")
        remove(f"{fileThumb}")
    except Exception as error:
        print(error)
        await app.send_message(message.chat.id, "Couldn't Extract The Audio From This File. Sorry!\n\nPlease report this to @akashpattnaik personally")
        await delMessage(infoMessage)


@app.on_message(filters.command("start"))
async def startCommand(_, message):
    userjoinStatus = await checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return await app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/PhantomProjects",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/PhantomProjectsGroup",
                    ),
                ]
            ])
        )
    await app.send_message(
        message.chat.id,
        f"Hoi **{message.from_user.first_name}**!\n"
        f"I am a **Audio Extractor Bot** made by **@akashpattnaik**, I extract audio from videos and send it to you.\n"
        f"For help - /commands\n\n"
        f"Acknowledgment -\n"
        f"[**Pyrogram**](https://github.com/pyrogram/pyrogram)\n"
        f"[**FFmpeg**](https://www.ffmpeg.org/)\n"
        f"[**Python**](https://www.python.org/)",
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )


@app.on_message(filters.command(["github", "source"]))
async def source_or_github(_, message):
    userjoinStatus = await checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return await app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/PhantomProjects",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/PhantomProjectsGroup",
                    ),
                ]
            ])
        )
    await app.send_message(
        message.chat.id,
        "My Source Code Can be Found On Github...\n"
        "https://github.com/BLUE-DEVIL1134/AudioExtractorBot"
    )


@app.on_message(filters.command("commands"))
async def _commands(_, message):
    userjoinStatus = await checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return await app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/PhantomProjects",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/PhantomProjectsGroup",
                    ),
                ]
            ])
        )
    await app.send_message(
        message.chat.id,
        "List of all Commands are given below -\n"
        "\n"
        "/commands - Show this message\n"
        "/start - Restart/Refresh the bot\n"
        "/github - Get the source code of this bot\n"
        "/help - Get help on how to use me.",
        parse_mode=ParseMode.MARKDOWN,
    )


@app.on_message(filters.command("help"))
async def _help(_, message):
    userjoinStatus = await checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return await app.send_message(
            message.chat.id,
            f"Sorry `{message.from_user.first_name}`,\n"
            f"I can't let you use me until you join both my **Channel** and **Group**.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="🖥Channel💺",
                        url="https://t.me/PhantomProjects",
                        ),
                ],
                [
                    InlineKeyboardButton(
                        text="🧬Group🚦",
                        url="https://t.me/PhantomProjectsGroup",
                    ),
                ]
            ])
        )
    await app.send_message(
        message.chat.id,
        "It's real **easy** to use me.\n"
        "All you need to do is send me a **video file** and i will **extract the audio** "
        "and send it to you.",
        parse_mode=ParseMode.MARKDOWN,
    )


if __name__ == "__main__":
    print("Starting ...")
    if not path.exists("./extracted"):
        mkdir("./extracted")
    app.run()
