
from . import generators

is_text = generators.keys("text")
"""`True` if "text" is in obj.keys()"""

has_caption = generators.keys("caption")
"""`True` if "caption" is in obj.keys()"""

contains_text = generators.keys("text", "caption")
"""`True` if either "text" or "caption" is in obj.keys()"""

is_photo = generators.keys("photo")
"""`True` if "photo" is in obj.keys()"""

is_video = generators.keys("video")
"""`True` if "video" is in obj.keys()"""

is_document = generators.keys("document")
"""`True` if "document" is in obj.keys()"""

is_reply = generators.keys("reply_to_message")
"""`True` if "reply_to_message" is in obj.keys()"""