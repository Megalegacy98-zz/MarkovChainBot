import discord
import markov
import random
import requests

bot = discord.Client()

@bot.event
async def on_ready():
	# tells the hoster that the bot is ready to recieve messages/commands
	print("Going through on ready")

@bot.event
async def on_message(message):
	# check if the message is from the user (since it's a self bot, if you don't want to make it a self bot, do:
	# if message.author != bot.user
	if message.author == bot.user:
		
		# set up variables
		input = ""
		final_sentence = ""
		
		# assert that it got the message
		print("Got message: " + message.content)
		
		# if the command is run
		if message.content.startswith('./markov'):
			# get the user's name
			user = message.content[message.content.index("v") + 2:]
			
			# loop through all channels (only general for now)
			for channel in message.server.channels:
				if channel.name == "general":
					# alerts hoster it's looking through a channel for messages
					print("GOING THROUGH " + channel.name)
					
					# try getting logs
					try:
						async for mes in bot.logs_from(channel, limit=5000):
							if mes.author == message.server.get_member_named(user):
								print(mes.content)
								
								input += mes.content + " "
					# if that's not possible (lack of perms for example) then go to the next channel
					except:
						continue
					
			# for each index in a random number between 10 and 20
			for a in range(random.randint(10, 20)):
				# if index is 0
				if(a == 0):
					# make first sentence have upper case letter
					final_sentence += markov.get_random_phrase(input)
					final_sentence = final_sentence[0].upper() + final_sentence[1:]
					final_sentence += " "
				else:
					# do it normally
					final_sentence += markov.get_random_phrase(input)
					final_sentence += " "
			# replace whitespace with period
			final_sentence = final_sentence[:len(final_sentence)-1] + "."
			
			# send the message
			await bot.send_message(message.channel, "```From: {0}\n\nTo: {1}\n\n\n{2}```".format(bot.user.name, user, final_sentence))
		
		if message.content.startswith("./attachmarkov"):
			print(message.attachments)
			if len(message.attachments) != 1:
				await bot.send_message(message.channel, "```ERROR:\n\nYou need one attachment```")
			else:
				final_sentence = ""
				attachment = message.attachments[0]
				input = requests.get(attachment["url"]).text
				
				for a in range(random.randint(10, 20)):
					# if index is 0
					if(a == 0):
						# make first sentence have upper case letter
						final_sentence += markov.get_random_phrase(input)
						final_sentence = final_sentence[0].upper() + final_sentence[1:]
						final_sentence += " "
					else:
						# do it normally
						final_sentence += markov.get_random_phrase(input)
						final_sentence += " "
				# replace whitespace with period
				final_sentence = final_sentence[:len(final_sentence)-1] + "."
				
				await bot.send_message(message.channel, "```{0}```".format(final_sentence))
				
				
							
	else:
		return

bot.run("token", bot=False)