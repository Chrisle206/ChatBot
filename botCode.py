import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from ec2_metadata import ec2_metadata

# Load environment variables from secret.env file.
load_dotenv('secret.env')

# Log the loaded environment variable for debugging
token = str(os.getenv('CHAT_BOT_TOKEN'))
print(f"Loaded bot token: {token}")

# Request the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
intents.members = True  # Enable the members intent if needed
intents.presences = True  # Enable the presence intent if needed

# Initialize the bot with these intents
client = commands.Bot(command_prefix='!', intents=intents)

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
    user_message = str(message.content)  # Extract the content of the message

    print(f'Message from {username} in {message.channel.name}: {user_message}')  # Log the message received

    if message.author == client.user:
        return  # Ignore messages sent by the bot itself

    # Find the channel where the bot should respond
    target_channel_name = "botchat"  # Replace with the actual name of the channel
    target_channel = discord.utils.get(message.guild.channels, name=target_channel_name)

    if target_channel and message.channel == target_channel:
        # If the message is sent in the specified channel and is "hello", respond with a greeting
        if user_message.lower() == "hello":
            await message.channel.send(f'Hello {username}!')
            try:
                ec2_region = ec2_metadata.region
                await message.channel.send(f"Sooner! {username} Your EC2 Data: {ec2_region}")
            except Exception as e:
                print(f"Error accessing EC2 metadata: {e}")
                await message.channel.send(f"Could not retrieve EC2 data: {e}")
            return

client.run(token)  # Run the bot with the provided token
