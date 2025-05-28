import discord
from discord.ext import commands, tasks
from discord import Interaction
import datetime
from discord import Member
from discord.ext.commands import MissingPermissions
from discord.utils import get
from datetime import timedelta
from discord import app_commands
from discord.ui import View, Modal, TextInput
import asyncio
import enum
from re import A
import typing
from datetime import datetime, timedelta  # Correct import
from discord.utils import utcnow
import json
from discord.ui import View, Button
import random
import time
from pypresence import Presence
import os
import re
import logging
import aiohttp
import requests

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)


x = current_time = datetime.now()



#client info BELOW

#trigger words?

client = commands.Bot(command_prefix=".", intents= discord.Intents.all())
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content

#client info ABOVE

#activity=discord.activity.Streaming(name="Making Bnuy Take A Shower", url="https://www.youtube.com/watch?v=ZHWZf1Z4B5k"), 

# Store the start time when the bot begins its activity
start_time = time.time()

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')
    
    # Log the syncing process
    try:
        await client.tree.sync()  # Sync commands to Discord
        logging.info("Successfully synced commands to Discord.")
    except discord.errors.HTTPException as e:
        logging.error(f"HTTP error while syncing commands: {e}")
    except discord.errors.DiscordException as e:
        logging.error(f"Discord exception while syncing commands: {e}")
    except Exception as e:
        logging.error(f"Unknown error occurred while syncing commands: {e}")


    
    # set activity to say "Idle, Booting up ChillTaxiOs 1.30 ... Please wait" and then it says on DND "Watching Chill Taxi Community"
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Booting up ChillTaxiOs 1.30 ... Please wait"
        ),
        status=discord.Status.idle
    )
    await asyncio.sleep(10)
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Chill Taxi Community"
        ),
        status=discord.Status.dnd
    )
    logging.info("Bot is now online and ready to receive commands.")
    # Log the start time
    logging.info(f"Bot started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Start the periodic censorship task
    client.loop.create_task(periodic_censorship())







@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.modal_submit:
        print(f"Modal interaction: {interaction.data}")  # Debugging: Print modal interaction data




@client.command()
async def ping(ctx):
    bot_latency = round(client.latency*1000)
    embed = discord.Embed(title="Jerry Wifi", color=discord.Color.green(),description=f"Pong! my current latency is : {bot_latency}ms") 
    embed.set_thumbnail(url="https://static-00.iconduck.com/assets.00/wifi-icon-512x419-04r2eqe8.png")
    await ctx.channel.send(embed = embed)


# below are kick/ban/nickname commands

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member:discord.Member, *, reason = None):
    if reason == None:
        reason="no reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f"User {member.mention} has been kicked for {reason}")



@client.command()
@commands.has_permissions(ban_members=True)
async def bans(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "No reason provided"
    
    # Try banning the member
    try:
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"User {member.mention} has been banned for {reason}")
        print(f"Banned {member.name} for reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I do not have permission to ban this user.")
        print("The bot doesn't have permission to ban members.")
    except discord.HTTPException as e:
        await ctx.send("An error occurred while banning the user.")
        print(f"HTTP error occurred while banning: {e}")
    
    # Attempt to send a DM to the banned user
    try:
        await member.send(f"You have been banned from **{ctx.guild.name}**.\nReason: {reason}")
        print(f"Sent DM to {member.name} with reason: {reason}")
    except discord.Forbidden:
        # This error happens if the user has DMs disabled for the server
        print(f"Could not send DM to {member.name}. They have DMs disabled.")
    except discord.HTTPException as e:
        # In case of other HTTP exceptions (rate limits, etc.)
        print(f"HTTP error occurred while sending DM: {e}")



@client.command()
@commands.has_permissions(change_nickname= True)
async def nickname(ctx, member: discord.Member, nick):
    embed = discord.Embed(title=f"Nickname Changed for {member.global_name}", description="Made by bnuy")
    await member.edit(nick=nick)
    embed.add_field(name=f"New Nickname", value=f"{member.global_name} **nickname was changed to →** {member.display_name}", inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.channel.send(embed = embed)
    

# Past This Line is (/) Commands, above this message is (.) commands.

@client.tree.command(name="add_role", description="Add a role to a user")
@commands.has_permissions(manage_roles=True)
async def add_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    # Check if the bot has permission to manage roles
    if not interaction.guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message("I do not have permission to manage roles.", ephemeral=True)
        return

    # Check if the role is higher than the bot's highest role
    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("I cannot assign a role that is higher than my highest role.", ephemeral=True)
        return

    # Add the role to the member
    await member.add_roles(role)
    await interaction.response.send_message(f"**{role.name}** has been added to {member.mention}.", ephemeral=False)


@client.tree.command(name="ping", description="Shows Jerry's Wifi Speed")
async def ping(interaction : Interaction):
    bot_latency = round(client.latency*1000)
    await interaction.response.send_message(f"Pong!... {bot_latency}ms")

#Calculator

@client.tree.command(name="addcal" , description="Addition")
async def add(interaction : discord.Interaction, firstvalue: int, secondvalue: int):
    await interaction.response.send_message(f"{firstvalue} + {secondvalue} = {firstvalue+secondvalue}")

@client.tree.command(name="subcal" , description="Subtraction")
async def add(interaction : discord.Interaction, firstvalue: int, secondvalue: int):
    await interaction.response.send_message(f"{firstvalue} - {secondvalue} = {firstvalue-secondvalue}")


@client.tree.command(name="divisioncal" , description="Division")
async def add(interaction : discord.Interaction, firstvalue: int, secondvalue: int):
    await interaction.response.send_message(f"{firstvalue} / {secondvalue} = {firstvalue/secondvalue}")

@client.tree.command(name="multiplicationcal" , description="Multiplication")
async def add(interaction : discord.Interaction, firstvalue: int, secondvalue: int):
    await interaction.response.send_message(f"{firstvalue} x {secondvalue} = {firstvalue*secondvalue}")


#sync

@client.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 711284441166774302:
        await client.tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner of this bot to use this command!')

# end of sync
class TrickOrTreatView(View):
    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label="Trick or Treat 😈", style=discord.ButtonStyle.success)
    async def trick_or_treat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
         outcomes = [
            ("🍬 Treat!", "You got some delicious Halloween candy! Enjoy your sugar rush!"),
            ("👻 Trick!", "Boo! A ghost jumped out and scared you! Better luck next time."),
            ("🕷️ Trick!", "A spider fell on your head! Spooky!"),
            ("🍭 Treat!", "You found a rare glowing lollipop! Lucky you."),
            ("💀 Trick!", "A skeleton danced aggressively at you. It was awkward."),
            ("🎉 Treat!", "Someone gave you a full-sized candy bar! Jackpot!"),
            ("🧛‍♂️ Trick!", "A vampire tried to bite you, but you escaped!"),
            ("🎃 Treat!", "You found a pumpkin full of candy! Time to celebrate Halloween!"),
            ("👽 Trick!", "An alien tried to abduct you, but you managed to run away!"),
            ("🦇 Treat!", "A friendly bat gave you a piece of candy! How nice!"),
            ("🧙‍♀️ Trick!", "A witch tried to cast a spell on you, but you dodged it!"),
            ("👹 Treat!", "You found a treasure chest filled with candy!"),
            ("👺 Trick!", "A goblin tried to trick you, but you saw through it!"),
            ("🕸️ Treat!", "You found a web of candy! Sweet and sticky!"),
            ("🦄 Treat!", "A unicorn gave you a magical candy! It sparkles!"),
            ("🎃 Trick!", "A jack-o'-lantern scared you, but it was just a decoration!")
        ]
        title, message = random.choice(outcomes)
        embed = discord.Embed(title=title, description=message, color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.stop()

@client.tree.command(name="trick_or_treat", description="Halloween Trick or Treat")
async def trick_or_treat(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎃 Trick or Treat!",
        description="It's Halloween night... do you dare press the button?\nYou might get candy... or something *creepy*!",
        color=discord.Color.orange()
    )
    embed.set_footer(text="Happy Halloween! 👻")
    await interaction.response.send_message(embed=embed, view=TrickOrTreatView())

#info about

@client.tree.command(name="knowabout", description="Know more about your peers!")
async def buddyknower(interaction: discord.Interaction, *, member: discord.Member):
    # Collecting roles, excluding the @everyone role
    roles = [role for role in member.roles[1:]]
    
    # Creating the embed message
    embed = discord.Embed(
        title=f"👤 {member.name}",
        description=f"**Display Name:** {member.display_name}",
        color=discord.Color.random()  # Random color for a fresh look
    )

    # Adding fields with improved formatting
    embed.add_field(name="Is this user a bot? <:bot_1:1321542381664866394><:bot_2:1321542391085404251> ", value=f"{member.bot}", inline=False)
    embed.add_field(
        name=f"Has this user boosted the server? <a:nitro_boost:1321534490706837595>", 
        value=f"{'Yes' if member.premium_since else 'No'}", 
        inline=False
    )
    embed.add_field(
        name="Account Created On <:Calendar:1321541624123359352>", 
        value=member.created_at.strftime("%A, %B %d, %Y at %I:%M %p"), 
        inline=False
    )
    embed.add_field(
        name="Joined Server On 🐤", 
        value=member.joined_at.strftime("%A, %B %d, %Y at %I:%M %p"),
        inline=False
    )
    embed.add_field(name="User ID <:idCard:1321533298681450536>", value=f"`{member.id}`", inline=False)
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)
    
    # Adding the user's profile picture
    embed.set_thumbnail(url=member.avatar.url)

    # Sending the response
    await interaction.response.send_message(embed=embed)


