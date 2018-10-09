# KitchenBot
#### Author: Nathan Weinberg
##### Written in Python 3.6

## Purpose
KitchenBot is a GroupMe bot that is designed to send messages to members of a Group at a certain period - in this case a reminder to clean the kitchen. It can also currently respond to HTTP GET and POST requests, the latter in a limited capacity whenever the bot is mentioned in the Group it is present within.

## Setup
GroupMe Bots require an account with GroupMe. They can be created either by API or via form; both methods are described on their Developers site which can be found [here](https://dev.groupme.com/).

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

### Sentiment Analysis
Using IBM Watson's Tone Analyzer API, KitchenBot can response to messages that don't have a preset response, based off their perceived tone. An IBM Cloud account is required for this feature to work.

Make sure to save your service username and password in your hosting environment as "IBM_USERNAME" and "IBM_PASSWORD", respectively. More information on the usage of this API can be found [here](https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/python.html?python).

## Usage
KitchenBot is currently configured to be hosted on the Heroku cloud platform using the Heroku Postgres database. All further reading will assume the usage of Heroku and Postgres; however theoretically you can use any hosting/database service.

### Packages
This bot uses the following packages: Flask, Gunicorn, Requests, APScheduler, passlib, psycopg2, and watson_developer_cloud. All can be either `pip` installed or found online. Ensure the installed versions match those specified in `requirements.txt`.

### Database Configuration
KitchenBot uses psycopg2 to interact via PostgreSQL with its database. More information on how to use these tools can be found [here](https://devcenter.heroku.com/articles/heroku-postgresql) and [here](http://initd.org/psycopg/docs/index.html).

## Migration
To move your bot from one GroupMe group to another, perform the following steps:

- Create a new GroupMe bot associated with your new group. The callback URL should be the same.
- Change your "GROUPME_BOT_ID" environmental variable to match the bot ID of your newly created-bot.
- Make appropriate changes to source code/database system

## Notes
KitchenBot was based off a tutorial by apnorton, which can be found [here](http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/).

To edit the timezone of a Heroku server, run the following command (your timezone must be in tz database time zone format):

`heroku config:add TZ=<your timezone>`

### Clock Sleeping Issue
The free tier of Heroku puts your app to sleep after a certain amount of time. This can lead to issues with the clock functions firing. This can be mitigated by using a third-party service to keep your app awake such as [Kaffeine](https://kaffeine.herokuapp.com/).
