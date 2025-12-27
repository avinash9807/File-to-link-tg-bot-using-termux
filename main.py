from telethon import TelegramClient, events
from aiohttp import web
import asyncio
import os
# Config file ko import kar rahe hain
import config 

client = TelegramClient('local_bot_session', config.API_ID, config.API_HASH)

async def stream_handler(request):
    try:
        peer = int(request.match_info['peer'])
        msg_id = int(request.match_info['msg_id'])
        
        if peer not in config.OWNERS:
            return web.Response(text="Access Denied!", status=403)
            
        msg = await client.get_messages(peer, ids=msg_id)
        file_size = msg.file.size
        file_name = msg.file.name or "file"

        range_header = request.headers.get('Range')
        start = 0
        if range_header:
            start = int(range_header.replace('bytes=', '').split('-')[0])

        resp = web.StreamResponse(status=206 if range_header else 200)
        resp.headers['Content-Type'] = 'application/octet-stream'
        resp.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
        resp.headers['Accept-Ranges'] = 'bytes'
        resp.headers['Content-Range'] = f'bytes {start}-{file_size-1}/{file_size}'
        resp.content_length = file_size - start
        
        await resp.prepare(request)

        async for chunk in client.iter_download(msg.media, offset=start):
            await resp.write(chunk)
            
        return resp
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(text="Error occurred", status=500)

app = web.Application()
app.router.add_get('/dl/{peer}/{msg_id}', stream_handler)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.sender_id in config.OWNERS:
        await event.reply("Welcome Back, **Avinash Chauhan**! 🚀\n\nMain active hoon. Bas file forward karo.")
    else:
        await event.reply("Bhai, ye bot private hai.")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.media and event.sender_id in config.OWNERS and not event.message.text.startswith('/start'):
        link = f"http://127.0.0.1:8080/dl/{event.chat_id}/{event.message.id}"
        await event.reply(f"🚀 **Direct Link:**\n\n`{link}`")

async def main():
    await client.start(bot_token=config.BOT_TOKEN)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '127.0.0.1', 8080).start()
    print("✅ Bot is Online for Avinash Chauhan!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
  
