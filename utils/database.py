import os

import discord

from documents import Message


async def create_msg_document(guild: discord.Guild, message: discord.Message):
    """Create a message document."""
    file_paths = await save_attachments(guild, message)

    return Message(
        name=message.author.name,
        content=message.content,
        timestamp=message.created_at,
        message_id=message.id,
        channel_id=message.channel.id,
        attachments=file_paths if file_paths else None,
    )


async def save_attachments(guild, message):
    file_paths = []
    if message.attachments:
        for i, attachment in enumerate(message.attachments):
            original = attachment.filename.split(".")
            file_name = (
                f"files/{guild.id}/{message.channel.id}/"
                f"{message.id}_{original[0]}_{i}.{original[1]}"
            )
            file_paths.append(file_name)
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            await attachment.save(file_name)
    return file_paths
