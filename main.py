
# СОЗДАЛ BOGO GAMERS

import time
from asyncio import sleep
import yaml
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from mcstatus import MinecraftServer

article_info = [
    {
        'Bot-settings': {
            'token': '',  # Bot's token
            'bot-name': '',  # Bot's name
            'id': '',  # Bot's id
            'prefix': '',  # Bot prefix
            'channel_id': ''  # Message channel
        },

        'Minecraft-settings': {
            'ip': '',
            'port': ''
        }
    }
]

try:
    with open("config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("Чтение завершено")
        print("Запуск бота")

except:

    with open("config.yaml", 'w') as yamlfile:
        data = yaml.dump(article_info, yamlfile)
        print("Файл настроек создан")
        time.sleep(3)
        exit()

try:
    bot: Bot = commands.Bot(command_prefix=data[0]['Bot-settings']['prefix'])
except:
    print('Ошибка:Отсуствует префикс')

try:
    @bot.command(name="статус")
    async def server_info(ctx):
        server = MinecraftServer.lookup(data[0]['Minecraft-settings']['ip'] + ':' + data[0]['Minecraft-settings']['port'])
        author = ctx.message.author
        status = server.status()
        Max = str(status.players.max)
        Online = str(status.players.online)
        await ctx.send(f'Игроков онлайн: ' + Online + f' из ' + Max)
except:
    print("Ошибка:Не найдено имя бота, command 1")
try:
    @bot.command(name="игроки")
    async def players_info(ctx):
        server = MinecraftServer.lookup(data[0]['Minecraft-settings']['ip'] + ':' + data[0]['Minecraft-settings']['port'])
        query = server.query()
        Players = str(query.players.names)
        await ctx.send(f'Игроки на сервере: ' + Players)
except:
    print("Ошибка:Не найдено имя бота, command 2")
try:
    @bot.event
    async def on_ready(count=0, error=0):
        while True:
            try:

                server = MinecraftServer.lookup(data[0]['Minecraft-settings']['ip'] + ':' + data[0]['Minecraft-settings']['port'])
                status = server.status()
                Max = str(status.players.max)
                Online = str(status.players.online)
                activity_string = 'Онлайн: ' + Online + f' из ' + Max
                await bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))
                await sleep(1)
                error = 0
                while count == 0:
                    try:
                        channel = await bot.fetch_channel(data[0]['Bot-settings']['channel_id'])
                        await channel.send('@everyone Сервер запущен')
                    except:
                        print('Ошибка:Не добавлен канал')
                    print("Сотояние сервера: Сервер запущен")
                    count += 1
                print(activity_string)

            except:
                while error == 0:
                    activity_string = 'Сервер отключён'
                    await bot.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))
                    print("Сотояние сервера: Ошибка: Сервер отключён или не верный ip и port")
                    error += 1
                    count = 0
                    try:
                        channel = await bot.fetch_channel(data[0]['Bot-settings']['channel_id'])
                        await channel.send('@everyone Сервер отключён')
                    except:
                        print('Ошибка: Не добавлен id Discord канала')

except:
    print("Ошибка:Не найдено имя бота, command 3")

try:
    bot.run(data[0]['Bot-settings']['token'])
except:
    print('Ошибка:Не найден токен бота')


