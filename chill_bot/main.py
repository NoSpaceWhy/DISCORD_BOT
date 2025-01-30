import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response  # Importing get_response from responses.py

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize intents
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

async def send_message(message: Message, user_message: str, is_command: bool) -> None:
    if not user_message:
        await message.channel.send("Your message was empty. Please provide input.")
        return
    
    try:
        if is_command:
            # Process command (prefixed with $)
            response = get_response(user_message, str(message.author))  # Pass the username
            await message.channel.send(response)
        else:
            # Do nothing for regular messages, just log them
            print(f"Received message from {message.author}: {user_message}")
    except Exception as e:
        print(f"Error: {e}")
        await message.channel.send("An error occurred while processing your message.")

@client.event
async def on_ready() -> None:
    print(f'{client.user} is running.')

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    user_message = message.content.strip()
    username = str(message.author)  # Extract username
    channel = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')

    if user_message.startswith('$'):
        # Handle command prefixed with $
        user_message = user_message[1:].strip()
        await send_message(message, user_message, is_command=True)
    else:
        # Do nothing for non-command messages, just record them
        await send_message(message, user_message, is_command=False)

def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
