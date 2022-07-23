import discord
from discord.ext import commands
import config
from discord import utils

class Main(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.change_presence(
			activity=discord.Streaming(name=' ', url='https://www.twitch.tv/regzoom')
		)
		
		for guild in self.bot.guilds:
			if guild.id == config.GUILD_ID:
				voice = utils.get(
					guild.voice_channels,
					id=config.VOICE_ID,
				)
				await voice.connect()

		print("Ready in discord")



	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id == config.POST_ID:
			channel = self.bot.get_channel(payload.channel_id) # получаем объект канала
			message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
			guild = message.guild
			member = utils.get(guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
			try:
				emoji = str(payload.emoji) # эмоджик который выбрал юзер
				role = utils.get(guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
			
				if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
					await member.add_roles(role)
					print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
				else:
					await message.remove_reaction(payload.emoji, member)
					print('[ERROR] Too many roles for user {0.display_name}'.format(member))
			
			except KeyError as e:
				print('[ERROR] KeyError, no role found for ' + emoji)
			except Exception as e:
				print(repr(e))
 
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		channel = self.bot.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
		try:
			emoji = str(payload.emoji) # эмоджик который выбрал юзер
			role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
 
			await member.remove_roles(role)
			print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
		except KeyError as e:
			print('[ERROR] KeyError, no role found for ' + emoji)
		except Exception as e:
			print(repr(e))

	@commands.command()

	async def asd(self, ctx):
		emb = discord.Embed(title = 'Правила нашего дискорд сервера', description = '```Основные```\n**Не использовать наш сервер для комерческой деятельности, рекламы/распостронения сторонних серверов и т.д** - наказание: БАН\n\n**Пропоганда наркотиков/суицида/терроризма, материалы содержащие сцены сексуального и шокирующего характера и т.д** - наказание: БАН\n\n**Запрещенно копирование профилей администрации, провокационные, шокирующие название личных комнат или ролей** - наказание: БАН\n\n**Запрещенно распостронение личной информации без согласия её владельца** - наказание: БАН\n\n**Запрещенно использовать другую учетную запись, чтобы избежать наложения на вас наказаний или фарма валюты сервера** - наказание: БАН\n\n**Администрация может выдавать наказания по своему усмотрению если считает, что ваши действия могут идти во вред участникам, а так же препятствовать их общению** - наказание: БАН\n\n**Запрещено разжигание национальной розни, дискриминация, сексизм, врождебность к любым религиозным круппам и людям с ограниченными возможностями** - наказание: МУТ/БАН\n\n**Запрещенны деструктивные действия по отношению к серверу: неконструктивная критика в сторону модерации, призывы покинуть сервер, попытки привескти к помехам в процессе развития сервера** - наказание: МУТ/БАН', colour = discord.Color.from_rgb(48,52,52))

		emb.set_image(url = '')

		await ctx.send(embed = emb)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		role= discord.utils.get(member.guild.roles, id = 999551351161884703)
		await member.add_roles(role)
		print('роль asd выдана')

async def setup(bot):
	await bot.add_cog(Main(bot))