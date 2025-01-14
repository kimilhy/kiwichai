import asyncio
from datetime import datetime 
from pyrogram import Client, filters
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError
import random 
import os
from datetime import datetime

API_ID = 
API_HASH = 
TOKEN = 
CHARACTER_ID = 
TRIGGER_WORDS = []
IMAGE_TRIGGER_WORDS = []
IMAGE_FOLDER = 

app = Client("char_ai_userbot", api_id=API_ID, api_hash=API_HASH)

chat_cache = {"chat_id": None}

MODULES_STATE = {
    "character_ai": True,
    "random_image": True,
} 
async def get_characterai_client():
    client = await get_client(token=TOKEN)
    return client

from datetime import datetime

async def get_characterai_response(client, username, user_message):
    try:

        if chat_cache["chat_id"] is None:
            chat, _ = await client.chat.create_chat(CHARACTER_ID)
            chat_cache["chat_id"] = chat.chat_id

        current_time = datetime.now() 
        formatted_message = f"{username}, {current_time}, {user_message}"


        answer = await client.chat.send_message(CHARACTER_ID, chat_cache["chat_id"], formatted_message)

        return answer.get_primary_candidate().text
    except SessionClosedError:
        print("session closed")
        chat_cache["chat_id"] = None  
        return ""
    except Exception as e:
        print(f"error: {e}")
        return "error"
    
async def send_random_image(client, chat_id):
    try:
       
        image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]

      
        if not image_files:
            await client.send_message(chat_id=chat_id, text="кирил где картинки?!")
            return
        
        image_file = random.choice(image_files)

        image_path = os.path.join(IMAGE_FOLDER, image_file)
        await client.send_photo(chat_id=chat_id, photo=image_path, caption=":)")
    except Exception as e:
        print(f"not found pics: {e}")
        await client.send_message(chat_id=chat_id, text="no pic")

@app.on_message(filters.command(["on", "off"]) & ~filters.bot)
async def toggle_module(client, message):
    if len(message.command) < 2:
        await message.reply("?")
        return

    command = message.command[0] 
    module_name = message.command[1] 

    if module_name == "message":
        MODULES_STATE["character_ai"] = (command == "on")
        state = "" if command == "on" else ""
        await message.reply(f"{state}")
    elif module_name == "random image":
        MODULES_STATE["random_image"] = (command == "on")
        state = "" if command == "on" else ""
        await message.reply(f"{state}")
    else:
        await message.reply("not found module")

@app.on_message(filters.text & ~filters.bot)
async def handle_message(client, message):
    user_message = message.text
    username = message.from_user.username or "Unknown"
    bot_username = (await client.get_me()).username

  
    if MODULES_STATE["random_image"]:
        should_send_image = any(trigger_word in user_message.lower() for trigger_word in IMAGE_TRIGGER_WORDS)
        if should_send_image:
            print(f"{user_message}")
            await send_random_image(client, message.chat.id)
            return

    if MODULES_STATE["character_ai"]:
        should_respond = (
            any(trigger_word in user_message.lower() for trigger_word in TRIGGER_WORDS) or
            f"@{bot_username}" in user_message or
            (message.reply_to_message and message.reply_to_message.from_user.is_self)
        )

        if should_respond:
            ai_client = await get_characterai_client()
            print(f"get message: {username}: {user_message}")
            bot_response = await get_characterai_response(ai_client, username, user_message)
            await message.reply(bot_response)
            return

    print(f"ignored: {user_message}")

if __name__ == "__main__":
    app.run()
