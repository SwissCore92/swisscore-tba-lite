"""
Telegram types scraped from 'Bot API 9.2 (August 15, 2025)'
"""

import typing as t
from pathlib import Path

from . import literals
from ...utils.files import InputFile


class Update(t.TypedDict):
    """
    ### [Update](https://core.telegram.org/bots/api#update)  
    
    This [object](https://core.telegram.org/bots/api#available-types) represents an incoming update.  
    At most **one** of the optional parameters can be present in any given update.
    """
    update_id: int
    message: t.NotRequired["Message"]
    edited_message: t.NotRequired["Message"]
    channel_post: t.NotRequired["Message"]
    edited_channel_post: t.NotRequired["Message"]
    business_connection: t.NotRequired["BusinessConnection"]
    business_message: t.NotRequired["Message"]
    edited_business_message: t.NotRequired["Message"]
    deleted_business_messages: t.NotRequired["BusinessMessagesDeleted"]
    message_reaction: t.NotRequired["MessageReactionUpdated"]
    message_reaction_count: t.NotRequired["MessageReactionCountUpdated"]
    inline_query: t.NotRequired["InlineQuery"]
    chosen_inline_result: t.NotRequired["ChosenInlineResult"]
    callback_query: t.NotRequired["CallbackQuery"]
    shipping_query: t.NotRequired["ShippingQuery"]
    pre_checkout_query: t.NotRequired["PreCheckoutQuery"]
    purchased_paid_media: t.NotRequired["PaidMediaPurchased"]
    poll: t.NotRequired["Poll"]
    poll_answer: t.NotRequired["PollAnswer"]
    my_chat_member: t.NotRequired["ChatMemberUpdated"]
    chat_member: t.NotRequired["ChatMemberUpdated"]
    chat_join_request: t.NotRequired["ChatJoinRequest"]
    chat_boost: t.NotRequired["ChatBoostUpdated"]
    removed_chat_boost: t.NotRequired["ChatBoostRemoved"]

class WebhookInfo(t.TypedDict):
    """
    ### [WebhookInfo](https://core.telegram.org/bots/api#webhookinfo)  
    
    Describes the current status of a webhook.
    
    All types used in the Bot API responses are represented as JSON\\-objects.
    
    It is safe to use 32\\-bit signed integers for storing all **Integer** fields unless otherwise noted.
    
    **Optional** fields may be not returned when irrelevant.
    """
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: t.NotRequired[str]
    last_error_date: t.NotRequired[int]
    last_error_message: t.NotRequired[str]
    last_synchronization_error_date: t.NotRequired[int]
    max_connections: t.NotRequired[int]
    allowed_updates: t.NotRequired[list[str]]

class User(t.TypedDict):
    """
    ### [User](https://core.telegram.org/bots/api#user)  
    
    This object represents a Telegram user or bot.
    """
    id: int
    is_bot: bool
    first_name: str
    last_name: t.NotRequired[str]
    username: t.NotRequired[str]
    language_code: t.NotRequired[str]
    is_premium: t.NotRequired[t.Literal[True]]
    added_to_attachment_menu: t.NotRequired[t.Literal[True]]
    can_join_groups: t.NotRequired[bool]
    can_read_all_group_messages: t.NotRequired[bool]
    supports_inline_queries: t.NotRequired[bool]
    can_connect_to_business: t.NotRequired[bool]
    has_main_web_app: t.NotRequired[bool]

class Chat(t.TypedDict):
    """
    ### [Chat](https://core.telegram.org/bots/api#chat)  
    
    This object represents a chat.
    """
    id: int
    type: str
    title: t.NotRequired[str]
    username: t.NotRequired[str]
    first_name: t.NotRequired[str]
    last_name: t.NotRequired[str]
    is_forum: t.NotRequired[t.Literal[True]]
    is_direct_messages: t.NotRequired[t.Literal[True]]

class ChatFullInfo(t.TypedDict):
    """
    ### [ChatFullInfo](https://core.telegram.org/bots/api#chatfullinfo)  
    
    This object contains full information about a chat.
    """
    id: int
    type: str
    accent_color_id: int
    max_reaction_count: int
    accepted_gift_types: "AcceptedGiftTypes"
    title: t.NotRequired[str]
    username: t.NotRequired[str]
    first_name: t.NotRequired[str]
    last_name: t.NotRequired[str]
    is_forum: t.NotRequired[t.Literal[True]]
    is_direct_messages: t.NotRequired[t.Literal[True]]
    photo: t.NotRequired["ChatPhoto"]
    active_usernames: t.NotRequired[list[str]]
    birthdate: t.NotRequired["Birthdate"]
    business_intro: t.NotRequired["BusinessIntro"]
    business_location: t.NotRequired["BusinessLocation"]
    business_opening_hours: t.NotRequired["BusinessOpeningHours"]
    personal_chat: t.NotRequired["Chat"]
    parent_chat: t.NotRequired["Chat"]
    available_reactions: t.NotRequired[list["ReactionType"]]
    background_custom_emoji_id: t.NotRequired[str]
    profile_accent_color_id: t.NotRequired[int]
    profile_background_custom_emoji_id: t.NotRequired[str]
    emoji_status_custom_emoji_id: t.NotRequired[str]
    emoji_status_expiration_date: t.NotRequired[int]
    bio: t.NotRequired[str]
    has_private_forwards: t.NotRequired[t.Literal[True]]
    has_restricted_voice_and_video_messages: t.NotRequired[t.Literal[True]]
    join_to_send_messages: t.NotRequired[t.Literal[True]]
    join_by_request: t.NotRequired[t.Literal[True]]
    description: t.NotRequired[str]
    invite_link: t.NotRequired[str]
    pinned_message: t.NotRequired["Message"]
    permissions: t.NotRequired["ChatPermissions"]
    can_send_paid_media: t.NotRequired[t.Literal[True]]
    slow_mode_delay: t.NotRequired[int]
    unrestrict_boost_count: t.NotRequired[int]
    message_auto_delete_time: t.NotRequired[int]
    has_aggressive_anti_spam_enabled: t.NotRequired[t.Literal[True]]
    has_hidden_members: t.NotRequired[t.Literal[True]]
    has_protected_content: t.NotRequired[t.Literal[True]]
    has_visible_history: t.NotRequired[t.Literal[True]]
    sticker_set_name: t.NotRequired[str]
    can_set_sticker_set: t.NotRequired[t.Literal[True]]
    custom_emoji_sticker_set_name: t.NotRequired[str]
    linked_chat_id: t.NotRequired[int]
    location: t.NotRequired["ChatLocation"]

class Message(t.TypedDict("Message", {"from": "User"})):
    """
    ### [Message](https://core.telegram.org/bots/api#message)  
    
    This object represents a message.
    """
    message_id: int
    date: int
    chat: "Chat"
    message_thread_id: t.NotRequired[int]
    direct_messages_topic: t.NotRequired["DirectMessagesTopic"]
    sender_chat: t.NotRequired["Chat"]
    sender_boost_count: t.NotRequired[int]
    sender_business_bot: t.NotRequired["User"]
    business_connection_id: t.NotRequired[str]
    forward_origin: t.NotRequired["MessageOrigin"]
    is_topic_message: t.NotRequired[t.Literal[True]]
    is_automatic_forward: t.NotRequired[t.Literal[True]]
    reply_to_message: t.NotRequired["Message"]
    external_reply: t.NotRequired["ExternalReplyInfo"]
    quote: t.NotRequired["TextQuote"]
    reply_to_story: t.NotRequired["Story"]
    reply_to_checklist_task_id: t.NotRequired[int]
    via_bot: t.NotRequired["User"]
    edit_date: t.NotRequired[int]
    has_protected_content: t.NotRequired[t.Literal[True]]
    is_from_offline: t.NotRequired[t.Literal[True]]
    is_paid_post: t.NotRequired[t.Literal[True]]
    media_group_id: t.NotRequired[str]
    author_signature: t.NotRequired[str]
    paid_star_count: t.NotRequired[int]
    text: t.NotRequired[str]
    entities: t.NotRequired[list["MessageEntity"]]
    link_preview_options: t.NotRequired["LinkPreviewOptions"]
    suggested_post_info: t.NotRequired["SuggestedPostInfo"]
    effect_id: t.NotRequired[str]
    animation: t.NotRequired["Animation"]
    audio: t.NotRequired["Audio"]
    document: t.NotRequired["Document"]
    paid_media: t.NotRequired["PaidMediaInfo"]
    photo: t.NotRequired[list["PhotoSize"]]
    sticker: t.NotRequired["Sticker"]
    story: t.NotRequired["Story"]
    video: t.NotRequired["Video"]
    video_note: t.NotRequired["VideoNote"]
    voice: t.NotRequired["Voice"]
    caption: t.NotRequired[str]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[t.Literal[True]]
    has_media_spoiler: t.NotRequired[t.Literal[True]]
    checklist: t.NotRequired["Checklist"]
    contact: t.NotRequired["Contact"]
    dice: t.NotRequired["Dice"]
    game: t.NotRequired["Game"]
    poll: t.NotRequired["Poll"]
    venue: t.NotRequired["Venue"]
    location: t.NotRequired["Location"]
    new_chat_members: t.NotRequired[list["User"]]
    left_chat_member: t.NotRequired["User"]
    new_chat_title: t.NotRequired[str]
    new_chat_photo: t.NotRequired[list["PhotoSize"]]
    delete_chat_photo: t.NotRequired[t.Literal[True]]
    group_chat_created: t.NotRequired[t.Literal[True]]
    supergroup_chat_created: t.NotRequired[t.Literal[True]]
    channel_chat_created: t.NotRequired[t.Literal[True]]
    message_auto_delete_timer_changed: t.NotRequired["MessageAutoDeleteTimerChanged"]
    migrate_to_chat_id: t.NotRequired[int]
    migrate_from_chat_id: t.NotRequired[int]
    pinned_message: t.NotRequired["MaybeInaccessibleMessage"]
    invoice: t.NotRequired["Invoice"]
    successful_payment: t.NotRequired["SuccessfulPayment"]
    refunded_payment: t.NotRequired["RefundedPayment"]
    users_shared: t.NotRequired["UsersShared"]
    chat_shared: t.NotRequired["ChatShared"]
    gift: t.NotRequired["GiftInfo"]
    unique_gift: t.NotRequired["UniqueGiftInfo"]
    connected_website: t.NotRequired[str]
    write_access_allowed: t.NotRequired["WriteAccessAllowed"]
    passport_data: t.NotRequired["PassportData"]
    proximity_alert_triggered: t.NotRequired["ProximityAlertTriggered"]
    boost_added: t.NotRequired["ChatBoostAdded"]
    chat_background_set: t.NotRequired["ChatBackground"]
    checklist_tasks_done: t.NotRequired["ChecklistTasksDone"]
    checklist_tasks_added: t.NotRequired["ChecklistTasksAdded"]
    direct_message_price_changed: t.NotRequired["DirectMessagePriceChanged"]
    forum_topic_created: t.NotRequired["ForumTopicCreated"]
    forum_topic_edited: t.NotRequired["ForumTopicEdited"]
    forum_topic_closed: t.NotRequired["ForumTopicClosed"]
    forum_topic_reopened: t.NotRequired["ForumTopicReopened"]
    general_forum_topic_hidden: t.NotRequired["GeneralForumTopicHidden"]
    general_forum_topic_unhidden: t.NotRequired["GeneralForumTopicUnhidden"]
    giveaway_created: t.NotRequired["GiveawayCreated"]
    giveaway: t.NotRequired["Giveaway"]
    giveaway_winners: t.NotRequired["GiveawayWinners"]
    giveaway_completed: t.NotRequired["GiveawayCompleted"]
    paid_message_price_changed: t.NotRequired["PaidMessagePriceChanged"]
    suggested_post_approved: t.NotRequired["SuggestedPostApproved"]
    suggested_post_approval_failed: t.NotRequired["SuggestedPostApprovalFailed"]
    suggested_post_declined: t.NotRequired["SuggestedPostDeclined"]
    suggested_post_paid: t.NotRequired["SuggestedPostPaid"]
    suggested_post_refunded: t.NotRequired["SuggestedPostRefunded"]
    video_chat_scheduled: t.NotRequired["VideoChatScheduled"]
    video_chat_started: t.NotRequired["VideoChatStarted"]
    video_chat_ended: t.NotRequired["VideoChatEnded"]
    video_chat_participants_invited: t.NotRequired["VideoChatParticipantsInvited"]
    web_app_data: t.NotRequired["WebAppData"]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]

class MessageId(t.TypedDict):
    """
    ### [MessageId](https://core.telegram.org/bots/api#messageid)  
    
    This object represents a unique message identifier.
    """
    message_id: int

class InaccessibleMessage(t.TypedDict):
    """
    ### [InaccessibleMessage](https://core.telegram.org/bots/api#inaccessiblemessage)  
    
    This object describes a message that was deleted or is otherwise inaccessible to the bot.
    """
    chat: "Chat"
    message_id: int
    date: int

class MessageEntity(t.TypedDict):
    """
    ### [MessageEntity](https://core.telegram.org/bots/api#messageentity)  
    
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    """
    type: str
    offset: int
    length: int
    url: t.NotRequired[str]
    user: t.NotRequired["User"]
    language: t.NotRequired[str]
    custom_emoji_id: t.NotRequired[str]

class TextQuote(t.TypedDict):
    """
    ### [TextQuote](https://core.telegram.org/bots/api#textquote)  
    
    This object contains information about the quoted part of a message that is replied to by the given message.
    """
    text: str
    position: int
    entities: t.NotRequired[list["MessageEntity"]]
    is_manual: t.NotRequired[t.Literal[True]]

class ExternalReplyInfo(t.TypedDict):
    """
    ### [ExternalReplyInfo](https://core.telegram.org/bots/api#externalreplyinfo)  
    
    This object contains information about a message that is being replied to, which may come from another chat or forum topic.
    """
    origin: "MessageOrigin"
    chat: t.NotRequired["Chat"]
    message_id: t.NotRequired[int]
    link_preview_options: t.NotRequired["LinkPreviewOptions"]
    animation: t.NotRequired["Animation"]
    audio: t.NotRequired["Audio"]
    document: t.NotRequired["Document"]
    paid_media: t.NotRequired["PaidMediaInfo"]
    photo: t.NotRequired[list["PhotoSize"]]
    sticker: t.NotRequired["Sticker"]
    story: t.NotRequired["Story"]
    video: t.NotRequired["Video"]
    video_note: t.NotRequired["VideoNote"]
    voice: t.NotRequired["Voice"]
    has_media_spoiler: t.NotRequired[t.Literal[True]]
    checklist: t.NotRequired["Checklist"]
    contact: t.NotRequired["Contact"]
    dice: t.NotRequired["Dice"]
    game: t.NotRequired["Game"]
    giveaway: t.NotRequired["Giveaway"]
    giveaway_winners: t.NotRequired["GiveawayWinners"]
    invoice: t.NotRequired["Invoice"]
    location: t.NotRequired["Location"]
    poll: t.NotRequired["Poll"]
    venue: t.NotRequired["Venue"]

class ReplyParameters(t.TypedDict):
    """
    ### [ReplyParameters](https://core.telegram.org/bots/api#replyparameters)  
    
    Describes reply parameters for the message that is being sent.
    """
    message_id: int
    chat_id: t.NotRequired[int | str]
    allow_sending_without_reply: t.NotRequired[bool]
    quote: t.NotRequired[str]
    quote_parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    quote_entities: t.NotRequired[list["MessageEntity"]]
    quote_position: t.NotRequired[int]
    checklist_task_id: t.NotRequired[int]

class MessageOriginUser(t.TypedDict):
    """
    ### [MessageOriginUser](https://core.telegram.org/bots/api#messageoriginuser)  
    
    The message was originally sent by a known user.
    """
    type: t.Literal["user"]
    date: int
    sender_user: "User"

class MessageOriginHiddenUser(t.TypedDict):
    """
    ### [MessageOriginHiddenUser](https://core.telegram.org/bots/api#messageoriginhiddenuser)  
    
    The message was originally sent by an unknown user.
    """
    type: t.Literal["hidden_user"]
    date: int
    sender_user_name: str

class MessageOriginChat(t.TypedDict):
    """
    ### [MessageOriginChat](https://core.telegram.org/bots/api#messageoriginchat)  
    
    The message was originally sent on behalf of a chat to a group chat.
    """
    type: t.Literal["chat"]
    date: int
    sender_chat: "Chat"
    author_signature: t.NotRequired[str]

