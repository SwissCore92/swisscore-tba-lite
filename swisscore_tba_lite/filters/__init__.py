"""Provides some filter generators and some preconfigured filters."""

from .helpers import false_on_key_error

from .generators import keys
from .generators import all_keys
from .generators import sub_keys
from .generators import regex
from .generators import text_startswith
from .generators import commands
from .generators import chat_ids
from .generators import chat_types
from .generators import from_users
from .generators import callback_data
from .generators import callback_data_startswith

from .composition import not_
from .composition import any_
from .composition import all_
from .composition import none_
from .composition import xor

from .pre_configured import is_text
from .pre_configured import has_caption
from .pre_configured import contains_text
from .pre_configured import is_photo
from .pre_configured import is_video
from .pre_configured import is_document
from .pre_configured import is_reply
