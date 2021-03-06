# Selfmoji

![video](https://i.imgur.com/Jf1kGKm.gif)

Do you like Discord? Do you like using emojis? Do you not like paying for Nitro:tm:?

With selfmoji you can have your own custom emojis in Discord.

## Installing

1. Clone repository
2. `pip install -r requirements.txt`
3. Place your discord token into config.json (see Sample Config)
4. Run the appropriate run script (Windows: run.bat)
5. See (this)[https://medium.com/@elijahlopezz/python-and-background-tasks-4f70b4a2efd8] to run script on startup

## Sample Config
```json
{
    "size": 64,
    "edit": true,
    "token": "",
    "emojis": {}
}
```

## Sending emojis

send `` `[emoji-name]` `` or `` `[emoji-name] [size]` `` where `[size]` is one of `16, 32, 64, ..., 512`

e.g. `` `weirdchamp` `` or `` `weirdchamp 256` ``

Send the `weirdchamp` emoji, first using the currently configured size, second explicitly using size `256`

If editing is enabled the bot will edit the message to be the desired emote, if editing is disabled the bot will delete the message and send a new one with the emote

If using the first form, the bot uses the currently configured size

## How Does it Work?

Selfmoji is a self-bot, it listens to your messages and acts accordingly. The bot links a discord emoji and sets the size using a URL parameter.

## The Problem with Mobile

In classic Discord:tm: fashion mobile doesn't handle this particularly well, while desktop Discord will size the emotes properly mobile finds the need to increase the size arbitrarily.

## Share Emojis

Selfmoji saves emoji in a file called `emojis.dict` in the format `emoji-name : link`

You can add emojis here manually and share with friends

## Commands

The bot uses the prefix `` as it's not likely to collide with anything else

### Add Emoji

``` ``add [emoji-name] [emoji-link] ```

e.g. ``` ``add sparklecat https://cdn.discordapp.com/emojis/654099753340239872.gif ```

![laugh](https://i.imgur.com/fuCfyS2.gif)

### Delete Emoji

``` ``remove [emoji-name] ```

### Rename Emoji

``` ``rename [current-name] [new-name] ```

### List Available Emoji

``` ``list ```

> Sends a message into the current chat listing all the emojis

``` ``slist ```

> **S**ilent list, sends a list of all emoji into the console

### Set Emoji Size

``` ``size [pixel-size] ```

Where `[pixel-size]` is one of `16, 32, 64, 128, 256, 512`

### Get the current size

``` ``size ```

> Sends a message to the current chat

### Enable / Disable Message Editing

``` ``edit ```

> Toggles editing

``` ``edit [true|yes|on] ```

> Enables editing

``` ``edit [false|no|off] ```

> Disables editing