#jazz that links to a random youtube video under the jazz category

@client.tree.command(name="jazz", description="Jazz up your day with some smooth tunes!")
async def jazz(interaction: discord.Interaction):
    jazz_videos = [
        "https://www.youtube.com/watch?v=MYPVQccHhAQ&pp=ygUEamF6eg%3D%3D",
        "https://www.youtube.com/watch?v=K110MtP_Mis&pp=ygUEamF6eg%3D%3D",
        "https://www.youtube.com/watch?v=A58iWc78M1A&pp=ygUEamF6eg%3D%3D"
    ]
    await interaction.response.send_message(random.choice(jazz_videos))

#kick

@client.tree.command(name="kick",description="-")
async def kick(interaction: discord.Interaction, *, member : discord.Member, reason:str):
        if interaction.user.id == 711284441166774302:
            await interaction.guild.kick(member)
        embed = discord.Embed(title=f"{member.global_name} has been kicked!")
        embed.add_field(name="reason", value=f">>> {reason}")
        embed.set_thumbnail(url=member.avatar._url)
        await interaction.response.send_message(embed=embed)


#ban

# Helper function to log banned users to the bannedusers.json file
def log_ban_to_json(user, reason, appeal, duration):
    try:
        with open('bannedusers.json', 'r') as f:
            banned_users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        banned_users = []

    ban_record = {
        "discord_name": str(user),
        "discord_id": str(user.id),
        "reason": reason,
        "appeal": appeal,
        "duration": duration,
        "timestamp": str(datetime.now())
    }

    banned_users.append(ban_record)

    with open('bannedusers.json', 'w') as f:
        json.dump(banned_users, f, indent=4)

# Slash Command to Ban a User
# Helper function to log banned users to the bannedusers.json file
def log_ban_to_json(user, reason, appeal, duration):
    try:
        with open('bannedusers.json', 'r') as f:
            banned_users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        banned_users = []

    ban_record = {
        "discord_name": str(user),
        "discord_id": str(user.id),
        "reason": reason,
        "appeal": appeal,
        "duration": duration,
        "timestamp": str(datetime.now())
    }

    banned_users.append(ban_record)

    with open('bannedusers.json', 'w') as f:
        json.dump(banned_users, f, indent=4)

