from typing import Union

from pyrogram import Client
from pyrogram.api import types, functions
from pyrogram.errors import PeerIdInvalid, UsernameInvalid


def get_full_user(cli: Client, cmd: str) -> Union[str, types.UserFull]:
    try:
        _user_full: types.UserFull = cli.send(
            functions.users.GetFullUser(
                id=cli.resolve_peer(cmd)
            )
        )
    except PeerIdInvalid as e:
        return str(e.CODE) + " " + e.ID
    except UsernameInvalid as e:
        return str(e.CODE) + " " + e.ID
    else:
        return _user_full
