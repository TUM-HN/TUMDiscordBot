"""
Function Utils
~~~~~~~~

Contains various functions required for the different elements of the bot.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""

import discord
import csv
import bot

from bot import bot_data
from shared import SurveyEntry

################################################################
#               TUTOR SESSION FEEDBACK FUNCTIONS               #
################################################################

DEFAULT_CASE_WARNING = "Incorrect group id."


async def add_student_to_attendance_list(
    message: discord.Message, group: list, status: bool, id: str
) -> None:
    """
    Adds a student to the specified group, only works if the student is in the INFUN server.

    Args:
        message :class:`discord.Message`: The message sent by the user.
        group :class:`list`: List of participants of the tutor group.
        status :class:`bool`: Indicates whether attendance verification has started.
        id :class:`str`: The ID of the tutor group.
    """

    current_guild = bot.bot.guilds[0]
    member = current_guild.get_member(message.author.id)
    if status and message.content.lower() == id and member.display_name not in group:
        group.append(member.display_name)
        await message.channel.send("You are added to the attendance list.")


def attendance_cleanup(group_id: str) -> None:
    """
    Reset the specified group status and clear the students group list.

    Args:
        group_id :class:`str`: The ID of the tutor group.
    """
    match group_id:
        case "g1":
            bot_data.group_1.clear()
            bot_data.group_1_status = False

        case "g2":
            bot_data.group_2.clear()
            bot_data.group_2_status = False

        case "g3":
            bot_data.group_3.clear()
            bot_data.group_3_status = False

        case "g4":
            bot_data.group_4.clear()
            bot_data.group_4_status = False

        case "g5":
            bot_data.group_5.clear()
            bot_data.group_5_status = False

        case _:
            raise RuntimeWarning(DEFAULT_CASE_WARNING)


def prepare_group_list_for_embed(id: str) -> str:
    """
    Adds a new line character for each student name, so that it will be displayed correctly in the embed.

    Args:
        id :class:`str`: The ID of the tutor group.

    Raises:
        :class:`RuntimeWarning`: Occurs when the tutor's group ID does not exist.

    Returns:
        :class:`str`: A list of students.
    """
    text = ""
    match id:
        case "g1":
            for entry in bot_data.group_1:
                text += entry + "\n"
            return text

        case "g2":
            for entry in bot_data.group_2:
                text += entry + "\n"
            return text

        case "g3":
            for entry in bot_data.group_3:
                text += entry + "\n"
            return text

        case "g4":
            for entry in bot_data.group_4:
                text += entry + "\n"
            return text

        case "g5":
            for entry in bot_data.group_5:
                text += entry + "\n"
            return text

        case _:
            raise RuntimeWarning(DEFAULT_CASE_WARNING)


def update_dm_accept_status(id: str) -> None:
    """
    Set the specified group status to True, so the messages from the students will be accepted by the bot.

    Args:
        id :class:`str`: The ID of the tutor group.

    Raises:
        :class:`RuntimeWarning`: Occurs when the tutor's group ID does not exist.
    """
    match id:
        case "g1":
            bot_data.group_1_status = True

        case "g2":
            bot_data.group_2_status = True

        case "g3":
            bot_data.group_3_status = True

        case "g4":
            bot_data.group_4_status = True

        case "g5":
            bot_data.group_5_status = True

        case _:
            raise RuntimeWarning(DEFAULT_CASE_WARNING)


####################################################################
#               Saving the SurveyEntry to a CSV File               #
####################################################################


def save_survey_entry_to_csv(path: str, entry: SurveyEntry) -> None:
    """
    Adds the student's answers to the csv file.

    Args:
        path :class:`str`: The path to the file.
        entry :class:`SurveryEntry`: The survey entry that contains the student's answers.
    """
    # Create the file if it doesn't exist.
    open(file=path, mode="a").close()

    header = list(entry.selected_options.keys())
    header.insert(0, "Name")
    # Write the data to a file.
    with open(file=path, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=header,
        )
        if verify_entry_not_in_csv(path=path, entry="Name"):
            writer.writeheader()

        # Create a row from the dictionary.
        row = {"Name": entry.student_name}
        for key in entry.selected_options.keys():
            row.update({key: entry.selected_options.get(key)})

        if verify_entry_not_in_csv(path=path, entry=entry.student_name):
            writer.writerow(rowdict=row)


def verify_entry_not_in_csv(path: str, entry: str) -> bool:
    """
    Verify whether an entry already exists in the csv file.

    Args:
        path :class:`str`: The path to the file.
        entry :class:`str`: String to check.

    Returns:
        :class:`bool`: Whether an entry already exists in the csv file.
    """

    with open(file=path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if entry in row:
                return False
        return True
