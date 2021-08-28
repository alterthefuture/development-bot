from discord.ext import commands
import discord
import datetime

class events(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self,member):
		try:
			channel = self.bot.get_channel(879241506408513566)
			await channel.edit(name=f"Members: {len(self.bot.users)}")

			welcome_channel = self.bot.get_channel(879239508770570240)

			embed=discord.Embed(title="Member Joined!",description=f"Welcome {member.mention} to **{member.guild.name}**\n\n**Notice**\nPlease read rules before checking out the server. <#879239879031144488>",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text="© 2021 Ritz Development™", icon_url=self.bot.user.avatar_url)

			await welcome_channel.send(embed=embed)

			welcome_logs = self.bot.get_channel(879436190401585222)

			embed=discord.Embed(description=f"**Welcome Logs |** {member.mention} has joined the server.",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_author(name=f"{member}", icon_url=member.avatar_url)
			embed.set_footer(text=f"ID: {member.id}")

			await welcome_logs.send(embed=embed)
		except:
			return

	@commands.Cog.listener()
	async def on_member_remove(self,member):
		try:
			channel = self.bot.get_channel(879241506408513566)
			await channel.edit(name=f"Members: {len(self.bot.users)}")

			leave_logs = self.bot.get_channel(879436190401585222)

			embed=discord.Embed(description=f"**Leave Logs |** {member.mention} has left the server.",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_author(name=f"{member}", icon_url=member.avatar_url)
			embed.set_footer(text=f"ID: {member.id}")

			await leave_logs.send(embed=embed)
		except:
			return

def setup(bot):
	bot.add_cog(events(bot))