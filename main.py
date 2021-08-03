import os
import config
import sqlite3
import discord
import datetime
import aiosqlite
from Views.Buttons import InviteButtons
from discord.ext import commands

class HelpEmbed(discord.Embed): # Our embed with some preset attributes to avoid setting it multiple times
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = discord.Color.blurple()


async def get_pre(bot, message):
    try:
        prefix = client.prefix[message.guild.id]
        return prefix
    except KeyError:
        pass
    con = await aiosqlite.connect('./threader.sqlite')
    create_guilds_table = """
CREATE TABLE IF NOT EXISTS guilds (
      ids INT UNIQUE PRIMARY key,
      prefix TEXT
);
"""
    cur = await con.execute(create_guilds_table)
    poger = """
    SELECT prefix FROM guilds WHERE ids = %s
    """ % (message.guild.id,)
    prefix = await con.execute(poger)
    new = await prefix.fetchone()
    await con.close()
    if new[0] is None:
        prefix = '?'
        client.prefix[message.guild.id] = '?'
    else:
        prefix = new
        client.prefix[message.guild.id] = prefix
    return prefix

intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=get_pre, intents=intents)
client.prefix = {}

class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__( # create our class with some aliases and cooldown
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.CooldownMapping.from_cooldown(2, 5.0, commands.BucketType.member),
                "aliases": ['commands', 'cmds'],
                'hidden': True
            }
        )
    
    async def send(self, **kwargs):
        """a short cut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.avatar.url)
        usable = 0 

        for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
            filtered_commands = await self.filter_commands(commands)
            if filtered_commands: 
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog: # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No Category"
                    description = "Commands with no category"

                embed.add_field(name=f"{name} Category [{amount_commands}]", value=description)

        embed.description = f"{len(client.commands)} commands | {usable} usable" 

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
        embed = HelpEmbed(title=signature, description=command.help or "No help found...")
        cog = command.cog
        if cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"
            
        embed.add_field(name="Usable", value=can_run)
        cooldown = command._buckets._cooldown
        if command._buckets and (cooldown): # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description or "No help found...")
        filtered_commands = await self.filter_commands(commands)
        if filtered_commands:
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
           
        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

client.help_command = MyHelp()

@client.event
async def on_ready():
    try:
        info = await client.application_info()
        print('----------------------------')
        print(f'{client.user} Is Now Online')
        print(f'Using {discord.__version__} discord.py version')
        print("Bot Code written by: Pizerite#5648")
        print('Feel free to dm me if you are in doubt!')
        print('##### Application Info #####')
        print(f'Name: {info.name}')
        print(f'Owner: {info.owner}')
        print('----------------------------')
    except Exception as err:
        print(err)


@client.command()
async def setprefix(ctx, prefix: str):
    if len(prefix) > 5:
        return await ctx.send('Prefix can only be 5 characters long!')
    con = await aiosqlite.connect('./threader.sqlite')
    cur = await con.execute('REPLACE INTO guilds(ids, prefix) VALUES(?,?) ON CONFLICT(ids) DO UPDATE SET prefix = ?, ids = ?', (ctx.guild.id, prefix, prefix, ctx.guild.id))
    await con.commit()
    client.prefix[ctx.guild.id] = prefix
    await con.close()
    if config.SAFE_EMOTE is None:
        emote = "\N{White Heavy Check Mark}"
    else:
        emote = config.SAFE_EMOTE
    await ctx.message.add_reaction(emote)

@client.command()
async def invite(ctx):
    link = f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot%20applications.commands"
    view = InviteButtons(link)
    await ctx.send('Here is my invite:', view=view)


for filename in os.listdir('./cogs'):
     if filename.endswith(".py"):
            client.load_extension(f'cogs.{filename[:-3]}')



client.run(config.BOT_TOKEN)
