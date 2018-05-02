# KitchenBot
#### Author: Nathan Weinberg
##### Written in Python 3.6

## Purpose
KitchenBot is a GroupMe bot that is designed to send messages to members of a Group at a certain period - in this case a reminder to clean the kitchen. It can also currently respond to HTTP GET and POST requests, the latter in a limited capacity whenever the bot is mentioned in the Group it is present within.

## Setup
GroupMe Bots require an account with GroupMe. They can be created either by API or via form; both methods are described on their Developers site which can be found here: https://dev.groupme.com/

Once done, you will need to incorporate the "bot_id" of your bot into your hosting environment as "GROUPME_BOT_ID". You will also need to incorporate the database URL you are using in the environment as "DATABASE_URL."

### Custom Messaging and Hashing
KitchenBot is currently configured to allow custom messages to be sent through it via an HTML form. To use this form a Web ID (password) is required, which is verified with a passlib SHA256 hash object. To set this value use the following code:

```python
>>> from passlib.hash import pbkdf2_sha256
>>> hash = pbkdf2_sha256.hash("your password")
>>> hash
<SAVE THIS VALUE>
```
Make sure to save the hashed value in your hosting environment as "WEB_ID."

## Usage
KitchenBot is currently configured to be hosted on the Heroku cloud platform using the Heroku Postgres database. All further reading will assume the usage of Heroku and Postgres; however theoretically you can use any hosting/database service.

### Packages
This bot uses the following packages: Flask, Gunicorn, Requests, APScheduler, and passlib, psycopg2. All can be either `pip` installed or found online. Ensure the installed versions match those specified in `requirements.txt`.

### Database Configuration
KitchenBot uses psycopg2 to interact via PostgreSQL with its database. More information on how to use these tools can be found here:

https://devcenter.heroku.com/articles/heroku-postgresql

http://initd.org/psycopg/docs/index.html

## Notes
KitchenBot was based off a tutorial by apnorton, which can be found here: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/

To edit the timezone of a Heroku server, run the following command (your timezone must be in tz database time zone format):

`heroku config:add TZ=<your timezone>`
