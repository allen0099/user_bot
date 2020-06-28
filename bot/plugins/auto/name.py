import logging
import re
from typing import List

from pyrogram import Client, Message, Filters

from bot.plugins import LOG_CHANNEL
from models.chats import WithPermission
from models.check.Name import Name

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(Filters.chat(WithPermission.get()) & Filters.new_chat_members)
def name_check(cli: Client, msg: Message) -> None:
    full_name: str = f"{msg.from_user.first_name} {msg.from_user.last_name}"

    rules: List[str] = Name.get_rules()
    reply: str = f"Full Name: {full_name}\n"

    for rule in rules:
        result: re.Match = re.search(rule, full_name)
        log.debug(f"Checking rule: {rule}")
        if result is not None:
            match = result.group()
            reply += f"Rule: {rule}\n" \
                     f"Match: {match}\n"
            break

    cli.send_message(LOG_CHANNEL, reply)
