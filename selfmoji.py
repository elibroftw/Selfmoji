import os
import re
import json
from typing import Optional

import crayons
from discord.ext import commands

bot = commands.Bot(command_prefix='``', self_bot=True)

config = {  # default
    'size': 64,
    'edit': True,
    'token': '',
    'emojis': {}
}

emojis = config['emojis']

sizes = {16, 32, 64, 128, 256, 512}


def to_int(s: str) -> int:
    try:
        i = int(s)
    except:
        raise ValueError(f'[{s}] is not a number')
    if i in sizes: return i
    raise ValueError(f'[{s}] is not in {sizes}')


def save_config():
    with open('config.json', 'w') as fp:
        json.dump(config, fp)


def read_config():
    global config, emojis
    try:
        with open('config.json') as fp:
            config = json.load(fp)
            emojis = config['emojis']
    except (FileNotFoundError, json.JSONDecodeError):
        save_config()


def get_token() -> str:
    if tok := os.getenv('DISCORD_TOKEN'):
        print(crayons.green('LOADED token from environment'))
        return tok
    token = config.get('token', '')
    if token != '': return token
    print('Enter Discord token:')
    print('HOW TO: https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs#how-to-get-a-user-token')
    token = input().replace('"', '')
    config['token'] = token
    save_config()
    return token


def main():
    print(crayons.green('Starting'))
    read_config()
    print(crayons.green(f"Emoji size: [{config['size']}]"))
    if config.get('token') == '': print(crayons.red(f'ERROR: token not found'))
    print(crayons.green(f"Message editing is {'enabled' if config['edit'] else 'disabled'}"))

    try:
        print(crayons.green(f'Loaded [{len(emojis)}] emojis'))
        print(crayons.cyan(str(list(emojis.keys()))))
    except EnvironmentError as enve:
        print(crayons.yellow(enve))
    try:
        bot.run(get_token(), bot=False)
    finally:
        print(crayons.yellow('SAVING CONFIG'))
        save_config()


@bot.command()
async def flush(ctx):
    try:
        save_config()
        print(crayons.green('Saved emojis'))
    finally:
        await ctx.message.delete()


@bot.command()
async def add(ctx, name, link):
    try:
        print(crayons.yellow(f'Registering emoji [{name}] with [{link}]'))
        emojis[name.strip()] = re.sub(r'&size=\d{2,3}', '', link.strip())
    finally:
        await ctx.message.delete()


@bot.command()
async def delete(ctx, name):
    try:
        name = name.strip()
        if name in emojis:
            print(crayons.yellow(f'Deleting emoji [{name}]'))
            del emojis[name.strip()]
        else:
            print(crayons.red(f'There is no emoji named [{name}]'))
    finally:
        await ctx.message.delete()


@bot.command()
async def rename(ctx, original, newname):
    try:
        original = original.strip()
        newname = newname.strip()
        if newname in emojis:
            print(crayons.red(f'Emoji [{newname}] already exists!'))
        elif original in emojis:
            print(crayons.yellow(f'Renaming emoji [{original}] to [{newname.strip()}]'))
            emojis[newname.strip()] = emojis[original]
            del emojis[original]
        else:
            print(crayons.red(f'There is no emoji named [{original}]'))
    finally:
        await ctx.message.delete()


@bot.command()
async def size(ctx, _size: Optional[str] = None):
    if _size:
        try:
            __size = to_int(size)
            print(crayons.yellow(f"Setting emoji size to {__size}"))
            config['size'] = __size
        except ValueError as ve:
            print(crayons.red(f"Error parsing input: {ve}"))
        finally:
            await ctx.message.delete()
    else:
        await ctx.send(f"Emoji size is `[{config['size']}]`")


@bot.command()
async def edit(ctx, opt: Optional[bool] = None):
    try:
        if opt is None:
            config['edit'] = not config['edit']
        else:
            config['edit'] = opt
        save_config()
    finally:
        print(crayons.cyan(f"Changed edit to [{config['edit']}]"))
        await ctx.message.delete()


@bot.command(aliases=['list'])
async def _list(ctx):
    # await ctx.message.delete()
    await ctx.send(f'There are `[{len(emojis)}]` emojis: `{list(emojis.keys())}`')


@bot.command()
async def slist(ctx):
    try:
        print(crayons.cyan(f'There are [{len(emojis)}] emojis: {list(emojis.keys())}'))
    finally:
        await ctx.message.delete()


@bot.event
async def on_command_error(ctx, error):
    print(crayons.red(error))


@bot.event
async def on_ready():
    print(crayons.green('ready!'))


@bot.event
async def on_message(message):
    if message.author != bot.user:
        return

    async def do_emoji(content, _size=None):
        if content not in emojis: return
        if not _size: _size = config['size']
        emoji = emojis[content] + f"&size={_size}"
        if config['edit']: await message.edit(content=emoji)
        else:
            await message.delete()
            await message.channel.send(emoji)

    content = message.content.strip()
    if match := re.match(r'`(\w+) (\d+)`', content):
        try:
            await do_emoji(match.group(1), to_int(match.group(2)))
        except Exception as e:
            if isinstance(e, ValueError):
                print(crayons.red(f'Error parsing input: {e}'))
            else:
                print(crayons.red(f'Unknown exception: {e}'))
            await message.delete()
    elif match := re.match(r'`([\w ]+)`', content):
        await do_emoji(match.group(1))
    else:
        await bot.process_commands(message)


if __name__ == "__main__":
    main()