# Slash Command to Ban a User
@client.tree.command(name="ban", description="Ban a user from the server.")
@app_commands.describe(user="The user to ban", reason="Reason for banning", appeal="Appeal status (Yes/No)", duration="Duration of the ban in days (optional)")
async def ban(interaction: discord.Interaction, user: discord.User, reason: str, appeal: str, duration: str = None):
    # Check if the user has permission to ban members
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("You do not have permission to ban members.", ephemeral=True)
        return

    # Parse the duration if provided
    end_time = None
    if duration:
        try:
            days = int(duration)
            if days <= 0:
                raise ValueError("Duration must be a positive number.")
            end_time = datetime.now() + timedelta(days=days)
        except ValueError:
            await interaction.response.send_message("Invalid duration. Please provide a valid number of days.", ephemeral=True)
            return

    # Send a message to the banned user with the reason and duration
    embed = discord.Embed(
        title="You've been banned",
        description=f"**Reason**: {reason}\n**Duration**: {duration if duration else 'Permanent'}",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Appeal", value="<:check_yes:1321576988384694323> Able To Appeal" if appeal.lower() == "yes" else "<:check_no:1321577002892787732> No Appeal")

    try:
        await user.send(embed=embed)  # Attempt to DM the banned user
    except discord.Forbidden:
        print(f"Could not DM {user.name}, they may have DMs disabled.")

    # Log the ban to the bannedusers.json file
    log_ban_to_json(user, reason, appeal, duration)

    # Send an embed to the channel where the command was run
    embed_channel = discord.Embed(
        title=f"{user.name} has been banned!",
        description=f"Banned by {interaction.user.name}\n**Reason**: {reason}\n**Duration**: {duration if duration else 'Permanent'}",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed_channel.set_thumbnail(url=user.avatar.url)
    embed_channel.add_field(name="Appeal", value="<:check_yes:1321576988384694323> Able To Appeal" if appeal.lower() == "yes" else "<:check_no:1321577002892787732> No Appeal")

    # Confirm the action to the user who initiated the command
    await interaction.response.send_message(f"Banned {user.name} successfully. Sending ban details...", ephemeral=True)

    # Send the embed to the channel where the slash command was run
    await interaction.channel.send(embed=embed_channel)

    # Ban the user from the server
    await interaction.guild.ban(user, reason=reason, delete_message_days=0)

    # If there is a temporary ban, unban the user after the specified duration
    if end_time:
        await asyncio.sleep((end_time - datetime.now()).total_seconds())  # Sleep until the ban should end
        await interaction.guild.unban(user)  # Unban the user after the duration

#sees edits
# Simple regex pattern to match words that could be considered offensive.
# Added the N-word here to be censored.
BAD_WORDS_REGEX = r'\b(?:[fF][uU][cC][kK]|[sS][hH][iI][tT]|[bB][iI][tT][cC][hH]|[aA][sS][sS]|[nN]\s?[iI]\s?[gG]\s?[gG]\s?[aA]\s?[rR]|[nN]\s?[iI]\s?[gG]\s?[gG]\s?[aA]\s?[eE])\b'

def censor_text(text: str) -> str:
    """
    This function censors bad words from the input text using a regex pattern.
    It replaces each bad word with asterisks (*****).
    """
    # Replace the bad words with "*****" using regex
    text = re.sub(BAD_WORDS_REGEX, '*****', text, flags=re.IGNORECASE)
    return text

def censor_log_file():
    """
    This function reads the log file, censors any bad words, and writes the updated content back to the file.
    """
    try:
        # Read the current contents of the log file
        with open("logtext.txt", "r", encoding="utf-8") as file:
            log_content = file.read()

        # Censor the bad words in the entire content
        censored_content = censor_text(log_content)

        # Overwrite the log file with the censored content
        with open("logtext.txt", "w", encoding="utf-8") as file:
            file.write(censored_content)

    except FileNotFoundError:
        print("logtext.txt not found.")
    except Exception as e:
        print(f"Error occurred while censoring log file: {e}")

@client.event
async def on_message_edit(before, after):
    # Ensure the event only logs if the message actually changes
    if before.content != after.content:
        await asyncio.sleep(2)
        
        # Censor the bad words from the 'before' and 'after' message content for the log file
        censored_before = censor_text(before.content)
        censored_after = censor_text(after.content)
        
        # Assuming x is already set with the time (could be anything, here just using {x} as placeholder)
        x = "2024-11-09 12:34:56 UTC"  # This would be the actual time or timestamp you want to use

        # Log message for file (censored)
        log_message = f"📝 Message edited in {before.channel} by {before.author}: Before: {censored_before} | After: {censored_after} | Time: {x}"

        # Open the log file and append the message
        with open("logtext.txt", "a", encoding="utf-8") as file:
            file.write(log_message + "\n")  # Ensure the message ends with a newline for separation
        
        # Print the uncensored message to the console
        print(f"📝 Message edited in {before.channel} by {before.author}: Before: {before.content} | After: {after.content} | Time: {x}")

@client.listen('on_message')
async def whatever_you_want_to_call_it(message):
    await asyncio.sleep(1)
    
    # Censor the bad words in the message content for the log file
    censored_message = censor_text(message.content)
    

    # Log message for file (censored)
    log_message = f"💬 Message from {message.author} in {message.channel}: {censored_message} | Time: {x}"

    # Open the log file and append the message
    with open("logtext.txt", "a", encoding="utf-8") as file:
        file.write(log_message + "\n")  # Ensure the message ends with a newline for separation
    
    # Print the uncensored message to the console
    print(f"💬 Message from {message.author} in {message.channel}: {message.content} | Time: {x}")

# Example of how you might periodically call the `censor_log_file` function
# You can call this function in your bot's code when needed (e.g., on startup, periodically, or after certain events)
async def periodic_censorship():
    # Let's say we want to run this function periodically every 10 minutes:
    await asyncio.sleep(120)  # 600 seconds = 10 minutes
    censor_log_file()
    print("Checked and censored the log file.")


# File to store warnings
WARNINGS_FILE = "warnings.json"

# Load warnings from file
try:
    with open(WARNINGS_FILE, "r") as file:
        warnings_db = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    warnings_db = {}  # Initialize as an empty dictionary if file is missing or corrupted

# Function to save warnings to file
def save_warnings():
    with open(WARNINGS_FILE, "w") as file:
        json.dump(warnings_db, file, indent=4)


# Slash command to issue a warning
@client.tree.command(name="warn", description="Issue a warning to a user")
@app_commands.default_permissions(administrator=True)
async def warn(interaction: discord.Interaction, user: discord.User, reason: str):
    # Check if the user already has warnings
    if str(user.id) not in warnings_db:
        warnings_db[str(user.id)] = []

    # Add the warning
    warnings_db[str(user.id)].append(reason)
    save_warnings()  # Save to file

    # Create an embed for the warning message
    embed = discord.Embed(
        title="You Have Been Warned!",
        description=f"Reason: {reason}",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.avatar.url)

    await interaction.response.send_message(embed=embed)

    try:
        # Notify the user via DM
        await user.send(embed=embed)
        # Notify in the server
        await interaction.response.send_message(
            f"{user.mention} has been warned for: {reason}",
            ephemeral=False
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            f"Could not send a DM to {user.mention}. They might have DMs disabled.",
            ephemeral=True
        )

# Slash command to remove warnings
@client.tree.command(name="removewarn", description="Remove warnings from a user")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    user="The user whose warnings you want to remove.",
    index="The warning index to remove (leave blank to remove all warnings)."
)
async def removewarn(interaction: discord.Interaction, user: discord.User, index: int = None):
    user_id = str(user.id)

    # Check if the user has warnings
    if user_id not in warnings_db or len(warnings_db[user_id]) == 0:
        await interaction.response.send_message(
            f"{user.mention} has no warnings to remove.",
            ephemeral=True
        )
        return

    if index is None:
        # Remove all warnings
        warnings_db[user_id].clear()
        save_warnings()  # Save changes
        await interaction.response.send_message(
            f"All warnings for {user.mention} have been removed.",
            ephemeral=True
        )
    else:
        try:
            removed_warning = warnings_db[user_id].pop(index - 1)
            save_warnings()  # Save changes
            await interaction.response.send_message(
                f"Warning #{index} for {user.mention} has been removed: `{removed_warning}`",
                ephemeral=True
            )
        except IndexError:
            await interaction.response.send_message(
                f"Invalid warning index. {user.mention} has {len(warnings_db[user_id])} warning(s).",
                ephemeral=True
            )

# Slash command to check warnings
@client.tree.command(name="warnings", description="Check how many warnings a user has")
@app_commands.default_permissions(administrator=True)
async def warnings(interaction: discord.Interaction, user: discord.User):
    user_id = str(user.id)

    # Check if the user has any warnings
    if user_id not in warnings_db or len(warnings_db[user_id]) == 0:
        await interaction.response.send_message(
            f"{user.mention} has no warnings.",
            ephemeral=False
        )
    else:
        # Display warnings
        embed = discord.Embed(
            title=f"Warnings for {user.name}",
            description="\n".join([f"{idx+1}. {warning}" for idx, warning in enumerate(warnings_db[user_id])]),
            color=discord.Color.orange(),
            timestamp=datetime.now()
    )
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=False)

