#!/usr/bin/env python3
# Copyright 2020 - David Todd (c0de@c0defox.es)
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

"""
    This file contains the web server for a simple bookmarking application
"""

import os
import _thread
from bottle import Bottle, run, response, route, template
from api import API
from telethon.sync import TelegramClient, events

_api = API()

# Load in the API tokens required for a telegram bot
api_id = os.environ.get('telethon_api_id', False)
api_hash = os.environ.get('telethon_api_hash', False)
api_token = os.environ.get('telethon_token', False)

# Create an instance of the Telethon bot
if api_id and api_hash and api_token:
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=api_token)
else:
    bot = False

bot_state = False

@bot.on(events.NewMessage)
async def handle_message_events(event):
    if 'start' in event.raw_text:
        await event.reply('started')

def start_bot_thread():
    """
        We run the telegram bot in a seperate thread
        to be able to also serve the HTTP content.

        The bot thread will be idle most of the time
        due to the async nature of it, and the fact
        that it won't receive much traffic
    """
    bot.start()
    bot.run_until_disconnected()

@route('/')
def index():
    return "This is the index"

# I haven't figured out how to get these routes inside the API yet...
@route('/save/<title>/<uri:path>')
def save_bookmark(title, uri):
    return _api.save_bookmark(title, uri)

@route('/getall')
@route('/get/all')
def get_all_bookmarks():
    return _api.get_all_bookmarks()

@route('/get/<bookmark_id>')
def get_bookmark(bookmark_id):
    return _api.get_bookmark(bookmark_id)

@route('/delete/<bookmark_id>')
def delete_bookmark(bookmark_id):
    return _api.delete_bookmark(bookmark_id)

@route('/update/title/<bookmark_id>/<title>')
def update_bookmark_title(bookmark_id, title):
    return _api.update_bookmark_title(bookmark_id, title)

@route('/update/uri/<bookmark_id>/<uri:path>')
def update_bookmark_uri(bookmark_id, uri):
    return _api.update_bookmark_uri(bookmark_id, uri)

if __name__ == '__main__':
    # Start the Telegram bot and the bottle server
    _thread.start_new_thread(start_bot_thread, ())
    run(host='localhost', port=8080)
