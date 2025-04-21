"""This package provides some filter generators and some preconfigured filters."""

from .helpers import false_on_key_error

from .generators import any_keys
from .generators import all_keys
from .generators import sub_keys
from .generators import regex
from .generators import text_startswith
from .generators import commands
from .generators import chat_ids
from .generators import chat_types
from .generators import from_ids
from .generators import callback_data
from .generators import callback_data_startswith
from .generators import max_age

from .composition import if_not
from .composition import if_any
from .composition import if_all
from .composition import if_none
from .composition import if_xor

from .pre_configured import is_text
from .pre_configured import has_caption
from .pre_configured import contains_text
from .pre_configured import is_reply
from .pre_configured import has_media_spoiler
from .pre_configured import is_animation
from .pre_configured import is_audio
from .pre_configured import is_document
from .pre_configured import is_paid_media
from .pre_configured import is_photo
from .pre_configured import is_sticker
from .pre_configured import is_story
from .pre_configured import is_video
from .pre_configured import is_video_note
from .pre_configured import is_voice
from .pre_configured import is_contact
from .pre_configured import is_dice
from .pre_configured import is_game
from .pre_configured import is_poll
from .pre_configured import is_venue
from .pre_configured import is_location
