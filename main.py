import json

import requests
from telebot import TeleBot

from consts import BASE_URL

token = None

with open("token.txt") as f:
    token = f.read().strip()

bot = TeleBot(token)


def get_user_token(user_id):
    with open("database.json", 'r') as f:
        db = json.load(f)
        return db.get(user_id)


def add_new_token(user_id, user_token):
    with open("database.json", 'r+') as f:
        db = json.load(f)
        db[user_id] = user_token
        json.dump(db, f)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    if not get_user_token(user_id):
        add_new_token(user_id, message.text.split()[-1])
        bot.reply_to(message, "Welcome to Party Bot")
    else:
        bot.reply_to(message, "Error, user id is already set")


@bot.message_handler(commands=["create_event"])
def create_event(message):
    user_id = message.from_user.id
    data_blocks = message.text.split('"')
    data_blocks = [block for block in data_blocks if bool(block.strip())]
    data = {
        "name": data_blocks[1],
        "description": data_blocks[2],
        "starts_at": data_blocks[3],
        "ends_at": data_blocks[4]
    }

    result = requests.post(f"{BASE_URL}/event", json=data, headers={"auth_telegram_token": get_user_token(user_id)})
    bot.reply_to(message, str(result.json()))


@bot.message_handler(commands=["get_events"])
def get_events(message):
    user_id = message.from_user.id
    result = requests.get(f"{BASE_URL}/event", headers={"auth_telegram_token": database[user_id]})
    bot.reply_to(message, str(result.json()))


@bot.message_handler(commands=["update_event"])
def update_event(message):
    bot.reply_to(message, "Welcome to Party Bot")


@bot.message_handler(commands=["delete_event"])
def delete_event(message):
    bot.reply_to(message, "Welcome to Party Bot")


bot.infinity_polling()
