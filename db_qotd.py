import discord
import json
import datetime
from db_checks import is_mod

from discord.ext import commands,tasks

class qotd(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.qotdcheck.start()
	@commands.command()
	@is_mod()
	async def addqotd(self, ctx, *, question : str):
		with open('qotd.json', 'r') as json_file_r0:
			qotdlist = json.load(json_file_r0)
		
		qotdlist.append(question)

		with open('qotd.json', 'w') as json_file_w0:
			json.dump(qotdlist,json_file_w0)

		await ctx.send('Question added!')

	@commands.command()
	@is_mod()
	async def getqotd(self, ctx, num : int):
		with open('qotd.json', 'r') as json_file_r1:
			qotdlist = json.load(json_file_r1)
		qotdReq = qotdlist[:num]
		qotdReqStr = ''
		nDone = False
		for n in range(num):
			qotdReqStr += f'[{n+1}] {qotdlist[n]} \n'
			if n == (len(qotdReq) - 1):
				break
		#qotdReqStr = '\n<a:flashingstars:598698378359996419> '.join(qotdReq)
		qotdEmbed = discord.Embed(title = 'QOTD', description = qotdReqStr, color=0xffb6c1)
		await ctx.send(embed=qotdEmbed)

	@getqotd.error
	async def getqotd_error(self,ctx, error):
		if isinstance(error,commands.errors.CommandInvokeError):
			await ctx.send("You don't have any questions set up!")

	@commands.command()
	@is_mod()
	async def removeqotd(self, ctx, num : int):
		with open('qotd.json', 'r') as json_file_r3:
			qotdlist = json.load(json_file_r3)

		await ctx.send(f'Are you sure you want to delete the following question? (yes/no)\n "{qotdlist[num-1]}"')
		def qotd_check(m):
			return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
		try:
			confirm = await self.bot.wait_for('message',check=qotd_check,timeout=60.0)
		except asyncio.TimeoutError:
			await ctx.send('QOTD delete request timed out.')
		else:
			if confirm.content.lower() == 'yes':
				del qotdlist[num-1]

				await ctx.send('question deleted')

			else:
				await ctx.send('deletion cancelled')

		with open('qotd.json', 'w') as json_file_w3:
			json.dump(qotdlist,json_file_w3)

	@commands.command()
	@is_mod()
	async def editqotd(self, ctx, num : int):
		with open('qotd.json', 'r') as json_file_r4:
			qotdlist = json.load(json_file_r4)

		await ctx.send(f'replace the following question by typing your new question below\n "{qotdlist[num-1]}"')
		def qotd_check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		try:
			newq = await self.bot.wait_for('message',check=qotd_check,timeout=60.0)
		except asyncio.TimeoutError:
			await ctx.send('QOTD edit request timed out.')
		else:
			qotdlist[num-1] = newq.content
			await ctx.send('question edited')

		with open('qotd.json', 'w') as json_file_w3:
			json.dump(qotdlist,json_file_w3)
	@commands.command()
	@is_mod()
	async def postqotd(self, ctx):
		dawdle = ctx.guild
		with open('qotd.json', 'r') as json_file_r5:
			qotdlist = json.load(json_file_r5)

		if qotdlist:
			qotdchannel = dawdle.get_channel(687707466179411981)
			qotdbanner = discord.File("qotdbanner.gif")
			await qotdchannel.send(file=qotdbanner)
			qotdbanner = discord.File("qotdbanner.gif")
			await qotdchannel.send(content=f'**Question of the Day**',file=qotdbanner)
			await qotdchannel.send(qotdlist[0])
			del qotdlist[0]
			await ctx.send('qotd posted!')

			with open('qotd.json', 'w') as json_file_w2:
					json.dump(qotdlist, json_file_w2)
		else:
			commandchannel = dawdle.get_channel(654787316665286714)
			await commandchannel.send("I didn't have a QOTD to post today! you'll have to do it manually")

	@tasks.loop(hours=1.0)
	async def qotdcheck(self):
		rightnow = datetime.datetime.utcnow()
		if rightnow.hour == 17:
			for guild in self.bot.guilds:
				if guild.name == 'dawdle':
					dawdle = guild
					break
			qotdchannel = dawdle.get_channel(687707466179411981)
			with open('qotd.json', 'r') as json_file_r2:
				qotdlist = json.load(json_file_r2)

			if qotdlist:
				qotdbanner = discord.File("qotdbanner.gif")
				await qotdchannel.send(file=qotdbanner)
				qotdbanner = discord.File("qotdbanner.gif")
				await qotdchannel.send(content=f'**Question of the Day**',file=qotdbanner)
				await qotdchannel.send(qotdlist[0])
				del qotdlist[0]

				with open('qotd.json', 'w') as json_file_w2:
					json.dump(qotdlist, json_file_w2)
			else:
				commandchannel = dawdle.get_channel(654787316665286714)
				await commandchannel.send("I didn't have a QOTD to post today! you'll have to do it manually")



