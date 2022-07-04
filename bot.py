import telebot
import random

bot = telebot.TeleBot('5414710410:AAHIn7GcUXxrK8XTeR_cHwxHybNMvmSvMiQ')

generatedLines = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Hi, this is a pickup line bot. Choose a category and I'll generate a pickup line for you!")

@bot.message_handler(commands=['generate'])
def get_pick_up_line(message):
	bot.send_message(message.chat.id,'Please wait while we generate a pick up line...')
	file = open('generatedLines.txt', 'r')
	generateLinesArr = file.read().split('\n')
	ind = random.randint(0,len(generateLinesArr)-1)
	line = generateLinesArr[ind]
	if line not in generatedLines:
		bot.send_message(message.chat.id, line)

@bot.message_handler(commands=['end'])
def send_welcome(message):
	generatedLines = []
	bot.send_message(message.chat.id, "Thank you for using the bot. Hope you had fun!")


bot.polling()