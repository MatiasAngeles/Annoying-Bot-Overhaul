# Crear un bot en la variable cliente y transferirle los privilegios
from bot import intents


from discord.ext.commands import commands


bot = commands.bot(command_prefix="$",intents=intents)