# Slash command to clear a user's warnings
# Slash command: timeout
@client.tree.command(name="timeout", description="Timeout a user for a specified duration.")
@app_commands.describe(
    member="The member you want to timeout.",
    duration="The duration of the timeout in minutes.",
    reason="The reason for the timeout (optional)."
)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided."):
    # Check permissions
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("You don't have permission to timeout members!", ephemeral=True)
        return

    # Calculate the timeout expiration time using utcnow() for an aware datetime
    timeout_until = utcnow() + timedelta(minutes=duration)

    try:
        # Apply the timeout
        await member.edit(timed_out_until=timeout_until, reason=reason)

        # Create the warning embed
        embed = discord.Embed(
            title="Time Out",
            description=f"{member} has been issued a **Time Out for '{reason}' and expires in {duration} minute(s).**",
            color=discord.Color.orange()
        )

        # Adding the timestamp
        embed.timestamp = datetime.now()

        # Adding the user's profile picture
        embed.set_thumbnail(url=member.avatar.url)

        # Send the embed to the member's DM
        await member.send(embed=embed)

        # Send the embed to the channel
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        # Handle errors
        await interaction.response.send_message(
            f"Failed to timeout {member.mention}. Error: {e}",
            ephemeral=True
        )

        # untimeout


# Slash command: untimeout
@client.tree.command(name="untimeout", description="Remove the timeout from a user.")
@app_commands.describe(
    member="The member you want to untimeout."
)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    # Check permissions
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("You don't have permission to untimeout members!", ephemeral=True)
        return

    # Ensure the member is currently timed out
    if member.timed_out_until is None or member.timed_out_until > discord.utils.utcnow():
        await interaction.response.send_message(f"{member.mention} is not currently timed out.", ephemeral=True)
        return

    try:
        # Remove the timeout
        await member.edit(timed_out_until=None, reason="Timeout removed by an admin")

        # Send a success message to the member
        await member.send(f"You have been untimeouted in {interaction.guild.name}.")

        # Send a message to the channel
        await interaction.response.send_message(f"{member.mention} has been untimeouted.", ephemeral=True)

    except Exception as e:
        # Handle errors
        await interaction.response.send_message(
            f"Failed to untimeout {member.mention}. Error: {e}",
            ephemeral=True
        )

