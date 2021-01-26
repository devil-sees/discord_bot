import discord
import random
import asyncio
from discord.ext import commands

bot_token = 'Nzk1OTk0MTM4NzA0MzQ3MTY2.X_RdTw.xiy2dcfdbJZQ7531_8Ab9TxCL_U'
dlt_cnl_id = 803213061640814612
Client = commands.Bot(command_prefix='+')

# -----------------------------------------------------
status_play = ("on Devil's Orders", "with Admin's Life", "Tic-Tac-Toe", "with TV's Remote")
status_stream = ("my marriage video", "Pokemon go Lite", "My Life", "How to drink water")
status_listen = ("baby cries", "friend's breakup  story", "My Lord", "an audiobook")
status_watch = ("Attack on Titan (Yes! I have subscription)", "Flat Earth Theory", "DVD Logo to hit the corner")
play = discord.Activity(type=discord.ActivityType.playing, name=random.choice(status_play))
stream = discord.Activity(type=discord.ActivityType.streaming, name=random.choice(status_stream), url=None)
listen = discord.Activity(type=discord.ActivityType.listening, name=random.choice(status_listen))
watch = discord.Activity(type=discord.ActivityType.watching, name=random.choice(status_watch))
status = (play, stream, listen, watch)
# -----------------------------------------------------
hug_gif_url = ("https://media.tenor.com/images/5234acd89edc16c27af403833863408a/tenor.gif",
               "https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057",
               "https://media.tenor.com/images/8090081dc5386a5272feb8bb29747a5d/tenor.gif")

troll_msg = ("I am not your slave!", "Eat 5-star, do nothing!", "I am on a vacation", "Meh!", "Later! I'm not in mood")

censor = ['fuck', 'penis']      # add only in lowercase


@Client.event
async def on_ready():
    print('Logged in as\n{0}: {1}\n-------'.format(Client.user.name, Client.user.id))
    # Prints Bot name and bot id on Console confirming bot is running successfully

    while True:             # Set Bot status to a random troll message and change every 2 minutes
        await Client.change_presence(activity=random.choice(status), status=discord.Status.idle)
        await asyncio.sleep(120)


@Client.event
async def on_message(message):
    msg = message.content.lower().startswith        # Abbreviation made to avoid confusion
    send_msg = message.channel.send                 # Abbreviation made to avoid confusion

    # ------------------------------------------------------------
    '''Hug Command to send a message saying User A has hugged User B along with a random gif image
    Deletes original msg by user
    Add or remove gifs from 'hug_gif_url' defined above
    Syntax: hug <tag user or your_message>'''
    if msg('hug'):
        await message.delete()              # Deletes original msg by user
        # Checks if user has tagged themselves
        if message.content.lower().lstrip('hug <@!').startswith(str(message.author.mention.lstrip('<@')).lower()):
            embed = discord.Embed(
                description=':speech_balloon:: {0} has hugged themselves'.format(message.author.mention),
                color=0xff22ff)
        else:
            embed = discord.Embed(
                description=':speech_balloon:: {0} has hugged {1}'.format(message.author.mention,
                                                                          message.content.lower().lstrip('hug')),
                color=0xff22ff)
        embed.set_image(url=random.choice(hug_gif_url))
        await send_msg(embed=embed)         # sends msg containing text and gif image

    # -------------------------------------------------------------
    # sends a random trolling message from 'troll_msg' defined above if user msg starts with do
    if message.content.lower() == 'do' or msg('do '):
        await send_msg(random.choice(troll_msg))

    # --------------------------------------------------------------
    '''Hi and Good Morning messages'''
    if msg('hi'):
        await send_msg(f"hello {message.author.mention}! We wish you have a great day!")
    if msg('good morning'):
        if not message.author.bot:
            await send_msg(f"Good Morning {message.author.mention}! Such a wonderful day it is!")

    # -------------------------------------------------------------
    '''Say command to delete message my user and sending the same via bot to avoid username reveal
    Syntax: &say <user_message>'''
    if message.content.startswith('&say'):
        await message.delete()
        await send_msg(message.content.lstrip('&say'))

    # -------------------------------------------------------------
    '''Spam command for adding a spam in any channel
    Syntax: &&spam, <1>, <2>, <spam_message>
    <1> = number of times to be spammed; cannot exceed 10; required
    <2> = Time interval for every message to spam; in seconds; optional; cannot exceed 4 hours
    original message by will be deleted once executed'''

    if message.content.startswith('&&spam'):
        if not message.author.bot:
            await message.delete()              # Delete the spamming syntax

            # noinspection PyBroadException
            try:
                syntax_cut_old = message.content.split(',')     # Splits the message separated by commas into list
                syntax_cut = []
                for i in syntax_cut_old:
                    syntax_cut.append(i.lstrip())               # removes any whitespaces after comma
                rest_message = ''
                no_times = int(syntax_cut[1])                   # Number of times message to be spammed

                if no_times > 10:                               # Can't spam more than 10 times
                    await send_msg("Cannot spam a message more than 10 times", delete_after=6)
                else:
                    try:
                        time_interval = int(syntax_cut[2])          # Check if time interval is given which is optional
                        if time_interval > 14400:                   # 14400 secs = 4 hrs
                            await send_msg("Cannot spam a message with waiting time more than 4 hours", delete_after=6)
                        else:
                            for i in syntax_cut[3:]:
                                rest_message = rest_message+' '+i   # Creating message from list to string
                            for i in range(no_times):               # Sending message given number of times
                                await send_msg(rest_message)
                                await asyncio.sleep(time_interval)  # wait till given time interval

                    except ValueError:              # If time interval is not given
                        for i in syntax_cut[2:]:                    # Creating message from list to string
                            rest_message = rest_message+' '+i
                        for i in range(no_times):                   # Sending message given number of times
                            await send_msg(rest_message)

            except Exception:
                await send_msg('Wrong Syntax for spamming', delete_after=6)

    # ---------------------------------------------------------------
    '''Deletes any message containing cuss words or foul language
    Add cuss words to ban in list 'censor' given on top lines
    Give a channel id in variable 'dlt_cnl_id' given on top lines to send deleted message
    You can set that channel having permission to read deleted message by Admin and Mod only for future inspection'''

    for i in str(message.content.lower()).split():      # Creates a list having all words of message
        if i in censor:                                 # Deletes whole message if any word matches the censored
            await message.delete()
            await send_msg(f'{message.author} You are not allowed to send any messages containing foul language!',
                           delete_after=2)              # Sends a warning message
            embed = discord.Embed(title=f'Following message sent by @{message.author} in '
                                        f'#{message.channel} was deleted.',
                                  description=f'{message.content}', color=0xffffff)
            await Client.get_channel(dlt_cnl_id).send(embed=embed)  # sends deleted message to specified channel

Client.run(bot_token)