class MessageOriginChannel(t.TypedDict):
    """
    ### [MessageOriginChannel](https://core.telegram.org/bots/api#messageoriginchannel)  
    
    The message was originally sent to a channel chat.
    """
    type: t.Literal["channel"]
    date: int
    chat: "Chat"
    message_id: int
    author_signature: t.NotRequired[str]

class PhotoSize(t.TypedDict):
    """
    ### [PhotoSize](https://core.telegram.org/bots/api#photosize)  
    
    This object represents one size of a photo or a [file](https://core.telegram.org/bots/api#document) / [sticker](https://core.telegram.org/bots/api#sticker) thumbnail.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: t.NotRequired[int]

class Animation(t.TypedDict):
    """
    ### [Animation](https://core.telegram.org/bots/api#animation)  
    
    This object represents an animation file (GIF or H.264/MPEG\\-4 AVC video without sound).
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: t.NotRequired["PhotoSize"]
    file_name: t.NotRequired[str]
    mime_type: t.NotRequired[str]
    file_size: t.NotRequired[int]

class Audio(t.TypedDict):
    """
    ### [Audio](https://core.telegram.org/bots/api#audio)  
    
    This object represents an audio file to be treated as music by the Telegram clients.
    """
    file_id: str
    file_unique_id: str
    duration: int
    performer: t.NotRequired[str]
    title: t.NotRequired[str]
    file_name: t.NotRequired[str]
    mime_type: t.NotRequired[str]
    file_size: t.NotRequired[int]
    thumbnail: t.NotRequired["PhotoSize"]

class Document(t.TypedDict):
    """
    ### [Document](https://core.telegram.org/bots/api#document)  
    
    This object represents a general file (as opposed to [photos](https://core.telegram.org/bots/api#photosize), [voice messages](https://core.telegram.org/bots/api#voice) and [audio files](https://core.telegram.org/bots/api#audio)).
    """
    file_id: str
    file_unique_id: str
    thumbnail: t.NotRequired["PhotoSize"]
    file_name: t.NotRequired[str]
    mime_type: t.NotRequired[str]
    file_size: t.NotRequired[int]

class Story(t.TypedDict):
    """
    ### [Story](https://core.telegram.org/bots/api#story)  
    
    This object represents a story.
    """
    chat: "Chat"
    id: int

