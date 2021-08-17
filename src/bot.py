#bot.py

import os
import discord
from discord.utils import find
from dotenv import load_dotenv
import random
from random import choice
import sqlite3

#bot commands import
from discord.ext import commands


#retreive token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


#Setup bot, and command prefix
bot = commands.Bot(command_prefix='!')


#on_ready function to connect bot to Discord & DB
@bot.event
async def on_ready():
    db = sqlite3.connect('restaurants.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants(
        name TEXT UNIQUE
        )
        ''')
    print(f'{bot.user.name} has connected to Discord.')


#Bot message when it joins a new server
@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}! Thank you for inviting me to your server!'.format(guild.name))



#Bot commands


#Hello
@bot.command(name='hello', help='Just saying hello.')
async def hello(ctx):
    await ctx.send('Hello')


#Roll Dice
@bot.command(name='rolldice', help='Simulate rolling dice. Speficy x dice, and y sides.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    try:
        dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
        ]
        embed = discord.Embed(title="Roll Dice", description=", ".join(dice))
        await ctx.send(embed=embed)
    except:
        embed1 = discord.Embed(title="Roll Dice", description="An error has occurred.\nMake sure after you type the command you also specify x dice, and y sides.")
        await ctx.send(embed=embed1)


#Coin Flip
determine_flip = [1,0]
@bot.command(name='coinflip', help='Flip a coin.')
async def coinflip(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="Coinflip", description="Heads.")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Coinflip", description="Tails.")
        await ctx.send(embed=embed)


#Add restaurant
@bot.command(name='addrestaurant', help='Add a restaurant to the DB. Wrap name in quotation marks (" ").')
async def addrestaurant(ctx, name):
    db = sqlite3.connect('restaurants.sqlite')
    cursor = db.cursor()
    try:    
        cursor.execute(f"INSERT INTO restaurants(name) VALUES(\'{name}\')")
        embed = discord.Embed(title="Add Restaurant", description=f"{name} has been added")
        await ctx.send(embed = embed)
    except:
        embed1 = discord.Embed(title="Add Restaurant", description=f"Either the name you entered is already in the database, or an error has occurred. Do not use any apostrophes (') when typing the name of the restaurant.")
        await ctx.send(embed=embed1)
    db.commit()
    cursor.close()
    db.close()
    

#View all restaurants in db
@bot.command(name='restaurants', help='See all restaurants in the DB.')
async def viewrestaurants(ctx):
    db = sqlite3.connect('restaurants.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM restaurants")
        result = cursor.fetchall()
        embed = discord.Embed(title="Restaurants", description=result)
        await ctx.send(embed=embed)
    except:
        embed1 = discord.Embed(title="Restaurants", description="An error has occurred.")
        await ctx.send(embed=embed1)
    db.commit()
    cursor.close()
    db.close()

#Randomly choose a restaurant
@bot.command(name='whattoeat', help='Randomly picks a restaurant from the DB.')
async def whattoeat(ctx):
    db = sqlite3.connect('restaurants.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM restaurants ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchall()
        embed = discord.Embed(title="What to Eat?", description=f"You should eat {result}!")
        await ctx.send(embed=embed)
    except:
        embed1 = discord.Embed(title="Restaurants", description="An error has occurred.")
        await ctx.send(embed=embed1)
    db.commit()
    cursor.close()
    db.close()

#Info
@bot.command(name='info', help='Some information about me.')
async def info(ctx):
    embed = discord.Embed(title="Info", description="This is the second bot created by Alex Samaroo (Judgement Kazzy#5298 on Discord).\nIt\'s a general-purpose bot that does a variety of things.")
    await ctx.send(embed=embed)

#API Token for bot
bot.run(TOKEN)