# File to store employee data
# JSON_FILE = 'employee_data.json'
# #HR ROLE
#
# # List of HR Role IDs
# HR_ROLE_IDS = ['1304921761124454433', '1300167248899473552']  # Replace with your actual HR role IDs
#
# # HR Review Channel ID
# REVIEW_CHANNEL_ID = 1308221445519966288  # Replace with your actual HR review channel ID
#
# # Load the JSON data if it exists, otherwise initialize an empty structure
# def load_data():
#     if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:  # Check if file exists and isn't empty
#         try:
#             with open(JSON_FILE, 'r') as file:
#                 return json.load(file)
#         except json.JSONDecodeError:
#             print("Error: The file is corrupted or not in valid JSON format.")
#             return {"employee_shifts": {}}  # Return an empty structure if invalid JSON
#     else:
#         return {"employee_shifts": {}}  # Initialize if file is missing or empty
#
# # Save the data back to the JSON file
# def save_data(data):
#     with open(JSON_FILE, 'w') as file:
#         json.dump(data, file, indent=4)
#
# # ShiftReviewButtons Class
# class ShiftReviewButtons(discord.ui.View):
#     def __init__(self, user_id, duration, embed, message, start_time_str, end_time_str, start_proof_link, end_proof_link):
#         super().__init__(timeout=None)
#         self.user_id = user_id
#         self.duration = duration
#         self.embed_message = embed
#         self.message = message
#         self.processed = False
#         self.start_time_str = start_time_str
#         self.end_time_str = end_time_str
#         self.start_proof_link = start_proof_link
#         self.end_proof_link = end_proof_link
#
#     @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
#     async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
#         if self.processed:
#             await interaction.response.send_message("This shift has already been reviewed.", ephemeral=True)
#             return
#
#         # Mark as processed
#         self.processed = True
#
#         # Update the original message
#         await self.message.edit(content=f"Shift accepted by {interaction.user.mention}", view=None)
#
#         # Update employee data
#         data = load_data()
#         employee_data = data["employee_shifts"].get(str(self.user_id), {"total_hours": 0})
#         employee_data["total_hours"] += self.duration.total_seconds() / 3600  # Add hours worked
#         data["employee_shifts"][str(self.user_id)] = employee_data
#         save_data(data)
#
#         await interaction.response.send_message(f"Shift review accepted by {interaction.user.mention}", ephemeral=True)
#
#     @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
#     async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
#         if self.processed:
#             await interaction.response.send_message("This shift has already been reviewed.", ephemeral=True)
#             return
#
#         # Mark as processed
#         self.processed = True
#
#         # Update the original message
#         await self.message.edit(content=f"Shift declined by {interaction.user.mention}", view=None)
#
#         await interaction.response.send_message(f"Shift review declined by {interaction.user.mention}", ephemeral=True)
#
#
# class ShiftLogModal(discord.ui.Modal, title="Log Your Shift"):
#     start_time = discord.ui.TextInput(
#         label="Start Time (HH:MM AM/PM or HH:MM)",
#         placeholder="e.g., 08:00 or 8:00 AM",
#         required=True,
#     )
#     end_time = discord.ui.TextInput(
#         label="End Time (HH:MM AM/PM or HH:MM)",
#         placeholder="e.g., 16:00 or 5:00 PM",
#         required=True,
#     )
#     start_proof_link = discord.ui.TextInput(
#         label="Start Proof Link (URL)",
#         placeholder="e.g., https://example.com/start-proof",
#         required=True,
#     )
#     end_proof_link = discord.ui.TextInput(
#         label="End Proof Link (URL)",
#         placeholder="e.g., https://example.com/end-proof",
#         required=True,
#     )
#
#     def __init__(self, channel):
#         super().__init__()
#         self.channel = channel
#
#     async def on_submit(self, interaction: discord.Interaction):
#         start_time_str = self.start_time.value.strip()
#         end_time_str = self.end_time.value.strip()
#         start_proof_link = self.start_proof_link.value.strip()
#         end_proof_link = self.end_proof_link.value.strip()
#
#         # Validate proof links
#         if not (start_proof_link.startswith("http://") or start_proof_link.startswith("https://")):
#             await interaction.response.send_message("Invalid Start Proof Link. Provide a valid URL.", ephemeral=True)
#             return
#
#         if not (end_proof_link.startswith("http://") or end_proof_link.startswith("https://")):
#             await interaction.response.send_message("Invalid End Proof Link. Provide a valid URL.", ephemeral=True)
#             return
#
#         try:
#             # Try parsing the start and end times in both 12-hour and 24-hour formats
#             try:
#                 start_dt = datetime.strptime(start_time_str, "%I:%M %p")  # 12-hour format with AM/PM
#             except ValueError:
#                 start_dt = datetime.strptime(start_time_str, "%H:%M")  # 24-hour format
#             
#             try:
#                 end_dt = datetime.strptime(end_time_str, "%I:%M %p")  # 12-hour format with AM/PM
#             except ValueError:
#                 end_dt = datetime.strptime(end_time_str, "%H:%M")  # 24-hour format
#
#             if end_dt <= start_dt:
#                 raise ValueError("End time must be after start time.")
#
#             duration = end_dt - start_dt
#
#             # Prepare the HR review embed
#             embed = discord.Embed(
#                 title="Shift Review",
#                 description=f"Shift logged by {interaction.user.mention}",
#                 color=discord.Color.blue(),
#             )
#             embed.add_field(name="Start Time", value=start_time_str, inline=True)
#             embed.add_field(name="End Time", value=end_time_str, inline=True)
#             embed.add_field(name="Duration", value=str(duration), inline=True)
#             embed.add_field(name="Start Proof Link", value=f"[Click Here]({start_proof_link})", inline=False)
#             embed.add_field(name="End Proof Link", value=f"[Click Here]({end_proof_link})", inline=False)
#             embed.set_footer(text=f"User ID: {interaction.user.id}")
#
#             # Prepare HR role mentions
#             role_mentions = " ".join([f"<@&{role_id}>" for role_id in HR_ROLE_IDS])
#
#             # Send message to review channel
#             message = await self.channel.send(
#                 f"{role_mentions}\nHere is the shift for review:",
#                 embed=embed,
#             )
#
#             # Attach ShiftReviewButtons
#             await message.edit(view=ShiftReviewButtons(interaction.user.id, duration, embed, message, start_time_str, end_time_str, start_proof_link, end_proof_link))
#
#             await interaction.response.send_message(
#                 "Your shift has been submitted for review.", ephemeral=True
#             )
#
#         except ValueError as e:
#             await interaction.response.send_message(str(e), ephemeral=True)
#
#
# # Registering the Slash Command for Logging Shifts
# @client.tree.command(name="logshift", description="Log your shift")
# async def log_shift(interaction: discord.Interaction):
#     # Fetch the HR review channel
#     review_channel = interaction.guild.get_channel(REVIEW_CHANNEL_ID)
#     if not review_channel:
#         await interaction.response.send_message("HR review channel not found.", ephemeral=True)
#         return
#
#     # Create the modal and show it to the user
#     modal = ShiftLogModal(channel=review_channel)
#     await interaction.response.send_modal(modal)
#
#
# @client.tree.command(name='view_shift', description='View your logged shifts.')
# async def view_shift(interaction: discord.Interaction):
#     user_id = str(interaction.user.id)  # Get the user ID as a string
#     try:
#         with open('employee_data.json', 'r') as f:
#             data = json.load(f)
#
#         employee_shifts = data.get('employee_shifts', {})
#         if user_id in employee_shifts:
#             total_hours = employee_shifts[user_id].get('total_hours', 0)
#             total_minutes = int(total_hours * 60)
#             hours = total_minutes // 60
#             minutes = total_minutes % 60
#             seconds = 0
#             formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"  # Ensure hh:mm:ss format
#
#             # Create the embed
#             embed = discord.Embed(
#                 title=interaction.user.name,  # Username as title
#                 description=f"You've worked for {formatted_time}",  # Total time worked
#                 color=discord.Color.yellow()  # Embed color
#             )
#
#             # Set the user's profile picture as the thumbnail
#             embed.set_thumbnail(url=interaction.user.avatar.url)
#
#             # If the total time worked is over 45 minutes, add the quota message
#             if total_minutes >= 45:
#                 embed.add_field(name="Quota Status", value="**You've reached the monthly quota.**", inline=False)
#
#             await interaction.response.send_message(embed=embed)
#         else:
#             await interaction.response.send_message("No shift data found for you.")
#     except FileNotFoundError:
#         await interaction.response.send_message("Employee data file not found.")
#     except json.JSONDecodeError:
#         await interaction.response.send_message("Error reading the employee data.")



# Channel and role IDs
CHANNEL_ID = 1300167249432281092
ALLOWED_ROLE_IDS = {1300167248899473553, 1300167248899473557, 1300167248916254875}  # Manager, COO, CEO


