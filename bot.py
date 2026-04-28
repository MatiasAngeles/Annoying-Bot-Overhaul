from settings import settings
import discord
from discord.ext import commands
from bot_logic import * 
import asyncio
import os
from bot_logic import get_dog_image_url
from red import classified

# Intents del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello. |:(')

@bot.command()
async def bye(ctx):
    await ctx.send('😒')

@bot.command()
async def password(ctx, cantidad: int):
    await ctx.send(gen_pass(cantidad))

@bot.command()
async def guess(ctx):
    await ctx.send('Guess a number between **1 and 10**.')

    def is_correct(m):
        return (
            m.author == ctx.author and
            m.channel == ctx.channel and
            m.content.isdigit()
        )

    answer = random.randint(1, 10)

    try:
        guess_msg = await bot.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.send(f'Sorry, you took too long. The number was **{answer}**.')

    if int(guess_msg.content) == answer:
        await ctx.send('That is correct.')
    else:
        await ctx.send(f'NO! The number was **{answer}**.')

@bot.group()
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
async def mem1(ctx):
    with open('images/meme1.jpeg', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def mem_random(ctx):
    # Diccionario de memes con rareza (pesos)
    memes_raros = {
        "meme1.jpeg": 10,   # común
        "meme2.jpeg": 8,    # menos común
        "meme3.jpeg": 4,    # raro
        "meme4.jpeg": 2,    # muy raro
        "meme5.jpeg": 1     # legendario
    }

    # Selección ponderada por rareza
    memes = list(memes_raros.keys())
    pesos = list(memes_raros.values())

    meme_elegido = random.choices(memes, weights=pesos, k=1)[0]

    with open(f'images/{meme_elegido}', 'rb') as f:
        picture = discord.File(f)

    await ctx.send(file=picture)

@bot.command('dog')
async def dog(ctx):
    '''Una vez que llamamos al comando dog, 
    el programa llama a la función get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attactment in ctx.message.attachments:
            file_name = attactment.filename
            file_url = attactment.url
            await attactment.save(f"./images/{file_name}")
            await ctx.send("Your Stupid File is Saved. |:(")
    else:
        await ctx.send("Get An Attachment, Idiot.")

@bot.command()
async def classifyai(ctx):
    if ctx.message.attachments:
        for attactment in ctx.message.attachments:
            file_name = attactment.filename
            file_url = attactment.url
            await attactment.save(f"./images/{file_name}")
            await ctx.send(classified(f"./images/{file_name}"))
    else:
        await ctx.send("Get An Attachment, Idiot.")

bot.run("Token Here")