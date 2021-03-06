import html
import logging

import pyrogram
from pyrogram import Client, Filters, Message
from pyrogram.api import functions, types

from bot.plugins import COMMAND_PREFIX
from models import Users

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(Filters.user(Users.get()) &
                   Filters.command("getu", prefixes=COMMAND_PREFIX) &
                   Filters.reply)
def getu(cli: Client, msg: Message) -> None:
    user_id = getattr(msg.reply_to_message.forward_from, 'id', None) or \
              getattr(msg.reply_to_message.from_user, 'id', None) or \
              getattr(msg.from_user, 'id', None)
    api_user: types.UserFull = cli.send(
        functions.users.GetFullUser(
            id=cli.resolve_peer(user_id)
        )
    )
    pyro_user: pyrogram.User = cli.get_users(user_id)

    msg.reply_text(f"User ID: <code>{pyro_user.id}</code>\n"
                   f"User datacenter: <code>{pyro_user.dc_id}</code>\n"
                   f"First Name: <a href='tg://user?id={pyro_user.id}'>{html.escape(pyro_user.first_name)}</a>\n"
                   f"Last Name: <code>{html.escape(str(pyro_user.last_name))}</code>\n"
                   f"Username: @{pyro_user.username}\n"
                   f"Bio: \n<code>{html.escape(str(api_user.about))}</code>\n"
                   f"<code>===DETAIL===</code>\n"
                   f"Verified: <code>{pyro_user.is_verified}</code>\n"
                   f"Scam: <code>{pyro_user.is_scam}</code>\n"
                   f"Telegram support: <code>{pyro_user.is_support}</code>\n"
                   f"Can call: <code>{api_user.phone_calls_available}</code>\n")
