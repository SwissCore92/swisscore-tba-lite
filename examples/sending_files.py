import os
from pathlib import Path

from swisscore_tba_lite import Bot
from swisscore_tba_lite import objects as tg
from swisscore_tba_lite.filters import commands, chat_ids

TOKEN = os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 1234))

bot = Bot(TOKEN)

@bot.event("message", chat_ids(ADMIN_ID), commands("test"))
async def test(msg: tg.Message):

    # send as str Path
    photo = "path/to/your/photo1.png"
    bot.send_photo(msg["chat"]["id"], photo, caption="from string path")

    # send as pathlib Path
    photo = Path(photo)
    bot.send_photo(msg["chat"]["id"], photo, caption="from pathlib path")

    # send as bytes
    with photo.open("rb") as f:
        photo = f.read()
    bot.send_photo(msg["chat"]["id"], photo, caption="from bytes")

    # send as inputfile (dict) {"content": <str, path, bytes>, "filename": <str>}
    # this is usefult when sending files as bytes but want to preserve the filename
    #   or if you want to send the file with a different name
    bot.send_photo(msg["chat"]["id"], {"content": photo, "filename": "my_photo.png"})


bot.start_polling()
