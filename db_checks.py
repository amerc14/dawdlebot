import discord
from discord.ext import commands
def is_mod():
	async def is_mod_predicate(ctx):
		adminroles = [490249474619211838, 514556928655884298, 623220291882975292]
		modroles = [490249474619211838, 514556928655884298, 623220291882975292, 519632663246536736]
		dawdle = ctx.guild
		is_mod = False
		for role in ctx.author.roles:
			if role.id in modroles:
				is_mod = True
				break
		return is_mod
	return commands.check(is_mod_predicate)

def is_member(guilds):
	async def is_member_predicate(ctx):
		for guild in guilds:
			if guild.name == 'dawdle':
				dawdle = guild
				break
		if dawdle.get_member(ctx.author.id):
			return True
		else:
			return False
	return commands.check(is_member_predicate)