#version 1.1

import asyncio
from pyrogram import Client, filters
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError
import g4f

#settings
API_ID = ""  
API_HASH = ""  
TOKEN = ""
CHARACTER_ID = ""  
TRIGGER_WORD = ""
G4F_TRIGGER = "" 
G4F_SYS_MESSAGE = "" 


app = Client("char_ai_userbot", api_id=API_ID, api_hash=API_HASH)
async def get_characterai_client():
    client = await get_client(token=TOKEN)
    return client
async def get_characterai_response(client, user_message):
    try:
        chat, greeting_message = await client.chat.create_chat(CHARACTER_ID)
        print(f"{greeting_message.author_name}: {greeting_message.get_primary_candidate().text}")
        answer = await client.chat.send_message(CHARACTER_ID, chat.chat_id, user_message)
        return answer.get_primary_candidate().text
    except SessionClosedError:
        print("Session closed.")
        return "session error!"
    except Exception as e:
        print(f"error: {e}")
        return "error"

async def get_g4f_response(user_message):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[
                {"role": "system", "content": G4F_SYS_MESSAGE},
                {"role": "user", "content": user_message},
            ],
        )
        return response
    except Exception as e:
        print(f"error G4F: {e}")
        return "error when ask GPT-4."
@app.on_message(filters.text & ~filters.bot)
async def handle_message(client, message):
    user_message = message.text
    chat_id = message.chat.id
    bot_username = (await client.get_me()).username 
    should_respond = (
        f"@{bot_username}" in user_message or  
        message.reply_to_message and message.reply_to_message.from_user.is_self or 
        TRIGGER_WORD.lower() in user_message.lower()  
    )
    if should_respond:
        print(f"get message from {message.from_user.username}: {user_message}")
        if G4F_TRIGGER.lower() in user_message.lower():
            bot_response = await get_g4f_response(user_message)
        else:
            ai_client = await get_characterai_client()
            bot_response = await get_characterai_response(ai_client, user_message)
        await message.reply(bot_response)
    else:
        print(f"ignored: {user_message}")
if __name__ == "__main__":
    app.run()
