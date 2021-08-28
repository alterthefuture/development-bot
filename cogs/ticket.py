from pymongo import MongoClient
from discord.ext import commands
from helper import *
import datetime
import asyncio

# Connecting to database
cluster = MongoClient("mongodb+srv://lxyOT:luxalmao2021!@alterdev.xqt1i.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["alter"]
collection = db["server"]

# Creating commands
class ticket(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def ticket(self,ctx):
		if ctx.channel.id != 879241056842043412:
			await ctx.message.delete()
			return await ctx.send(embed=create_embed(f"{ctx.author.mention} if you want to create a ticket, go to <#879241056842043412>"),delete_after=5)

		if ctx.author.id in collection.find_one({"_id": ctx.guild.id})["ticket_users"]:
			await ctx.message.delete()
			return await ctx.author.send(embed=create_embed(f"{ctx.author.mention} you already have a ticket created, Please close it to create a new one."))

		try:
			for category in ctx.guild.categories:
				if category.id == 879441889349238826:
					break

			ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[-1]) + 1
			ticket_channel = await category.create_text_channel(f"ticket {ticket_num}", permission_synced=True)

			await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

			embed=discord.Embed(title="Ticket Opened",description=f"Support will be with you shortly. Use `!close` to close the ticket.",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_footer(text="© 2021 Alters Development™",icon_url=self.bot.user.avatar_url)
			await ticket_channel.send(f"{ctx.author.mention} Welcome!", embed=embed)

			collection.update_one({"_id": ctx.guild.id}, {"$push": {"ticket_users": ctx.author.id}})
			collection.update_one({"_id": ctx.guild.id}, {"$push": {"ticket_channels": ticket_channel.id}})

			ticket_logs = self.bot.get_channel(879436225537278032)

			embed=discord.Embed(description=f"**Ticket Logs |** {ctx.author.mention} created the ticket **{ticket_channel}** -> <#{ticket_channel.id}>",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
			embed.set_footer(text=f"ID: {ctx.author.id}")

			await ticket_logs.send(embed=embed)
		except:
			return await ctx.send(embed=create_embed(f"Failed to create ticket channel."),delete_after=5)

	@commands.command()
	async def close(self,ctx,member:discord.Member=None):
		if ctx.channel.id not in collection.find_one({"_id": ctx.guild.id})["ticket_channels"]:
			await ctx.message.delete()
			return await ctx.send(embed=create_embed(f"{ctx.author.mention} this channel is not a ticket channel."),delete_after=5)

		if member == None:
			return await ctx.send(embed=create_embed(f"Please mention the user who created the ticket."),delete_after=5)

		if member.id not in collection.find_one({"_id": ctx.guild.id})["ticket_users"]:
			await ctx.message.delete()
			return await ctx.send(embed=create_embed(f"{member.mention} does not own a ticket."),delete_after=5)

		try:
			await ctx.send(embed=create_embed("Closing ticket in a few seconds..."))
			await asyncio.sleep(2)
			await ctx.channel.delete()

			collection.update_one({"_id": ctx.guild.id}, {"$pull": {"ticket_channels": ctx.channel.id}})
			collection.update_one({"_id": ctx.guild.id}, {"$pull": {"ticket_users": member.id}})

			ticket_logs = self.bot.get_channel(879436225537278032)

			embed=discord.Embed(description=f"**Ticket Logs |** {member.mention} closed the ticket **{ctx.channel}**",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
			embed.set_author(name=f"{member}", icon_url=member.avatar_url)
			embed.set_footer(text=f"ID: {member.id}")

			await ticket_logs.send(embed=embed)
		except:
			return await ctx.send(embed=create_embed(f"Failed to delete ticket channel."),delete_after=5)

	@commands.command()
	@commands.is_owner()
	async def tc(self,ctx):
		embed=discord.Embed(description="To create a ticket type `!ticket`",colour=0x00FFFF,timestamp=datetime.datetime.utcnow())
		embed.set_author(name=f"Purchase Product")
		embed.set_footer(text="© 2021 Alters Development™",icon_url=self.bot.user.avatar_url)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(ticket(bot))