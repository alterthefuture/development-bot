from discord.ext import commands
from helper import *
import discord
import datetime

class verify(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def verify(self,ctx):
		if ctx.channel.id != 879238478175555650:
			await ctx.message.delete()

		try:
			verify_role = discord.utils.get(ctx.guild.roles, name="community")
			await ctx.author.add_roles(verify_role)

			embed=discord.Embed(description=f"You have been successfully verified in **{ctx.guild.name}**, please enjoy your stay!\n\n - <#879239879031144488>\n - <#879240476287467541>",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_author(name="Verification Success")
			embed.set_footer(text="© 2021 Ritz Development™",icon_url=self.bot.user.avatar_url)

			await ctx.author.send(embed=embed)

			verify_logs = self.bot.get_channel(879436262447136858)

			embed=discord.Embed(description=f"**Verify Logs |** {ctx.author.mention} has successfully verified.",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
			embed.set_footer(text=f"ID: {ctx.author.id}")

			await verify_logs.send(embed=embed)
		except:
			return

	@commands.command()
	@commands.is_owner()
	async def vc(self,ctx):
		embed=discord.Embed(description="To gain access to the server type `!verify`",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
		embed.set_author(name=f"Verify")
		embed.set_footer(text="© 2021 Ritz Development™",icon_url=self.bot.user.avatar_url)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(verify(bot))