class Video(t.TypedDict):
    """
    ### [Video](https://core.telegram.org/bots/api#video)  
    
    This object represents a video file.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: t.NotRequired["PhotoSize"]
    cover: t.NotRequired[list["PhotoSize"]]
    start_timestamp: t.NotRequired[int]
    file_name: t.NotRequired[str]
    mime_type: t.NotRequired[str]
    file_size: t.NotRequired[int]

class VideoNote(t.TypedDict):
    """
    ### [VideoNote](https://core.telegram.org/bots/api#videonote)  
    
    This object represents a [video message](https://telegram.org/blog/video-messages-and-telescope) (available in Telegram apps as of [v.4\\.0](https://telegram.org/blog/video-messages-and-telescope)).
    """
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: t.NotRequired["PhotoSize"]
    file_size: t.NotRequired[int]

class Voice(t.TypedDict):
    """
    ### [Voice](https://core.telegram.org/bots/api#voice)  
    
    This object represents a voice note.
    """
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: t.NotRequired[str]
    file_size: t.NotRequired[int]

class PaidMediaInfo(t.TypedDict):
    """
    ### [PaidMediaInfo](https://core.telegram.org/bots/api#paidmediainfo)  
    
    Describes the paid media added to a message.
    """
    star_count: int
    paid_media: list["PaidMedia"]

class PaidMediaPreview(t.TypedDict):
    """
    ### [PaidMediaPreview](https://core.telegram.org/bots/api#paidmediapreview)  
    
    The paid media isn't available before the payment.
    """
    type: t.Literal["preview"]
    width: t.NotRequired[int]
    height: t.NotRequired[int]
    duration: t.NotRequired[int]

class PaidMediaPhoto(t.TypedDict):
    """
    ### [PaidMediaPhoto](https://core.telegram.org/bots/api#paidmediaphoto)  
    
    The paid media is a photo.
    """
    type: t.Literal["photo"]
    photo: list["PhotoSize"]

class PaidMediaVideo(t.TypedDict):
    """
    ### [PaidMediaVideo](https://core.telegram.org/bots/api#paidmediavideo)  
    
    The paid media is a video.
    """
    type: t.Literal["video"]
    video: "Video"

class Contact(t.TypedDict):
    """
    ### [Contact](https://core.telegram.org/bots/api#contact)  
    
    This object represents a phone contact.
    """
    phone_number: str
    first_name: str
    last_name: t.NotRequired[str]
    user_id: t.NotRequired[int]
    vcard: t.NotRequired[str]

class Dice(t.TypedDict):
    """
    ### [Dice](https://core.telegram.org/bots/api#dice)  
    
    This object represents an animated emoji that displays a random value.
    """
    emoji: str
    value: int

class PollOption(t.TypedDict):
    """
    ### [PollOption](https://core.telegram.org/bots/api#polloption)  
    
    This object contains information about one answer option in a poll.
    """
    text: str
    voter_count: int
    text_entities: t.NotRequired[list["MessageEntity"]]

class InputPollOption(t.TypedDict):
    """
    ### [InputPollOption](https://core.telegram.org/bots/api#inputpolloption)  
    
    This object contains information about one answer option in a poll to be sent.
    """
    text: str
    text_parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    text_entities: t.NotRequired[list["MessageEntity"]]

class PollAnswer(t.TypedDict):
    """
    ### [PollAnswer](https://core.telegram.org/bots/api#pollanswer)  
    
    This object represents an answer of a user in a non\\-anonymous poll.
    """
    poll_id: str
    option_ids: list[int]
    voter_chat: t.NotRequired["Chat"]
    user: t.NotRequired["User"]

class Poll(t.TypedDict):
    """
    ### [Poll](https://core.telegram.org/bots/api#poll)  
    
    This object contains information about a poll.
    """
    id: str
    question: str
    options: list["PollOption"]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    question_entities: t.NotRequired[list["MessageEntity"]]
    correct_option_id: t.NotRequired[int]
    explanation: t.NotRequired[str]
    explanation_entities: t.NotRequired[list["MessageEntity"]]
    open_period: t.NotRequired[int]
    close_date: t.NotRequired[int]

class ChecklistTask(t.TypedDict):
    """
    ### [ChecklistTask](https://core.telegram.org/bots/api#checklisttask)  
    
    Describes a task in a checklist.
    """
    id: int
    text: str
    text_entities: t.NotRequired[list["MessageEntity"]]
    completed_by_user: t.NotRequired["User"]
    completion_date: t.NotRequired[int]

class Checklist(t.TypedDict):
    """
    ### [Checklist](https://core.telegram.org/bots/api#checklist)  
    
    Describes a checklist.
    """
    title: str
    tasks: list["ChecklistTask"]
    title_entities: t.NotRequired[list["MessageEntity"]]
    others_can_add_tasks: t.NotRequired[t.Literal[True]]
    others_can_mark_tasks_as_done: t.NotRequired[t.Literal[True]]

class InputChecklistTask(t.TypedDict):
    """
    ### [InputChecklistTask](https://core.telegram.org/bots/api#inputchecklisttask)  
    
    Describes a task to add to a checklist.
    """
    id: int
    text: str
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    text_entities: t.NotRequired[list["MessageEntity"]]

class InputChecklist(t.TypedDict):
    """
    ### [InputChecklist](https://core.telegram.org/bots/api#inputchecklist)  
    
    Describes a checklist to create.
    """
    title: str
    tasks: list["InputChecklistTask"]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    title_entities: t.NotRequired[list["MessageEntity"]]
    others_can_add_tasks: t.NotRequired[bool]
    others_can_mark_tasks_as_done: t.NotRequired[bool]

class ChecklistTasksDone(t.TypedDict):
    """
    ### [ChecklistTasksDone](https://core.telegram.org/bots/api#checklisttasksdone)  
    
    Describes a service message about checklist tasks marked as done or not done.
    """
    checklist_message: t.NotRequired["Message"]
    marked_as_done_task_ids: t.NotRequired[list[int]]
    marked_as_not_done_task_ids: t.NotRequired[list[int]]

class ChecklistTasksAdded(t.TypedDict):
    """
    ### [ChecklistTasksAdded](https://core.telegram.org/bots/api#checklisttasksadded)  
    
    Describes a service message about tasks added to a checklist.
    """
    tasks: list["ChecklistTask"]
    checklist_message: t.NotRequired["Message"]

class Location(t.TypedDict):
    """
    ### [Location](https://core.telegram.org/bots/api#location)  
    
    This object represents a point on the map.
    """
    latitude: float
    longitude: float
    horizontal_accuracy: t.NotRequired[float]
    live_period: t.NotRequired[int]
    heading: t.NotRequired[int]
    proximity_alert_radius: t.NotRequired[int]

class Venue(t.TypedDict):
    """
    ### [Venue](https://core.telegram.org/bots/api#venue)  
    
    This object represents a venue.
    """
    location: "Location"
    title: str
    address: str
    foursquare_id: t.NotRequired[str]
    foursquare_type: t.NotRequired[str]
    google_place_id: t.NotRequired[str]
    google_place_type: t.NotRequired[str]

class WebAppData(t.TypedDict):
    """
    ### [WebAppData](https://core.telegram.org/bots/api#webappdata)  
    
    Describes data sent from a [Web App](https://core.telegram.org/bots/webapps) to the bot.
    """
    data: str
    button_text: str

class ProximityAlertTriggered(t.TypedDict):
    """
    ### [ProximityAlertTriggered](https://core.telegram.org/bots/api#proximityalerttriggered)  
    
    This object represents the content of a service message, sent whenever a user in the chat triggers a proximity alert set by another user.
    """
    traveler: "User"
    watcher: "User"
    distance: int

class MessageAutoDeleteTimerChanged(t.TypedDict):
    """
    ### [MessageAutoDeleteTimerChanged](https://core.telegram.org/bots/api#messageautodeletetimerchanged)  
    
    This object represents a service message about a change in auto\\-delete timer settings.
    """
    message_auto_delete_time: int

class ChatBoostAdded(t.TypedDict):
    """
    ### [ChatBoostAdded](https://core.telegram.org/bots/api#chatboostadded)  
    
    This object represents a service message about a user boosting a chat.
    """
    boost_count: int

class BackgroundFillSolid(t.TypedDict):
    """
    ### [BackgroundFillSolid](https://core.telegram.org/bots/api#backgroundfillsolid)  
    
    The background is filled using the selected color.
    """
    type: t.Literal["solid"]
    color: int

class BackgroundFillGradient(t.TypedDict):
    """
    ### [BackgroundFillGradient](https://core.telegram.org/bots/api#backgroundfillgradient)  
    
    The background is a gradient fill.
    """
    type: t.Literal["gradient"]
    top_color: int
    bottom_color: int
    rotation_angle: int

class BackgroundFillFreeformGradient(t.TypedDict):
    """
    ### [BackgroundFillFreeformGradient](https://core.telegram.org/bots/api#backgroundfillfreeformgradient)  
    
    The background is a freeform gradient that rotates after every message in the chat.
    """
    type: t.Literal["freeform_gradient"]
    colors: list[int]

class BackgroundTypeFill(t.TypedDict):
    """
    ### [BackgroundTypeFill](https://core.telegram.org/bots/api#backgroundtypefill)  
    
    The background is automatically filled based on the selected colors.
    """
    type: t.Literal["fill"]
    fill: "BackgroundFill"
    dark_theme_dimming: int

class BackgroundTypeWallpaper(t.TypedDict):
    """
    ### [BackgroundTypeWallpaper](https://core.telegram.org/bots/api#backgroundtypewallpaper)  
    
    The background is a wallpaper in the JPEG format.
    """
    type: t.Literal["wallpaper"]
    document: "Document"
    dark_theme_dimming: int
    is_blurred: t.NotRequired[t.Literal[True]]
    is_moving: t.NotRequired[t.Literal[True]]

class BackgroundTypePattern(t.TypedDict):
    """
    ### [BackgroundTypePattern](https://core.telegram.org/bots/api#backgroundtypepattern)  
    
    The background is a .PNG or .TGV (gzipped subset of SVG with MIME type “application/x\\-tgwallpattern”) pattern to be combined with the background fill chosen by the user.
    """
    type: t.Literal["pattern"]
    document: "Document"
    fill: "BackgroundFill"
    intensity: int
    is_inverted: t.NotRequired[t.Literal[True]]
    is_moving: t.NotRequired[t.Literal[True]]

class BackgroundTypeChatTheme(t.TypedDict):
    """
    ### [BackgroundTypeChatTheme](https://core.telegram.org/bots/api#backgroundtypechattheme)  
    
    The background is taken directly from a built\\-in chat theme.
    """
    type: t.Literal["chat_theme"]
    theme_name: str

class ChatBackground(t.TypedDict):
    """
    ### [ChatBackground](https://core.telegram.org/bots/api#chatbackground)  
    
    This object represents a chat background.
    """
    type: "BackgroundType"

class ForumTopicCreated(t.TypedDict):
    """
    ### [ForumTopicCreated](https://core.telegram.org/bots/api#forumtopiccreated)  
    
    This object represents a service message about a new forum topic created in the chat.
    """
    name: str
    icon_color: int
    icon_custom_emoji_id: t.NotRequired[str]

class ForumTopicClosed(t.TypedDict):
    """
    ### [ForumTopicClosed](https://core.telegram.org/bots/api#forumtopicclosed)  
    
    This object represents a service message about a forum topic closed in the chat. Currently holds no information.
    """
    

class ForumTopicEdited(t.TypedDict):
    """
    ### [ForumTopicEdited](https://core.telegram.org/bots/api#forumtopicedited)  
    
    This object represents a service message about an edited forum topic.
    """
    name: t.NotRequired[str]
    icon_custom_emoji_id: t.NotRequired[str]

class ForumTopicReopened(t.TypedDict):
    """
    ### [ForumTopicReopened](https://core.telegram.org/bots/api#forumtopicreopened)  
    
    This object represents a service message about a forum topic reopened in the chat. Currently holds no information.
    """
    

class GeneralForumTopicHidden(t.TypedDict):
    """
    ### [GeneralForumTopicHidden](https://core.telegram.org/bots/api#generalforumtopichidden)  
    
    This object represents a service message about General forum topic hidden in the chat. Currently holds no information.
    """
    

class GeneralForumTopicUnhidden(t.TypedDict):
    """
    ### [GeneralForumTopicUnhidden](https://core.telegram.org/bots/api#generalforumtopicunhidden)  
    
    This object represents a service message about General forum topic unhidden in the chat. Currently holds no information.
    """
    

class SharedUser(t.TypedDict):
    """
    ### [SharedUser](https://core.telegram.org/bots/api#shareduser)  
    
    This object contains information about a user that was shared with the bot using a [KeyboardButtonRequestUsers](https://core.telegram.org/bots/api#keyboardbuttonrequestusers) button.
    """
    user_id: int
    first_name: t.NotRequired[str]
    last_name: t.NotRequired[str]
    username: t.NotRequired[str]
    photo: t.NotRequired[list["PhotoSize"]]

class UsersShared(t.TypedDict):
    """
    ### [UsersShared](https://core.telegram.org/bots/api#usersshared)  
    
    This object contains information about the users whose identifiers were shared with the bot using a [KeyboardButtonRequestUsers](https://core.telegram.org/bots/api#keyboardbuttonrequestusers) button.
    """
    request_id: int
    users: list["SharedUser"]

class ChatShared(t.TypedDict):
    """
    ### [ChatShared](https://core.telegram.org/bots/api#chatshared)  
    
    This object contains information about a chat that was shared with the bot using a [KeyboardButtonRequestChat](https://core.telegram.org/bots/api#keyboardbuttonrequestchat) button.
    """
    request_id: int
    chat_id: int
    title: t.NotRequired[str]
    username: t.NotRequired[str]
    photo: t.NotRequired[list["PhotoSize"]]

class WriteAccessAllowed(t.TypedDict):
    """
    ### [WriteAccessAllowed](https://core.telegram.org/bots/api#writeaccessallowed)  
    
    This object represents a service message about a user allowing a bot to write messages after adding it to the attachment menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method [requestWriteAccess](https://core.telegram.org/bots/webapps#initializing-mini-apps).
    """
    from_request: t.NotRequired[bool]
    web_app_name: t.NotRequired[str]
    from_attachment_menu: t.NotRequired[bool]

class VideoChatScheduled(t.TypedDict):
    """
    ### [VideoChatScheduled](https://core.telegram.org/bots/api#videochatscheduled)  
    
    This object represents a service message about a video chat scheduled in the chat.
    """
    start_date: int

class VideoChatStarted(t.TypedDict):
    """
    ### [VideoChatStarted](https://core.telegram.org/bots/api#videochatstarted)  
    
    This object represents a service message about a video chat started in the chat. Currently holds no information.
    """
    

class VideoChatEnded(t.TypedDict):
    """
    ### [VideoChatEnded](https://core.telegram.org/bots/api#videochatended)  
    
    This object represents a service message about a video chat ended in the chat.
    """
    duration: int

class VideoChatParticipantsInvited(t.TypedDict):
    """
    ### [VideoChatParticipantsInvited](https://core.telegram.org/bots/api#videochatparticipantsinvited)  
    
    This object represents a service message about new members invited to a video chat.
    """
    users: list["User"]

class PaidMessagePriceChanged(t.TypedDict):
    """
    ### [PaidMessagePriceChanged](https://core.telegram.org/bots/api#paidmessagepricechanged)  
    
    Describes a service message about a change in the price of paid messages within a chat.
    """
    paid_message_star_count: int

class DirectMessagePriceChanged(t.TypedDict):
    """
    ### [DirectMessagePriceChanged](https://core.telegram.org/bots/api#directmessagepricechanged)  
    
    Describes a service message about a change in the price of direct messages sent to a channel chat.
    """
    are_direct_messages_enabled: bool
    direct_message_star_count: t.NotRequired[int]

class SuggestedPostApproved(t.TypedDict):
    """
    ### [SuggestedPostApproved](https://core.telegram.org/bots/api#suggestedpostapproved)  
    
    Describes a service message about the approval of a suggested post.
    """
    send_date: int
    suggested_post_message: t.NotRequired["Message"]
    price: t.NotRequired["SuggestedPostPrice"]

class SuggestedPostApprovalFailed(t.TypedDict):
    """
    ### [SuggestedPostApprovalFailed](https://core.telegram.org/bots/api#suggestedpostapprovalfailed)  
    
    Describes a service message about the failed approval of a suggested post. Currently, only caused by insufficient user funds at the time of approval.
    """
    price: "SuggestedPostPrice"
    suggested_post_message: t.NotRequired["Message"]

class SuggestedPostDeclined(t.TypedDict):
    """
    ### [SuggestedPostDeclined](https://core.telegram.org/bots/api#suggestedpostdeclined)  
    
    Describes a service message about the rejection of a suggested post.
    """
    suggested_post_message: t.NotRequired["Message"]
    comment: t.NotRequired[str]

class SuggestedPostPaid(t.TypedDict):
    """
    ### [SuggestedPostPaid](https://core.telegram.org/bots/api#suggestedpostpaid)  
    
    Describes a service message about a successful payment for a suggested post.
    """
    currency: str
    suggested_post_message: t.NotRequired["Message"]
    amount: t.NotRequired[int]
    star_amount: t.NotRequired["StarAmount"]

class SuggestedPostRefunded(t.TypedDict):
    """
    ### [SuggestedPostRefunded](https://core.telegram.org/bots/api#suggestedpostrefunded)  
    
    Describes a service message about a payment refund for a suggested post.
    """
    reason: str
    suggested_post_message: t.NotRequired["Message"]

class GiveawayCreated(t.TypedDict):
    """
    ### [GiveawayCreated](https://core.telegram.org/bots/api#giveawaycreated)  
    
    This object represents a service message about the creation of a scheduled giveaway.
    """
    prize_star_count: t.NotRequired[int]

class Giveaway(t.TypedDict):
    """
    ### [Giveaway](https://core.telegram.org/bots/api#giveaway)  
    
    This object represents a message about a scheduled giveaway.
    """
    chats: list["Chat"]
    winners_selection_date: int
    winner_count: int
    only_new_members: t.NotRequired[t.Literal[True]]
    has_public_winners: t.NotRequired[t.Literal[True]]
    prize_description: t.NotRequired[str]
    country_codes: t.NotRequired[list[str]]
    prize_star_count: t.NotRequired[int]
    premium_subscription_month_count: t.NotRequired[int]

class GiveawayWinners(t.TypedDict):
    """
    ### [GiveawayWinners](https://core.telegram.org/bots/api#giveawaywinners)  
    
    This object represents a message about the completion of a giveaway with public winners.
    """
    chat: "Chat"
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: list["User"]
    additional_chat_count: t.NotRequired[int]
    prize_star_count: t.NotRequired[int]
    premium_subscription_month_count: t.NotRequired[int]
    unclaimed_prize_count: t.NotRequired[int]
    only_new_members: t.NotRequired[t.Literal[True]]
    was_refunded: t.NotRequired[t.Literal[True]]
    prize_description: t.NotRequired[str]

class GiveawayCompleted(t.TypedDict):
    """
    ### [GiveawayCompleted](https://core.telegram.org/bots/api#giveawaycompleted)  
    
    This object represents a service message about the completion of a giveaway without public winners.
    """
    winner_count: int
    unclaimed_prize_count: t.NotRequired[int]
    giveaway_message: t.NotRequired["Message"]
    is_star_giveaway: t.NotRequired[t.Literal[True]]

class LinkPreviewOptions(t.TypedDict):
    """
    ### [LinkPreviewOptions](https://core.telegram.org/bots/api#linkpreviewoptions)  
    
    Describes the options used for link preview generation.
    """
    is_disabled: t.NotRequired[bool]
    url: t.NotRequired[str]
    prefer_small_media: t.NotRequired[bool]
    prefer_large_media: t.NotRequired[bool]
    show_above_text: t.NotRequired[bool]

class SuggestedPostPrice(t.TypedDict):
    """
    ### [SuggestedPostPrice](https://core.telegram.org/bots/api#suggestedpostprice)  
    
    Describes the price of a suggested post.
    """
    currency: str
    amount: int

class SuggestedPostInfo(t.TypedDict):
    """
    ### [SuggestedPostInfo](https://core.telegram.org/bots/api#suggestedpostinfo)  
    
    Contains information about a suggested post.
    """
    state: str
    price: t.NotRequired["SuggestedPostPrice"]
    send_date: t.NotRequired[int]

class SuggestedPostParameters(t.TypedDict):
    """
    ### [SuggestedPostParameters](https://core.telegram.org/bots/api#suggestedpostparameters)  
    
    Contains parameters of a post that is being suggested by the bot.
    """
    price: t.NotRequired["SuggestedPostPrice"]
    send_date: t.NotRequired[int]

class DirectMessagesTopic(t.TypedDict):
    """
    ### [DirectMessagesTopic](https://core.telegram.org/bots/api#directmessagestopic)  
    
    Describes a topic of a direct messages chat.
    """
    topic_id: int
    user: t.NotRequired["User"]

class UserProfilePhotos(t.TypedDict):
    """
    ### [UserProfilePhotos](https://core.telegram.org/bots/api#userprofilephotos)  
    
    This object represent a user's profile pictures.
    """
    total_count: int
    photos: list[list["PhotoSize"]]

class File(t.TypedDict):
    """
    ### [File](https://core.telegram.org/bots/api#file)  
    
    This object represents a file ready to be downloaded. The file can be downloaded via the link `https://api.telegram.org/file/bot<token>/<file_path>`. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling [getFile](https://core.telegram.org/bots/api#getfile).
    
    The maximum file size to download is 20 MB
    """
    file_id: str
    file_unique_id: str
    file_size: t.NotRequired[int]
    file_path: t.NotRequired[str]

class WebAppInfo(t.TypedDict):
    """
    ### [WebAppInfo](https://core.telegram.org/bots/api#webappinfo)  
    
    Describes a [Web App](https://core.telegram.org/bots/webapps).
    """
    url: str

class ReplyKeyboardMarkup(t.TypedDict):
    """
    ### [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)  
    
    This object represents a [custom keyboard](https://core.telegram.org/bots/features#keyboards) with reply options (see [Introduction to bots](https://core.telegram.org/bots/features#keyboards) for details and examples). Not supported in channels and for messages sent on behalf of a Telegram Business account.
    """
    keyboard: list[list["KeyboardButton"]]
    is_persistent: t.NotRequired[bool]
    resize_keyboard: t.NotRequired[bool]
    one_time_keyboard: t.NotRequired[bool]
    input_field_placeholder: t.NotRequired[str]
    selective: t.NotRequired[bool]

class KeyboardButton(t.TypedDict):
    """
    ### [KeyboardButton](https://core.telegram.org/bots/api#keyboardbutton)  
    
    This object represents one button of the reply keyboard. At most one of the optional fields must be used to specify type of the button. For simple text buttons, *String* can be used instead of this object to specify the button text.
    
    **Note:** *request\\_users* and *request\\_chat* options will only work in Telegram versions released after 3 February, 2023\\. Older clients will display *unsupported message*.
    """
    text: str
    request_users: t.NotRequired["KeyboardButtonRequestUsers"]
    request_chat: t.NotRequired["KeyboardButtonRequestChat"]
    request_contact: t.NotRequired[bool]
    request_location: t.NotRequired[bool]
    request_poll: t.NotRequired["KeyboardButtonPollType"]
    web_app: t.NotRequired["WebAppInfo"]

class KeyboardButtonRequestUsers(t.TypedDict):
    """
    ### [KeyboardButtonRequestUsers](https://core.telegram.org/bots/api#keyboardbuttonrequestusers)  
    
    This object defines the criteria used to request suitable users. Information about the selected users will be shared with the bot when the corresponding button is pressed. [More about requesting users »](https://core.telegram.org/bots/features#chat-and-user-selection)
    """
    request_id: int
    user_is_bot: t.NotRequired[bool]
    user_is_premium: t.NotRequired[bool]
    max_quantity: t.NotRequired[int]
    request_name: t.NotRequired[bool]
    request_username: t.NotRequired[bool]
    request_photo: t.NotRequired[bool]

class KeyboardButtonRequestChat(t.TypedDict):
    """
    ### [KeyboardButtonRequestChat](https://core.telegram.org/bots/api#keyboardbuttonrequestchat)  
    
    This object defines the criteria used to request a suitable chat. Information about the selected chat will be shared with the bot when the corresponding button is pressed. The bot will be granted requested rights in the chat if appropriate. [More about requesting chats »](https://core.telegram.org/bots/features#chat-and-user-selection).
    """
    request_id: int
    chat_is_channel: bool
    chat_is_forum: t.NotRequired[bool]
    chat_has_username: t.NotRequired[bool]
    chat_is_created: t.NotRequired[bool]
    user_administrator_rights: t.NotRequired["ChatAdministratorRights"]
    bot_administrator_rights: t.NotRequired["ChatAdministratorRights"]
    bot_is_member: t.NotRequired[bool]
    request_title: t.NotRequired[bool]
    request_username: t.NotRequired[bool]
    request_photo: t.NotRequired[bool]

class KeyboardButtonPollType(t.TypedDict):
    """
    ### [KeyboardButtonPollType](https://core.telegram.org/bots/api#keyboardbuttonpolltype)  
    
    This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.
    """
    type: t.NotRequired[str]

class ReplyKeyboardRemove(t.TypedDict):
    """
    ### [ReplyKeyboardRemove](https://core.telegram.org/bots/api#replykeyboardremove)  
    
    Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter\\-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one\\-time keyboards that are hidden immediately after the user presses a button (see [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)). Not supported in channels and for messages sent on behalf of a Telegram Business account.
    """
    remove_keyboard: t.Literal[True]
    selective: t.NotRequired[bool]

class InlineKeyboardMarkup(t.TypedDict):
    """
    ### [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup)  
    
    This object represents an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards) that appears right next to the message it belongs to.
    """
    inline_keyboard: list[list["InlineKeyboardButton"]]

class InlineKeyboardButton(t.TypedDict):
    """
    ### [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)  
    
    This object represents one button of an inline keyboard. Exactly one of the optional fields must be used to specify type of the button.
    """
    text: str
    url: t.NotRequired[str]
    callback_data: t.NotRequired[str]
    web_app: t.NotRequired["WebAppInfo"]
    login_url: t.NotRequired["LoginUrl"]
    switch_inline_query: t.NotRequired[str]
    switch_inline_query_current_chat: t.NotRequired[str]
    switch_inline_query_chosen_chat: t.NotRequired["SwitchInlineQueryChosenChat"]
    copy_text: t.NotRequired["CopyTextButton"]
    callback_game: t.NotRequired["CallbackGame"]
    pay: t.NotRequired[bool]

class LoginUrl(t.TypedDict):
    """
    ### [LoginUrl](https://core.telegram.org/bots/api#loginurl)  
    
    This object represents a parameter of the inline keyboard button used to automatically authorize a user. Serves as a great replacement for the [Telegram Login Widget](https://core.telegram.org/widgets/login) when the user is coming from Telegram. All the user needs to do is tap/click a button and confirm that they want to log in:
    
    Telegram apps support these buttons as of [version 5\\.7](https://telegram.org/blog/privacy-discussions-web-bots#meet-seamless-web-bots).
    
    Sample bot: [@discussbot](https://t.me/discussbot)
    """
    url: str
    forward_text: t.NotRequired[str]
    bot_username: t.NotRequired[str]
    request_write_access: t.NotRequired[bool]

class SwitchInlineQueryChosenChat(t.TypedDict):
    """
    ### [SwitchInlineQueryChosenChat](https://core.telegram.org/bots/api#switchinlinequerychosenchat)  
    
    This object represents an inline button that switches the current user to inline mode in a chosen chat, with an optional default inline query.
    """
    query: t.NotRequired[str]
    allow_user_chats: t.NotRequired[bool]
    allow_bot_chats: t.NotRequired[bool]
    allow_group_chats: t.NotRequired[bool]
    allow_channel_chats: t.NotRequired[bool]

class CopyTextButton(t.TypedDict):
    """
    ### [CopyTextButton](https://core.telegram.org/bots/api#copytextbutton)  
    
    This object represents an inline keyboard button that copies specified text to the clipboard.
    """
    text: str

class CallbackQuery(t.TypedDict("CallbackQuery", {"from": "User"})):
    """
    ### [CallbackQuery](https://core.telegram.org/bots/api#callbackquery)  
    
    This object represents an incoming callback query from a callback button in an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards). If the button that originated the query was attached to a message sent by the bot, the field *message* will be present. If the button was attached to a message sent via the bot (in [inline mode](https://core.telegram.org/bots/api#inline-mode)), the field *inline\\_message\\_id* will be present. Exactly one of the fields *data* or *game\\_short\\_name* will be present.
    
    **NOTE:** After the user presses a callback button, Telegram clients will display a progress bar until you call [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery). It is, therefore, necessary to react by calling [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery) even if no notification to the user is needed (e.g., without specifying any of the optional parameters).
    """
    id: str
    chat_instance: str
    message: t.NotRequired["MaybeInaccessibleMessage"]
    inline_message_id: t.NotRequired[str]
    data: t.NotRequired[str]
    game_short_name: t.NotRequired[str]

class ForceReply(t.TypedDict):
    """
    ### [ForceReply](https://core.telegram.org/bots/api#forcereply)  
    
    Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if the user has selected the bot's message and tapped 'Reply'). This can be extremely useful if you want to create user\\-friendly step\\-by\\-step interfaces without having to sacrifice [privacy mode](https://core.telegram.org/bots/features#privacy-mode). Not supported in channels and for messages sent on behalf of a Telegram Business account.
    
    **Example:** A [poll bot](https://t.me/PollBot) for groups runs in privacy mode (only receives commands, replies to its messages and mentions). There could be two ways to create a new poll:
    
    * Explain the user how to send a command with parameters (e.g. /newpoll question answer1 answer2\\). May be appealing for hardcore users but lacks modern day polish.
    * Guide the user through a step\\-by\\-step process. 'Please send me your question', 'Cool, now let's add the first answer option', 'Great. Keep adding answer options, then send /done when you're ready'.
    
    The last option is definitely more attractive. And if you use [ForceReply](https://core.telegram.org/bots/api#forcereply) in your bot's questions, it will receive the user's answers even if it only receives replies, commands and mentions \\- without any extra work for the user.
    """
    force_reply: t.Literal[True]
    input_field_placeholder: t.NotRequired[str]
    selective: t.NotRequired[bool]

class ChatPhoto(t.TypedDict):
    """
    ### [ChatPhoto](https://core.telegram.org/bots/api#chatphoto)  
    
    This object represents a chat photo.
    """
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

class ChatInviteLink(t.TypedDict):
    """
    ### [ChatInviteLink](https://core.telegram.org/bots/api#chatinvitelink)  
    
    Represents an invite link for a chat.
    """
    invite_link: str
    creator: "User"
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: t.NotRequired[str]
    expire_date: t.NotRequired[int]
    member_limit: t.NotRequired[int]
    pending_join_request_count: t.NotRequired[int]
    subscription_period: t.NotRequired[int]
    subscription_price: t.NotRequired[int]

class ChatAdministratorRights(t.TypedDict):
    """
    ### [ChatAdministratorRights](https://core.telegram.org/bots/api#chatadministratorrights)  
    
    Represents the rights of an administrator in a chat.
    """
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: t.NotRequired[bool]
    can_edit_messages: t.NotRequired[bool]
    can_pin_messages: t.NotRequired[bool]
    can_manage_topics: t.NotRequired[bool]
    can_manage_direct_messages: t.NotRequired[bool]

class ChatMemberUpdated(t.TypedDict("ChatMemberUpdated", {"from": "User"})):
    """
    ### [ChatMemberUpdated](https://core.telegram.org/bots/api#chatmemberupdated)  
    
    This object represents changes in the status of a chat member.
    """
    chat: "Chat"
    date: int
    old_chat_member: "ChatMember"
    new_chat_member: "ChatMember"
    invite_link: t.NotRequired["ChatInviteLink"]
    via_join_request: t.NotRequired[bool]
    via_chat_folder_invite_link: t.NotRequired[bool]

class ChatMemberOwner(t.TypedDict):
    """
    ### [ChatMemberOwner](https://core.telegram.org/bots/api#chatmemberowner)  
    
    Represents a [chat member](https://core.telegram.org/bots/api#chatmember) that owns the chat and has all administrator privileges.
    """
    status: t.Literal["creator"]
    user: "User"
    is_anonymous: bool
    custom_title: t.NotRequired[str]

class ChatMemberAdministrator(t.TypedDict):
    """
    ### [ChatMemberAdministrator](https://core.telegram.org/bots/api#chatmemberadministrator)  
    
    Represents a [chat member](https://core.telegram.org/bots/api#chatmember) that has some additional privileges.
    """
    status: t.Literal["administrator"]
    user: "User"
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: t.NotRequired[bool]
    can_edit_messages: t.NotRequired[bool]
    can_pin_messages: t.NotRequired[bool]
    can_manage_topics: t.NotRequired[bool]
    can_manage_direct_messages: t.NotRequired[bool]
    custom_title: t.NotRequired[str]

class ChatMemberMember(t.TypedDict):
    """
    ### [ChatMemberMember](https://core.telegram.org/bots/api#chatmembermember)  
    
    Represents a [chat member](https://core.telegram.org/bots/api#chatmember) that has no additional privileges or restrictions.
    """
    status: t.Literal["member"]
    user: "User"
    until_date: t.NotRequired[int]

class ChatMemberRestricted(t.TypedDict):
    """
    ### [ChatMemberRestricted](https://core.telegram.org/bots/api#chatmemberrestricted)  
    
    Represents a [chat member](https://core.telegram.org/bots/api#chatmember) that is under certain restrictions in the chat. Supergroups only.
    """
    status: t.Literal["restricted"]
    user: "User"
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int

class ChatMemberLeft(t.TypedDict):
    """
    ### [ChatMemberLeft](https://core.telegram.org/bots/api#chatmemberleft)  
    
    Represents a [chat member](https://core.telegram.org/bots/api#chatmember) that isn't currently a member of the chat, but may join it themselves.
    """
    status: t.Literal["left"]
    user: "User"

class ChatMemberBanned(t.TypedDict):
    """
    ### [ChatMemberBanned](https://core.telegram.org/bots/api#chatmemberbanned)  
    
    Represents a [chat member](https://core.telegram.org/bots/api#chatmember) that was banned in the chat and can't return to the chat or view chat messages.
    """
    status: t.Literal["kicked"]
    user: "User"
    until_date: int

class ChatJoinRequest(t.TypedDict("ChatJoinRequest", {"from": "User"})):
    """
    ### [ChatJoinRequest](https://core.telegram.org/bots/api#chatjoinrequest)  
    
    Represents a join request sent to a chat.
    """
    chat: "Chat"
    user_chat_id: int
    date: int
    bio: t.NotRequired[str]
    invite_link: t.NotRequired["ChatInviteLink"]

class ChatPermissions(t.TypedDict):
    """
    ### [ChatPermissions](https://core.telegram.org/bots/api#chatpermissions)  
    
    Describes actions that a non\\-administrator user is allowed to take in a chat.
    """
    can_send_messages: t.NotRequired[bool]
    can_send_audios: t.NotRequired[bool]
    can_send_documents: t.NotRequired[bool]
    can_send_photos: t.NotRequired[bool]
    can_send_videos: t.NotRequired[bool]
    can_send_video_notes: t.NotRequired[bool]
    can_send_voice_notes: t.NotRequired[bool]
    can_send_polls: t.NotRequired[bool]
    can_send_other_messages: t.NotRequired[bool]
    can_add_web_page_previews: t.NotRequired[bool]
    can_change_info: t.NotRequired[bool]
    can_invite_users: t.NotRequired[bool]
    can_pin_messages: t.NotRequired[bool]
    can_manage_topics: t.NotRequired[bool]

class Birthdate(t.TypedDict):
    """
    ### [Birthdate](https://core.telegram.org/bots/api#birthdate)  
    
    Describes the birthdate of a user.
    """
    day: int
    month: int
    year: t.NotRequired[int]

class BusinessIntro(t.TypedDict):
    """
    ### [BusinessIntro](https://core.telegram.org/bots/api#businessintro)  
    
    Contains information about the start page settings of a Telegram Business account.
    """
    title: t.NotRequired[str]
    message: t.NotRequired[str]
    sticker: t.NotRequired["Sticker"]

class BusinessLocation(t.TypedDict):
    """
    ### [BusinessLocation](https://core.telegram.org/bots/api#businesslocation)  
    
    Contains information about the location of a Telegram Business account.
    """
    address: str
    location: t.NotRequired["Location"]

class BusinessOpeningHoursInterval(t.TypedDict):
    """
    ### [BusinessOpeningHoursInterval](https://core.telegram.org/bots/api#businessopeninghoursinterval)  
    
    Describes an interval of time during which a business is open.
    """
    opening_minute: int
    closing_minute: int

class BusinessOpeningHours(t.TypedDict):
    """
    ### [BusinessOpeningHours](https://core.telegram.org/bots/api#businessopeninghours)  
    
    Describes the opening hours of a business.
    """
    time_zone_name: str
    opening_hours: list["BusinessOpeningHoursInterval"]

class StoryAreaPosition(t.TypedDict):
    """
    ### [StoryAreaPosition](https://core.telegram.org/bots/api#storyareaposition)  
    
    Describes the position of a clickable area within a story.
    """
    x_percentage: float
    y_percentage: float
    width_percentage: float
    height_percentage: float
    rotation_angle: float
    corner_radius_percentage: float

class LocationAddress(t.TypedDict):
    """
    ### [LocationAddress](https://core.telegram.org/bots/api#locationaddress)  
    
    Describes the physical address of a location.
    """
    country_code: str
    state: t.NotRequired[str]
    city: t.NotRequired[str]
    street: t.NotRequired[str]

class StoryAreaTypeLocation(t.TypedDict):
    """
    ### [StoryAreaTypeLocation](https://core.telegram.org/bots/api#storyareatypelocation)  
    
    Describes a story area pointing to a location. Currently, a story can have up to 10 location areas.
    """
    type: t.Literal["location"]
    latitude: float
    longitude: float
    address: t.NotRequired["LocationAddress"]

class StoryAreaTypeSuggestedReaction(t.TypedDict):
    """
    ### [StoryAreaTypeSuggestedReaction](https://core.telegram.org/bots/api#storyareatypesuggestedreaction)  
    
    Describes a story area pointing to a suggested reaction. Currently, a story can have up to 5 suggested reaction areas.
    """
    type: t.Literal["suggested_reaction"]
    reaction_type: "ReactionType"
    is_dark: t.NotRequired[bool]
    is_flipped: t.NotRequired[bool]

class StoryAreaTypeLink(t.TypedDict):
    """
    ### [StoryAreaTypeLink](https://core.telegram.org/bots/api#storyareatypelink)  
    
    Describes a story area pointing to an HTTP or tg:// link. Currently, a story can have up to 3 link areas.
    """
    type: t.Literal["link"]
    url: str

class StoryAreaTypeWeather(t.TypedDict):
    """
    ### [StoryAreaTypeWeather](https://core.telegram.org/bots/api#storyareatypeweather)  
    
    Describes a story area containing weather information. Currently, a story can have up to 3 weather areas.
    """
    type: t.Literal["weather"]
    temperature: float
    emoji: str
    background_color: int

class StoryAreaTypeUniqueGift(t.TypedDict):
    """
    ### [StoryAreaTypeUniqueGift](https://core.telegram.org/bots/api#storyareatypeuniquegift)  
    
    Describes a story area pointing to a unique gift. Currently, a story can have at most 1 unique gift area.
    """
    type: t.Literal["unique_gift"]
    name: str

class StoryArea(t.TypedDict):
    """
    ### [StoryArea](https://core.telegram.org/bots/api#storyarea)  
    
    Describes a clickable area on a story media.
    """
    position: "StoryAreaPosition"
    type: "StoryAreaType"

class ChatLocation(t.TypedDict):
    """
    ### [ChatLocation](https://core.telegram.org/bots/api#chatlocation)  
    
    Represents a location to which a chat is connected.
    """
    location: "Location"
    address: str

class ReactionTypeEmoji(t.TypedDict):
    """
    ### [ReactionTypeEmoji](https://core.telegram.org/bots/api#reactiontypeemoji)  
    
    The reaction is based on an emoji.
    """
    type: t.Literal["emoji"]
    emoji: literals.ReactionEmoji

class ReactionTypeCustomEmoji(t.TypedDict):
    """
    ### [ReactionTypeCustomEmoji](https://core.telegram.org/bots/api#reactiontypecustomemoji)  
    
    The reaction is based on a custom emoji.
    """
    type: t.Literal["custom_emoji"]
    custom_emoji_id: str

class ReactionTypePaid(t.TypedDict):
    """
    ### [ReactionTypePaid](https://core.telegram.org/bots/api#reactiontypepaid)  
    
    The reaction is paid.
    """
    type: t.Literal["paid"]

class ReactionCount(t.TypedDict):
    """
    ### [ReactionCount](https://core.telegram.org/bots/api#reactioncount)  
    
    Represents a reaction added to a message along with the number of times it was added.
    """
    type: "ReactionType"
    total_count: int

class MessageReactionUpdated(t.TypedDict):
    """
    ### [MessageReactionUpdated](https://core.telegram.org/bots/api#messagereactionupdated)  
    
    This object represents a change of a reaction on a message performed by a user.
    """
    chat: "Chat"
    message_id: int
    date: int
    old_reaction: list["ReactionType"]
    new_reaction: list["ReactionType"]
    user: t.NotRequired["User"]
    actor_chat: t.NotRequired["Chat"]

class MessageReactionCountUpdated(t.TypedDict):
    """
    ### [MessageReactionCountUpdated](https://core.telegram.org/bots/api#messagereactioncountupdated)  
    
    This object represents reaction changes on a message with anonymous reactions.
    """
    chat: "Chat"
    message_id: int
    date: int
    reactions: list["ReactionCount"]

class ForumTopic(t.TypedDict):
    """
    ### [ForumTopic](https://core.telegram.org/bots/api#forumtopic)  
    
    This object represents a forum topic.
    """
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: t.NotRequired[str]

class Gift(t.TypedDict):
    """
    ### [Gift](https://core.telegram.org/bots/api#gift)  
    
    This object represents a gift that can be sent by the bot.
    """
    id: str
    sticker: "Sticker"
    star_count: int
    upgrade_star_count: t.NotRequired[int]
    total_count: t.NotRequired[int]
    remaining_count: t.NotRequired[int]
    publisher_chat: t.NotRequired["Chat"]

class Gifts(t.TypedDict):
    """
    ### [Gifts](https://core.telegram.org/bots/api#gifts)  
    
    This object represent a list of gifts.
    """
    gifts: list["Gift"]

class UniqueGiftModel(t.TypedDict):
    """
    ### [UniqueGiftModel](https://core.telegram.org/bots/api#uniquegiftmodel)  
    
    This object describes the model of a unique gift.
    """
    name: str
    sticker: "Sticker"
    rarity_per_mille: int

class UniqueGiftSymbol(t.TypedDict):
    """
    ### [UniqueGiftSymbol](https://core.telegram.org/bots/api#uniquegiftsymbol)  
    
    This object describes the symbol shown on the pattern of a unique gift.
    """
    name: str
    sticker: "Sticker"
    rarity_per_mille: int

class UniqueGiftBackdropColors(t.TypedDict):
    """
    ### [UniqueGiftBackdropColors](https://core.telegram.org/bots/api#uniquegiftbackdropcolors)  
    
    This object describes the colors of the backdrop of a unique gift.
    """
    center_color: int
    edge_color: int
    symbol_color: int
    text_color: int

class UniqueGiftBackdrop(t.TypedDict):
    """
    ### [UniqueGiftBackdrop](https://core.telegram.org/bots/api#uniquegiftbackdrop)  
    
    This object describes the backdrop of a unique gift.
    """
    name: str
    colors: "UniqueGiftBackdropColors"
    rarity_per_mille: int

class UniqueGift(t.TypedDict):
    """
    ### [UniqueGift](https://core.telegram.org/bots/api#uniquegift)  
    
    This object describes a unique gift that was upgraded from a regular gift.
    """
    base_name: str
    name: str
    number: int
    model: "UniqueGiftModel"
    symbol: "UniqueGiftSymbol"
    backdrop: "UniqueGiftBackdrop"
    publisher_chat: t.NotRequired["Chat"]

class GiftInfo(t.TypedDict):
    """
    ### [GiftInfo](https://core.telegram.org/bots/api#giftinfo)  
    
    Describes a service message about a regular gift that was sent or received.
    """
    gift: "Gift"
    owned_gift_id: t.NotRequired[str]
    convert_star_count: t.NotRequired[int]
    prepaid_upgrade_star_count: t.NotRequired[int]
    can_be_upgraded: t.NotRequired[t.Literal[True]]
    text: t.NotRequired[str]
    entities: t.NotRequired[list["MessageEntity"]]
    is_private: t.NotRequired[t.Literal[True]]

class UniqueGiftInfo(t.TypedDict):
    """
    ### [UniqueGiftInfo](https://core.telegram.org/bots/api#uniquegiftinfo)  
    
    Describes a service message about a unique gift that was sent or received.
    """
    gift: "UniqueGift"
    origin: str
    last_resale_star_count: t.NotRequired[int]
    owned_gift_id: t.NotRequired[str]
    transfer_star_count: t.NotRequired[int]
    next_transfer_date: t.NotRequired[int]

class OwnedGiftRegular(t.TypedDict):
    """
    ### [OwnedGiftRegular](https://core.telegram.org/bots/api#ownedgiftregular)  
    
    Describes a regular gift owned by a user or a chat.
    """
    type: t.Literal["regular"]
    gift: "Gift"
    send_date: int
    owned_gift_id: t.NotRequired[str]
    sender_user: t.NotRequired["User"]
    text: t.NotRequired[str]
    entities: t.NotRequired[list["MessageEntity"]]
    is_private: t.NotRequired[t.Literal[True]]
    is_saved: t.NotRequired[t.Literal[True]]
    can_be_upgraded: t.NotRequired[t.Literal[True]]
    was_refunded: t.NotRequired[t.Literal[True]]
    convert_star_count: t.NotRequired[int]
    prepaid_upgrade_star_count: t.NotRequired[int]

class OwnedGiftUnique(t.TypedDict):
    """
    ### [OwnedGiftUnique](https://core.telegram.org/bots/api#ownedgiftunique)  
    
    Describes a unique gift received and owned by a user or a chat.
    """
    type: t.Literal["unique"]
    gift: "UniqueGift"
    send_date: int
    owned_gift_id: t.NotRequired[str]
    sender_user: t.NotRequired["User"]
    is_saved: t.NotRequired[t.Literal[True]]
    can_be_transferred: t.NotRequired[t.Literal[True]]
    transfer_star_count: t.NotRequired[int]
    next_transfer_date: t.NotRequired[int]

class OwnedGifts(t.TypedDict):
    """
    ### [OwnedGifts](https://core.telegram.org/bots/api#ownedgifts)  
    
    Contains the list of gifts received and owned by a user or a chat.
    """
    total_count: int
    gifts: list["OwnedGift"]
    next_offset: t.NotRequired[str]

class AcceptedGiftTypes(t.TypedDict):
    """
    ### [AcceptedGiftTypes](https://core.telegram.org/bots/api#acceptedgifttypes)  
    
    This object describes the types of gifts that can be gifted to a user or a chat.
    """
    unlimited_gifts: bool
    limited_gifts: bool
    unique_gifts: bool
    premium_subscription: bool

class StarAmount(t.TypedDict):
    """
    ### [StarAmount](https://core.telegram.org/bots/api#staramount)  
    
    Describes an amount of Telegram Stars.
    """
    amount: int
    nanostar_amount: t.NotRequired[int]

class BotCommand(t.TypedDict):
    """
    ### [BotCommand](https://core.telegram.org/bots/api#botcommand)  
    
    This object represents a bot command.
    """
    command: str
    description: str

class BotCommandScopeDefault(t.TypedDict):
    """
    ### [BotCommandScopeDefault](https://core.telegram.org/bots/api#botcommandscopedefault)  
    
    Represents the default [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands. Default commands are used if no commands with a [narrower scope](https://core.telegram.org/bots/api#determining-list-of-commands) are specified for the user.
    """
    type: t.Literal["default"]

class BotCommandScopeAllPrivateChats(t.TypedDict):
    """
    ### [BotCommandScopeAllPrivateChats](https://core.telegram.org/bots/api#botcommandscopeallprivatechats)  
    
    Represents the [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands, covering all private chats.
    """
    type: t.Literal["all_private_chats"]

class BotCommandScopeAllGroupChats(t.TypedDict):
    """
    ### [BotCommandScopeAllGroupChats](https://core.telegram.org/bots/api#botcommandscopeallgroupchats)  
    
    Represents the [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands, covering all group and supergroup chats.
    """
    type: t.Literal["all_group_chats"]

class BotCommandScopeAllChatAdministrators(t.TypedDict):
    """
    ### [BotCommandScopeAllChatAdministrators](https://core.telegram.org/bots/api#botcommandscopeallchatadministrators)  
    
    Represents the [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands, covering all group and supergroup chat administrators.
    """
    type: t.Literal["all_chat_administrators"]

class BotCommandScopeChat(t.TypedDict):
    """
    ### [BotCommandScopeChat](https://core.telegram.org/bots/api#botcommandscopechat)  
    
    Represents the [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands, covering a specific chat.
    """
    type: t.Literal["chat"]
    chat_id: int | str

class BotCommandScopeChatAdministrators(t.TypedDict):
    """
    ### [BotCommandScopeChatAdministrators](https://core.telegram.org/bots/api#botcommandscopechatadministrators)  
    
    Represents the [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands, covering all administrators of a specific group or supergroup chat.
    """
    type: t.Literal["chat_administrators"]
    chat_id: int | str

class BotCommandScopeChatMember(t.TypedDict):
    """
    ### [BotCommandScopeChatMember](https://core.telegram.org/bots/api#botcommandscopechatmember)  
    
    Represents the [scope](https://core.telegram.org/bots/api#botcommandscope) of bot commands, covering a specific member of a group or supergroup chat.
    """
    type: t.Literal["chat_member"]
    chat_id: int | str
    user_id: int

class BotName(t.TypedDict):
    """
    ### [BotName](https://core.telegram.org/bots/api#botname)  
    
    This object represents the bot's name.
    """
    name: str

class BotDescription(t.TypedDict):
    """
    ### [BotDescription](https://core.telegram.org/bots/api#botdescription)  
    
    This object represents the bot's description.
    """
    description: str

class BotShortDescription(t.TypedDict):
    """
    ### [BotShortDescription](https://core.telegram.org/bots/api#botshortdescription)  
    
    This object represents the bot's short description.
    """
    short_description: str

class MenuButtonCommands(t.TypedDict):
    """
    ### [MenuButtonCommands](https://core.telegram.org/bots/api#menubuttoncommands)  
    
    Represents a menu button, which opens the bot's list of commands.
    """
    type: t.Literal["commands"]

class MenuButtonWebApp(t.TypedDict):
    """
    ### [MenuButtonWebApp](https://core.telegram.org/bots/api#menubuttonwebapp)  
    
    Represents a menu button, which launches a [Web App](https://core.telegram.org/bots/webapps).
    """
    type: t.Literal["web_app"]
    text: str
    web_app: "WebAppInfo"

class MenuButtonDefault(t.TypedDict):
    """
    ### [MenuButtonDefault](https://core.telegram.org/bots/api#menubuttondefault)  
    
    Describes that no specific value for the menu button was set.
    """
    type: t.Literal["default"]

class ChatBoostSourcePremium(t.TypedDict):
    """
    ### [ChatBoostSourcePremium](https://core.telegram.org/bots/api#chatboostsourcepremium)  
    
    The boost was obtained by subscribing to Telegram Premium or by gifting a Telegram Premium subscription to another user.
    """
    source: t.Literal["premium"]
    user: "User"

class ChatBoostSourceGiftCode(t.TypedDict):
    """
    ### [ChatBoostSourceGiftCode](https://core.telegram.org/bots/api#chatboostsourcegiftcode)  
    
    The boost was obtained by the creation of Telegram Premium gift codes to boost a chat. Each such code boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription.
    """
    source: t.Literal["gift_code"]
    user: "User"

class ChatBoostSourceGiveaway(t.TypedDict):
    """
    ### [ChatBoostSourceGiveaway](https://core.telegram.org/bots/api#chatboostsourcegiveaway)  
    
    The boost was obtained by the creation of a Telegram Premium or a Telegram Star giveaway. This boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription for Telegram Premium giveaways and *prize\\_star\\_count* / 500 times for one year for Telegram Star giveaways.
    """
    source: t.Literal["giveaway"]
    giveaway_message_id: int
    user: t.NotRequired["User"]
    prize_star_count: t.NotRequired[int]
    is_unclaimed: t.NotRequired[t.Literal[True]]

class ChatBoost(t.TypedDict):
    """
    ### [ChatBoost](https://core.telegram.org/bots/api#chatboost)  
    
    This object contains information about a chat boost.
    """
    boost_id: str
    add_date: int
    expiration_date: int
    source: "ChatBoostSource"

class ChatBoostUpdated(t.TypedDict):
    """
    ### [ChatBoostUpdated](https://core.telegram.org/bots/api#chatboostupdated)  
    
    This object represents a boost added to a chat or changed.
    """
    chat: "Chat"
    boost: "ChatBoost"

class ChatBoostRemoved(t.TypedDict):
    """
    ### [ChatBoostRemoved](https://core.telegram.org/bots/api#chatboostremoved)  
    
    This object represents a boost removed from a chat.
    """
    chat: "Chat"
    boost_id: str
    remove_date: int
    source: "ChatBoostSource"

class UserChatBoosts(t.TypedDict):
    """
    ### [UserChatBoosts](https://core.telegram.org/bots/api#userchatboosts)  
    
    This object represents a list of boosts added to a chat by a user.
    """
    boosts: list["ChatBoost"]

class BusinessBotRights(t.TypedDict):
    """
    ### [BusinessBotRights](https://core.telegram.org/bots/api#businessbotrights)  
    
    Represents the rights of a business bot.
    """
    can_reply: t.NotRequired[t.Literal[True]]
    can_read_messages: t.NotRequired[t.Literal[True]]
    can_delete_sent_messages: t.NotRequired[t.Literal[True]]
    can_delete_all_messages: t.NotRequired[t.Literal[True]]
    can_edit_name: t.NotRequired[t.Literal[True]]
    can_edit_bio: t.NotRequired[t.Literal[True]]
    can_edit_profile_photo: t.NotRequired[t.Literal[True]]
    can_edit_username: t.NotRequired[t.Literal[True]]
    can_change_gift_settings: t.NotRequired[t.Literal[True]]
    can_view_gifts_and_stars: t.NotRequired[t.Literal[True]]
    can_convert_gifts_to_stars: t.NotRequired[t.Literal[True]]
    can_transfer_and_upgrade_gifts: t.NotRequired[t.Literal[True]]
    can_transfer_stars: t.NotRequired[t.Literal[True]]
    can_manage_stories: t.NotRequired[t.Literal[True]]

class BusinessConnection(t.TypedDict):
    """
    ### [BusinessConnection](https://core.telegram.org/bots/api#businessconnection)  
    
    Describes the connection of the bot with a business account.
    """
    id: str
    user: "User"
    user_chat_id: int
    date: int
    is_enabled: bool
    rights: t.NotRequired["BusinessBotRights"]

class BusinessMessagesDeleted(t.TypedDict):
    """
    ### [BusinessMessagesDeleted](https://core.telegram.org/bots/api#businessmessagesdeleted)  
    
    This object is received when messages are deleted from a connected business account.
    """
    business_connection_id: str
    chat: "Chat"
    message_ids: list[int]

class ResponseParameters(t.TypedDict):
    """
    ### [ResponseParameters](https://core.telegram.org/bots/api#responseparameters)  
    
    Describes why a request was unsuccessful.
    """
    migrate_to_chat_id: t.NotRequired[int]
    retry_after: t.NotRequired[int]

class InputMediaPhoto(t.TypedDict):
    """
    ### [InputMediaPhoto](https://core.telegram.org/bots/api#inputmediaphoto)  
    
    Represents a photo to be sent.
    """
    type: t.Literal["photo"]
    media: str | Path | bytes | InputFile
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    has_spoiler: t.NotRequired[bool]

class InputMediaVideo(t.TypedDict):
    """
    ### [InputMediaVideo](https://core.telegram.org/bots/api#inputmediavideo)  
    
    Represents a video to be sent.
    """
    type: t.Literal["video"]
    media: str | Path | bytes | InputFile
    thumbnail: t.NotRequired[str | Path | bytes | InputFile]
    cover: t.NotRequired[str | Path | bytes | InputFile]
    start_timestamp: t.NotRequired[int]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    width: t.NotRequired[int]
    height: t.NotRequired[int]
    duration: t.NotRequired[int]
    supports_streaming: t.NotRequired[bool]
    has_spoiler: t.NotRequired[bool]

class InputMediaAnimation(t.TypedDict):
    """
    ### [InputMediaAnimation](https://core.telegram.org/bots/api#inputmediaanimation)  
    
    Represents an animation file (GIF or H.264/MPEG\\-4 AVC video without sound) to be sent.
    """
    type: t.Literal["animation"]
    media: str | Path | bytes | InputFile
    thumbnail: t.NotRequired[str | Path | bytes | InputFile]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    width: t.NotRequired[int]
    height: t.NotRequired[int]
    duration: t.NotRequired[int]
    has_spoiler: t.NotRequired[bool]

class InputMediaAudio(t.TypedDict):
    """
    ### [InputMediaAudio](https://core.telegram.org/bots/api#inputmediaaudio)  
    
    Represents an audio file to be treated as music to be sent.
    """
    type: t.Literal["audio"]
    media: str | Path | bytes | InputFile
    thumbnail: t.NotRequired[str | Path | bytes | InputFile]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    duration: t.NotRequired[int]
    performer: t.NotRequired[str]
    title: t.NotRequired[str]

class InputMediaDocument(t.TypedDict):
    """
    ### [InputMediaDocument](https://core.telegram.org/bots/api#inputmediadocument)  
    
    Represents a general file to be sent.
    """
    type: t.Literal["document"]
    media: str | Path | bytes | InputFile
    thumbnail: t.NotRequired[str | Path | bytes | InputFile]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    disable_content_type_detection: t.NotRequired[bool]

class InputPaidMediaPhoto(t.TypedDict):
    """
    ### [InputPaidMediaPhoto](https://core.telegram.org/bots/api#inputpaidmediaphoto)  
    
    The paid media to send is a photo.
    """
    type: t.Literal["photo"]
    media: str | Path | bytes | InputFile

class InputPaidMediaVideo(t.TypedDict):
    """
    ### [InputPaidMediaVideo](https://core.telegram.org/bots/api#inputpaidmediavideo)  
    
    The paid media to send is a video.
    """
    type: t.Literal["video"]
    media: str | Path | bytes | InputFile
    thumbnail: t.NotRequired[str | Path | bytes | InputFile]
    cover: t.NotRequired[str | Path | bytes | InputFile]
    start_timestamp: t.NotRequired[int]
    width: t.NotRequired[int]
    height: t.NotRequired[int]
    duration: t.NotRequired[int]
    supports_streaming: t.NotRequired[bool]

class InputProfilePhotoStatic(t.TypedDict):
    """
    ### [InputProfilePhotoStatic](https://core.telegram.org/bots/api#inputprofilephotostatic)  
    
    A static profile photo in the .JPG format.
    """
    type: t.Literal["static"]
    photo: str | Path | bytes | InputFile

class InputProfilePhotoAnimated(t.TypedDict):
    """
    ### [InputProfilePhotoAnimated](https://core.telegram.org/bots/api#inputprofilephotoanimated)  
    
    An animated profile photo in the MPEG4 format.
    """
    type: t.Literal["animated"]
    animation: str | Path | bytes | InputFile
    main_frame_timestamp: t.NotRequired[float]

class InputStoryContentPhoto(t.TypedDict):
    """
    ### [InputStoryContentPhoto](https://core.telegram.org/bots/api#inputstorycontentphoto)  
    
    Describes a photo to post as a story.
    """
    type: t.Literal["photo"]
    photo: str | Path | bytes | InputFile

class InputStoryContentVideo(t.TypedDict):
    """
    ### [InputStoryContentVideo](https://core.telegram.org/bots/api#inputstorycontentvideo)  
    
    Describes a video to post as a story.
    """
    type: t.Literal["video"]
    video: str | Path | bytes | InputFile
    duration: t.NotRequired[float]
    cover_frame_timestamp: t.NotRequired[float]
    is_animation: t.NotRequired[bool]

class Sticker(t.TypedDict):
    """
    ### [Sticker](https://core.telegram.org/bots/api#sticker)  
    
    This object represents a sticker.
    """
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: t.NotRequired["PhotoSize"]
    emoji: t.NotRequired[str]
    set_name: t.NotRequired[str]
    premium_animation: t.NotRequired["File"]
    mask_position: t.NotRequired["MaskPosition"]
    custom_emoji_id: t.NotRequired[str]
    needs_repainting: t.NotRequired[t.Literal[True]]
    file_size: t.NotRequired[int]

class StickerSet(t.TypedDict):
    """
    ### [StickerSet](https://core.telegram.org/bots/api#stickerset)  
    
    This object represents a sticker set.
    """
    name: str
    title: str
    sticker_type: str
    stickers: list["Sticker"]
    thumbnail: t.NotRequired["PhotoSize"]

class MaskPosition(t.TypedDict):
    """
    ### [MaskPosition](https://core.telegram.org/bots/api#maskposition)  
    
    This object describes the position on faces where a mask should be placed by default.
    """
    point: str
    x_shift: float
    y_shift: float
    scale: float

class InputSticker(t.TypedDict):
    """
    ### [InputSticker](https://core.telegram.org/bots/api#inputsticker)  
    
    This object describes a sticker to be added to a sticker set.
    """
    sticker: str | Path | bytes | InputFile
    format: str
    emoji_list: list[str]
    mask_position: t.NotRequired["MaskPosition"]
    keywords: t.NotRequired[list[str]]

class InlineQuery(t.TypedDict("InlineQuery", {"from": "User"})):
    """
    ### [InlineQuery](https://core.telegram.org/bots/api#inlinequery)  
    
    This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.
    """
    id: str
    query: str
    offset: str
    chat_type: t.NotRequired[str]
    location: t.NotRequired["Location"]

class InlineQueryResultsButton(t.TypedDict):
    """
    ### [InlineQueryResultsButton](https://core.telegram.org/bots/api#inlinequeryresultsbutton)  
    
    This object represents a button to be shown above inline query results. You **must** use exactly one of the optional fields.
    """
    text: str
    web_app: t.NotRequired["WebAppInfo"]
    start_parameter: t.NotRequired[str]

class InlineQueryResultArticle(t.TypedDict):
    """
    ### [InlineQueryResultArticle](https://core.telegram.org/bots/api#inlinequeryresultarticle)  
    
    Represents a link to an article or web page.
    """
    type: t.Literal["article"]
    id: str
    title: str
    input_message_content: "InputMessageContent"
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    url: t.NotRequired[str]
    description: t.NotRequired[str]
    thumbnail_url: t.NotRequired[str]
    thumbnail_width: t.NotRequired[int]
    thumbnail_height: t.NotRequired[int]

class InlineQueryResultPhoto(t.TypedDict):
    """
    ### [InlineQueryResultPhoto](https://core.telegram.org/bots/api#inlinequeryresultphoto)  
    
    Represents a link to a photo. By default, this photo will be sent by the user with optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the photo.
    """
    type: t.Literal["photo"]
    id: str
    photo_url: str
    thumbnail_url: str
    photo_width: t.NotRequired[int]
    photo_height: t.NotRequired[int]
    title: t.NotRequired[str]
    description: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultGif(t.TypedDict):
    """
    ### [InlineQueryResultGif](https://core.telegram.org/bots/api#inlinequeryresultgif)  
    
    Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the animation.
    """
    type: t.Literal["gif"]
    id: str
    gif_url: str
    thumbnail_url: str
    gif_width: t.NotRequired[int]
    gif_height: t.NotRequired[int]
    gif_duration: t.NotRequired[int]
    thumbnail_mime_type: t.NotRequired[str]
    title: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultMpeg4Gif(t.TypedDict):
    """
    ### [InlineQueryResultMpeg4Gif](https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif)  
    
    Represents a link to a video animation (H.264/MPEG\\-4 AVC video without sound). By default, this animated MPEG\\-4 file will be sent by the user with optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the animation.
    """
    type: t.Literal["mpeg4_gif"]
    id: str
    mpeg4_url: str
    thumbnail_url: str
    mpeg4_width: t.NotRequired[int]
    mpeg4_height: t.NotRequired[int]
    mpeg4_duration: t.NotRequired[int]
    thumbnail_mime_type: t.NotRequired[str]
    title: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultVideo(t.TypedDict):
    """
    ### [InlineQueryResultVideo](https://core.telegram.org/bots/api#inlinequeryresultvideo)  
    
    Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the video.
    
    If an InlineQueryResultVideo message contains an embedded video (e.g., YouTube), you **must** replace its content using *input\\_message\\_content*.
    """
    type: t.Literal["video"]
    id: str
    video_url: str
    mime_type: str
    thumbnail_url: str
    title: str
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    video_width: t.NotRequired[int]
    video_height: t.NotRequired[int]
    video_duration: t.NotRequired[int]
    description: t.NotRequired[str]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultAudio(t.TypedDict):
    """
    ### [InlineQueryResultAudio](https://core.telegram.org/bots/api#inlinequeryresultaudio)  
    
    Represents a link to an MP3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the audio.
    """
    type: t.Literal["audio"]
    id: str
    audio_url: str
    title: str
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    performer: t.NotRequired[str]
    audio_duration: t.NotRequired[int]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultVoice(t.TypedDict):
    """
    ### [InlineQueryResultVoice](https://core.telegram.org/bots/api#inlinequeryresultvoice)  
    
    Represents a link to a voice recording in an .OGG container encoded with OPUS. By default, this voice recording will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the the voice message.
    """
    type: t.Literal["voice"]
    id: str
    voice_url: str
    title: str
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    voice_duration: t.NotRequired[int]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultDocument(t.TypedDict):
    """
    ### [InlineQueryResultDocument](https://core.telegram.org/bots/api#inlinequeryresultdocument)  
    
    Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the file. Currently, only **.PDF** and **.ZIP** files can be sent using this method.
    """
    type: t.Literal["document"]
    id: str
    title: str
    document_url: str
    mime_type: str
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    description: t.NotRequired[str]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]
    thumbnail_url: t.NotRequired[str]
    thumbnail_width: t.NotRequired[int]
    thumbnail_height: t.NotRequired[int]

class InlineQueryResultLocation(t.TypedDict):
    """
    ### [InlineQueryResultLocation](https://core.telegram.org/bots/api#inlinequeryresultlocation)  
    
    Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the location.
    """
    type: t.Literal["location"]
    id: str
    latitude: float
    longitude: float
    title: str
    horizontal_accuracy: t.NotRequired[float]
    live_period: t.NotRequired[int]
    heading: t.NotRequired[int]
    proximity_alert_radius: t.NotRequired[int]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]
    thumbnail_url: t.NotRequired[str]
    thumbnail_width: t.NotRequired[int]
    thumbnail_height: t.NotRequired[int]

class InlineQueryResultVenue(t.TypedDict):
    """
    ### [InlineQueryResultVenue](https://core.telegram.org/bots/api#inlinequeryresultvenue)  
    
    Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the venue.
    """
    type: t.Literal["venue"]
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: t.NotRequired[str]
    foursquare_type: t.NotRequired[str]
    google_place_id: t.NotRequired[str]
    google_place_type: t.NotRequired[str]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]
    thumbnail_url: t.NotRequired[str]
    thumbnail_width: t.NotRequired[int]
    thumbnail_height: t.NotRequired[int]

class InlineQueryResultContact(t.TypedDict):
    """
    ### [InlineQueryResultContact](https://core.telegram.org/bots/api#inlinequeryresultcontact)  
    
    Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the contact.
    """
    type: t.Literal["contact"]
    id: str
    phone_number: str
    first_name: str
    last_name: t.NotRequired[str]
    vcard: t.NotRequired[str]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]
    thumbnail_url: t.NotRequired[str]
    thumbnail_width: t.NotRequired[int]
    thumbnail_height: t.NotRequired[int]

class InlineQueryResultGame(t.TypedDict):
    """
    ### [InlineQueryResultGame](https://core.telegram.org/bots/api#inlinequeryresultgame)  
    
    Represents a [Game](https://core.telegram.org/bots/api#games).
    """
    type: t.Literal["game"]
    id: str
    game_short_name: str
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]

class InlineQueryResultCachedPhoto(t.TypedDict):
    """
    ### [InlineQueryResultCachedPhoto](https://core.telegram.org/bots/api#inlinequeryresultcachedphoto)  
    
    Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the photo.
    """
    type: t.Literal["photo"]
    id: str
    photo_file_id: str
    title: t.NotRequired[str]
    description: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedGif(t.TypedDict):
    """
    ### [InlineQueryResultCachedGif](https://core.telegram.org/bots/api#inlinequeryresultcachedgif)  
    
    Represents a link to an animated GIF file stored on the Telegram servers. By default, this animated GIF file will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with specified content instead of the animation.
    """
    type: t.Literal["gif"]
    id: str
    gif_file_id: str
    title: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedMpeg4Gif(t.TypedDict):
    """
    ### [InlineQueryResultCachedMpeg4Gif](https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif)  
    
    Represents a link to a video animation (H.264/MPEG\\-4 AVC video without sound) stored on the Telegram servers. By default, this animated MPEG\\-4 file will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the animation.
    """
    type: t.Literal["mpeg4_gif"]
    id: str
    mpeg4_file_id: str
    title: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedSticker(t.TypedDict):
    """
    ### [InlineQueryResultCachedSticker](https://core.telegram.org/bots/api#inlinequeryresultcachedsticker)  
    
    Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the sticker.
    """
    type: t.Literal["sticker"]
    id: str
    sticker_file_id: str
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedDocument(t.TypedDict):
    """
    ### [InlineQueryResultCachedDocument](https://core.telegram.org/bots/api#inlinequeryresultcacheddocument)  
    
    Represents a link to a file stored on the Telegram servers. By default, this file will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the file.
    """
    type: t.Literal["document"]
    id: str
    title: str
    document_file_id: str
    description: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedVideo(t.TypedDict):
    """
    ### [InlineQueryResultCachedVideo](https://core.telegram.org/bots/api#inlinequeryresultcachedvideo)  
    
    Represents a link to a video file stored on the Telegram servers. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the video.
    """
    type: t.Literal["video"]
    id: str
    video_file_id: str
    title: str
    description: t.NotRequired[str]
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    show_caption_above_media: t.NotRequired[bool]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedVoice(t.TypedDict):
    """
    ### [InlineQueryResultCachedVoice](https://core.telegram.org/bots/api#inlinequeryresultcachedvoice)  
    
    Represents a link to a voice message stored on the Telegram servers. By default, this voice message will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the voice message.
    """
    type: t.Literal["voice"]
    id: str
    voice_file_id: str
    title: str
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InlineQueryResultCachedAudio(t.TypedDict):
    """
    ### [InlineQueryResultCachedAudio](https://core.telegram.org/bots/api#inlinequeryresultcachedaudio)  
    
    Represents a link to an MP3 audio file stored on the Telegram servers. By default, this audio file will be sent by the user. Alternatively, you can use *input\\_message\\_content* to send a message with the specified content instead of the audio.
    """
    type: t.Literal["audio"]
    id: str
    audio_file_id: str
    caption: t.NotRequired[str]
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    caption_entities: t.NotRequired[list["MessageEntity"]]
    reply_markup: t.NotRequired["InlineKeyboardMarkup"]
    input_message_content: t.NotRequired["InputMessageContent"]

class InputTextMessageContent(t.TypedDict):
    """
    ### [InputTextMessageContent](https://core.telegram.org/bots/api#inputtextmessagecontent)  
    
    Represents the [content](https://core.telegram.org/bots/api#inputmessagecontent) of a text message to be sent as the result of an inline query.
    """
    message_text: str
    parse_mode: t.NotRequired[t.Literal["HTML", "Markdown", "MarkdownV2"]]
    entities: t.NotRequired[list["MessageEntity"]]
    link_preview_options: t.NotRequired["LinkPreviewOptions"]

class InputLocationMessageContent(t.TypedDict):
    """
    ### [InputLocationMessageContent](https://core.telegram.org/bots/api#inputlocationmessagecontent)  
    
    Represents the [content](https://core.telegram.org/bots/api#inputmessagecontent) of a location message to be sent as the result of an inline query.
    """
    latitude: float
    longitude: float
    horizontal_accuracy: t.NotRequired[float]
    live_period: t.NotRequired[int]
    heading: t.NotRequired[int]
    proximity_alert_radius: t.NotRequired[int]

class InputVenueMessageContent(t.TypedDict):
    """
    ### [InputVenueMessageContent](https://core.telegram.org/bots/api#inputvenuemessagecontent)  
    
    Represents the [content](https://core.telegram.org/bots/api#inputmessagecontent) of a venue message to be sent as the result of an inline query.
    """
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: t.NotRequired[str]
    foursquare_type: t.NotRequired[str]
    google_place_id: t.NotRequired[str]
    google_place_type: t.NotRequired[str]

class InputContactMessageContent(t.TypedDict):
    """
    ### [InputContactMessageContent](https://core.telegram.org/bots/api#inputcontactmessagecontent)  
    
    Represents the [content](https://core.telegram.org/bots/api#inputmessagecontent) of a contact message to be sent as the result of an inline query.
    """
    phone_number: str
    first_name: str
    last_name: t.NotRequired[str]
    vcard: t.NotRequired[str]

class InputInvoiceMessageContent(t.TypedDict):
    """
    ### [InputInvoiceMessageContent](https://core.telegram.org/bots/api#inputinvoicemessagecontent)  
    
    Represents the [content](https://core.telegram.org/bots/api#inputmessagecontent) of an invoice message to be sent as the result of an inline query.
    """
    title: str
    description: str
    payload: str
    currency: str
    prices: list["LabeledPrice"]
    provider_token: t.NotRequired[str]
    max_tip_amount: t.NotRequired[int]
    suggested_tip_amounts: t.NotRequired[list[int]]
    provider_data: t.NotRequired[str]
    photo_url: t.NotRequired[str]
    photo_size: t.NotRequired[int]
    photo_width: t.NotRequired[int]
    photo_height: t.NotRequired[int]
    need_name: t.NotRequired[bool]
    need_phone_number: t.NotRequired[bool]
    need_email: t.NotRequired[bool]
    need_shipping_address: t.NotRequired[bool]
    send_phone_number_to_provider: t.NotRequired[bool]
    send_email_to_provider: t.NotRequired[bool]
    is_flexible: t.NotRequired[bool]

class ChosenInlineResult(t.TypedDict("ChosenInlineResult", {"from": "User"})):
    """
    ### [ChosenInlineResult](https://core.telegram.org/bots/api#choseninlineresult)  
    
    Represents a [result](https://core.telegram.org/bots/api#inlinequeryresult) of an inline query that was chosen by the user and sent to their chat partner.
    
    **Note:** It is necessary to enable [inline feedback](https://core.telegram.org/bots/inline#collecting-feedback) via [@BotFather](https://t.me/botfather) in order to receive these objects in updates.
    """
    result_id: str
    query: str
    location: t.NotRequired["Location"]
    inline_message_id: t.NotRequired[str]

class SentWebAppMessage(t.TypedDict):
    """
    ### [SentWebAppMessage](https://core.telegram.org/bots/api#sentwebappmessage)  
    
    Describes an inline message sent by a [Web App](https://core.telegram.org/bots/webapps) on behalf of a user.
    """
    inline_message_id: t.NotRequired[str]

class PreparedInlineMessage(t.TypedDict):
    """
    ### [PreparedInlineMessage](https://core.telegram.org/bots/api#preparedinlinemessage)  
    
    Describes an inline message to be sent by a user of a Mini App.
    
    Your bot can accept payments from Telegram users. Please see the [introduction to payments](https://core.telegram.org/bots/payments) for more details on the process and how to set up payments for your bot.
    """
    id: str
    expiration_date: int

class LabeledPrice(t.TypedDict):
    """
    ### [LabeledPrice](https://core.telegram.org/bots/api#labeledprice)  
    
    This object represents a portion of the price for goods or services.
    """
    label: str
    amount: int

class Invoice(t.TypedDict):
    """
    ### [Invoice](https://core.telegram.org/bots/api#invoice)  
    
    This object contains basic information about an invoice.
    """
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int

class ShippingAddress(t.TypedDict):
    """
    ### [ShippingAddress](https://core.telegram.org/bots/api#shippingaddress)  
    
    This object represents a shipping address.
    """
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str

class OrderInfo(t.TypedDict):
    """
    ### [OrderInfo](https://core.telegram.org/bots/api#orderinfo)  
    
    This object represents information about an order.
    """
    name: t.NotRequired[str]
    phone_number: t.NotRequired[str]
    email: t.NotRequired[str]
    shipping_address: t.NotRequired["ShippingAddress"]

class ShippingOption(t.TypedDict):
    """
    ### [ShippingOption](https://core.telegram.org/bots/api#shippingoption)  
    
    This object represents one shipping option.
    """
    id: str
    title: str
    prices: list["LabeledPrice"]

class SuccessfulPayment(t.TypedDict):
    """
    ### [SuccessfulPayment](https://core.telegram.org/bots/api#successfulpayment)  
    
    This object contains basic information about a successful payment. Note that if the buyer initiates a chargeback with the relevant payment provider following this transaction, the funds may be debited from your balance. This is outside of Telegram's control.
    """
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    subscription_expiration_date: t.NotRequired[int]
    is_recurring: t.NotRequired[t.Literal[True]]
    is_first_recurring: t.NotRequired[t.Literal[True]]
    shipping_option_id: t.NotRequired[str]
    order_info: t.NotRequired["OrderInfo"]

class RefundedPayment(t.TypedDict):
    """
    ### [RefundedPayment](https://core.telegram.org/bots/api#refundedpayment)  
    
    This object contains basic information about a refunded payment.
    """
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: t.NotRequired[str]

class ShippingQuery(t.TypedDict("ShippingQuery", {"from": "User"})):
    """
    ### [ShippingQuery](https://core.telegram.org/bots/api#shippingquery)  
    
    This object contains information about an incoming shipping query.
    """
    id: str
    invoice_payload: str
    shipping_address: "ShippingAddress"

class PreCheckoutQuery(t.TypedDict("PreCheckoutQuery", {"from": "User"})):
    """
    ### [PreCheckoutQuery](https://core.telegram.org/bots/api#precheckoutquery)  
    
    This object contains information about an incoming pre\\-checkout query.
    """
    id: str
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: t.NotRequired[str]
    order_info: t.NotRequired["OrderInfo"]

class PaidMediaPurchased(t.TypedDict("PaidMediaPurchased", {"from": "User"})):
    """
    ### [PaidMediaPurchased](https://core.telegram.org/bots/api#paidmediapurchased)  
    
    This object contains information about a paid media purchase.
    """
    paid_media_payload: str

class RevenueWithdrawalStatePending(t.TypedDict):
    """
    ### [RevenueWithdrawalStatePending](https://core.telegram.org/bots/api#revenuewithdrawalstatepending)  
    
    The withdrawal is in progress.
    """
    type: t.Literal["pending"]

class RevenueWithdrawalStateSucceeded(t.TypedDict):
    """
    ### [RevenueWithdrawalStateSucceeded](https://core.telegram.org/bots/api#revenuewithdrawalstatesucceeded)  
    
    The withdrawal succeeded.
    """
    type: t.Literal["succeeded"]
    date: int
    url: str

class RevenueWithdrawalStateFailed(t.TypedDict):
    """
    ### [RevenueWithdrawalStateFailed](https://core.telegram.org/bots/api#revenuewithdrawalstatefailed)  
    
    The withdrawal failed and the transaction was refunded.
    """
    type: t.Literal["failed"]

class AffiliateInfo(t.TypedDict):
    """
    ### [AffiliateInfo](https://core.telegram.org/bots/api#affiliateinfo)  
    
    Contains information about the affiliate that received a commission via this transaction.
    """
    commission_per_mille: int
    amount: int
    affiliate_user: t.NotRequired["User"]
    affiliate_chat: t.NotRequired["Chat"]
    nanostar_amount: t.NotRequired[int]

class TransactionPartnerUser(t.TypedDict):
    """
    ### [TransactionPartnerUser](https://core.telegram.org/bots/api#transactionpartneruser)  
    
    Describes a transaction with a user.
    """
    type: t.Literal["user"]
    transaction_type: str
    user: "User"
    affiliate: t.NotRequired["AffiliateInfo"]
    invoice_payload: t.NotRequired[str]
    subscription_period: t.NotRequired[int]
    paid_media: t.NotRequired[list["PaidMedia"]]
    paid_media_payload: t.NotRequired[str]
    gift: t.NotRequired["Gift"]
    premium_subscription_duration: t.NotRequired[int]

class TransactionPartnerChat(t.TypedDict):
    """
    ### [TransactionPartnerChat](https://core.telegram.org/bots/api#transactionpartnerchat)  
    
    Describes a transaction with a chat.
    """
    type: t.Literal["chat"]
    chat: "Chat"
    gift: t.NotRequired["Gift"]

class TransactionPartnerAffiliateProgram(t.TypedDict):
    """
    ### [TransactionPartnerAffiliateProgram](https://core.telegram.org/bots/api#transactionpartneraffiliateprogram)  
    
    Describes the affiliate program that issued the affiliate commission received via this transaction.
    """
    type: t.Literal["affiliate_program"]
    commission_per_mille: int
    sponsor_user: t.NotRequired["User"]

class TransactionPartnerFragment(t.TypedDict):
    """
    ### [TransactionPartnerFragment](https://core.telegram.org/bots/api#transactionpartnerfragment)  
    
    Describes a withdrawal transaction with Fragment.
    """
    type: t.Literal["fragment"]
    withdrawal_state: t.NotRequired["RevenueWithdrawalState"]

class TransactionPartnerTelegramAds(t.TypedDict):
    """
    ### [TransactionPartnerTelegramAds](https://core.telegram.org/bots/api#transactionpartnertelegramads)  
    
    Describes a withdrawal transaction to the Telegram Ads platform.
    """
    type: t.Literal["telegram_ads"]

class TransactionPartnerTelegramApi(t.TypedDict):
    """
    ### [TransactionPartnerTelegramApi](https://core.telegram.org/bots/api#transactionpartnertelegramapi)  
    
    Describes a transaction with payment for [paid broadcasting](https://core.telegram.org/bots/api#paid-broadcasts).
    """
    type: t.Literal["telegram_api"]
    request_count: int

class TransactionPartnerOther(t.TypedDict):
    """
    ### [TransactionPartnerOther](https://core.telegram.org/bots/api#transactionpartnerother)  
    
    Describes a transaction with an unknown source or recipient.
    """
    type: t.Literal["other"]

class StarTransaction(t.TypedDict):
    """
    ### [StarTransaction](https://core.telegram.org/bots/api#startransaction)  
    
    Describes a Telegram Star transaction. Note that if the buyer initiates a chargeback with the payment provider from whom they acquired Stars (e.g., Apple, Google) following this transaction, the refunded Stars will be deducted from the bot's balance. This is outside of Telegram's control.
    """
    id: str
    amount: int
    date: int
    nanostar_amount: t.NotRequired[int]
    source: t.NotRequired["TransactionPartner"]
    receiver: t.NotRequired["TransactionPartner"]

class StarTransactions(t.TypedDict):
    """
    ### [StarTransactions](https://core.telegram.org/bots/api#startransactions)  
    
    Contains a list of Telegram Star transactions.
    
    **Telegram Passport** is a unified authorization method for services that require personal identification. Users can upload their documents once, then instantly share their data with services that require real\\-world ID (finance, ICOs, etc.). Please see the [manual](https://core.telegram.org/passport) for details.
    """
    transactions: list["StarTransaction"]

class PassportData(t.TypedDict):
    """
    ### [PassportData](https://core.telegram.org/bots/api#passportdata)  
    
    Describes Telegram Passport data shared with the bot by the user.
    """
    data: list["EncryptedPassportElement"]
    credentials: "EncryptedCredentials"

class PassportFile(t.TypedDict):
    """
    ### [PassportFile](https://core.telegram.org/bots/api#passportfile)  
    
    This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.
    """
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int

class EncryptedPassportElement(t.TypedDict):
    """
    ### [EncryptedPassportElement](https://core.telegram.org/bots/api#encryptedpassportelement)  
    
    Describes documents or other Telegram Passport elements shared with the bot by the user.
    """
    type: str
    hash: str
    data: t.NotRequired[str]
    phone_number: t.NotRequired[str]
    email: t.NotRequired[str]
    files: t.NotRequired[list["PassportFile"]]
    front_side: t.NotRequired["PassportFile"]
    reverse_side: t.NotRequired["PassportFile"]
    selfie: t.NotRequired["PassportFile"]
    translation: t.NotRequired[list["PassportFile"]]

class EncryptedCredentials(t.TypedDict):
    """
    ### [EncryptedCredentials](https://core.telegram.org/bots/api#encryptedcredentials)  
    
    Describes data required for decrypting and authenticating [EncryptedPassportElement](https://core.telegram.org/bots/api#encryptedpassportelement). See the [Telegram Passport Documentation](https://core.telegram.org/passport#receiving-information) for a complete description of the data decryption and authentication processes.
    """
    data: str
    hash: str
    secret: str

class PassportElementErrorDataField(t.TypedDict):
    """
    ### [PassportElementErrorDataField](https://core.telegram.org/bots/api#passportelementerrordatafield)  
    
    Represents an issue in one of the data fields that was provided by the user. The error is considered resolved when the field's value changes.
    """
    source: t.Literal["data"]
    type: str
    field_name: str
    data_hash: str
    message: str

class PassportElementErrorFrontSide(t.TypedDict):
    """
    ### [PassportElementErrorFrontSide](https://core.telegram.org/bots/api#passportelementerrorfrontside)  
    
    Represents an issue with the front side of a document. The error is considered resolved when the file with the front side of the document changes.
    """
    source: t.Literal["front_side"]
    type: str
    file_hash: str
    message: str

class PassportElementErrorReverseSide(t.TypedDict):
    """
    ### [PassportElementErrorReverseSide](https://core.telegram.org/bots/api#passportelementerrorreverseside)  
    
    Represents an issue with the reverse side of a document. The error is considered resolved when the file with reverse side of the document changes.
    """
    source: t.Literal["reverse_side"]
    type: str
    file_hash: str
    message: str

class PassportElementErrorSelfie(t.TypedDict):
    """
    ### [PassportElementErrorSelfie](https://core.telegram.org/bots/api#passportelementerrorselfie)  
    
    Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes.
    """
    source: t.Literal["selfie"]
    type: str
    file_hash: str
    message: str

class PassportElementErrorFile(t.TypedDict):
    """
    ### [PassportElementErrorFile](https://core.telegram.org/bots/api#passportelementerrorfile)  
    
    Represents an issue with a document scan. The error is considered resolved when the file with the document scan changes.
    """
    source: t.Literal["file"]
    type: str
    file_hash: str
    message: str

class PassportElementErrorFiles(t.TypedDict):
    """
    ### [PassportElementErrorFiles](https://core.telegram.org/bots/api#passportelementerrorfiles)  
    
    Represents an issue with a list of scans. The error is considered resolved when the list of files containing the scans changes.
    """
    source: t.Literal["files"]
    type: str
    file_hashes: list[str]
    message: str

class PassportElementErrorTranslationFile(t.TypedDict):
    """
    ### [PassportElementErrorTranslationFile](https://core.telegram.org/bots/api#passportelementerrortranslationfile)  
    
    Represents an issue with one of the files that constitute the translation of a document. The error is considered resolved when the file changes.
    """
    source: t.Literal["translation_file"]
    type: str
    file_hash: str
    message: str

class PassportElementErrorTranslationFiles(t.TypedDict):
    """
    ### [PassportElementErrorTranslationFiles](https://core.telegram.org/bots/api#passportelementerrortranslationfiles)  
    
    Represents an issue with the translated version of a document. The error is considered resolved when a file with the document translation change.
    """
    source: t.Literal["translation_files"]
    type: str
    file_hashes: list[str]
    message: str

class PassportElementErrorUnspecified(t.TypedDict):
    """
    ### [PassportElementErrorUnspecified](https://core.telegram.org/bots/api#passportelementerrorunspecified)  
    
    Represents an issue in an unspecified place. The error is considered resolved when new data is added.
    
    Your bot can offer users **HTML5 games** to play solo or to compete against each other in groups and one\\-on\\-one chats. Create games via [@BotFather](https://t.me/botfather) using the */newgame* command. Please note that this kind of power requires responsibility: you will need to accept the terms for each game that your bots will be offering.
    
    * Games are a new type of content on Telegram, represented by the [Game](https://core.telegram.org/bots/api#game) and [InlineQueryResultGame](https://core.telegram.org/bots/api#inlinequeryresultgame) objects.
    * Once you've created a game via [BotFather](https://t.me/botfather), you can send games to chats as regular messages using the [sendGame](https://core.telegram.org/bots/api#sendgame) method, or use [inline mode](https://core.telegram.org/bots/api#inline-mode) with [InlineQueryResultGame](https://core.telegram.org/bots/api#inlinequeryresultgame).
    * If you send the game message without any buttons, it will automatically have a 'Play *GameName*' button. When this button is pressed, your bot gets a [CallbackQuery](https://core.telegram.org/bots/api#callbackquery) with the *game\\_short\\_name* of the requested game. You provide the correct URL for this particular user and the app opens the game in the in\\-app browser.
    * You can manually add multiple buttons to your game message. Please note that the first button in the first row **must always** launch the game, using the field *callback\\_game* in [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton). You can add extra buttons according to taste: e.g., for a description of the rules, or to open the game's official community.
    * To make your game more attractive, you can upload a GIF animation that demonstrates the game to the users via [BotFather](https://t.me/botfather) (see [Lumberjack](https://t.me/gamebot?game=lumberjack) for example).
    * A game message will also display high scores for the current chat. Use [setGameScore](https://core.telegram.org/bots/api#setgamescore) to post high scores to the chat with the game, add the *disable\\_edit\\_message* parameter to disable automatic update of the message with the current scoreboard.
    * Use [getGameHighScores](https://core.telegram.org/bots/api#getgamehighscores) to get data for in\\-game high score tables.
    * You can also add an extra [sharing button](https://core.telegram.org/bots/games#sharing-your-game-to-telegram-chats) for users to share their best score to different chats.
    * For examples of what can be done using this new stuff, check the [@gamebot](https://t.me/gamebot) and [@gamee](https://t.me/gamee) bots.
    """
    source: t.Literal["unspecified"]
    type: str
    element_hash: str
    message: str

class Game(t.TypedDict):
    """
    ### [Game](https://core.telegram.org/bots/api#game)  
    
    This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.
    """
    title: str
    description: str
    photo: list["PhotoSize"]
    text: t.NotRequired[str]
    text_entities: t.NotRequired[list["MessageEntity"]]
    animation: t.NotRequired["Animation"]

class CallbackGame(t.TypedDict):
    """
    ### [CallbackGame](https://core.telegram.org/bots/api#callbackgame)  
    
    A placeholder, currently holds no information. Use [BotFather](https://t.me/botfather) to set up your game.
    """
    

class GameHighScore(t.TypedDict):
    """
    ### [GameHighScore](https://core.telegram.org/bots/api#gamehighscore)  
    
    This object represents one row of the high scores table for a game.
    
    And that's about all we've got for now.  
    If you've got any questions, please check out our [**Bot FAQ »**](https://core.telegram.org/bots/faq)
    """
    position: int
    user: "User"
    score: int

class MaybeInaccessibleMessage(Message, InaccessibleMessage):
    """
    ### [MaybeInaccessibleMessage](https://core.telegram.org/bots/api#maybeinaccessiblemessage)  
    
    This object describes a message that can be inaccessible to the bot. It can be one of
    
    * [Message](https://core.telegram.org/bots/api#message)
    * [InaccessibleMessage](https://core.telegram.org/bots/api#inaccessiblemessage)
    """

class MessageOrigin(MessageOriginUser, MessageOriginHiddenUser, MessageOriginChat, MessageOriginChannel):
    """
    ### [MessageOrigin](https://core.telegram.org/bots/api#messageorigin)  
    
    This object describes the origin of a message. It can be one of
    
    * [MessageOriginUser](https://core.telegram.org/bots/api#messageoriginuser)
    * [MessageOriginHiddenUser](https://core.telegram.org/bots/api#messageoriginhiddenuser)
    * [MessageOriginChat](https://core.telegram.org/bots/api#messageoriginchat)
    * [MessageOriginChannel](https://core.telegram.org/bots/api#messageoriginchannel)
    """
    type: t.Literal["user", "hidden_user", "chat", "channel"]

class PaidMedia(PaidMediaPreview, PaidMediaPhoto, PaidMediaVideo):
    """
    ### [PaidMedia](https://core.telegram.org/bots/api#paidmedia)  
    
    This object describes paid media. Currently, it can be one of
    
    * [PaidMediaPreview](https://core.telegram.org/bots/api#paidmediapreview)
    * [PaidMediaPhoto](https://core.telegram.org/bots/api#paidmediaphoto)
    * [PaidMediaVideo](https://core.telegram.org/bots/api#paidmediavideo)
    """
    type: t.Literal["preview", "photo", "video"]

class BackgroundFill(BackgroundFillSolid, BackgroundFillGradient, BackgroundFillFreeformGradient):
    """
    ### [BackgroundFill](https://core.telegram.org/bots/api#backgroundfill)  
    
    This object describes the way a background is filled based on the selected colors. Currently, it can be one of
    
    * [BackgroundFillSolid](https://core.telegram.org/bots/api#backgroundfillsolid)
    * [BackgroundFillGradient](https://core.telegram.org/bots/api#backgroundfillgradient)
    * [BackgroundFillFreeformGradient](https://core.telegram.org/bots/api#backgroundfillfreeformgradient)
    """
    type: t.Literal["solid", "gradient", "freeform_gradient"]

class BackgroundType(BackgroundTypeFill, BackgroundTypeWallpaper, BackgroundTypePattern, BackgroundTypeChatTheme):
    """
    ### [BackgroundType](https://core.telegram.org/bots/api#backgroundtype)  
    
    This object describes the type of a background. Currently, it can be one of
    
    * [BackgroundTypeFill](https://core.telegram.org/bots/api#backgroundtypefill)
    * [BackgroundTypeWallpaper](https://core.telegram.org/bots/api#backgroundtypewallpaper)
    * [BackgroundTypePattern](https://core.telegram.org/bots/api#backgroundtypepattern)
    * [BackgroundTypeChatTheme](https://core.telegram.org/bots/api#backgroundtypechattheme)
    """
    type: t.Literal["fill", "wallpaper", "pattern", "chat_theme"]

class ChatMember(ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned):
    """
    ### [ChatMember](https://core.telegram.org/bots/api#chatmember)  
    
    This object contains information about one member of a chat. Currently, the following 6 types of chat members are supported:
    
    * [ChatMemberOwner](https://core.telegram.org/bots/api#chatmemberowner)
    * [ChatMemberAdministrator](https://core.telegram.org/bots/api#chatmemberadministrator)
    * [ChatMemberMember](https://core.telegram.org/bots/api#chatmembermember)
    * [ChatMemberRestricted](https://core.telegram.org/bots/api#chatmemberrestricted)
    * [ChatMemberLeft](https://core.telegram.org/bots/api#chatmemberleft)
    * [ChatMemberBanned](https://core.telegram.org/bots/api#chatmemberbanned)
    """
    status: t.Literal["creator", "administrator", "member", "restricted", "left", "kicked"]

class StoryAreaType(StoryAreaTypeLocation, StoryAreaTypeSuggestedReaction, StoryAreaTypeLink, StoryAreaTypeWeather, StoryAreaTypeUniqueGift):
    """
    ### [StoryAreaType](https://core.telegram.org/bots/api#storyareatype)  
    
    Describes the type of a clickable area on a story. Currently, it can be one of
    
    * [StoryAreaTypeLocation](https://core.telegram.org/bots/api#storyareatypelocation)
    * [StoryAreaTypeSuggestedReaction](https://core.telegram.org/bots/api#storyareatypesuggestedreaction)
    * [StoryAreaTypeLink](https://core.telegram.org/bots/api#storyareatypelink)
    * [StoryAreaTypeWeather](https://core.telegram.org/bots/api#storyareatypeweather)
    * [StoryAreaTypeUniqueGift](https://core.telegram.org/bots/api#storyareatypeuniquegift)
    """
    type: t.Literal["location", "suggested_reaction", "link", "weather", "unique_gift"]

class ReactionType(ReactionTypeEmoji, ReactionTypeCustomEmoji, ReactionTypePaid):
    """
    ### [ReactionType](https://core.telegram.org/bots/api#reactiontype)  
    
    This object describes the type of a reaction. Currently, it can be one of
    
    * [ReactionTypeEmoji](https://core.telegram.org/bots/api#reactiontypeemoji)
    * [ReactionTypeCustomEmoji](https://core.telegram.org/bots/api#reactiontypecustomemoji)
    * [ReactionTypePaid](https://core.telegram.org/bots/api#reactiontypepaid)
    """
    type: t.Literal["emoji", "custom_emoji", "paid"]

class OwnedGift(OwnedGiftRegular, OwnedGiftUnique):
    """
    ### [OwnedGift](https://core.telegram.org/bots/api#ownedgift)  
    
    This object describes a gift received and owned by a user or a chat. Currently, it can be one of
    
    * [OwnedGiftRegular](https://core.telegram.org/bots/api#ownedgiftregular)
    * [OwnedGiftUnique](https://core.telegram.org/bots/api#ownedgiftunique)
    """
    type: t.Literal["regular", "unique"]

class BotCommandScope(BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, BotCommandScopeChat, BotCommandScopeChatAdministrators, BotCommandScopeChatMember):
    """
    ### [BotCommandScope](https://core.telegram.org/bots/api#botcommandscope)  
    
    This object represents the scope to which bot commands are applied. Currently, the following 7 scopes are supported:
    
    * [BotCommandScopeDefault](https://core.telegram.org/bots/api#botcommandscopedefault)
    * [BotCommandScopeAllPrivateChats](https://core.telegram.org/bots/api#botcommandscopeallprivatechats)
    * [BotCommandScopeAllGroupChats](https://core.telegram.org/bots/api#botcommandscopeallgroupchats)
    * [BotCommandScopeAllChatAdministrators](https://core.telegram.org/bots/api#botcommandscopeallchatadministrators)
    * [BotCommandScopeChat](https://core.telegram.org/bots/api#botcommandscopechat)
    * [BotCommandScopeChatAdministrators](https://core.telegram.org/bots/api#botcommandscopechatadministrators)
    * [BotCommandScopeChatMember](https://core.telegram.org/bots/api#botcommandscopechatmember)
    """
    type: t.Literal["default", "all_private_chats", "all_group_chats", "all_chat_administrators", "chat", "chat_administrators", "chat_member"]

class MenuButton(MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault):
    """
    ### [MenuButton](https://core.telegram.org/bots/api#menubutton)  
    
    This object describes the bot's menu button in a private chat. It should be one of
    
    * [MenuButtonCommands](https://core.telegram.org/bots/api#menubuttoncommands)
    * [MenuButtonWebApp](https://core.telegram.org/bots/api#menubuttonwebapp)
    * [MenuButtonDefault](https://core.telegram.org/bots/api#menubuttondefault)
    
    If a menu button other than [MenuButtonDefault](https://core.telegram.org/bots/api#menubuttondefault) is set for a private chat, then it is applied in the chat. Otherwise the default menu button is applied. By default, the menu button opens the list of bot commands.
    """
    type: t.Literal["commands", "web_app", "default"]

class ChatBoostSource(ChatBoostSourcePremium, ChatBoostSourceGiftCode, ChatBoostSourceGiveaway):
    """
    ### [ChatBoostSource](https://core.telegram.org/bots/api#chatboostsource)  
    
    This object describes the source of a chat boost. It can be one of
    
    * [ChatBoostSourcePremium](https://core.telegram.org/bots/api#chatboostsourcepremium)
    * [ChatBoostSourceGiftCode](https://core.telegram.org/bots/api#chatboostsourcegiftcode)
    * [ChatBoostSourceGiveaway](https://core.telegram.org/bots/api#chatboostsourcegiveaway)
    """
    source: t.Literal["premium", "gift_code", "giveaway"]

class InputMedia(InputMediaAnimation, InputMediaDocument, InputMediaAudio, InputMediaPhoto, InputMediaVideo):
    """
    ### [InputMedia](https://core.telegram.org/bots/api#inputmedia)  
    
    This object represents the content of a media message to be sent. It should be one of
    
    * [InputMediaAnimation](https://core.telegram.org/bots/api#inputmediaanimation)
    * [InputMediaDocument](https://core.telegram.org/bots/api#inputmediadocument)
    * [InputMediaAudio](https://core.telegram.org/bots/api#inputmediaaudio)
    * [InputMediaPhoto](https://core.telegram.org/bots/api#inputmediaphoto)
    * [InputMediaVideo](https://core.telegram.org/bots/api#inputmediavideo)
    """
    type: t.Literal["animation", "document", "audio", "photo", "video"]

class InputPaidMedia(InputPaidMediaPhoto, InputPaidMediaVideo):
    """
    ### [InputPaidMedia](https://core.telegram.org/bots/api#inputpaidmedia)  
    
    This object describes the paid media to be sent. Currently, it can be one of
    
    * [InputPaidMediaPhoto](https://core.telegram.org/bots/api#inputpaidmediaphoto)
    * [InputPaidMediaVideo](https://core.telegram.org/bots/api#inputpaidmediavideo)
    """
    type: t.Literal["photo", "video"]

class InputProfilePhoto(InputProfilePhotoStatic, InputProfilePhotoAnimated):
    """
    ### [InputProfilePhoto](https://core.telegram.org/bots/api#inputprofilephoto)  
    
    This object describes a profile photo to set. Currently, it can be one of
    
    * [InputProfilePhotoStatic](https://core.telegram.org/bots/api#inputprofilephotostatic)
    * [InputProfilePhotoAnimated](https://core.telegram.org/bots/api#inputprofilephotoanimated)
    """
    type: t.Literal["static", "animated"]

class InputStoryContent(InputStoryContentPhoto, InputStoryContentVideo):
    """
    ### [InputStoryContent](https://core.telegram.org/bots/api#inputstorycontent)  
    
    This object describes the content of a story to post. Currently, it can be one of
    
    * [InputStoryContentPhoto](https://core.telegram.org/bots/api#inputstorycontentphoto)
    * [InputStoryContentVideo](https://core.telegram.org/bots/api#inputstorycontentvideo)
    """
    type: t.Literal["photo", "video"]

class InlineQueryResult(InlineQueryResultCachedAudio, InlineQueryResultCachedDocument, InlineQueryResultCachedGif, InlineQueryResultCachedMpeg4Gif, InlineQueryResultCachedPhoto, InlineQueryResultCachedSticker, InlineQueryResultCachedVideo, InlineQueryResultCachedVoice, InlineQueryResultArticle, InlineQueryResultAudio, InlineQueryResultContact, InlineQueryResultGame, InlineQueryResultDocument, InlineQueryResultGif, InlineQueryResultLocation, InlineQueryResultMpeg4Gif, InlineQueryResultPhoto, InlineQueryResultVenue, InlineQueryResultVideo, InlineQueryResultVoice):
    """
    ### [InlineQueryResult](https://core.telegram.org/bots/api#inlinequeryresult)  
    
    This object represents one result of an inline query. Telegram clients currently support results of the following 20 types:
    
    * [InlineQueryResultCachedAudio](https://core.telegram.org/bots/api#inlinequeryresultcachedaudio)
    * [InlineQueryResultCachedDocument](https://core.telegram.org/bots/api#inlinequeryresultcacheddocument)
    * [InlineQueryResultCachedGif](https://core.telegram.org/bots/api#inlinequeryresultcachedgif)
    * [InlineQueryResultCachedMpeg4Gif](https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif)
    * [InlineQueryResultCachedPhoto](https://core.telegram.org/bots/api#inlinequeryresultcachedphoto)
    * [InlineQueryResultCachedSticker](https://core.telegram.org/bots/api#inlinequeryresultcachedsticker)
    * [InlineQueryResultCachedVideo](https://core.telegram.org/bots/api#inlinequeryresultcachedvideo)
    * [InlineQueryResultCachedVoice](https://core.telegram.org/bots/api#inlinequeryresultcachedvoice)
    * [InlineQueryResultArticle](https://core.telegram.org/bots/api#inlinequeryresultarticle)
    * [InlineQueryResultAudio](https://core.telegram.org/bots/api#inlinequeryresultaudio)
    * [InlineQueryResultContact](https://core.telegram.org/bots/api#inlinequeryresultcontact)
    * [InlineQueryResultGame](https://core.telegram.org/bots/api#inlinequeryresultgame)
    * [InlineQueryResultDocument](https://core.telegram.org/bots/api#inlinequeryresultdocument)
    * [InlineQueryResultGif](https://core.telegram.org/bots/api#inlinequeryresultgif)
    * [InlineQueryResultLocation](https://core.telegram.org/bots/api#inlinequeryresultlocation)
    * [InlineQueryResultMpeg4Gif](https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif)
    * [InlineQueryResultPhoto](https://core.telegram.org/bots/api#inlinequeryresultphoto)
    * [InlineQueryResultVenue](https://core.telegram.org/bots/api#inlinequeryresultvenue)
    * [InlineQueryResultVideo](https://core.telegram.org/bots/api#inlinequeryresultvideo)
    * [InlineQueryResultVoice](https://core.telegram.org/bots/api#inlinequeryresultvoice)
    
    **Note:** All URLs passed in inline query results will be available to end users and therefore must be assumed to be **public**.
    """
    type: t.Literal["audio", "document", "gif", "mpeg4_gif", "photo", "sticker", "video", "voice", "article", "audio", "contact", "game", "document", "gif", "location", "mpeg4_gif", "photo", "venue", "video", "voice"]

class InputMessageContent(InputTextMessageContent, InputLocationMessageContent, InputVenueMessageContent, InputContactMessageContent, InputInvoiceMessageContent):
    """
    ### [InputMessageContent](https://core.telegram.org/bots/api#inputmessagecontent)  
    
    This object represents the content of a message to be sent as a result of an inline query. Telegram clients currently support the following 5 types:
    
    * [InputTextMessageContent](https://core.telegram.org/bots/api#inputtextmessagecontent)
    * [InputLocationMessageContent](https://core.telegram.org/bots/api#inputlocationmessagecontent)
    * [InputVenueMessageContent](https://core.telegram.org/bots/api#inputvenuemessagecontent)
    * [InputContactMessageContent](https://core.telegram.org/bots/api#inputcontactmessagecontent)
    * [InputInvoiceMessageContent](https://core.telegram.org/bots/api#inputinvoicemessagecontent)
    """

class RevenueWithdrawalState(RevenueWithdrawalStatePending, RevenueWithdrawalStateSucceeded, RevenueWithdrawalStateFailed):
    """
    ### [RevenueWithdrawalState](https://core.telegram.org/bots/api#revenuewithdrawalstate)  
    
    This object describes the state of a revenue withdrawal operation. Currently, it can be one of
    
    * [RevenueWithdrawalStatePending](https://core.telegram.org/bots/api#revenuewithdrawalstatepending)
    * [RevenueWithdrawalStateSucceeded](https://core.telegram.org/bots/api#revenuewithdrawalstatesucceeded)
    * [RevenueWithdrawalStateFailed](https://core.telegram.org/bots/api#revenuewithdrawalstatefailed)
    """
    type: t.Literal["pending", "succeeded", "failed"]

class TransactionPartner(TransactionPartnerUser, TransactionPartnerChat, TransactionPartnerAffiliateProgram, TransactionPartnerFragment, TransactionPartnerTelegramAds, TransactionPartnerTelegramApi, TransactionPartnerOther):
    """
    ### [TransactionPartner](https://core.telegram.org/bots/api#transactionpartner)  
    
    This object describes the source of a transaction, or its recipient for outgoing transactions. Currently, it can be one of
    
    * [TransactionPartnerUser](https://core.telegram.org/bots/api#transactionpartneruser)
    * [TransactionPartnerChat](https://core.telegram.org/bots/api#transactionpartnerchat)
    * [TransactionPartnerAffiliateProgram](https://core.telegram.org/bots/api#transactionpartneraffiliateprogram)
    * [TransactionPartnerFragment](https://core.telegram.org/bots/api#transactionpartnerfragment)
    * [TransactionPartnerTelegramAds](https://core.telegram.org/bots/api#transactionpartnertelegramads)
    * [TransactionPartnerTelegramApi](https://core.telegram.org/bots/api#transactionpartnertelegramapi)
    * [TransactionPartnerOther](https://core.telegram.org/bots/api#transactionpartnerother)
    """
    type: t.Literal["user", "chat", "affiliate_program", "fragment", "telegram_ads", "telegram_api", "other"]

class PassportElementError(PassportElementErrorDataField, PassportElementErrorFrontSide, PassportElementErrorReverseSide, PassportElementErrorSelfie, PassportElementErrorFile, PassportElementErrorFiles, PassportElementErrorTranslationFile, PassportElementErrorTranslationFiles, PassportElementErrorUnspecified):
    """
    ### [PassportElementError](https://core.telegram.org/bots/api#passportelementerror)  
    
    This object represents an error in the Telegram Passport element which was submitted that should be resolved by the user. It should be one of:
    
    * [PassportElementErrorDataField](https://core.telegram.org/bots/api#passportelementerrordatafield)
    * [PassportElementErrorFrontSide](https://core.telegram.org/bots/api#passportelementerrorfrontside)
    * [PassportElementErrorReverseSide](https://core.telegram.org/bots/api#passportelementerrorreverseside)
    * [PassportElementErrorSelfie](https://core.telegram.org/bots/api#passportelementerrorselfie)
    * [PassportElementErrorFile](https://core.telegram.org/bots/api#passportelementerrorfile)
    * [PassportElementErrorFiles](https://core.telegram.org/bots/api#passportelementerrorfiles)
    * [PassportElementErrorTranslationFile](https://core.telegram.org/bots/api#passportelementerrortranslationfile)
    * [PassportElementErrorTranslationFiles](https://core.telegram.org/bots/api#passportelementerrortranslationfiles)
    * [PassportElementErrorUnspecified](https://core.telegram.org/bots/api#passportelementerrorunspecified)
    """
    source: t.Literal["data", "front_side", "reverse_side", "selfie", "file", "files", "translation_file", "translation_files", "unspecified"]
