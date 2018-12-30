import discord as dsc
import mysql.connector as sql
import configparser as cfg

configuration = cfg.ConfigParser()
configuration.read("discord.ini")

database = sql.connect(user=configuration.get("login","username"), password=configuration.get("login","password"), host=configuration.get("login","host"), database=configuration.get("login","database"))

#Begin SQL function definitions

async def addCharacter(DiscordUser, BeyondID, CharacterName):
    beyondOwner = await getBeyondNameFromDiscord(DiscordUser)
    addchar = ("insert into characters values""(%s, %s, %s") #this query adds an entry for a character to the mysql database.
    data = (BeyondID, beyondOwner, CharacterName)
    cursor = database.cursor()
    cursor.execute(addchar,data)
async def getBeyondNameFromDiscord(DiscordName):
    query = ("select BeyondName from users ""where DiscordName=%s") #this query goes through the database, and returns every dndbeyond username associated with a discord username. there should only be one.
    data = (DiscordName)
    cursor = database.cursor()
    cursor.execute(query, data)
    return cursor[0]
async def getCharacters():
    query = ("select * from characters") #this query gets every character from the database.
    cursor = database.cursor()
    cursor.execute(query)
    return cursor

#End SQL function definitions
#Begin Discord function definitions
async def listChars(message):
    reply = ""
    cursor = await getCharacters()
    for beyondID, BeyondOwner, val in cursor:
        reply += '{}|{} \n '.format(beyondID,BeyondOwner)
        print(beyondID)
        print(BeyondOwner)
    await client.send_message(message.channel, reply)

async def test(message):
    await client.send_message(message.channel, "Hello, World! I\'m Trying out Discord.py for our bot. this way, Shauna should also be able to read the code, once she\'s done with her class.")

async def uid(message):
    await client.send_message(message.channel,message.author)


#End Discord function definitions

CommandsList = {
            "!test": test,
            "!uid":uid,
            "!list":listChars
        }

client = dsc.Client()

commandPrefix = '!'

async def doCommand(message):
    method = CommandsList.get(message.content)
    await method(message)
###Code Below this point shouldn't need to be altered, Ever.
@client.event
async def on_ready():
    print("Logged in")

@client.event
async def on_message(message):
    if message.content.startswith(commandPrefix):
        await doCommand(message)
    
client.run(configuration.get("login", "discordtoken"))
