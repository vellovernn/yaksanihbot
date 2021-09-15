import asyncio
import csv
import random
from asyncio import sleep
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserPrivacyRestrictedError,
    UserNotMutualContactError
)
from telethon.tl.functions.channels import (
    InviteToChannelRequest,
    EditBannedRequest,
    GetFullChannelRequest)
from telethon.tl.types import InputPeerUser, ChatBannedRights
from telethon.tl import functions
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError)

from userbot.events import register
from userbot import CMD_HELP


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await event.reply("`This is a private channel/group or I am banned from there`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Invalid channel/group`")
            return None
    return chat_info


@register(outgoing=True, pattern=r"^\.invtall(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        kimak = await event.reply("`peles wait cok...`")
    else:
        kimak = await event.edit("`peles wait cok..`")
    anakbabi = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await kimak.edit("`Maaf ler, bisa add orang disini`")
    s = 0
    f = 0
    error = 'None'

    await kimak.edit("**Duaaaar Memek**\n\Menculik Orang Ges ya.......`")
    async for user in event.client.iter_participants(anakbabi.full_chat.id):
        try:
            if error.startswith("Too"):
                return await kimak.edit(f"**Ooo asu limit**\n(`Error ya babi coba lagi nanti`)\n**Error** : \n`{error}`\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people")
            await event.client(functions.channels.InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await kimak.edit(f"**Penculikan Berjalan...**\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people\n\n**× LastError:** `{error}`")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await kimak.edit(f"**Penculikan Selesai** \n\n• Successfully Invited `{s}` people \n• failed to invite `{f}` people")


@register(outgoing=True, pattern=r"^\.getbabi$")
async def scrapmem(event):
    chat = event.chat_id
    await event.edit("`Tunggu Gesyaa...`")
    event.client
    members = await event.client.get_participants(chat, aggressive=True)

    with open("members.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(["user_id", "hash"])
        for member in members:
            writer.writerow([member.id, member.access_hash])
    await event.edit("`Anak Babi Terkumpul..`")


@register(outgoing=True, pattern=r"^\.addmemb$")
async def admem(event):
    await event.edit("`Proses Menambahkan 0 Babi...`")
    chat = await event.get_chat()
    event.client
    users = []
    with open("members.csv", encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {'id': int(row[0]), 'hash': int(row[1])}
            users.append(user)
    n = 0
    for user in users:
        n += 1
        if n % 30 == 0:
            await event.edit(f"`Mencapai 30 babi, tunggu gesyaa selama {900/60} menit`")
            await asyncio.sleep(900)
        try:
            userin = InputPeerUser(user['id'], user['hash'])
            await event.client(InviteToChannelRequest(chat, [userin]))
            await asyncio.sleep(random.randrange(5, 7))
            await event.edit(f"`Prosess Menambahkan {n} Babi...`")
        except TypeError:
            n -= 1
            continue
        except UserAlreadyParticipantError:
            n -= 1
            continue
        except UserPrivacyRestrictedError:
            n -= 1
            continue
        except UserNotMutualContactError:
            n -= 1
            continue


# Port By @VckyouuBitch From GeezProject
# Perkontolan Dengan Hapus Credits
@register(outgoing=True, pattern="^.musnahkan(?: |$)(.*)")
async def testing(event):
    nikal = await event.get_chat()
    chutiya = await event.client.get_me()
    admin = nikal.admin_rights
    creator = nikal.creator
    if not admin and not creator:
        await event.edit("Kau bukan admin ya babi")
        return
    await event.edit("Diam bngsat")
# Thank for Dark_Cobra
    everyone = await event.client.get_participants(event.chat_id)
    for user in everyone:
        if user.id == chutiya.id:
            pass
        try:
            await event.client(EditBannedRequest(event.chat_id, int(user.id), ChatBannedRights(until_date=None, view_messages=True)))
        except Exception as e:
            await event.edit(str(e))
        await sleep(.5)
    await event.edit("Kalem cok kalem")


CMD_HELP.update({
    "invtall":
        "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.inviteall groups username`\
          \n⚡ : __Scrapes users from the given chat to your group__."
})

CMD_HELP.update(
    {
        "allban": "**Plugin : **`allban`\
    \n\n**Syntax : **`.allban`\
    \n**Function : **ban all members in 1 cmnd"
    }
)

CMD_HELP.update({
    "anakbabi":
    "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.getmemb`\
   \nUsage : Mengumpulkan Babi dari Obrolan\
   \n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.addmemb`\
   \nUsage : Menambahkan Babi ke Obrolan\
   \nTata Cara Menggunakannya:  Pertama, Anda harus melakukan .getmemb terlebih dahulu dari Obrolan. Lalu buka grup Anda dan ketik .addmemb untuk menambahkan mereka ke grup Anda."
})
