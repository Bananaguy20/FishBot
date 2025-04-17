import discord
from discord.ext import commands
import asyncio
import json
from pathlib import Path

# Configuration class to store excluded users
class BotConfig:
    def __init__(self):
        self.config_path = Path("config.json")
        self.config = self._load_config()
    
    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "excluded_users": []
        }
    
    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

# Initialize bot with configuration
config = BotConfig()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Sync commands when the bot starts
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f"Excluded users: {config.config['excluded_users']}")
    await bot.tree.sync()  # Sync commands globally
    print("Commands synced!")

# Slash command to exclude a user
@bot.tree.command(name="exclude", description="Exclude a user from fish reactions")
async def exclude(ctx, user: discord.Member):
    """Exclude a user from fish reactions."""
    user_id = user.id
    if user_id not in config.config["excluded_users"]:
        config.config["excluded_users"].append(user_id)
        config.save_config()
        await ctx.respond(f"Excluded {user.mention} from fish reactions")
    else:
        await ctx.respond(f"{user.mention} is already excluded")

# Slash command to include a user
@bot.tree.command(name="include", description="Include a user in fish reactions")
async def include(ctx, user: discord.Member):
    """Include a user in fish reactions."""
    user_id = user.id
    if user_id in config.config["excluded_users"]:
        config.config["excluded_users"].remove(user_id)
        config.save_config()
        await ctx.respond(f"Will now react to {user.mention}'s messages")
    else:
        await ctx.respond(f"{user.mention} is not excluded")

# Event to react to messages
@bot.event
async def on_message(message):
    try:
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return
        
        # Check if user is excluded
        if message.author.id in config.config["excluded_users"]:
            return
        
        # Add fish reaction to the message
        await message.add_reaction('🐟')
        
    except discord.Forbidden:
        print(f"Bot lacks permissions to react in {message.channel}")
    except discord.HTTPException as e:
        print(f"HTTP error while reacting: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the bot
TOKEN = 'NUH UH NOT FOR YOU'
bot.run(TOKEN)
