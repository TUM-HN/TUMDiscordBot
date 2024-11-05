"""
Main
~~~~~~~~

Used to run the specified version of the bot on different discord servers.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""

import bot

bot_version = input(
    "What version of the bot would you like to work with? (MAIN or DEV)\n"
)
if bot_version == "MAIN":
    bot.start("TOKEN")
elif bot_version == "DEV":
    bot.start("DEV_TOKEN")
else:
    print("Incorrect bot version!")
