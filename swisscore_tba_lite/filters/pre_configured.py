from . import generators

is_text = generators.any_keys("text")
"""`True` if "text" is in obj.keys()"""

has_caption = generators.any_keys("caption")
"""`True` if "caption" is in obj.keys()"""

contains_text = generators.any_keys("text", "caption")
"""`True` if either "text" or "caption" is in obj.keys()"""

is_reply = generators.any_keys("reply_to_message")
"""`True` if "reply_to_message" is in obj.keys()"""

has_media_spoiler = generators.any_keys("has_media_spoiler")
"""`True` if "has_media_spoiler" is in obj.keys()"""


is_animation = generators.any_keys("animation")
"""`True` if "animation" is in obj.keys()"""

is_audio = generators.any_keys("audio")
"""`True` if "audio" is in obj.keys()"""

is_document = generators.any_keys("document")
"""`True` if "document" is in obj.keys()"""

is_paid_media = generators.any_keys("paid_media")
"""`True` if "paid_media" is in obj.keys()"""

is_photo = generators.any_keys("photo")
"""`True` if "photo" is in obj.keys()"""

is_sticker = generators.any_keys("sticker")
"""`True` if "sticker" is in obj.keys()"""

is_story = generators.any_keys("story")
"""`True` if "story" is in obj.keys()"""

is_video = generators.any_keys("video")
"""`True` if "video" is in obj.keys()"""

is_video_note = generators.any_keys("video_note")
"""`True` if "video_note" is in obj.keys()"""

is_voice = generators.any_keys("voice")
"""`True` if "voice" is in obj.keys()"""

is_contact = generators.any_keys("contact")
"""`True` if "contact" is in obj.keys()"""

is_dice = generators.any_keys("dice")
"""`True` if "dice" is in obj.keys()"""

is_game = generators.any_keys("game")
"""`True` if "game" is in obj.keys()"""

is_poll = generators.any_keys("poll")
"""`True` if "poll" is in obj.keys()"""

is_venue = generators.any_keys("venue")
"""`True` if "venue" is in obj.keys()"""

is_location = generators.any_keys("location")
"""`True` if "location" is in obj.keys()"""