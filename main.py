import asyncio
from pyrogram import Client, filters
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

# Настройки
API_ID = ""
API_HASH = ""
TOKEN = ""
CHARACTER_ID = "-"

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
        return "Ошибка сессии!"
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Произошла ошибка."

@app.on_message(filters.text & ~filters.bot)
async def handle_message(client, message):
    user_message = message.text
    chat_id = message.chat.id
    
    print(f"Получено сообщение от {message.from_user.username}: {user_message}")
   
    ai_client = await get_characterai_client()
    bot_response = await get_characterai_response(ai_client, user_message)
    await message.reply(bot_response)

if __name__ == "__main__":
    app.run()
