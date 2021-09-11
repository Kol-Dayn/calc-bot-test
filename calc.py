import discord
from discord.ext import commands
# do pip install discord-components to install lib
from discord_components import *
import datetime
 
client = commands.Bot(command_prefix = '+')
client.remove_command('help')
 
@client.event
async def on_ready():
    #turns on discord components lib
    DiscordComponents(client)
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(name=f'+calc', type= discord.ActivityType.watching))
    print('Login!')
 
#buttons array
buttons = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blue, label='×'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blue, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blue, label='+'),
        Button(style=ButtonStyle.red, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blue, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
]
 
#calculates answer
def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occurred.'
    return result
 
@client.command()
async def calc(ctx):
    m = await ctx.send(content='Калькулятор создан')
    expression = 'Введите пример..'
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(title=f'Калькулятор - {ctx.author.name} | {ctx.author.id}', color=0xf5ce42, description=expression,
                        timestamp=delta)
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await client.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[
            0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression == 'Введите пример..' or expression == 'An error occurred.':
                expression = ''
            if res.component.label == 'Exit':
                await res.respond(content='Калькулятор закрыт!', type=7)
                break
            elif res.component.label == '←':
                expression = expression[:-1]
            elif res.component.label == 'Clear':
                expression = 'Введите пример..'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression += res.component.label
            f = discord.Embed(title=f'Калькулятор - {res.author.name} | {res.author.id}', color=0xf5ce42, description=expression,
                                timestamp=delta)
            await res.respond(content='', embed=f, components=buttons, type=7)
 
client.run('ODg2MTAzNDQ0NzIzNzU3MTI2.YTwuJA.QA0CxHUNLekC4NmlzZWpVetsi-M')