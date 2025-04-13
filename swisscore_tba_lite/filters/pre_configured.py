
from . import generators

is_text = generators.any_keys("text")
"""`True` if "text" is in obj.any_keys()"""

has_caption = generators.any_keys("caption")
"""`True` if "caption" is in obj.any_keys()"""

contains_text = generators.any_keys("text", "caption")
"""`True` if either "text" or "caption" is in obj.any_keys()"""

is_photo = generators.any_keys("photo")
"""`True` if "photo" is in obj.any_keys()"""

is_video = generators.any_keys("video")
"""`True` if "video" is in obj.any_keys()"""

is_document = generators.any_keys("document")
"""`True` if "document" is in obj.any_keys()"""

is_reply = generators.any_keys("reply_to_message")
"""`True` if "reply_to_message" is in obj.any_keys()"""