@client.tree.command(name="shiftlog_reminder", description="Ping everyone to remind them to submit shift logs.")
async def shiftlog_reminder(interaction: discord.Interaction):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Send the reminder as an embed
    channel = interaction.guild.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Shift Log Reminder 📋",
            description="Please do your **45 minute** quota for this month! \n\n Don't forget to sumbit your shift at /log_shift with proof of start and end time!",
            color=discord.Color.yellow(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1259172586613379163/1308223247149695006/2esd.png?ex=67431817&is=6741c697&hm=ad06c34dd9296b90e1cee1813be8c8f19d1bf1b3746f8bd27fef794843c82688&")
        embed.set_footer(text="Shift Management System")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1259172586613379163/1308225434110001172/Drawing-62.sketchpad_6.png?ex=67431a21&is=6741c8a1&hm=c5461cbc371146e2f034b5ea296f3423766e2ac6cfe616a0f911f685ff99761d&")  # Optional thumbnail

  # Send the embed message
        message = await channel.send(content="@everyone", embed=embed)

        # React to the message with the custom emoji
        custom_emoji = "<:ChillTaxi:1306659907923218552>"
        await message.add_reaction(custom_emoji)

        await interaction.response.send_message("Shift log reminder sent as an embed with a banner and reaction.", ephemeral=True)
    else:
        await interaction.response.send_message("Failed to find the channel.", ephemeral=True)

# Allowed roles
ALLOWED_ROLE_IDS = {1300167248899473553, 1300167248899473557, 1300167248916254875}  # Manager, COO, CEO



@client.tree.command(name="send_message", description="Send a message to a specific channel.")
@app_commands.describe(
    channel_id="Channel ID where the message will be sent.",
    message="Content of the message."
)
async def send_message(interaction: discord.Interaction, channel_id: str, message: str):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Get the channel
    channel = interaction.guild.get_channel(int(channel_id))
    if not channel:
        await interaction.response.send_message("Invalid channel ID. Please provide a valid ID.", ephemeral=True)
        return

    # Send the message
    await channel.send(message)
    await interaction.response.send_message("Message successfully sent.", ephemeral=True)

@client.tree.command(name="post_embed", description="Post a custom embed message to a specific channel.")
@app_commands.describe(
    channel_id="Channel ID where the embed will be sent.",
    title="Title of the embed message.",
    message="Content of the embed message."
)
async def post_embed(interaction: discord.Interaction, channel_id: str, title: str, message: str):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Get the channel
    channel = interaction.guild.get_channel(int(channel_id))
    if not channel:
        await interaction.response.send_message("Invalid channel ID. Please provide a valid ID.", ephemeral=True)
        return

    # Create the embed
    embed = discord.Embed(
        title=title,
        description=message,
        color=discord.Color.yellow(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1259172586613379163/1308223247149695006/2esd.png?ex=67431817&is=6741c697&hm=ad06c34dd9296b90e1cee1813be8c8f19d1bf1b3746f8bd27fef794843c82688&")  # Banner URL
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1259172586613379163/1308225434110001172/Drawing-62.sketchpad_6.png?ex=67431a21&is=6741c8a1&hm=c5461cbc371146e2f034b5ea296f3423766e2ac6cfe616a0f911f685ff99761d&")  # Logo thumbnail URL
    embed.set_footer(text=f"Message Sent By {interaction.user.display_name}")  # Footer with the user's name
    embed.timestamp = discord.utils.utcnow()  # Set the timestamp to now

    # Send the embed message
    await channel.send(embed=embed)
    await interaction.response.send_message("Embed message successfully posted.", ephemeral=True)

# fun games

@client.tree.command(name="rps", description="Play Rock-Paper-Scissors!")
async def rps(interaction: discord.Interaction, choice: str, difficulty: str = "easy"):
    user_choice = choice.lower()
    valid_choices = ["rock", "paper", "scissors"]
    difficulties = ["easy", "medium", "hard", "hell fire"]
    
    if user_choice not in valid_choices:
        await interaction.response.send_message("Invalid choice! Please choose Rock, Paper, or Scissors.", ephemeral=True)
        return

    if difficulty.lower() not in difficulties:
        await interaction.response.send_message("Invalid difficulty! Please choose from Easy, Medium, Hard, or Hell Fire.", ephemeral=True)
        return

    # Bot's move based on difficulty
    if difficulty.lower() == "easy":
        # Easy: Bot chooses randomly with no strategy
        bot_choice = random.choice(valid_choices)
        bot_response = "Easy mode, let's play around!"
    elif difficulty.lower() == "medium":
        # Medium: Bot uses common sense, may counter your move
        bot_choice = random.choice(valid_choices)
        if random.random() < 0.5:  # 50% chance for bot to play strategically
            bot_choice = {"rock": "paper", "paper": "scissors", "scissors": "rock"}[user_choice]
        bot_response = "Medium mode, it's getting interesting!"
    elif difficulty.lower() == "hard":
        # Hard: Bot uses a perfect counter-strategy
        bot_choice = {"rock": "paper", "paper": "scissors", "scissors": "rock"}[user_choice]
        bot_response = "Hard mode, prepare to lose!"
    else:  # Hell Fire
        # Hell Fire: The bot has a virtually perfect counter-strategy (0.00000001% chance of losing)
        bot_choice = {"rock": "paper", "paper": "scissors", "scissors": "rock"}[user_choice]
        if random.random() < 0.00000001:  # A tiny chance for the bot to lose
            bot_choice = random.choice([c for c in valid_choices if c != user_choice])
        bot_response = "HELL FIRE! 🔥 Your chances of winning are *so low*, they're practically nonexistent!"

    # Determine winner
    result = "It's a tie!"
    if (user_choice == "rock" and bot_choice == "scissors") or \
       (user_choice == "paper" and bot_choice == "rock") or \
       (user_choice == "scissors" and bot_choice == "paper"):
        result = "You win!"
    elif user_choice != bot_choice:
        result = "You lose!"

    # Send response
    embed = discord.Embed(
        title="Rock-Paper-Scissors",
        description=f"You chose: **{user_choice.capitalize()}**\nBot chose: **{bot_choice.capitalize()}**\n\n**{result}**\n\n{bot_response}",
        color=discord.Color.random()
    )
    await interaction.response.send_message(embed=embed)

# Add the command choices for autocompletion
@rps.autocomplete("choice")
async def rps_autocomplete(interaction: discord.Interaction, current: str):
    options = ["Rock", "Paper", "Scissors"]
    return [
        app_commands.Choice(name=option, value=option.lower())
        for option in options if current.lower() in option.lower()
    ]

@rps.autocomplete("difficulty")
async def difficulty_autocomplete(interaction: discord.Interaction, current: str):
    options = ["Easy", "Medium", "Hard", "Hell Fire"]
    return [
        app_commands.Choice(name=option, value=option.lower())
        for option in options if current.lower() in option.lower()
    ]

# test

@client.tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Test command received!")

# personal

class PaginationView(View):
    def __init__(self, interaction, pages):
        super().__init__(timeout=180)  # Increased timeout to avoid timing out quickly
        self.interaction = interaction
        self.pages = pages
        self.current_page = 0
        self.message = None  # Initialize message as None

        # Buttons
        self.prev_button = Button(label="Previous", style=discord.ButtonStyle.primary)
        self.next_button = Button(label="Next", style=discord.ButtonStyle.primary)

        self.prev_button.callback = self.prev_page
        self.next_button.callback = self.next_page

        self.add_item(self.prev_button)
        self.add_item(self.next_button)

    async def send(self):
        """Send the initial embed with the view."""
        await self.interaction.response.send_message(embed=self.get_embed(), view=self, ephemeral=False)
        self.message = await self.interaction.original_response()

    def get_embed(self):
        """Generate an embed for the current page."""
        embed = discord.Embed(title="Banned Users", color=discord.Color.red())
        embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}")

        for user in self.pages[self.current_page]:
            name = user.get("discord_name", "Unknown")
            user_id = user.get("discord_id", "Unknown")
            reason = user.get("reason", "No reason provided")
            duration = user.get("duration")
            appeal = user.get("appeal", "No reason provided")
            embed.add_field(
            name=name,
            value=(
            f"ID: {user_id}\n"
            f"Reason: {reason}\n"
            f"Duration: {f'{duration} day(s)' if duration else 'Permanent'}\n"
            f"Appealable: {appeal}"
         ),
            inline=False
        )

        return embed

    async def prev_page(self, interaction: discord.Interaction):
        """Handle 'Previous' button interaction."""
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return

        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.defer()  # Defer to acknowledge the interaction
            await self.message.edit(embed=self.get_embed())  # Update the embed

    async def next_page(self, interaction: discord.Interaction):
        """Handle 'Next' button interaction."""
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return

        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await interaction.response.defer()  # Defer to acknowledge the interaction
            await self.message.edit(embed=self.get_embed())  # Update the embed

# Function to load banned users from a JSON file
def load_banned_users():
    try:
        with open("bannedusers.json", "r") as file:
            data = file.read()
            if not data.strip():
                return []
            return json.loads(data)
    except FileNotFoundError:
        logging.error("bannedusers.json file not found.")
        return []
    except json.JSONDecodeError:
        logging.error("Error decoding JSON in bannedusers.json.")
        return []

@client.tree.command(name="banrecords")
async def banrecords(interaction: discord.Interaction):
    """Command to display ban records with pagination."""
    if interaction.user.id != 711284441166774302:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    data = load_banned_users()
    if not data:
        await interaction.response.send_message("No banned users found.", ephemeral=False)
        return

    items_per_page = 5
    pages = [data[i:i + items_per_page] for i in range(0, len(data), items_per_page)]

    view = PaginationView(interaction, pages)
    await view.send()




badge_emojis = {
    1: ("CEO", "<a:Owner:1322252664767250492>"),
    2: ("COO", "<a:Coowner:1322252795939913829>"),
    3: ("Bot Developer", "<:BotDeveloper:1322252722346393621>"),
    4: ("General Manager", "<a:GeneralManager:1322252688481587253>"),
    5: ("Associate General Manager", "<a:AssociateGeneralManager:1322252709381931140>"),
    6: ("Head Supervisor", "<:HeadSupervisor:1322252676792057886>"),
    7: ("Supervisor", "<:Supervisor:1322252652326817802>"),
    8: ("Firestone Law Enforcement Officer", "<:Badge:1322304878621626458>"),
    9: ("Firestone Department of Commerce", "<:DOCM:1322307523688140881>"),
    10: ("Firestone Department of Public Works", "<:DPW:1323768628780335124>")
}

@client.command()
async def employeedata(ctx):
    discord_id = str(ctx.author.id)  # Get the Discord ID of the user running the command

    # Load the employee image data (with badges)
    with open('employeeimgndata.json', 'r') as file:
        employee_img_data = json.load(file)

    # Load the employee shift data (with total_hours)
    with open('employee_data.json', 'r') as file:
        employee_data = json.load(file)

    # Search for the user in the employee image data
    user_data = None
    for data in employee_img_data:
        if str(data['discord_id']) == discord_id:
            user_data = data
            break

    if user_data:
        roblox_id = user_data['roblox_id']
        roblox_name = user_data['roblox_name']
        badges = user_data.get('badges', [])

        # Now, get the total_hours from the employee_data file
        total_hours = 0.0
        if 'employee_shifts' in employee_data:
            shifts = employee_data['employee_shifts']
            if discord_id in shifts:
                total_hours = shifts[discord_id].get('total_hours', 0.0)

        # Ensure total_hours is a valid number
        try:
            total_hours = float(total_hours)
        except ValueError:
            print(f"Error: Invalid total_hours value for {discord_id}")
            total_hours = 0.0  # Default to 0 if not valid

        # Convert total_hours to total seconds for accurate conversion
        total_seconds = total_hours * 3600  # Multiply by 3600 to get total seconds

        # Calculate hours, minutes, and seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        # Format the time as HH:MM:SS
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

        # Build the badge string
        badge_str = ""
        for badge in badges:
            badge_name, badge_emoji = badge_emojis.get(badge, ("Unknown Badge", ""))
            badge_str += f"{badge_emoji} **{badge_name}**\n"
        if not badge_str:
            badge_str = "None"

        # Build the embed
        embed = discord.Embed(
            title=f"{roblox_name}'s Profile",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Roblox Username", value=roblox_name)
        embed.add_field(name="Roblox ID", value=roblox_id)
        embed.add_field(name="Total Hours Worked", value=formatted_time)  # Display formatted time
        embed.add_field(name="Badges", value=badge_str)

        # Get the Discord profile image for the user
        user = await client.fetch_user(discord_id)
        embed.set_thumbnail(url=user.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

    else:
        await ctx.send("No employee data found for you.")

@client.tree.command(name="send_dm", description="Send a direct message to a user.")
@app_commands.describe(
    user="The user to send a DM to",
    message="The message to send",
    upload_file="Optional file to upload"
)
async def send_dm(
    interaction: discord.Interaction,
    user: discord.User,
    message: str,
    upload_file: discord.Attachment = None
):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    try:
        # Send the DM with or without an attachment
        if upload_file is not None:
            await user.send(content=message, file=await upload_file.to_file())
        else:
            await user.send(message)
        await interaction.response.send_message(f"DM sent to {user.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"Could not send DM to {user.mention}. They might have DMs disabled.", ephemeral=True)

# remove rank with message in dms with custom "reason"

@client.command()
async def removerank(ctx, user: discord.Member, rank: str, *, reason: str):
    # Check if the user has an allowed role
    user_roles = {role.id for role in ctx.author.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await ctx.send("You do not have permission to use this command.")
        return

    # Remove the rank from the user
    await user.remove_roles(discord.utils.get(ctx.guild.roles, name=rank))
    await ctx.send(f"Removed rank **{rank}** from {user.mention}.")

    # Send a DM to the user with the reason
    try:
        await user.send(f"You have been removed from the **{rank}** role. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send(f"Could not send DM to {user.mention}. They might have DMs disabled.")


# Define the watchlist dictionary at the top of your file or before any commands that use it
WATCHLIST_FILE = "watchlist.json"

# Load the watchlist from file (if exists)
def load_watchlist():
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save the watchlist to file
def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f, indent=4)

# set a "watchlist" so users get a tag # when a HR or any rank above can see the user is active in the server and training course provided by instructor.
@client.tree.command(name="watchlist", description="Add a user to the watchlist.")
@app_commands.describe(
    member="The member to add to the watchlist.",
    reason="Reason for adding to the watchlist."
)
async def watchlist_command(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Load existing watchlist
    watchlist = load_watchlist()

    # Add or update only the selected member, preserving others
    watchlist[str(member.id)] = {
        "username": member.display_name,
        "id": member.id,
        "reason": reason,
        "added_by": interaction.user.id
    }

    # Save the updated watchlist
    try:
        save_watchlist(watchlist)
    except Exception as e:
        await interaction.response.send_message(f"Failed to save watchlist: {e}", ephemeral=True)
        return

    await interaction.response.send_message(
        f"Added {member.mention} to the watchlist.\nReason: {reason}\nAdded by: {interaction.user.mention}",
        ephemeral=True
    )

@client.tree.command(name="view_watchlist", description="View the current watchlist.")
async def view_watchlist(interaction: discord.Interaction):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Load the watchlist from watchlist.json
    watchlist_data = load_watchlist()

    if not watchlist_data:
        await interaction.response.send_message("The watchlist is currently empty.", ephemeral=True)
        return

    class WatchlistPaginationView(View):
        def __init__(self, author_id, guild, pages):
            super().__init__(timeout=180)
            self.author_id = author_id
            self.guild = guild
            self.pages = pages
            self.current_page = 0
            self.message = None

            self.prev_button = Button(label="Previous", style=discord.ButtonStyle.primary)
            self.next_button = Button(label="Next", style=discord.ButtonStyle.primary)
            self.prev_button.callback = self.prev_page
            self.next_button.callback = self.next_page
            self.add_item(self.prev_button)
            self.add_item(self.next_button)

        def get_embed(self):
            embed = discord.Embed(
                title="Watchlist",
                description="List of users currently on the watchlist.",
                color=discord.Color.orange()
            )
            for user_id, info in self.pages[self.current_page]:
                member = self.guild.get_member(int(user_id))
                display_name = member.display_name if member else f"User ID: {user_id}"
                reason = info.get("reason", "No reason provided.")
                added_by_id = info.get("added_by")
                added_by_member = self.guild.get_member(added_by_id) if added_by_id else None
                added_by_name = added_by_member.display_name if added_by_member else f"User ID: {added_by_id}" if added_by_id else "Unknown"
                embed.add_field(
                    name=display_name,
                    value=f"**Reason:** {reason}\n**Added by:** {added_by_name}",
                    inline=False
                )
            embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}")
            return embed

        async def send(self, interaction):
            await interaction.response.send_message(embed=self.get_embed(), view=self, ephemeral=True)
            self.message = await interaction.original_response()

        async def prev_page(self, interaction: discord.Interaction):
            if interaction.user.id != self.author_id:
                await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
                return
            if self.current_page > 0:
                self.current_page -= 1
                await interaction.response.edit_message(embed=self.get_embed(), view=self)

        async def next_page(self, interaction: discord.Interaction):
            if interaction.user.id != self.author_id:
                await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
                return
            if self.current_page < len(self.pages) - 1:
                self.current_page += 1
                await interaction.response.edit_message(embed=self.get_embed(), view=self)

    # Prepare paginated data
    items = list(watchlist_data.items())
    items_per_page = 5
    pages = [items[i:i + items_per_page] for i in range(0, len(items), items_per_page)]

    if not pages:
        await interaction.response.send_message("The watchlist is currently empty.", ephemeral=True)
        return

    view = WatchlistPaginationView(interaction.user.id, interaction.guild, pages)
    await view.send(interaction)

# watchlist removal and removes data from watchlist.json from that user ID which matches in the json deleting their info.
@client.tree.command(name="remove_watchlist", description="Remove a user from the watchlist.")
@app_commands.describe(
    member="The member to remove from the watchlist.",
    reason="Reason for removing from the watchlist."
)
async def remove_watchlist_command(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Load existing watchlist
    watchlist = load_watchlist()

    # Remove the member from the watchlist if they exist
    if str(member.id) in watchlist:
        del watchlist[str(member.id)]
        save_watchlist(watchlist)
        await interaction.response.send_message(
            f"Removed {member.mention} from the watchlist.\nReason: {reason}\nRemoved by: {interaction.user.mention}",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(f"{member.mention} is not on the watchlist.", ephemeral=True)


# Utility functions for extension data
def load_extension_data():
    try:
        with open("extension.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_extension_data(data):
    with open("extension.json", "w") as f:
        json.dump(data, f, indent=4)

# Extension command with approval/decline and DM notification
@client.tree.command(name="extension", description="Grant or decline an extension for a user.")
@app_commands.describe(
    member="The member to add to the extension list.",
    reason="Reason for the extension.",
    approved="Was the extension approved? (yes/no)"
)
async def extension_command(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided.",
    approved: str = "yes"
):
    # Check if the user has an allowed role
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    approved = approved.lower()
    if approved not in ("yes", "no"):
        await interaction.response.send_message("Please specify 'yes' or 'no' for approval.", ephemeral=True)
        return

    # Load existing extension data
    extension_data = load_extension_data()

    # Add/update the member in the extension list
    extension_data[str(member.id)] = {
        "reason": reason,
        "granted_by": interaction.user.id,
        "approved": approved
    }
    save_extension_data(extension_data)

    # Prepare DM embed
    embed = discord.Embed(
        title="Extension Request",
        color=discord.Color.yellow()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1259172586613379163/1308223247149695006/chilltaxi.png")
    if approved == "yes":
        embed.description = f"Your extension has been **approved** by {interaction.user.mention}.\n**Reason:** {reason}"
    else:
        embed.description = f"Your extension has been **declined** by {interaction.user.mention}.\n**Reason:** {reason}"

    # Try to DM the user
    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(f"Could not DM {member.mention}. They might have DMs disabled.", ephemeral=True)
        return

    await interaction.response.send_message(
        f"{member.mention} has been {'approved for' if approved == 'yes' else 'declined for'} an extension.\nReason: {reason}\nBy: {interaction.user.mention}",
        ephemeral=True
    )

# View extension list
@client.tree.command(name="view_extension", description="View the current extension list.")
async def view_extension_command(interaction: discord.Interaction):
    extension_data = load_extension_data()
    if not extension_data:
        await interaction.response.send_message("The extension list is currently empty.", ephemeral=True)
        return

    embed = discord.Embed(title="Extension List", color=discord.Color.blue())
    for user_id, data in extension_data.items():
        member = interaction.guild.get_member(int(user_id))
        if member:
            status = "Approved" if data.get("approved") == "yes" else "Declined"
            embed.add_field(
                name=member.display_name,
                value=f"Status: **{status}**\nReason: {data.get('reason', 'No reason')}\nBy: <@{data.get('granted_by')}>",
                inline=False
            )

    await interaction.response.send_message(embed=embed)

# Remove from extension list
@client.tree.command(name="remove_extension", description="Remove a user from the extension list.")
@app_commands.describe(
    member="The member to remove from the extension list.",
    reason="Reason for removing from the extension list."
)
async def remove_extension_command(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
    user_roles = {role.id for role in interaction.user.roles}
    if not ALLOWED_ROLE_IDS.intersection(user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    extension_data = load_extension_data()
    if str(member.id) in extension_data:
        del extension_data[str(member.id)]
        save_extension_data(extension_data)
        await interaction.response.send_message(
            f"Removed {member.mention} from the extension list.\nReason: {reason}\nRemoved by: {interaction.user.mention}",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(f"{member.mention} is not on the extension list.", ephemeral=True)

client.run(os.environ["DISCORD_TOKEN"])
