import os
from pathlib import Path

from swisscore_tba_lite import Bot
from swisscore_tba_lite import objects as tg
from swisscore_tba_lite.filters import chat_ids, is_document

TOKEN = os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 1234))

bot = Bot(TOKEN)

@bot.event("message", chat_ids(ADMIN_ID), is_document)
async def test(msg: tg.Message):
    doc = msg["document"]

    file = await bot.get_file(doc["file_id"])

    # download as file 
    #   if the path is a directory the file name will be taken as it is on the server
    #   else the provided filename will be used.
    #   you can optionaly allow/dissallow overwriting if the file name already exists
    path = await bot.download(file).as_file("path/to/save/file", overwrite=False)

    # download as bytes
    file_content = await bot.download(file).as_bytes()

    # download as base64 (bytes or str)
    #   as base64 bytes
    b64_bytes = await bot.download(file).as_base64()
    #   as base64 string
    b64_str = await bot.download(file).as_base64("utf-8")


bot.start_polling()
