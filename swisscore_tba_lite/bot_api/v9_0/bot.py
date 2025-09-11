
import typing as t
from asyncio import Task
from pathlib import Path

from . import objects as tg, literals
from ...core.base_bot import BaseBot, api_method_wrapper
from ...utils.files import InputFile

class Bot(BaseBot):
    """
    Telegram Bot API methods scraped from '**Bot API 9.0** *(April 11, 2025)*'
    """
    @api_method_wrapper()
    def get_updates(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        timeout: int | None = None,
        allowed_updates: list[literals.UpdateType] | None = None
    ) -> Task[list[tg.Update]]:
        """
        ### [getUpdates](https://core.telegram.org/bots/api#getupdates)  
        
        Use this method to receive incoming updates using long polling ([wiki](https://en.wikipedia.org/wiki/Push_technology#Long_polling)). Returns an Array of [Update](https://core.telegram.org/bots/api#update) objects.
        
        > **Notes**  
        > **1\\.** This method will not work if an outgoing webhook is set up.  
        > **2\\.** In order to avoid getting duplicate updates, recalculate *offset* after each server response.
        """

    @api_method_wrapper(check_input_files=["certificate"])
    def set_webhook(
        self,
        url: str,
        *,
        certificate: Path | bytes | tg.InputFile | None = None,
        ip_address: str | None = None,
        max_connections: int | None = None,
        allowed_updates: list[literals.UpdateType] | None = None,
        drop_pending_updates: bool | None = None,
        secret_token: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setWebhook](https://core.telegram.org/bots/api#setwebhook)  
        
        Use this method to specify a URL and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified URL, containing a JSON\\-serialized [Update](https://core.telegram.org/bots/api#update). In case of an unsuccessful request (a request with response [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) different from `2XY`), we will repeat the request and give up after a reasonable amount of attempts. Returns *True* on success.
        
        If you'd like to make sure that the webhook was set by you, you can specify secret data in the parameter *secret\\_token*. If specified, the request will contain a header “X\\-Telegram\\-Bot\\-Api\\-Secret\\-Token” with the secret token as content.
        
        > **Notes**  
        > **1\\.** You will not be able to receive updates using [getUpdates](https://core.telegram.org/bots/api#getupdates) for as long as an outgoing webhook is set up.  
        > **2\\.** To use a self\\-signed certificate, you need to upload your [public key certificate](https://core.telegram.org/bots/self-signed) using *certificate* parameter. Please upload as InputFile, sending a String will not work.  
        > **3\\.** Ports currently supported *for webhooks*: **443, 80, 88, 8443**.
        > 
        > 
        > If you're having any trouble setting up webhooks, please check out this [amazing guide to webhooks](https://core.telegram.org/bots/webhooks).
        """

    @api_method_wrapper()
    def delete_webhook(
        self,
        *,
        drop_pending_updates: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteWebhook](https://core.telegram.org/bots/api#deletewebhook)  
        
        Use this method to remove webhook integration if you decide to switch back to [getUpdates](https://core.telegram.org/bots/api#getupdates). Returns *True* on success.
        """

    @api_method_wrapper()
    def get_webhook_info(self) -> Task[tg.WebhookInfo]:
        """
        ### [getWebhookInfo](https://core.telegram.org/bots/api#getwebhookinfo)  
        
        Use this method to get current webhook status. Requires no parameters. On success, returns a [WebhookInfo](https://core.telegram.org/bots/api#webhookinfo) object. If the bot is using [getUpdates](https://core.telegram.org/bots/api#getupdates), will return an object with the *url* field empty.
        """

    @api_method_wrapper()
    def get_me(self) -> Task[tg.User]:
        """
        ### [getMe](https://core.telegram.org/bots/api#getme)  
        
        A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a [User](https://core.telegram.org/bots/api#user) object.
        """

    @api_method_wrapper()
    def log_out(self) -> Task[t.Literal[True]]:
        """
        ### [logOut](https://core.telegram.org/bots/api#logout)  
        
        Use this method to log out from the cloud Bot API server before launching the bot locally. You **must** log out the bot before running it locally, otherwise there is no guarantee that the bot will receive updates. After a successful call, you can immediately log in on a local server, but will not be able to log in back to the cloud Bot API server for 10 minutes. Returns *True* on success. Requires no parameters.
        """

    @api_method_wrapper()
    def close(self) -> Task[t.Literal[True]]:
        """
        ### [close](https://core.telegram.org/bots/api#close)  
        
        Use this method to close the bot instance before moving it from one local server to another. You need to delete the webhook before calling this method to ensure that the bot isn't launched again after server restart. The method will return error 429 in the first 10 minutes after the bot is launched. Returns *True* on success. Requires no parameters.
        """

    @api_method_wrapper()
    def send_message(
        self,
        chat_id: int | str,
        text: str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        entities: list[tg.MessageEntity] | None = None,
        link_preview_options: tg.LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendMessage](https://core.telegram.org/bots/api#sendmessage)  
        
        Use this method to send text messages. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        *,
        message_thread_id: int | None = None,
        video_start_timestamp: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None
    ) -> Task[tg.Message]:
        """
        ### [forwardMessage](https://core.telegram.org/bots/api#forwardmessage)  
        
        Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def forward_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        *,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None
    ) -> Task[list[tg.MessageId]]:
        """
        ### [forwardMessages](https://core.telegram.org/bots/api#forwardmessages)  
        
        Use this method to forward multiple messages of any kind. If some of the specified messages can't be found or forwarded, they are skipped. Service messages and messages with protected content can't be forwarded. Album grouping is kept for forwarded messages. On success, an array of [MessageId](https://core.telegram.org/bots/api#messageid) of the sent messages is returned.
        """

    @api_method_wrapper()
    def copy_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        *,
        message_thread_id: int | None = None,
        video_start_timestamp: int | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.MessageId]:
        """
        ### [copyMessage](https://core.telegram.org/bots/api#copymessage)  
        
        Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz [poll](https://core.telegram.org/bots/api#poll) can be copied only if the value of the field *correct\\_option\\_id* is known to the bot. The method is analogous to the method [forwardMessage](https://core.telegram.org/bots/api#forwardmessage), but the copied message doesn't have a link to the original message. Returns the [MessageId](https://core.telegram.org/bots/api#messageid) of the sent message on success.
        """

    @api_method_wrapper()
    def copy_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        *,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        remove_caption: bool | None = None
    ) -> Task[list[tg.MessageId]]:
        """
        ### [copyMessages](https://core.telegram.org/bots/api#copymessages)  
        
        Use this method to copy messages of any kind. If some of the specified messages can't be found or copied, they are skipped. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz [poll](https://core.telegram.org/bots/api#poll) can be copied only if the value of the field *correct\\_option\\_id* is known to the bot. The method is analogous to the method [forwardMessages](https://core.telegram.org/bots/api#forwardmessages), but the copied messages don't have a link to the original message. Album grouping is kept for copied messages. On success, an array of [MessageId](https://core.telegram.org/bots/api#messageid) of the sent messages is returned.
        """

    @api_method_wrapper(check_input_files=["photo"])
    def send_photo(
        self,
        chat_id: int | str,
        photo: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendPhoto](https://core.telegram.org/bots/api#sendphoto)  
        
        Use this method to send photos. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper(check_input_files=["audio", "thumbnail"])
    def send_audio(
        self,
        chat_id: int | str,
        audio: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        duration: int | None = None,
        performer: str | None = None,
        title: str | None = None,
        thumbnail: Path | bytes | tg.InputFile | str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendAudio](https://core.telegram.org/bots/api#sendaudio)  
        
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the [sendVoice](https://core.telegram.org/bots/api#sendvoice) method instead.
        """

    @api_method_wrapper(check_input_files=["document", "thumbnail"])
    def send_document(
        self,
        chat_id: int | str,
        document: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        thumbnail: Path | bytes | tg.InputFile | str | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        disable_content_type_detection: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendDocument](https://core.telegram.org/bots/api#senddocument)  
        
        Use this method to send general files. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        """

    @api_method_wrapper(check_input_files=["video", "thumbnail", "cover"])
    def send_video(
        self,
        chat_id: int | str,
        video: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: Path | bytes | tg.InputFile | str | None = None,
        cover: Path | bytes | tg.InputFile | str | None = None,
        start_timestamp: int | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        supports_streaming: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendVideo](https://core.telegram.org/bots/api#sendvideo)  
        
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as [Document](https://core.telegram.org/bots/api#document)). On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        """

    @api_method_wrapper(check_input_files=["animation", "thumbnail"])
    def send_animation(
        self,
        chat_id: int | str,
        animation: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: Path | bytes | tg.InputFile | str | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendAnimation](https://core.telegram.org/bots/api#sendanimation)  
        
        Use this method to send animation files (GIF or H.264/MPEG\\-4 AVC video without sound). On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        """

    @api_method_wrapper(check_input_files=["voice"])
    def send_voice(
        self,
        chat_id: int | str,
        voice: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        duration: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendVoice](https://core.telegram.org/bots/api#sendvoice)  
        
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as [Audio](https://core.telegram.org/bots/api#audio) or [Document](https://core.telegram.org/bots/api#document)). On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        """

    @api_method_wrapper(check_input_files=["video_note", "thumbnail"])
    def send_video_note(
        self,
        chat_id: int | str,
        video_note: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        length: int | None = None,
        thumbnail: Path | bytes | tg.InputFile | str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendVideoNote](https://core.telegram.org/bots/api#sendvideonote)  
        
        As of [v.4\\.0](https://telegram.org/blog/video-messages-and-telescope), Telegram clients support rounded square MPEG4 videos of up to 1 minute long. Use this method to send video messages. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper(check_input_media={"media": ["thumbnail", "cover", "media"]})
    def send_paid_media(
        self,
        chat_id: int | str,
        star_count: int,
        media: list[tg.InputPaidMedia],
        *,
        business_connection_id: str | None = None,
        payload: str | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendPaidMedia](https://core.telegram.org/bots/api#sendpaidmedia)  
        
        Use this method to send paid media. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper(check_input_media={"media": ["thumbnail", "cover", "media"]})
    def send_media_group(
        self,
        chat_id: int | str,
        media: list[tg.InputMediaAudio | tg.InputMediaDocument | tg.InputMediaPhoto | tg.InputMediaVideo],
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None
    ) -> Task[list[tg.Message]]:
        """
        ### [sendMediaGroup](https://core.telegram.org/bots/api#sendmediagroup)  
        
        Use this method to send a group of photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an array of [Messages](https://core.telegram.org/bots/api#message) that were sent is returned.
        """

    @api_method_wrapper()
    def send_location(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        horizontal_accuracy: float | None = None,
        live_period: int | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendLocation](https://core.telegram.org/bots/api#sendlocation)  
        
        Use this method to send point on the map. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def send_venue(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendVenue](https://core.telegram.org/bots/api#sendvenue)  
        
        Use this method to send information about a venue. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def send_contact(
        self,
        chat_id: int | str,
        phone_number: str,
        first_name: str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        last_name: str | None = None,
        vcard: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendContact](https://core.telegram.org/bots/api#sendcontact)  
        
        Use this method to send phone contacts. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def send_poll(
        self,
        chat_id: int | str,
        question: str,
        options: list[tg.InputPollOption],
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        question_parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        question_entities: list[tg.MessageEntity] | None = None,
        is_anonymous: bool | None = None,
        type: str | None = None,
        allows_multiple_answers: bool | None = None,
        correct_option_id: int | None = None,
        explanation: str | None = None,
        explanation_parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        explanation_entities: list[tg.MessageEntity] | None = None,
        open_period: int | None = None,
        close_date: int | None = None,
        is_closed: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendPoll](https://core.telegram.org/bots/api#sendpoll)  
        
        Use this method to send a native poll. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def send_dice(
        self,
        chat_id: int | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        emoji: literals.DiceEmoji | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendDice](https://core.telegram.org/bots/api#senddice)  
        
        Use this method to send an animated emoji that will display a random value. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def send_chat_action(
        self,
        chat_id: int | str,
        action: literals.ChatAction,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [sendChatAction](https://core.telegram.org/bots/api#sendchataction)  
        
        Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns *True* on success.
        
        > Example: The [ImageBot](https://t.me/imagebot) needs some time to process a request and upload the image. Instead of sending a text message along the lines of “Retrieving image, please wait…”, the bot may use [sendChatAction](https://core.telegram.org/bots/api#sendchataction) with *action* \\= *upload\\_photo*. The user will see a “sending photo” status for the bot.
        
        We only recommend using this method when a response from the bot will take a **noticeable** amount of time to arrive.
        """

    @api_method_wrapper()
    def set_message_reaction(
        self,
        chat_id: int | str,
        message_id: int,
        *,
        reaction: list[tg.ReactionType] | None = None,
        is_big: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setMessageReaction](https://core.telegram.org/bots/api#setmessagereaction)  
        
        Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_user_profile_photos(
        self,
        user_id: int,
        *,
        offset: int | None = None,
        limit: int | None = None
    ) -> Task[tg.UserProfilePhotos]:
        """
        ### [getUserProfilePhotos](https://core.telegram.org/bots/api#getuserprofilephotos)  
        
        Use this method to get a list of profile pictures for a user. Returns a [UserProfilePhotos](https://core.telegram.org/bots/api#userprofilephotos) object.
        """

    @api_method_wrapper()
    def set_user_emoji_status(
        self,
        user_id: int,
        *,
        emoji_status_custom_emoji_id: str | None = None,
        emoji_status_expiration_date: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setUserEmojiStatus](https://core.telegram.org/bots/api#setuseremojistatus)  
        
        Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method [requestEmojiStatusAccess](https://core.telegram.org/bots/webapps#initializing-mini-apps). Returns *True* on success.
        """

    @api_method_wrapper()
    def get_file(self, file_id: str) -> Task[tg.File]:
        """
        ### [getFile](https://core.telegram.org/bots/api#getfile)  
        
        Use this method to get basic information about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a [File](https://core.telegram.org/bots/api#file) object is returned. The file can then be downloaded via the link `https://api.telegram.org/file/bot<token>/<file_path>`, where `<file_path>` is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling [getFile](https://core.telegram.org/bots/api#getfile) again.
        
        **Note:** This function may not preserve the original file name and MIME type. You should save the file's MIME type and name (if available) when the File object is received.
        """

    @api_method_wrapper()
    def ban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        *,
        until_date: int | None = None,
        revoke_messages: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [banChatMember](https://core.telegram.org/bots/api#banchatmember)  
        
        Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless [unbanned](https://core.telegram.org/bots/api#unbanchatmember) first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def unban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        *,
        only_if_banned: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [unbanChatMember](https://core.telegram.org/bots/api#unbanchatmember)  
        
        Use this method to unban a previously banned user in a supergroup or channel. The user will **not** return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be **removed** from the chat. If you don't want this, use the parameter *only\\_if\\_banned*. Returns *True* on success.
        """

    @api_method_wrapper()
    def restrict_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        permissions: tg.ChatPermissions,
        *,
        use_independent_chat_permissions: bool | None = None,
        until_date: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [restrictChatMember](https://core.telegram.org/bots/api#restrictchatmember)  
        
        Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass *True* for all permissions to lift restrictions from a user. Returns *True* on success.
        """

    @api_method_wrapper()
    def promote_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        *,
        is_anonymous: bool | None = None,
        can_manage_chat: bool | None = None,
        can_delete_messages: bool | None = None,
        can_manage_video_chats: bool | None = None,
        can_restrict_members: bool | None = None,
        can_promote_members: bool | None = None,
        can_change_info: bool | None = None,
        can_invite_users: bool | None = None,
        can_post_stories: bool | None = None,
        can_edit_stories: bool | None = None,
        can_delete_stories: bool | None = None,
        can_post_messages: bool | None = None,
        can_edit_messages: bool | None = None,
        can_pin_messages: bool | None = None,
        can_manage_topics: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [promoteChatMember](https://core.telegram.org/bots/api#promotechatmember)  
        
        Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass *False* for all boolean parameters to demote a user. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_chat_administrator_custom_title(
        self,
        chat_id: int | str,
        user_id: int,
        custom_title: str
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatAdministratorCustomTitle](https://core.telegram.org/bots/api#setchatadministratorcustomtitle)  
        
        Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def ban_chat_sender_chat(
        self,
        chat_id: int | str,
        sender_chat_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [banChatSenderChat](https://core.telegram.org/bots/api#banchatsenderchat)  
        
        Use this method to ban a channel chat in a supergroup or a channel. Until the chat is [unbanned](https://core.telegram.org/bots/api#unbanchatsenderchat), the owner of the banned chat won't be able to send messages on behalf of **any of their channels**. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def unban_chat_sender_chat(
        self,
        chat_id: int | str,
        sender_chat_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [unbanChatSenderChat](https://core.telegram.org/bots/api#unbanchatsenderchat)  
        
        Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_chat_permissions(
        self,
        chat_id: int | str,
        permissions: tg.ChatPermissions,
        *,
        use_independent_chat_permissions: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatPermissions](https://core.telegram.org/bots/api#setchatpermissions)  
        
        Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the *can\\_restrict\\_members* administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def export_chat_invite_link(self, chat_id: int | str) -> Task[str]:
        """
        ### [exportChatInviteLink](https://core.telegram.org/bots/api#exportchatinvitelink)  
        
        Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as *String* on success.
        
        > Note: Each administrator in a chat generates their own invite links. Bots can't use invite links generated by other administrators. If you want your bot to work with invite links, it will need to generate its own link using [exportChatInviteLink](https://core.telegram.org/bots/api#exportchatinvitelink) or by calling the [getChat](https://core.telegram.org/bots/api#getchat) method. If your bot needs to generate a new primary invite link replacing its previous one, use [exportChatInviteLink](https://core.telegram.org/bots/api#exportchatinvitelink) again.
        """

    @api_method_wrapper()
    def create_chat_invite_link(
        self,
        chat_id: int | str,
        *,
        name: str | None = None,
        expire_date: int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None
    ) -> Task[tg.ChatInviteLink]:
        """
        ### [createChatInviteLink](https://core.telegram.org/bots/api#createchatinvitelink)  
        
        Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method [revokeChatInviteLink](https://core.telegram.org/bots/api#revokechatinvitelink). Returns the new invite link as [ChatInviteLink](https://core.telegram.org/bots/api#chatinvitelink) object.
        """

    @api_method_wrapper()
    def edit_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        *,
        name: str | None = None,
        expire_date: int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None
    ) -> Task[tg.ChatInviteLink]:
        """
        ### [editChatInviteLink](https://core.telegram.org/bots/api#editchatinvitelink)  
        
        Use this method to edit a non\\-primary invite link created by the bot. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the edited invite link as a [ChatInviteLink](https://core.telegram.org/bots/api#chatinvitelink) object.
        """

    @api_method_wrapper()
    def create_chat_subscription_invite_link(
        self,
        chat_id: int | str,
        subscription_period: int,
        subscription_price: int,
        *,
        name: str | None = None
    ) -> Task[tg.ChatInviteLink]:
        """
        ### [createChatSubscriptionInviteLink](https://core.telegram.org/bots/api#createchatsubscriptioninvitelink)  
        
        Use this method to create a [subscription invite link](https://telegram.org/blog/superchannels-star-reactions-subscriptions#star-subscriptions) for a channel chat. The bot must have the *can\\_invite\\_users* administrator rights. The link can be edited using the method [editChatSubscriptionInviteLink](https://core.telegram.org/bots/api#editchatsubscriptioninvitelink) or revoked using the method [revokeChatInviteLink](https://core.telegram.org/bots/api#revokechatinvitelink). Returns the new invite link as a [ChatInviteLink](https://core.telegram.org/bots/api#chatinvitelink) object.
        """

    @api_method_wrapper()
    def edit_chat_subscription_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        *,
        name: str | None = None
    ) -> Task[tg.ChatInviteLink]:
        """
        ### [editChatSubscriptionInviteLink](https://core.telegram.org/bots/api#editchatsubscriptioninvitelink)  
        
        Use this method to edit a subscription invite link created by the bot. The bot must have the *can\\_invite\\_users* administrator rights. Returns the edited invite link as a [ChatInviteLink](https://core.telegram.org/bots/api#chatinvitelink) object.
        """

    @api_method_wrapper()
    def revoke_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str
    ) -> Task[tg.ChatInviteLink]:
        """
        ### [revokeChatInviteLink](https://core.telegram.org/bots/api#revokechatinvitelink)  
        
        Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as [ChatInviteLink](https://core.telegram.org/bots/api#chatinvitelink) object.
        """

    @api_method_wrapper()
    def approve_chat_join_request(
        self,
        chat_id: int | str,
        user_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [approveChatJoinRequest](https://core.telegram.org/bots/api#approvechatjoinrequest)  
        
        Use this method to approve a chat join request. The bot must be an administrator in the chat for this to work and must have the *can\\_invite\\_users* administrator right. Returns *True* on success.
        """

    @api_method_wrapper()
    def decline_chat_join_request(
        self,
        chat_id: int | str,
        user_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [declineChatJoinRequest](https://core.telegram.org/bots/api#declinechatjoinrequest)  
        
        Use this method to decline a chat join request. The bot must be an administrator in the chat for this to work and must have the *can\\_invite\\_users* administrator right. Returns *True* on success.
        """

    @api_method_wrapper(check_input_files=["photo"])
    def set_chat_photo(
        self,
        chat_id: int | str,
        photo: Path | bytes | tg.InputFile
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatPhoto](https://core.telegram.org/bots/api#setchatphoto)  
        
        Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_chat_photo(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [deleteChatPhoto](https://core.telegram.org/bots/api#deletechatphoto)  
        
        Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_chat_title(
        self,
        chat_id: int | str,
        title: str
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatTitle](https://core.telegram.org/bots/api#setchattitle)  
        
        Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_chat_description(
        self,
        chat_id: int | str,
        *,
        description: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatDescription](https://core.telegram.org/bots/api#setchatdescription)  
        
        Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def pin_chat_message(
        self,
        chat_id: int | str,
        message_id: int,
        *,
        business_connection_id: str | None = None,
        disable_notification: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [pinChatMessage](https://core.telegram.org/bots/api#pinchatmessage)  
        
        Use this method to add a message to the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can\\_pin\\_messages' administrator right in a supergroup or 'can\\_edit\\_messages' administrator right in a channel. Returns *True* on success.
        """

    @api_method_wrapper()
    def unpin_chat_message(
        self,
        chat_id: int | str,
        *,
        business_connection_id: str | None = None,
        message_id: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [unpinChatMessage](https://core.telegram.org/bots/api#unpinchatmessage)  
        
        Use this method to remove a message from the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can\\_pin\\_messages' administrator right in a supergroup or 'can\\_edit\\_messages' administrator right in a channel. Returns *True* on success.
        """

    @api_method_wrapper()
    def unpin_all_chat_messages(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [unpinAllChatMessages](https://core.telegram.org/bots/api#unpinallchatmessages)  
        
        Use this method to clear the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can\\_pin\\_messages' administrator right in a supergroup or 'can\\_edit\\_messages' administrator right in a channel. Returns *True* on success.
        """

    @api_method_wrapper()
    def leave_chat(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [leaveChat](https://core.telegram.org/bots/api#leavechat)  
        
        Use this method for your bot to leave a group, supergroup or channel. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_chat(self, chat_id: int | str) -> Task[tg.ChatFullInfo]:
        """
        ### [getChat](https://core.telegram.org/bots/api#getchat)  
        
        Use this method to get up\\-to\\-date information about the chat. Returns a [ChatFullInfo](https://core.telegram.org/bots/api#chatfullinfo) object on success.
        """

    @api_method_wrapper()
    def get_chat_administrators(self, chat_id: int | str) -> Task[list[tg.ChatMember]]:
        """
        ### [getChatAdministrators](https://core.telegram.org/bots/api#getchatadministrators)  
        
        Use this method to get a list of administrators in a chat, which aren't bots. Returns an Array of [ChatMember](https://core.telegram.org/bots/api#chatmember) objects.
        """

    @api_method_wrapper()
    def get_chat_member_count(self, chat_id: int | str) -> Task[int]:
        """
        ### [getChatMemberCount](https://core.telegram.org/bots/api#getchatmembercount)  
        
        Use this method to get the number of members in a chat. Returns *Int* on success.
        """

    @api_method_wrapper()
    def get_chat_member(
        self,
        chat_id: int | str,
        user_id: int
    ) -> Task[tg.ChatMember]:
        """
        ### [getChatMember](https://core.telegram.org/bots/api#getchatmember)  
        
        Use this method to get information about a member of a chat. The method is only guaranteed to work for other users if the bot is an administrator in the chat. Returns a [ChatMember](https://core.telegram.org/bots/api#chatmember) object on success.
        """

    @api_method_wrapper()
    def set_chat_sticker_set(
        self,
        chat_id: int | str,
        sticker_set_name: str
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatStickerSet](https://core.telegram.org/bots/api#setchatstickerset)  
        
        Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field *can\\_set\\_sticker\\_set* optionally returned in [getChat](https://core.telegram.org/bots/api#getchat) requests to check if the bot can use this method. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_chat_sticker_set(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [deleteChatStickerSet](https://core.telegram.org/bots/api#deletechatstickerset)  
        
        Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field *can\\_set\\_sticker\\_set* optionally returned in [getChat](https://core.telegram.org/bots/api#getchat) requests to check if the bot can use this method. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_forum_topic_icon_stickers(self) -> Task[list[tg.Sticker]]:
        """
        ### [getForumTopicIconStickers](https://core.telegram.org/bots/api#getforumtopiciconstickers)  
        
        Use this method to get custom emoji stickers, which can be used as a forum topic icon by any user. Requires no parameters. Returns an Array of [Sticker](https://core.telegram.org/bots/api#sticker) objects.
        """

    @api_method_wrapper()
    def create_forum_topic(
        self,
        chat_id: int | str,
        name: str,
        *,
        icon_color: int | None = None,
        icon_custom_emoji_id: str | None = None
    ) -> Task[tg.ForumTopic]:
        """
        ### [createForumTopic](https://core.telegram.org/bots/api#createforumtopic)  
        
        Use this method to create a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights. Returns information about the created topic as a [ForumTopic](https://core.telegram.org/bots/api#forumtopic) object.
        """

    @api_method_wrapper()
    def edit_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        *,
        name: str | None = None,
        icon_custom_emoji_id: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [editForumTopic](https://core.telegram.org/bots/api#editforumtopic)  
        
        Use this method to edit name and icon of a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights, unless it is the creator of the topic. Returns *True* on success.
        """

    @api_method_wrapper()
    def close_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [closeForumTopic](https://core.telegram.org/bots/api#closeforumtopic)  
        
        Use this method to close an open topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights, unless it is the creator of the topic. Returns *True* on success.
        """

    @api_method_wrapper()
    def reopen_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [reopenForumTopic](https://core.telegram.org/bots/api#reopenforumtopic)  
        
        Use this method to reopen a closed topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights, unless it is the creator of the topic. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteForumTopic](https://core.telegram.org/bots/api#deleteforumtopic)  
        
        Use this method to delete a forum topic along with all its messages in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_delete\\_messages* administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def unpin_all_forum_topic_messages(
        self,
        chat_id: int | str,
        message_thread_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [unpinAllForumTopicMessages](https://core.telegram.org/bots/api#unpinallforumtopicmessages)  
        
        Use this method to clear the list of pinned messages in a forum topic. The bot must be an administrator in the chat for this to work and must have the *can\\_pin\\_messages* administrator right in the supergroup. Returns *True* on success.
        """

    @api_method_wrapper()
    def edit_general_forum_topic(
        self,
        chat_id: int | str,
        name: str
    ) -> Task[t.Literal[True]]:
        """
        ### [editGeneralForumTopic](https://core.telegram.org/bots/api#editgeneralforumtopic)  
        
        Use this method to edit the name of the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def close_general_forum_topic(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [closeGeneralForumTopic](https://core.telegram.org/bots/api#closegeneralforumtopic)  
        
        Use this method to close an open 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def reopen_general_forum_topic(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [reopenGeneralForumTopic](https://core.telegram.org/bots/api#reopengeneralforumtopic)  
        
        Use this method to reopen a closed 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights. The topic will be automatically unhidden if it was hidden. Returns *True* on success.
        """

    @api_method_wrapper()
    def hide_general_forum_topic(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [hideGeneralForumTopic](https://core.telegram.org/bots/api#hidegeneralforumtopic)  
        
        Use this method to hide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights. The topic will be automatically closed if it was open. Returns *True* on success.
        """

    @api_method_wrapper()
    def unhide_general_forum_topic(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [unhideGeneralForumTopic](https://core.telegram.org/bots/api#unhidegeneralforumtopic)  
        
        Use this method to unhide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the *can\\_manage\\_topics* administrator rights. Returns *True* on success.
        """

    @api_method_wrapper()
    def unpin_all_general_forum_topic_messages(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [unpinAllGeneralForumTopicMessages](https://core.telegram.org/bots/api#unpinallgeneralforumtopicmessages)  
        
        Use this method to clear the list of pinned messages in a General forum topic. The bot must be an administrator in the chat for this to work and must have the *can\\_pin\\_messages* administrator right in the supergroup. Returns *True* on success.
        """

    @api_method_wrapper()
    def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [answerCallbackQuery](https://core.telegram.org/bots/api#answercallbackquery)  
        
        Use this method to send answers to callback queries sent from [inline keyboards](https://core.telegram.org/bots/features#inline-keyboards). The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, *True* is returned.
        
        > Alternatively, the user can be redirected to the specified Game URL. For this option to work, you must first create a game for your bot via [@BotFather](https://t.me/botfather) and accept the terms. Otherwise, you may use links like `t.me/your_bot?start=XXXX` that open your bot with a parameter.
        """

    @api_method_wrapper()
    def get_user_chat_boosts(
        self,
        chat_id: int | str,
        user_id: int
    ) -> Task[tg.UserChatBoosts]:
        """
        ### [getUserChatBoosts](https://core.telegram.org/bots/api#getuserchatboosts)  
        
        Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a [UserChatBoosts](https://core.telegram.org/bots/api#userchatboosts) object.
        """

    @api_method_wrapper()
    def get_business_connection(self, business_connection_id: str) -> Task[tg.BusinessConnection]:
        """
        ### [getBusinessConnection](https://core.telegram.org/bots/api#getbusinessconnection)  
        
        Use this method to get information about the connection of the bot with a business account. Returns a [BusinessConnection](https://core.telegram.org/bots/api#businessconnection) object on success.
        """

    @api_method_wrapper()
    def set_my_commands(
        self,
        commands: list[tg.BotCommand],
        *,
        scope: tg.BotCommandScope | None = None,
        language_code: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setMyCommands](https://core.telegram.org/bots/api#setmycommands)  
        
        Use this method to change the list of the bot's commands. See [this manual](https://core.telegram.org/bots/features#commands) for more details about bot commands. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_my_commands(
        self,
        *,
        scope: tg.BotCommandScope | None = None,
        language_code: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteMyCommands](https://core.telegram.org/bots/api#deletemycommands)  
        
        Use this method to delete the list of the bot's commands for the given scope and user language. After deletion, [higher level commands](https://core.telegram.org/bots/api#determining-list-of-commands) will be shown to affected users. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_my_commands(
        self,
        *,
        scope: tg.BotCommandScope | None = None,
        language_code: str | None = None
    ) -> Task[list[tg.BotCommand]]:
        """
        ### [getMyCommands](https://core.telegram.org/bots/api#getmycommands)  
        
        Use this method to get the current list of the bot's commands for the given scope and user language. Returns an Array of [BotCommand](https://core.telegram.org/bots/api#botcommand) objects. If commands aren't set, an empty list is returned.
        """

    @api_method_wrapper()
    def set_my_name(
        self,
        *,
        name: str | None = None,
        language_code: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setMyName](https://core.telegram.org/bots/api#setmyname)  
        
        Use this method to change the bot's name. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_my_name(
        self,
        *,
        language_code: str | None = None
    ) -> Task[tg.BotName]:
        """
        ### [getMyName](https://core.telegram.org/bots/api#getmyname)  
        
        Use this method to get the current bot name for the given user language. Returns [BotName](https://core.telegram.org/bots/api#botname) on success.
        """

    @api_method_wrapper()
    def set_my_description(
        self,
        *,
        description: str | None = None,
        language_code: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setMyDescription](https://core.telegram.org/bots/api#setmydescription)  
        
        Use this method to change the bot's description, which is shown in the chat with the bot if the chat is empty. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_my_description(
        self,
        *,
        language_code: str | None = None
    ) -> Task[tg.BotDescription]:
        """
        ### [getMyDescription](https://core.telegram.org/bots/api#getmydescription)  
        
        Use this method to get the current bot description for the given user language. Returns [BotDescription](https://core.telegram.org/bots/api#botdescription) on success.
        """

    @api_method_wrapper()
    def set_my_short_description(
        self,
        *,
        short_description: str | None = None,
        language_code: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setMyShortDescription](https://core.telegram.org/bots/api#setmyshortdescription)  
        
        Use this method to change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_my_short_description(
        self,
        *,
        language_code: str | None = None
    ) -> Task[tg.BotShortDescription]:
        """
        ### [getMyShortDescription](https://core.telegram.org/bots/api#getmyshortdescription)  
        
        Use this method to get the current bot short description for the given user language. Returns [BotShortDescription](https://core.telegram.org/bots/api#botshortdescription) on success.
        """

    @api_method_wrapper()
    def set_chat_menu_button(
        self,
        *,
        chat_id: int | None = None,
        menu_button: tg.MenuButton | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setChatMenuButton](https://core.telegram.org/bots/api#setchatmenubutton)  
        
        Use this method to change the bot's menu button in a private chat, or the default menu button. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_chat_menu_button(
        self,
        *,
        chat_id: int | None = None
    ) -> Task[tg.MenuButton]:
        """
        ### [getChatMenuButton](https://core.telegram.org/bots/api#getchatmenubutton)  
        
        Use this method to get the current value of the bot's menu button in a private chat, or the default menu button. Returns [MenuButton](https://core.telegram.org/bots/api#menubutton) on success.
        """

    @api_method_wrapper()
    def set_my_default_administrator_rights(
        self,
        *,
        rights: tg.ChatAdministratorRights | None = None,
        for_channels: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setMyDefaultAdministratorRights](https://core.telegram.org/bots/api#setmydefaultadministratorrights)  
        
        Use this method to change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. These rights will be suggested to users, but they are free to modify the list before adding the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_my_default_administrator_rights(
        self,
        *,
        for_channels: bool | None = None
    ) -> Task[tg.ChatAdministratorRights]:
        """
        ### [getMyDefaultAdministratorRights](https://core.telegram.org/bots/api#getmydefaultadministratorrights)  
        
        Use this method to get the current default administrator rights of the bot. Returns [ChatAdministratorRights](https://core.telegram.org/bots/api#chatadministratorrights) on success.
        """

    @api_method_wrapper()
    def edit_message_text(
        self,
        text: str,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        entities: list[tg.MessageEntity] | None = None,
        link_preview_options: tg.LinkPreviewOptions | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [editMessageText](https://core.telegram.org/bots/api#editmessagetext)  
        
        Use this method to edit text and [game](https://core.telegram.org/bots/api#games) messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within **48 hours** from the time they were sent.
        """

    @api_method_wrapper()
    def edit_message_caption(
        self,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [editMessageCaption](https://core.telegram.org/bots/api#editmessagecaption)  
        
        Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within **48 hours** from the time they were sent.
        """

    @api_method_wrapper(check_input_media={"media": ["thumbnail", "cover", "media"]})
    def edit_message_media(
        self,
        media: tg.InputMedia,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [editMessageMedia](https://core.telegram.org/bots/api#editmessagemedia)  
        
        Use this method to edit animation, audio, document, photo, or video messages, or to add media to text messages. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file\\_id or specify a URL. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within **48 hours** from the time they were sent.
        """

    @api_method_wrapper()
    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        live_period: int | None = None,
        horizontal_accuracy: float | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [editMessageLiveLocation](https://core.telegram.org/bots/api#editmessagelivelocation)  
        
        Use this method to edit live location messages. A location can be edited until its *live\\_period* expires or editing is explicitly disabled by a call to [stopMessageLiveLocation](https://core.telegram.org/bots/api#stopmessagelivelocation). On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned.
        """

    @api_method_wrapper()
    def stop_message_live_location(
        self,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [stopMessageLiveLocation](https://core.telegram.org/bots/api#stopmessagelivelocation)  
        
        Use this method to stop updating a live location message before *live\\_period* expires. On success, if the message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned.
        """

    @api_method_wrapper()
    def edit_message_reply_markup(
        self,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [editMessageReplyMarkup](https://core.telegram.org/bots/api#editmessagereplymarkup)  
        
        Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within **48 hours** from the time they were sent.
        """

    @api_method_wrapper()
    def stop_poll(
        self,
        chat_id: int | str,
        message_id: int,
        *,
        business_connection_id: str | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Poll]:
        """
        ### [stopPoll](https://core.telegram.org/bots/api#stoppoll)  
        
        Use this method to stop a poll which was sent by the bot. On success, the stopped [Poll](https://core.telegram.org/bots/api#poll) is returned.
        """

    @api_method_wrapper()
    def delete_message(
        self,
        chat_id: int | str,
        message_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteMessage](https://core.telegram.org/bots/api#deletemessage)  
        
        Use this method to delete a message, including service messages, with the following limitations:  
        \\- A message can only be deleted if it was sent less than 48 hours ago.  
        \\- Service messages about a supergroup, channel, or forum topic creation can't be deleted.  
        \\- A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.  
        \\- Bots can delete outgoing messages in private chats, groups, and supergroups.  
        \\- Bots can delete incoming messages in private chats.  
        \\- Bots granted *can\\_post\\_messages* permissions can delete outgoing messages in channels.  
        \\- If the bot is an administrator of a group, it can delete any message there.  
        \\- If the bot has *can\\_delete\\_messages* permission in a supergroup or a channel, it can delete any message there.  
        Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_messages(
        self,
        chat_id: int | str,
        message_ids: list[int]
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteMessages](https://core.telegram.org/bots/api#deletemessages)  
        
        Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_available_gifts(self) -> Task[tg.Gifts]:
        """
        ### [getAvailableGifts](https://core.telegram.org/bots/api#getavailablegifts)  
        
        Returns the list of gifts that can be sent by the bot to users and channel chats. Requires no parameters. Returns a [Gifts](https://core.telegram.org/bots/api#gifts) object.
        """

    @api_method_wrapper()
    def send_gift(
        self,
        gift_id: str,
        *,
        user_id: int | None = None,
        chat_id: int | str | None = None,
        pay_for_upgrade: bool | None = None,
        text: str | None = None,
        text_parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        text_entities: list[tg.MessageEntity] | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [sendGift](https://core.telegram.org/bots/api#sendgift)  
        
        Sends a gift to the given user or channel chat. The gift can't be converted to Telegram Stars by the receiver. Returns *True* on success.
        """

    @api_method_wrapper()
    def gift_premium_subscription(
        self,
        user_id: int,
        month_count: int,
        star_count: int,
        *,
        text: str | None = None,
        text_parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        text_entities: list[tg.MessageEntity] | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [giftPremiumSubscription](https://core.telegram.org/bots/api#giftpremiumsubscription)  
        
        Gifts a Telegram Premium subscription to the given user. Returns *True* on success.
        """

    @api_method_wrapper()
    def verify_user(
        self,
        user_id: int,
        *,
        custom_description: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [verifyUser](https://core.telegram.org/bots/api#verifyuser)  
        
        Verifies a user [on behalf of the organization](https://telegram.org/verify#third-party-verification) which is represented by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def verify_chat(
        self,
        chat_id: int | str,
        *,
        custom_description: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [verifyChat](https://core.telegram.org/bots/api#verifychat)  
        
        Verifies a chat [on behalf of the organization](https://telegram.org/verify#third-party-verification) which is represented by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def remove_user_verification(self, user_id: int) -> Task[t.Literal[True]]:
        """
        ### [removeUserVerification](https://core.telegram.org/bots/api#removeuserverification)  
        
        Removes verification from a user who is currently verified [on behalf of the organization](https://telegram.org/verify#third-party-verification) represented by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def remove_chat_verification(self, chat_id: int | str) -> Task[t.Literal[True]]:
        """
        ### [removeChatVerification](https://core.telegram.org/bots/api#removechatverification)  
        
        Removes verification from a chat that is currently verified [on behalf of the organization](https://telegram.org/verify#third-party-verification) represented by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def read_business_message(
        self,
        business_connection_id: str,
        chat_id: int,
        message_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [readBusinessMessage](https://core.telegram.org/bots/api#readbusinessmessage)  
        
        Marks incoming message as read on behalf of a business account. Requires the *can\\_read\\_messages* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_business_messages(
        self,
        business_connection_id: str,
        message_ids: list[int]
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteBusinessMessages](https://core.telegram.org/bots/api#deletebusinessmessages)  
        
        Delete messages on behalf of a business account. Requires the *can\\_delete\\_sent\\_messages* business bot right to delete messages sent by the bot itself, or the *can\\_delete\\_all\\_messages* business bot right to delete any message. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_business_account_name(
        self,
        business_connection_id: str,
        first_name: str,
        *,
        last_name: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setBusinessAccountName](https://core.telegram.org/bots/api#setbusinessaccountname)  
        
        Changes the first and last name of a managed business account. Requires the *can\\_change\\_name* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_business_account_username(
        self,
        business_connection_id: str,
        *,
        username: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setBusinessAccountUsername](https://core.telegram.org/bots/api#setbusinessaccountusername)  
        
        Changes the username of a managed business account. Requires the *can\\_change\\_username* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_business_account_bio(
        self,
        business_connection_id: str,
        *,
        bio: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setBusinessAccountBio](https://core.telegram.org/bots/api#setbusinessaccountbio)  
        
        Changes the bio of a managed business account. Requires the *can\\_change\\_bio* business bot right. Returns *True* on success.
        """

    @api_method_wrapper(check_input_media={"photo": ["animation", "photo"]})
    def set_business_account_profile_photo(
        self,
        business_connection_id: str,
        photo: tg.InputProfilePhoto,
        *,
        is_public: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setBusinessAccountProfilePhoto](https://core.telegram.org/bots/api#setbusinessaccountprofilephoto)  
        
        Changes the profile photo of a managed business account. Requires the *can\\_edit\\_profile\\_photo* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def remove_business_account_profile_photo(
        self,
        business_connection_id: str,
        *,
        is_public: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [removeBusinessAccountProfilePhoto](https://core.telegram.org/bots/api#removebusinessaccountprofilephoto)  
        
        Removes the current profile photo of a managed business account. Requires the *can\\_edit\\_profile\\_photo* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_business_account_gift_settings(
        self,
        business_connection_id: str,
        show_gift_button: bool,
        accepted_gift_types: tg.AcceptedGiftTypes
    ) -> Task[t.Literal[True]]:
        """
        ### [setBusinessAccountGiftSettings](https://core.telegram.org/bots/api#setbusinessaccountgiftsettings)  
        
        Changes the privacy settings pertaining to incoming gifts in a managed business account. Requires the *can\\_change\\_gift\\_settings* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_business_account_star_balance(self, business_connection_id: str) -> Task[tg.StarAmount]:
        """
        ### [getBusinessAccountStarBalance](https://core.telegram.org/bots/api#getbusinessaccountstarbalance)  
        
        Returns the amount of Telegram Stars owned by a managed business account. Requires the *can\\_view\\_gifts\\_and\\_stars* business bot right. Returns [StarAmount](https://core.telegram.org/bots/api#staramount) on success.
        """

    @api_method_wrapper()
    def transfer_business_account_stars(
        self,
        business_connection_id: str,
        star_count: int
    ) -> Task[t.Literal[True]]:
        """
        ### [transferBusinessAccountStars](https://core.telegram.org/bots/api#transferbusinessaccountstars)  
        
        Transfers Telegram Stars from the business account balance to the bot's balance. Requires the *can\\_transfer\\_stars* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def get_business_account_gifts(
        self,
        business_connection_id: str,
        *,
        exclude_unsaved: bool | None = None,
        exclude_saved: bool | None = None,
        exclude_unlimited: bool | None = None,
        exclude_limited: bool | None = None,
        exclude_unique: bool | None = None,
        sort_by_price: bool | None = None,
        offset: str | None = None,
        limit: int | None = None
    ) -> Task[tg.OwnedGifts]:
        """
        ### [getBusinessAccountGifts](https://core.telegram.org/bots/api#getbusinessaccountgifts)  
        
        Returns the gifts received and owned by a managed business account. Requires the *can\\_view\\_gifts\\_and\\_stars* business bot right. Returns [OwnedGifts](https://core.telegram.org/bots/api#ownedgifts) on success.
        """

    @api_method_wrapper()
    def convert_gift_to_stars(
        self,
        business_connection_id: str,
        owned_gift_id: str
    ) -> Task[t.Literal[True]]:
        """
        ### [convertGiftToStars](https://core.telegram.org/bots/api#convertgifttostars)  
        
        Converts a given regular gift to Telegram Stars. Requires the *can\\_convert\\_gifts\\_to\\_stars* business bot right. Returns *True* on success.
        """

    @api_method_wrapper()
    def upgrade_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        *,
        keep_original_details: bool | None = None,
        star_count: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [upgradeGift](https://core.telegram.org/bots/api#upgradegift)  
        
        Upgrades a given regular gift to a unique gift. Requires the *can\\_transfer\\_and\\_upgrade\\_gifts* business bot right. Additionally requires the *can\\_transfer\\_stars* business bot right if the upgrade is paid. Returns *True* on success.
        """

    @api_method_wrapper()
    def transfer_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        new_owner_chat_id: int,
        *,
        star_count: int | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [transferGift](https://core.telegram.org/bots/api#transfergift)  
        
        Transfers an owned unique gift to another user. Requires the *can\\_transfer\\_and\\_upgrade\\_gifts* business bot right. Requires *can\\_transfer\\_stars* business bot right if the transfer is paid. Returns *True* on success.
        """

    @api_method_wrapper(check_input_media={"content": ["video", "photo"]})
    def post_story(
        self,
        business_connection_id: str,
        content: tg.InputStoryContent,
        active_period: int,
        *,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        areas: list[tg.StoryArea] | None = None,
        post_to_chat_page: bool | None = None,
        protect_content: bool | None = None
    ) -> Task[tg.Story]:
        """
        ### [postStory](https://core.telegram.org/bots/api#poststory)  
        
        Posts a story on behalf of a managed business account. Requires the *can\\_manage\\_stories* business bot right. Returns [Story](https://core.telegram.org/bots/api#story) on success.
        """

    @api_method_wrapper(check_input_media={"content": ["video", "photo"]})
    def edit_story(
        self,
        business_connection_id: str,
        story_id: int,
        content: tg.InputStoryContent,
        *,
        caption: str | None = None,
        parse_mode: t.Literal["HTML", "Markdown", "MarkdownV2"] | None = None,
        caption_entities: list[tg.MessageEntity] | None = None,
        areas: list[tg.StoryArea] | None = None
    ) -> Task[tg.Story]:
        """
        ### [editStory](https://core.telegram.org/bots/api#editstory)  
        
        Edits a story previously posted by the bot on behalf of a managed business account. Requires the *can\\_manage\\_stories* business bot right. Returns [Story](https://core.telegram.org/bots/api#story) on success.
        """

    @api_method_wrapper()
    def delete_story(
        self,
        business_connection_id: str,
        story_id: int
    ) -> Task[t.Literal[True]]:
        """
        ### [deleteStory](https://core.telegram.org/bots/api#deletestory)  
        
        Deletes a story previously posted by the bot on behalf of a managed business account. Requires the *can\\_manage\\_stories* business bot right. Returns *True* on success.
        
        The following methods and objects allow your bot to handle stickers and sticker sets.
        """

    @api_method_wrapper(check_input_files=["sticker"])
    def send_sticker(
        self,
        chat_id: int | str,
        sticker: Path | bytes | tg.InputFile | str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        emoji: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.ForceReply | tg.ReplyKeyboardRemove | tg.ReplyKeyboardMarkup | tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendSticker](https://core.telegram.org/bots/api#sendsticker)  
        
        Use this method to send static .WEBP, [animated](https://telegram.org/blog/animated-stickers) .TGS, or [video](https://telegram.org/blog/video-stickers-better-reactions) .WEBM stickers. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def get_sticker_set(self, name: str) -> Task[tg.StickerSet]:
        """
        ### [getStickerSet](https://core.telegram.org/bots/api#getstickerset)  
        
        Use this method to get a sticker set. On success, a [StickerSet](https://core.telegram.org/bots/api#stickerset) object is returned.
        """

    @api_method_wrapper()
    def get_custom_emoji_stickers(self, custom_emoji_ids: list[str]) -> Task[list[tg.Sticker]]:
        """
        ### [getCustomEmojiStickers](https://core.telegram.org/bots/api#getcustomemojistickers)  
        
        Use this method to get information about custom emoji stickers by their identifiers. Returns an Array of [Sticker](https://core.telegram.org/bots/api#sticker) objects.
        """

    @api_method_wrapper(check_input_files=["sticker"])
    def upload_sticker_file(
        self,
        user_id: int,
        sticker: Path | bytes | tg.InputFile,
        sticker_format: literals.StickerFormat
    ) -> Task[tg.File]:
        """
        ### [uploadStickerFile](https://core.telegram.org/bots/api#uploadstickerfile)  
        
        Use this method to upload a file with a sticker for later use in the [createNewStickerSet](https://core.telegram.org/bots/api#createnewstickerset), [addStickerToSet](https://core.telegram.org/bots/api#addstickertoset), or [replaceStickerInSet](https://core.telegram.org/bots/api#replacestickerinset) methods (the file can be used multiple times). Returns the uploaded [File](https://core.telegram.org/bots/api#file) on success.
        """

    @api_method_wrapper(check_input_media={"stickers": ["sticker"]})
    def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: list[tg.InputSticker],
        *,
        sticker_type: str | None = None,
        needs_repainting: bool | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [createNewStickerSet](https://core.telegram.org/bots/api#createnewstickerset)  
        
        Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. Returns *True* on success.
        """

    @api_method_wrapper(check_input_media={"sticker": ["sticker"]})
    def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: tg.InputSticker
    ) -> Task[t.Literal[True]]:
        """
        ### [addStickerToSet](https://core.telegram.org/bots/api#addstickertoset)  
        
        Use this method to add a new sticker to a set created by the bot. Emoji sticker sets can have up to 200 stickers. Other sticker sets can have up to 120 stickers. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int
    ) -> Task[t.Literal[True]]:
        """
        ### [setStickerPositionInSet](https://core.telegram.org/bots/api#setstickerpositioninset)  
        
        Use this method to move a sticker in a set created by the bot to a specific position. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_sticker_from_set(self, sticker: str) -> Task[t.Literal[True]]:
        """
        ### [deleteStickerFromSet](https://core.telegram.org/bots/api#deletestickerfromset)  
        
        Use this method to delete a sticker from a set created by the bot. Returns *True* on success.
        """

    @api_method_wrapper(check_input_media={"sticker": ["sticker"]})
    def replace_sticker_in_set(
        self,
        user_id: int,
        name: str,
        old_sticker: str,
        sticker: tg.InputSticker
    ) -> Task[t.Literal[True]]:
        """
        ### [replaceStickerInSet](https://core.telegram.org/bots/api#replacestickerinset)  
        
        Use this method to replace an existing sticker in a sticker set with a new one. The method is equivalent to calling [deleteStickerFromSet](https://core.telegram.org/bots/api#deletestickerfromset), then [addStickerToSet](https://core.telegram.org/bots/api#addstickertoset), then [setStickerPositionInSet](https://core.telegram.org/bots/api#setstickerpositioninset). Returns *True* on success.
        """

    @api_method_wrapper()
    def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: list[str]
    ) -> Task[t.Literal[True]]:
        """
        ### [setStickerEmojiList](https://core.telegram.org/bots/api#setstickeremojilist)  
        
        Use this method to change the list of emoji assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_sticker_keywords(
        self,
        sticker: str,
        *,
        keywords: list[str] | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setStickerKeywords](https://core.telegram.org/bots/api#setstickerkeywords)  
        
        Use this method to change search keywords assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_sticker_mask_position(
        self,
        sticker: str,
        *,
        mask_position: tg.MaskPosition | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setStickerMaskPosition](https://core.telegram.org/bots/api#setstickermaskposition)  
        
        Use this method to change the [mask position](https://core.telegram.org/bots/api#maskposition) of a mask sticker. The sticker must belong to a sticker set that was created by the bot. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_sticker_set_title(
        self,
        name: str,
        title: str
    ) -> Task[t.Literal[True]]:
        """
        ### [setStickerSetTitle](https://core.telegram.org/bots/api#setstickersettitle)  
        
        Use this method to set the title of a created sticker set. Returns *True* on success.
        """

    @api_method_wrapper(check_input_files=["thumbnail"])
    def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        format: literals.StickerFormat,
        *,
        thumbnail: Path | bytes | tg.InputFile | str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setStickerSetThumbnail](https://core.telegram.org/bots/api#setstickersetthumbnail)  
        
        Use this method to set the thumbnail of a regular or mask sticker set. The format of the thumbnail file must match the format of the stickers in the set. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        *,
        custom_emoji_id: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [setCustomEmojiStickerSetThumbnail](https://core.telegram.org/bots/api#setcustomemojistickersetthumbnail)  
        
        Use this method to set the thumbnail of a custom emoji sticker set. Returns *True* on success.
        """

    @api_method_wrapper()
    def delete_sticker_set(self, name: str) -> Task[t.Literal[True]]:
        """
        ### [deleteStickerSet](https://core.telegram.org/bots/api#deletestickerset)  
        
        Use this method to delete a sticker set that was created by the bot. Returns *True* on success.
        
        The following methods and objects allow your bot to work in [inline mode](https://core.telegram.org/bots/inline).  
        Please see our [Introduction to Inline bots](https://core.telegram.org/bots/inline) for more details.
        
        To enable this option, send the `/setinline` command to [@BotFather](https://t.me/botfather) and provide the placeholder text that the user will see in the input field after typing your bot's name.
        """

    @api_method_wrapper()
    def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[tg.InlineQueryResult],
        *,
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        button: tg.InlineQueryResultsButton | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [answerInlineQuery](https://core.telegram.org/bots/api#answerinlinequery)  
        
        Use this method to send answers to an inline query. On success, *True* is returned.  
        No more than **50** results per query are allowed.
        """

    @api_method_wrapper()
    def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: tg.InlineQueryResult
    ) -> Task[tg.SentWebAppMessage]:
        """
        ### [answerWebAppQuery](https://core.telegram.org/bots/api#answerwebappquery)  
        
        Use this method to set the result of an interaction with a [Web App](https://core.telegram.org/bots/webapps) and send a corresponding message on behalf of the user to the chat from which the query originated. On success, a [SentWebAppMessage](https://core.telegram.org/bots/api#sentwebappmessage) object is returned.
        """

    @api_method_wrapper()
    def save_prepared_inline_message(
        self,
        user_id: int,
        result: tg.InlineQueryResult,
        *,
        allow_user_chats: bool | None = None,
        allow_bot_chats: bool | None = None,
        allow_group_chats: bool | None = None,
        allow_channel_chats: bool | None = None
    ) -> Task[tg.PreparedInlineMessage]:
        """
        ### [savePreparedInlineMessage](https://core.telegram.org/bots/api#savepreparedinlinemessage)  
        
        Stores a message that can be sent by a user of a Mini App. Returns a [PreparedInlineMessage](https://core.telegram.org/bots/api#preparedinlinemessage) object.
        """

    @api_method_wrapper()
    def send_invoice(
        self,
        chat_id: int | str,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[tg.LabeledPrice],
        *,
        message_thread_id: int | None = None,
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        start_parameter: str | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendInvoice](https://core.telegram.org/bots/api#sendinvoice)  
        
        Use this method to send invoices. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[tg.LabeledPrice],
        *,
        business_connection_id: str | None = None,
        provider_token: str | None = None,
        subscription_period: int | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None
    ) -> Task[str]:
        """
        ### [createInvoiceLink](https://core.telegram.org/bots/api#createinvoicelink)  
        
        Use this method to create a link for an invoice. Returns the created invoice link as *String* on success.
        """

    @api_method_wrapper()
    def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        *,
        shipping_options: list[tg.ShippingOption] | None = None,
        error_message: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [answerShippingQuery](https://core.telegram.org/bots/api#answershippingquery)  
        
        If you sent an invoice requesting a shipping address and the parameter *is\\_flexible* was specified, the Bot API will send an [Update](https://core.telegram.org/bots/api#update) with a *shipping\\_query* field to the bot. Use this method to reply to shipping queries. On success, *True* is returned.
        """

    @api_method_wrapper()
    def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        *,
        error_message: str | None = None
    ) -> Task[t.Literal[True]]:
        """
        ### [answerPreCheckoutQuery](https://core.telegram.org/bots/api#answerprecheckoutquery)  
        
        Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an [Update](https://core.telegram.org/bots/api#update) with the field *pre\\_checkout\\_query*. Use this method to respond to such pre\\-checkout queries. On success, *True* is returned. **Note:** The Bot API must receive an answer within 10 seconds after the pre\\-checkout query was sent.
        """

    @api_method_wrapper()
    def get_star_transactions(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None
    ) -> Task[tg.StarTransactions]:
        """
        ### [getStarTransactions](https://core.telegram.org/bots/api#getstartransactions)  
        
        Returns the bot's Telegram Star transactions in chronological order. On success, returns a [StarTransactions](https://core.telegram.org/bots/api#startransactions) object.
        """

    @api_method_wrapper()
    def refund_star_payment(
        self,
        user_id: int,
        telegram_payment_charge_id: str
    ) -> Task[t.Literal[True]]:
        """
        ### [refundStarPayment](https://core.telegram.org/bots/api#refundstarpayment)  
        
        Refunds a successful payment in [Telegram Stars](https://t.me/BotNews/90). Returns *True* on success.
        """

    @api_method_wrapper()
    def edit_user_star_subscription(
        self,
        user_id: int,
        telegram_payment_charge_id: str,
        is_canceled: bool
    ) -> Task[t.Literal[True]]:
        """
        ### [editUserStarSubscription](https://core.telegram.org/bots/api#edituserstarsubscription)  
        
        Allows the bot to cancel or re\\-enable extension of a subscription paid in Telegram Stars. Returns *True* on success.
        """

    @api_method_wrapper()
    def set_passport_data_errors(
        self,
        user_id: int,
        errors: list[tg.PassportElementError]
    ) -> Task[t.Literal[True]]:
        """
        ### [setPassportDataErrors](https://core.telegram.org/bots/api#setpassportdataerrors)  
        
        Informs a user that some of the Telegram Passport elements they provided contains errors. The user will not be able to re\\-submit their Passport to you until the errors are fixed (the contents of the field for which you returned the error must change). Returns *True* on success.
        
        Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason. For example, if a birthday date seems invalid, a submitted document is blurry, a scan shows evidence of tampering, etc. Supply some details in the error message to make sure the user knows how to correct the issues.
        """

    @api_method_wrapper()
    def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        *,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: tg.ReplyParameters | None = None,
        reply_markup: tg.InlineKeyboardMarkup | None = None
    ) -> Task[tg.Message]:
        """
        ### [sendGame](https://core.telegram.org/bots/api#sendgame)  
        
        Use this method to send a game. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.
        """

    @api_method_wrapper()
    def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        force: bool | None = None,
        disable_edit_message: bool | None = None,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None
    ) -> Task[tg.Message | t.Literal[True]]:
        """
        ### [setGameScore](https://core.telegram.org/bots/api#setgamescore)  
        
        Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the [Message](https://core.telegram.org/bots/api#message) is returned, otherwise *True* is returned. Returns an error, if the new score is not greater than the user's current score in the chat and *force* is *False*.
        """

    @api_method_wrapper()
    def get_game_high_scores(
        self,
        user_id: int,
        *,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None
    ) -> Task[list[tg.GameHighScore]]:
        """
        ### [getGameHighScores](https://core.telegram.org/bots/api#getgamehighscores)  
        
        Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. Returns an Array of [GameHighScore](https://core.telegram.org/bots/api#gamehighscore) objects.
        
        > This method will currently return scores for the target user, plus two of their closest neighbors on each side. Will also return the top three users if the user and their neighbors are not among them. Please note that this behavior is subject to change.
        """


