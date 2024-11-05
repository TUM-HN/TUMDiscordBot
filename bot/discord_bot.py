"""
Discord Bot
~~~~~~~~

A basic bot created for the tutors and instructors of the Introductory Programming course.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""

import asyncio
import datetime
import json
import random
import discord
import time
import datetime
import utility
import re

from bot import bot_data
from bot.ui.view import TutorSessionView, DifficultyView, ScoreView, AnnouncementView
from os import path
from threading import Thread
from discord import option
from discord.ext import commands

##################################
#              INIT              #
##################################

bot = commands.Bot(
    intents=discord.Intents.all(),
    status=discord.Status.streaming,
    activity=discord.Streaming(
        name="Coding with Jimbo", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ),
)

###########################################
#              BOT FUNCTIONS              #
###########################################


def start(token) -> None:
    """
    Startup function.

    Args:
        token :class:`str`: The bot token to use.
    """

    # Verify if the file exists
    if path.isfile(".secrets.json") is False:
        raise FileNotFoundError("Secrets file not found!")

    # Read the credentials
    with open(".secrets.json") as sf:
        secrets = json.load(sf)

    # Run the bot.
    bot.run(secrets[token])


def _verify_author_roles(user: discord.User | discord.Member) -> bool:
    """
    Ensure that the user has the required role to use the command.

    Args:
        user :class:`User` | :class:`Member`: The user whose roles are to be verified.
    """
    access_roles = [
        1170005834336571412,
        1163821146832130053,
        1163821146832130055,
        1170716415205068843,
    ]
    for role in user.roles:
        if role.id in access_roles:
            return True
    return False


def _lectures_loop(
    quiz_view: discord.ui.View,
    lecture_view: discord.ui.View,
    category_id=1163821148069441566,
    timeout=30,
) -> None:
    """
    A loop running on a background thread.
    Uses asyncio to run async functions on the bot event loop.

    Args:
        quiz_view :class:`discord.ui.View`: View used for the quiz survey.
        lecture_view :class:`discord.ui.View`: View used for the lecture survey.
        category_id :class:`int`: ID of the category where the new text channel should be created.
        timeout :class:`int`: How many seconds we should wait for a result before raising an error.
    """

    asyncio.set_event_loop(bot.loop)
    while True:
        if len(bot_data.lectures.keys()) > 0:
            key_to_remove = None
            for key in bot_data.lectures:
                # Create the expected date by spliting the key from dictionary.
                key_split = key.split("-")
                expected_date = datetime.date(
                    year=int(key_split[0]),
                    month=int(key_split[1]),
                    day=int(key_split[2]),
                )

                # The time (hour, minute) should be changed for testing.
                # Send the lecture beginning message.
                if _time_check(expected_date, 9, 29, 35):
                    # Key that will be removed from the dictionary.
                    key_to_remove = key

                    # At the beginning create the new text channel.
                    test_guild = bot.guilds[0]
                    text_channel = asyncio.run_coroutine_threadsafe(
                        coro=test_guild.create_text_channel(
                            name=f"lecture-{datetime.date.today()}",
                            category=test_guild.get_channel(category_id),
                            topic="Lecture Channel",
                            nsfw=False,
                        ),
                        loop=bot.loop,
                    ).result(timeout)

                    # Send the welcome message with topics list.
                    _send_message_in_text_channel(
                        text_channel=text_channel,
                        message=f"```\nHello, welcome to the lecture!\nThe content of today's lecture is the following:\n{_get_topics(bot_data.lectures.get(key))}\n```",
                        timeout=timeout,
                    )

                    # Wait N seconds before sending the quiz survey.
                    # In this case 5 minutes, until the end of the quiz.
                    time.sleep(300)
                    if _time_check(expected_date, 9, 34, 45):
                        # Send the quiz survey.
                        _send_message_in_text_channel(
                            text_channel=text_channel,
                            message="```\nPlease share your opinion on the quiz.\n```",
                            timeout=timeout,
                            view=quiz_view,
                        )

                    # Wait N seconds before sending the lecture survey.
                    # In this case 6 hours, until the end of the lecture.
                    time.sleep(21600)
                    if _time_check(expected_date, 15, 0, 59):
                        # Send the lecture survey.
                        _send_message_in_text_channel(
                            text_channel=text_channel,
                            message="```\nWe hope you enjoyed our lecture, please tell us how difficult the content presented was for you?\n```",
                            timeout=timeout,
                            view=lecture_view,
                        )

            # Remove the old lecture key.
            if key_to_remove is not None:
                bot_data.lectures.pop(key_to_remove)
                key_to_remove = None

            # Wait one minute before trying again.
            time.sleep(60)
        else:
            # Finish the execution since there are no more elements in the dictionary.
            break


def _time_check(
    expected_date: datetime.date, hour: int, minute_start: int, minute_end: int
) -> bool:
    """
    Verify that the expected date is equal to the current date,
    then verify if the current iteration is within the expected time period (e.g. 14:01 - 14:15).

    Args:
        expected_date :class:`datetime.date`:
        hour :class:`int`: Expected hour.
        minute_start :class:`int`: Beginning of the time period.
        minute_end :class:`int`: End of the time period.

    Returns:
        :class:`bool`: Result of the comparison.
    """
    todays_date = datetime.datetime.now()
    return (
        expected_date.year == todays_date.year
        and expected_date.month == todays_date.month
        and expected_date.day == todays_date.day
        and todays_date.hour == hour
        and todays_date.minute > minute_start
        and todays_date.minute < minute_end
    )


def _get_topics(topics_list: list) -> str:
    """
    Converts a list of topics to a string that contains each topic with its index on different lines.

    Args:
        topics_list :class:`list`: List that contains lecture topics.

    Returns:
        :class:`str`: String that represents the topics list.
    """
    topics = ""
    for topic in topics_list:
        topics = topics + str((topics_list.index(topic) + 1)) + ". " + topic + "\n"
    return topics


def _send_message_in_text_channel(
    text_channel: discord.TextChannel,
    message: str,
    timeout: int,
    view: discord.ui.View | None = None,
) -> None:
    """
    Send a message in the text channel with the use of threadsafe operations.
    Uses asyncio to run async functions on the bot event loop.

    Args:
        text_channel :class:`discord.TextChannel`: Text channel to use.
        message :class:`str`: Actual message to send.
        timeout :class:`int`: How many seconds we should wait for a result before raising an error.
    """
    asyncio.run_coroutine_threadsafe(
        coro=text_channel.send(content=message, view=view),
        loop=bot.loop,
    ).result(timeout=timeout)


########################################
#              BOT EVENTS              #
########################################


@bot.event
async def on_ready() -> None:
    # Views creation is deprecated, don't use this code.
    # Create views for the background process.
    # quiz_view_for_thread = get_view("quiz", bot)
    # lecture_view_for_thread = get_view("lecture", bot)
    # # Uncomment when the lecture_loop function is ready or is being tested.
    # background_thread = Thread(
    #     target=_lectures_loop,
    #     args=(
    #         quiz_view_for_thread,
    #         lecture_view_for_thread,
    #     ),
    #     daemon=True,
    # )
    # background_thread.start()
    print(
        f'-----\nLogged in as {bot.user.name}.\nWith the bot id="{bot.user.id}"\n-----'
    )


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == (bot.user or message.author.bot):
        return

    message_content = message.content.lower()

    # Only check for the attendance message when the input is 2 characters and includes g for the group.
    if len(message_content) == 2 and "g" in message_content:
        await utility.add_student_to_attendance_list(
            message=message,
            group=bot_data.group_1,
            status=bot_data.group_1_status,
            id="g1",
        )
        await utility.add_student_to_attendance_list(
            message=message,
            group=bot_data.group_2,
            status=bot_data.group_2_status,
            id="g2",
        )
        await utility.add_student_to_attendance_list(
            message=message,
            group=bot_data.group_3,
            status=bot_data.group_3_status,
            id="g3",
        )
        await utility.add_student_to_attendance_list(
            message=message,
            group=bot_data.group_4,
            status=bot_data.group_4_status,
            id="g4",
        )
        await utility.add_student_to_attendance_list(
            message=message,
            group=bot_data.group_5,
            status=bot_data.group_5_status,
            id="g5",
        )


################################################
#              BOT SLASH COMMANDS              #
################################################


@bot.slash_command(description="Ping-Pong game.")
async def ping(ctx: discord.ApplicationContext) -> None:
    await ctx.respond(f"Pong! Answered with the {random.randrange(0, 1000)} ms delay.")


@bot.slash_command(description="Greets the user.")
async def hello(ctx: discord.ApplicationContext) -> None:
    await ctx.respond(
        f"Hello {ctx.author.mention}! I hope you have a nice day. :blush:"
    )


@bot.slash_command(description="Deletes the specified amount of messages from channel.")
@option(
    "limit",
    description="Enter the number of messages.",
    min_value=0,
    default=0,
)
async def clear(ctx: discord.ApplicationContext, limit: int) -> None:
    if _verify_author_roles(ctx.author):
        await ctx.channel.purge(limit=limit)
        await ctx.respond("Channel cleared!")
        await ctx.channel.purge(limit=1)
    else:
        await ctx.respond(bot_data.PERMISSION_DENIED)


@bot.slash_command(
    name="give-student-role",
    description="Gives users without roles (just with @everyone) a student role.",
)
async def give_student_role(ctx: discord.ApplicationContext) -> None:
    student_role = ctx.guild.get_role(1170006871713796208)
    if _verify_author_roles(ctx.author):
        await ctx.respond("Adding new roles! It can take some time...")
        members = ctx.guild.members
        for member in members:
            # Avoid discord complaints
            time.sleep(0.5)
            # User without roles should get a Student role.
            if len(member.roles) == 1:
                await member.add_roles(student_role)
        await ctx.channel.send("New roles have been added!")
    else:
        await ctx.respond(bot_data.PERMISSION_DENIED)


@bot.slash_command(
    name="attendance",
    description="Start or stop the attendance check for the specified group.",
)
@option(
    "status",
    description='Enter "start" to begin the check or "stop" to end it.',
)
@option(
    "group_id",
    description="Enter the group id (e.g. g5).",
)
async def attendance(
    ctx: discord.ApplicationContext,
    status: str,
    group_id: str,
) -> None:
    match status.lower():
        case "start":
            if _verify_author_roles(ctx.author):
                await ctx.respond(
                    f"{ctx.author.mention}, accepting messages in DM for the group {group_id.lower()}."
                )
                utility.update_dm_accept_status(group_id.lower())
            else:
                await ctx.respond(bot_data.PERMISSION_DENIED)
        case "stop":
            if _verify_author_roles(ctx.author):
                await ctx.respond(
                    f"{ctx.author.mention}, messages in DM are no longer accepted for the group {group_id.lower()}."
                )
                # Send the tutor students list.
                tutor_dm = await ctx.author.create_dm()
                embed = discord.Embed(
                    title=f"Tutor Group {group_id} Attendance", colour=ctx.author.colour
                )
                embed.add_field(
                    name="Students List",
                    inline=False,
                    value=utility.prepare_group_list_for_embed(group_id.lower()),
                )
                await tutor_dm.send(embed=embed)

                # Cleanup
                utility.attendance_cleanup(group_id=group_id.lower())
            else:
                await ctx.respond(bot_data.PERMISSION_DENIED)
        case _:
            await ctx.respond(
                f'{ctx.author.mention}, can not recognize the status argument. Please make sure to use "start" or "stop" for the status argument.'
            )


@bot.slash_command(
    name="tutor-session-feedback",
    description="Allows students to leave feedback on tutor sessions.",
)
@option(
    "group_id",
    description="Enter your group id.",
)
async def tutor_session_feedback(
    ctx: discord.ApplicationContext,
    group_id: str,
) -> None:
    if _verify_author_roles(ctx.author):
        default_value = "`0 %`"
        embed = discord.Embed(title="Tutor Session Feedback", colour=ctx.author.color)
        embed.add_field(name="Participants: 0", inline=False, value="")
        embed.add_field(name="Good", inline=True, value=default_value)
        embed.add_field(name="Satisfactory", inline=True, value=default_value)
        embed.add_field(name="Poor", inline=True, value=default_value)
        embed.set_author(
            name="Author: " + ctx.author.display_name, icon_url=ctx.author.avatar.url
        )
        await ctx.respond(
            embed=embed,
            view=TutorSessionView(group_id=group_id),
        )
    else:
        await ctx.respond(bot_data.PERMISSION_DENIED)


@bot.slash_command(
    name="create-complex-survey",
    description="Create a multiple question survey.",
)
@option("message", description="Survey announcement message.")
@option(
    "main_topic",
    description='The main topic of the survey, e.g. "exercise T01E01".',
)
@option(
    "channel", discord.TextChannel, description="The channel to publish the survey."
)
async def create_complex_survey(
    ctx: discord.ApplicationContext,
    message: str,
    main_topic: str,
    channel: discord.TextChannel,
) -> None:
    # Default author check.
    def is_valid_response(m: discord.Message):
        return m.author == ctx.author

    # Button list verification.
    def is_valid_buttons_list(buttons: list) -> bool:
        if len(buttons) == 0:
            return False

        for button in buttons:
            if button != "Difficulty" and button != "Score":
                return False

        return True

    # Start the interaction.
    await ctx.respond(
        "```Please send a list of the questions that should be included in the survey, you have five minutes to respond.\nYour message must be in the following format:\n"
        + "1. Question 1\n2. Question 2\n...\nn. Question n```"
    )

    # Message processing, create a list only with the questions/button types.
    def get_list(response: discord.Message) -> list:
        temp = []
        temp_split = re.split(r"\d\.", response.content)
        # First element is empty, so remove it.
        temp_split.pop(0)
        # Remove the new line character and space at the beginning for each question.
        for string in temp_split:
            if string.index(" ") == 0:
                temp.append(string.replace("\n", "").replace(" ", "", 1))
            else:
                temp.append(string.replace("\n", ""))
        return temp

    # Get list of the questions.
    try:
        response: discord.Message = await bot.wait_for(
            "message", check=is_valid_response, timeout=300.0
        )
    except TimeoutError:
        return await ctx.send_followup("Sorry, you took too long to respond.")

    questions = get_list(response=response)
    print(questions)
    if len(questions) == 0:
        await ctx.send_followup(
            "Invalid question list provided, interaction aborted.\nPlease try again later."
        )
        return
    else:
        await ctx.send_followup(
            "```Please send a list of the button type that should be used for each question, you have five minutes to respond."
            + "\nThere are two supported button types: 'Difficulty' and 'Score', make sure to write the types without any typos!"
            + "\nYour message must be in the following format:\n"
            + "1. ButtonType 1\n2. ButtonType 2\n...\nn. ButtonType n```"
        )

    # Get list of the button types.
    try:
        response: discord.Message = await bot.wait_for(
            "message", check=is_valid_response, timeout=300.0
        )
    except TimeoutError:
        return await ctx.send_followup("Sorry, you took too long to respond.")

    button_types = get_list(response=response)
    if is_valid_buttons_list(button_types):
        await ctx.send_followup(
            "Creating the multiple question survey, it may take some time."
        )
    else:
        await ctx.send_followup(
            "Invalid button type list provided, interaction aborted.\nPlease try again later."
        )
        return

    if len(questions) != len(button_types):
        await ctx.send_followup(
            "The number of questions is not equal to the number of button types, interaction aborted.\nPlease try again later"
        )
        return

    # Prepare the dictionary with the views.
    views_queue = []
    for type in button_types:
        match (type):
            case "Difficulty":
                views_queue.append(
                    DifficultyView(
                        guild=ctx.guild,
                        topic=main_topic,
                        display_message=questions.pop(0),
                        views_queue=views_queue,
                        disable_after_interaction=True,
                    )
                )
            case "Score":
                views_queue.append(
                    ScoreView(
                        guild=ctx.guild,
                        topic=main_topic,
                        display_message=questions.pop(0),
                        views_queue=views_queue,
                        disable_after_interaction=True,
                    )
                )

    await channel.send(
        content=f"```{message}```",
        view=AnnouncementView(
            topic=main_topic, guild=ctx.guild, views_queue=views_queue
        ),
    )


@bot.slash_command(
    name="create-simple-survey", description="Create a one question survey."
)
@option("message", description="Survey announcement message.")
@option(
    "button_type",
    description="The button that will be attached to the survey.",
    choices=["Difficulty", "Score"],
)
@option(
    "main_topic",
    description='The main topic of the survey, e.g. "exercise T01E01".',
)
@option(
    "channel", discord.TextChannel, description="The channel to publish the survey."
)
async def create_simple_survey(
    ctx: discord.ApplicationContext,
    message: str,
    button_type: str,
    main_topic: str,
    channel: discord.TextChannel,
):
    await ctx.respond("Creating the survey, it may take some time.")

    # Prepare the view.
    view = (
        DifficultyView(guild=ctx.guild, topic=main_topic, display_message=message)
        if button_type == "Difficulty"
        else ScoreView(guild=ctx.guild, topic=main_topic, display_message=message)
    )

    await channel.send(content=f"```{message}```", view=view)
