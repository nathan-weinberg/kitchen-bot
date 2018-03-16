# KitchenBot
#### Author: Nathan Weinberg
##### Written in Python 3.6

## Purpose
KitchenBot is a GroupMe bot currently under development that is designed to send messages to members of a Group at a certain period - in this case a reminder to clean the kitchen. It can also currently respond to HTTP GET and POST requests, the latter in a limited capacity whenever the bot is mentioned in the Group it is present within.

## Setup
GroupMe Bots require an account with GroupMe. They can be created either by API or via form; both methods are described on their Developers site which can be found here: https://dev.groupme.com/

Once done, you will need to incorporate the "bot_id" of your bot into your hosting environment as "GROUPME_BOT_ID".

## Usage
KitchenBot must be hosted on a platform of some sort; personally I use the Heroku cloud platform.

### Packages
This bot uses the following packages: Flask, Gunicorn, Requests, and APScheduler. All can be either `pip` installed or found online. Ensure the installed versions match those specified in `requirements.txt`.

## Notes
KitchenBot was based off a tutorial by apnorton, which can be found here: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/