import os
from typing import List, Optional

import discord

from documents import Message


async def create_msg_document(guild: discord.Guild, message: discord.Message):
    """Create a message document."""
    file_paths = await save_attachments(
        message.attachments, guild.id, message.channel.id, message.id
    )

    return Message(
        name=message.author.name,
        content=message.content,
        timestamp=message.created_at,
        message_id=message.id,
        channel_id=message.channel.id,
        attachments=file_paths if file_paths else None,
    )


async def save_attachments(
    attachments: List, guild_id: int, channel_id: int, message_id: int
) -> Optional[List[str]]:
    file_paths = []
    if attachments:
        for i, attachment in enumerate(attachments):

            if isinstance(attachment, discord.Attachment):
                original = getattr(attachment, "filename", None)

            if isinstance(attachment, dict):
                original = attachment.get("filename")

            if not original:
                continue

            original = original.split(".")

            file_name = (
                f"files/{guild_id}/{channel_id}/"
                f"{message_id}_{original[0]}_{i}.{original[1]}"
            )
            file_paths.append(file_name)
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            if isinstance(attachment, discord.Attachment):
                await attachment.save(file_name)

        return file_paths if file_paths else None
