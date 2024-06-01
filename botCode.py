import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from ec2_metadata import ec2_metadata

# Load environment variables from secret.env file.
load_dotenv('secret.env')

# Request the necessary intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent
intents.presences = True  # Enable the presence intent if needed

# Initialize the bot with these intents
client = commands.Bot(command_prefix='!', intents=intents)

# Access the environment variable for the bot token
token = str(os.getenv('CHAT_BOT_TOKEN'))

@client.event
async def on_ready():
    """
    Event triggered when the bot is successfully logged in and ready to start processing events.
    """
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    """
    Event triggered whenever a message is sent in any server the bot is connected to.
    """
    username = str(message.author).split("#")[0]  # Extract username from message author's name
    channel = str(1245794405349068800)  # ID of the channel where the bot will respond
    user_message = str(message.content)  # Extract the content of the message

    print(f'Message from {username} in {channel}: {user_message}')  # Log the message received

    if message.author == client.user:
        return  # Ignore messages sent by the bot itself

    if channel == "1245794405349068800":
        # If the message is sent in the specified channel and is "hello", respond with a greeting
        if user_message.lower() == "hello":
            await message.channel.send(f'Hello {username}!')
            await message.channel.send(f"Sooner! {username} Your EC2 Data: {ec2_metadata.region}")
            return

client.run(token)  # Run the bot with the provided token
