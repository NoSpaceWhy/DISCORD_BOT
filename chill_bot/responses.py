from random import choice, randint
from collections import defaultdict
import asyncio  # Import asyncio to handle sleep and timers
from discord import Intents, Client, Message

# Initialize intents
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Initialize user coin storage
user_coin = defaultdict(int) # Defaulting to 0 coin for new users
monster_killed = False  # Flag to track if the monster has been killed

# for the game to get coins
async def respawn_monster():
    global monster_killed
    await asyncio.sleep(20)  # Wait for 10 seconds
    monster_killed = False  # Respawn the monster after 10 seconds
    print("The monster has respawned.")


def BET(user_coin, username):
    
    roll = randint(1,6)
    if roll == 1:
        user_coin += user_coin
        return f"You won your bet.\nNow your bank account is {user_coin[username]}"
    
    else:  
        user_coin -= user_coin
        return f"You lost your bet.\nNow your bank account is {user_coin[username]}"
    
    

def get_response(user_input: str, username: str,) -> str:
    global monster_killed
    global user_coin
    
    lowered: str = user_input.strip().lower()
    
    if not lowered:
        return "You didn't provide any input."

    if "hello" in lowered:
        return "Hello there! type help to know more"
    
    elif "roll dice" in lowered:
        return f"You rolled a {randint(1, 6)}."

    elif "help" in lowered:
        return "I can respond to commands like 'hello', 'roll dice', 'coin', 'kill monster'."

    elif "kill monster" in lowered:
        if monster_killed:
            return "The monster is already dead (it will respawn). You can try something else."
        else:
            # If the monster hasn't been killed yet, reward the player and mark the monster as dead.
            user_coin[username] += 100  # Reward 100 coin for killing the monster
            monster_killed = True
            # Start the respawn timer
            asyncio.create_task(respawn_monster())  # This will respawn the monster after 10 seconds
            return f"Congratulations {username}! You killed the monster and earned 100 coin. Your current balance is {user_coin[username]}."

    elif "coin" in lowered:
        return f"{username},The number of coins you have is {user_coin[username]}."
    
    elif "give" in lowered:
        user_coin[username] += 10000
        return f"{username} has been given 10,000 coins."
    
    elif "bet" in lowered:
        return f"You are going to bet all your money to get the double amount.\n {BET()}"
    
    else:
        return choice([
            "You can roll a dice.",
            "What did you say?",
            "Don't you have anything to talk about?",])
