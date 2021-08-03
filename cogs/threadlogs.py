import typing
import config
import discord
import sqlite3
import aiosqlite
from entropy import stablizer
from discord.ext import commands
from profanity import profanity



class ThreadLogging(commands.Cog, name="Utilities", description = "Commands related to thread logging configurations can be found here!"):
    def __init__(self, client):
        self.client = client
        self.cache = []
        self.maincache = {}
        self.emergency = {}
        if config.SAFE_EMOTE is None:
            self.safe = "\N{White Heavy Check Mark}"
        else:
            self.safe = config.SAFE_EMOTE
        if config.EMERGENCY_EMOTE is None:
            self.emergence = "\N{Snowflake}"
        else:
            self.emergence = config.EMERGENCY_EMOTE
        if config.DANGER_EMOTE is None:
            self.danger = "\N{No Entry}"
        else:
            self.danger = config.DANGER_EMOTE
        if config.UPDATED_EMOTE is None:
            self.updated = "\N{Large Yellow Circle}"
        else:
            self.updated = config.UPDATED_EMOTE
        if config.DEFAULT_EMOTE is None:
            self.default = "\N{White Question Mark Ornament}"
        else:
            self.default = config.DEFAULT_EMOTE

    @staticmethod
    async def db():
        con = await aiosqlite.connect('./threader.sqlite')
        return con


    @commands.command()
    async def bind(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        con = await self.db()
        try:
            cursror = await con.execute('SELECT channel_id FROM guilds where ids = ?', (ctx.guild.id,))
        except sqlite3.OperationalError:
            await con.execute('ALTER TABLE guilds ADD COLUMN channel_id INT')
        await con.execute('REPLACE INTO guilds(ids, channel_id) VALUES(?,?) ON CONFLICT(ids) DO UPDATE SET channel_id = ?, ids = ?', (ctx.guild.id, channel.id, channel.id, ctx.guild.id))
        await con.commit()
        self.maincache[ctx.guild.id] = channel.id
        await ctx.send(f'Logging channel has now been binded to: {channel.mention}')


    @commands.command(aliases=['emr'])
    async def emergencyrole(self, ctx, role: typing.Union[discord.Role, str]=None):
        if not role:
            return await ctx.send(f'Correct syntax is: {ctx.prefix}emergency @role')
        con = await self.db()
        if isinstance(role, str):
            if role == "None":
                 try:
                    cursror = await con.execute('SELECT emergency_id FROM guilds where ids = ?', (ctx.guild.id,))
                 except sqlite3.OperationalError:
                    await con.execute('ALTER TABLE guilds ADD COLUMN emergency_id INT')
                 await con.execute('REPLACE INTO guilds(ids, emergency_id) VALUES(?,0) ON CONFLICT(ids) DO UPDATE SET emergency_id = 0, ids = ?', (ctx.guild.id, ctx.guild.id))
                 await con.commit()
                 self.emergency[ctx.guild.id] = 0
                 return await ctx.send("Successfully set emergency role as None!")  
        try:
            cursror = await con.execute('SELECT emergency_id FROM guilds where ids = ?', (ctx.guild.id,))
        except sqlite3.OperationalError:
            await con.execute('ALTER TABLE guilds ADD COLUMN emergency_id INT')
        await con.execute('REPLACE INTO guilds(ids, emergency_id) VALUES(?,?) ON CONFLICT(ids) DO UPDATE SET emergency_id = ?, ids = ?', (ctx.guild.id, role.id, role.id, ctx.guild.id))
        await con.commit()
        await ctx.send(f'Emergency Role has now been binded to: {role.mention}')
        


    @commands.Cog.listener()
    async def on_thread_join(self, thread: discord.Thread):
        if thread.message_count > 2:
            return await channel.send(f'{self.safe} | {thread.owner.mention}\'s ({thread.owner.name}) thread is no longer archived:  `{thread.name}` ({thread.mention}) in {thread.parent.mention}')
        if thread.id in self.cache:
            return
        self.cache.append(thread.id)
        con = await self.db()
        try:
            curses = self.maincache[thread.guild.id]
        except KeyError:
            cursor = await con.execute('SELECT channel_id FROM guilds where ids = ?', (thread.guild.id,))
            if cursor is None:
                return
            curses = await cursor.fetchone()
            curses = curses[0]
            self.maincache[thread.guild.id] = curses
        channel = self.client.get_channel(curses)
        if not channel:
            return print('Channel wasn\'t found! Please make sure it does exist')
        word_modified = await stablizer(thread.name)
        if profanity.contains_profanity(thread.name) is True or profanity.contains_profanity(word_modified) is True:
            try:
                try:
                    emergency = self.emergency[thread.guild.id].mention

                except AttributeError:
                    emergency = self.emergency[thread.guild.id]
                    if emergency == 0:
                        emergency = None
            except KeyError:
                 try:
                    cursor = await con.execute('SELECT emergency_id FROM guilds where ids = ?', (thread.guild.id,))
                    curse = await cursor.fetchone()
                    if curse[0] == 0:
                        emergency = None
                    else:
                        emergency = thread.guild.get_role(int(curse[0])).mention
                        if not emergency:
                            emergency = thread.guild.default_role.name
                 except sqlite3.OperationalError:
                    emergency = thread.guild.default_role.name
                 self.emergency[thread.guild.id] = emergency
            if not emergency:
                return await channel.send(f'{self.emergence} | {thread.owner.mention} ({thread.owner.name}) Created a thread which might contain a bad word: `{thread.name}` ({thread.mention})')
            else: 
                return await channel.send(f'<{self.emergence}| || {emergency} || {thread.owner.mention} ({thread.owner.name}) Created a thread which might contain a bad word: `{thread.name}` ({thread.mention})')
        await channel.send(f'{self.safe} | {thread.owner.mention} ({thread.owner.name}) Created a thread `{thread.name}` ({thread.mention}) in {thread.parent.mention}')

    @commands.Cog.listener()
    async def on_thread_delete(self, thread: discord.Thread):
        async for x in thread.guild.audit_logs(limit=1, action=discord.AuditLogAction.thread_delete):
            try:
                new_user = x.user
            except:
                new_user = thread.owner
        con = await self.db()
        try:
            curses = self.maincache[thread.guild.id]
        except KeyError:  
            cursor = await con.execute('SELECT channel_id FROM guilds where ids = ?', (thread.guild.id,))
            if cursor is None:
                return
            curses = await cursor.fetchone()
            curses = curses[0]
            self.maincache[thread.guild.id] = curses
        channel = self.client.get_channel(curses)
        if not channel:
            return print('Channel wasn\'t found! Please make sure it does exist')
        try:
            await channel.send(f'{self.danger} | {new_user.mention} ({new_user.name})  Deleted a thread: `{thread.name}` in {thread.parent.mention}')
        except AttributeError:
            await channel.send(f'{self.danger} | {new_user.mention} ({new_user.name})  Deleted a thread: `{thread.name}`')


    @commands.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        async for x in before.guild.audit_logs(limit=1):
                re_name = x.user
        con = await self.db()
        try:
            curses = self.maincache[after.guild.id]
        except KeyError:  
            cursor = await con.execute('SELECT channel_id FROM guilds where ids = ?', (before.guild.id,))
            if cursor is None:
                return
            curses = await cursor.fetchone()
            curses = curses[0]
            self.maincache[before.guild.id] = curses
        channel = self.client.get_channel(curses)
        if not channel:
            return print('Channel wasn\'t found! Please make sure it does exist')
        if before.name != after.name:
            await channel.send(f'{self.updated} | {re_name.mention} ({re_name.name}) Changed the name of a Thread from `{before.name}` to `{after.name}` ({after.mention}) in {before.parent.mention}')
        if not before.archived and after.archived:
            await channel.send(f'{self.default} | {re_name.mention} ({re_name.name}) Archived a thread `{before.name}` ({after.mention}) in {before.parent.mention}')
        if before.archived and not after.archived:
            await channel.send(f'{self.safe} | {before.owner.mention}\'s ({re_name.name}) thread is no longer archived:  `{before.name}` ({before.mention}) in {before.parent.mention}')

def setup(client):
    client.add_cog(ThreadLogging(client))