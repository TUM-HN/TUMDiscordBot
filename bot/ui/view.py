"""
Contains various views used when interacting with the bot.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""

import discord

from discord.enums import ButtonStyle
from shared import SurveyEntry
from utility import save_survey_entry_to_csv
from datetime import date
from bot.ui.button import DynamicButton


class TutorSessionView(discord.ui.View):
    """Represents a custom UI view.
    A view that is used to collect the student's feedback regarding the specified tutor session with the use of embeded message and buttons.
    The students see the survey as anonymous, but we still save the name of the student for each entry.

    Parameters
    ----------
    *items: :class:`Item`
        The initial items attached to this view.
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    group_id: :class:`str`
        Tutor group id, e.g. 'g5'

    Attributes
    ----------
    timeout: Optional[:class:`float`]
        Timeout from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    children: List[:class:`Item`]
        The list of children attached to this view.
    disable_on_timeout: :class:`bool`
        Whether to disable the view when the timeout is reached. Defaults to ``False``.
    message: Optional[:class:`.Message`]
        The message that this view is attached to.
        If ``None`` then the view has not been sent with a message.
    parent: Optional[:class:`.Interaction`]
        The parent interaction which this view was sent from.
        If ``None`` then the view was not sent using :meth:`InteractionResponse.send_message`.
    group_id: :class:`str`
        Tutor group id.
    """

    def __init__(self, group_id: str):
        super().__init__(timeout=3600, disable_on_timeout=True)
        self.group_id = group_id
        self.users_interacted_with_view = []
        self.users_good_review = []
        self.users_satisfactory_review = []
        self.users_poor_review = []
        self.good_feedback_percentage = 0
        self.mid_feedback_percentage = 0
        self.bad_feedback_percentage = 0
        self.path = f"./data/tutor_session_feedback/{group_id}_{str(date.today())}.csv"

    @discord.ui.button(label="Good", style=ButtonStyle.primary)
    async def good_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id not in self.users_interacted_with_view:
            self.users_interacted_with_view.append(interaction.user.id)
            self.users_good_review.append(
                SurveyEntry(interaction.user.name, {"Feedback": "Good"})
            )
            await interaction.response.edit_message(
                embed=self.update_percentage(interaction.message.embeds[0])
            )
        else:
            # Nothing to update
            await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label="Satisfactory", style=ButtonStyle.primary)
    async def satisfactory_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id not in self.users_interacted_with_view:
            self.users_interacted_with_view.append(interaction.user.id)
            self.users_satisfactory_review.append(
                SurveyEntry(interaction.user.name, {"Feedback": "Satisfactory"})
            )
            await interaction.response.edit_message(
                embed=self.update_percentage(interaction.message.embeds[0])
            )
        else:
            # Nothing to update
            await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label="Poor", style=ButtonStyle.primary)
    async def poor_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id not in self.users_interacted_with_view:
            self.users_interacted_with_view.append(interaction.user.id)
            self.users_poor_review.append(
                SurveyEntry(interaction.user.name, {"Feedback": "Poor"})
            )
            await interaction.response.edit_message(
                embed=self.update_percentage(interaction.message.embeds[0])
            )
        else:
            # Nothing to update
            await interaction.response.edit_message(embed=interaction.message.embeds[0])

    async def on_timeout(self) -> None:
        self.disable_all_items()
        for list in [
            self.users_good_review,
            self.users_satisfactory_review,
            self.users_poor_review,
        ]:
            for entry in list:
                save_survey_entry_to_csv(self.path, entry)
        return await super().on_timeout()

    def update_percentage(self, embed: discord.Embed) -> discord.Embed:
        """
        Updates the percentage for each option in the embed according to the number of entires in the lists and returns the updated Embed variable.

        Args:
            embed :class:`discord.Embed`: Original Embed.

        Returns:
            :class:`discord.Embed`: Updated Embed.
        """
        for field in embed.fields:
            if "Participants" in field.name:
                field.name = "Participants: " + str(
                    len(self.users_interacted_with_view)
                )
            match field.name:
                case "Good":
                    field.value = (
                        "`"
                        + str(
                            format(
                                len(self.users_good_review)
                                / (len(self.users_interacted_with_view) / 100),
                                ".2f",
                            )
                        )
                        + " %`"
                    )
                case "Satisfactory":
                    field.value = (
                        "`"
                        + str(
                            format(
                                len(self.users_satisfactory_review)
                                / (len(self.users_interacted_with_view) / 100),
                                ".2f",
                            )
                        )
                        + " %`"
                    )
                case "Poor":
                    field.value = (
                        "`"
                        + str(
                            format(
                                len(self.users_poor_review)
                                / (len(self.users_interacted_with_view) / 100),
                                ".2f",
                            )
                        )
                        + " %`"
                    )
        return embed


class AnnouncementView(discord.ui.View):
    """Represents a custom UI view.
    Initial view that is attached to the main message.\n
    Allows students to participate in the survey.

    Parameters
    ----------
    *items: :class:`Item`
        The initial items attached to this view.
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    topic: :class:`str`
        The main topic of the current survey.
    guild: :class:`discord.Guild`
        The guild associated with the view.
    views_queue: :class:`list`
        The views queue that will be used to continue the current interaction and extend the survey.


    Attributes
    ----------
    timeout: Optional[:class:`float`]
        Timeout from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    children: List[:class:`Item`]
        The list of children attached to this view.
    disable_on_timeout: :class:`bool`
        Whether to disable the view when the timeout is reached. Defaults to ``False``.
    message: Optional[:class:`.Message`]
        The message that this view is attached to.
        If ``None`` then the view has not been sent with a message.
    parent: Optional[:class:`.Interaction`]
        The parent interaction which this view was sent from.
        If ``None`` then the view was not sent using :meth:`InteractionResponse.send_message`.
    users_interacted_with_view: :class:`list`
        The list of the user ids that interracted with the view.
    topic: :class:`str`
        The main topic of the current survey.
    guild: :class:`discord.Guild`
        The guild associated with the view.
    views_queue: :class:`list`
        The views queue that will be used to continue the current interaction and extend the survey.
    """

    def __init__(self, topic: str, guild: discord.Guild, views_queue: list):
        super().__init__(timeout=8800, disable_on_timeout=True)
        self.users_interacted_with_view = []
        self.topic = topic
        self.guild = guild
        self.views_queue = views_queue

    @discord.ui.button(label="Participate", style=ButtonStyle.green)
    async def participate_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(view=self)
        if interaction.user.id not in self.users_interacted_with_view:
            self.users_interacted_with_view.append(interaction.user.id)
            # Get the view from the queue and remove it.
            next_view = self.views_queue.pop(0)
            await interaction.user.send(
                content=f"```{next_view.display_message}```", view=next_view
            )
        else:
            await interaction.user.send("You've already taken the survey.")


class DifficultyView(discord.ui.View):
    """Represents a custom UI view.
    A view that is used to gather the student's opinion on how challenging the assigned topic was.

    Parameters
    ----------
    *items: :class:`Item`
        The initial items attached to this view.
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    guild: :class:`discord.Guild`
        The guild associated with the view.
    topic: :class:`str`
        The main topic of the current survey.
    message: :class:`str`
        The message that will be displayed with the view.
    views_queue: :class:`list`
        The views queue that will be used to continue the current interaction and extend the survey.
    disable_after_interaction: :class:`bool`
        If the view element(s) must be disabled after the interaction is complete.

    Attributes
    ----------
    timeout: Optional[:class:`float`]
        Timeout from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    children: List[:class:`Item`]
        The list of children attached to this view.
    disable_on_timeout: :class:`bool`
        Whether to disable the view when the timeout is reached. Defaults to ``False``.
    message: Optional[:class:`.Message`]
        The message that this view is attached to.
        If ``None`` then the view has not been sent with a message.
    parent: Optional[:class:`.Interaction`]
        The parent interaction which this view was sent from.
        If ``None`` then the view was not sent using :meth:`InteractionResponse.send_message`.
    users_interacted_with_view: :class:`list`
        The list of the user ids that interracted with the view.
    type: :class:`str`
        The view type.
    guild: :class:`discord.Guild`
        The guild associated with the view.
    topic: :class:`str`
        The main topic of the current survey.
    display_message: :class:`str`
        The message that will be displayed with the view.
    views_queue: :class:`list`
        The views queue that will be used to continue the current interaction and extend the survey.
    disable_after_interaction: :class:`bool`
        If the view element(s) must be disabled after the interaction is complete.
    survey_entry: :class:`shared.entry.SurveyEntry`
        The survey entry that contains the student's name and answers.
    """

    def __init__(
        self,
        guild: discord.Guild | None = None,
        topic: str | None = "Empty",
        display_message: str | None = "Empty",
        views_queue: list | None = None,
        disable_after_interaction: bool | None = False,
    ):
        super().__init__(timeout=1800, disable_on_timeout=True)
        self.users_interacted_with_view = []
        self.type = "Difficutly"
        self.guild = guild
        self.topic = topic
        self.display_message = display_message
        self.views_queue = views_queue
        self.disable_after_interaction = disable_after_interaction
        self.survey_entry = SurveyEntry()
        self.children.append(
            DynamicButton(
                label="Very Easy", style=ButtonStyle.green, view_reference=self
            )
        )
        self.children.append(
            DynamicButton(label="Easy", style=ButtonStyle.primary, view_reference=self)
        )
        self.children.append(
            DynamicButton(
                label="Medium", style=ButtonStyle.primary, view_reference=self
            )
        )
        self.children.append(
            DynamicButton(label="Hard", style=ButtonStyle.primary, view_reference=self)
        )
        self.children.append(
            DynamicButton(label="Very Hard", style=ButtonStyle.red, view_reference=self)
        )


class ScoreView(discord.ui.View):
    """Represents a custom UI view.
    A view that is used to collect students' opinions about the expected grade they will receive for a specified topic.

    Parameters
    ----------
    *items: :class:`Item`
        The initial items attached to this view.
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    guild: :class:`discord.Guild`
        The guild associated with the view.
    topic: :class:`str`
        The main topic of the current survey.
    message: :class:`str`
        The message that will be displayed with the view.
    views_queue: :class:`list`
        The views queue that will be used to continue the current interaction and extend the survey.
    disable_after_interaction: :class:`bool`
        If the view element(s) must be disabled after the interaction is complete.

    Attributes
    ----------
    timeout: Optional[:class:`float`]
        Timeout from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    children: List[:class:`Item`]
        The list of children attached to this view.
    disable_on_timeout: :class:`bool`
        Whether to disable the view when the timeout is reached. Defaults to ``False``.
    message: Optional[:class:`.Message`]
        The message that this view is attached to.
        If ``None`` then the view has not been sent with a message.
    parent: Optional[:class:`.Interaction`]
        The parent interaction which this view was sent from.
        If ``None`` then the view was not sent using :meth:`InteractionResponse.send_message`.
    users_interacted_with_view: :class:`list`
        The list of the user ids that interracted with the view.
    type: :class:`str`
        The view type.
    guild: :class:`discord.Guild`
        The guild associated with the view.
    topic: :class:`str`
        The main topic of the current survey.
    display_message: :class:`str`
        The message that will be displayed with the view.
    views_queue: :class:`list`
        The views queue that will be used to continue the current interaction and extend the survey.
    disable_after_interaction: :class:`bool`
        If the view element(s) must be disabled after the interaction is complete.
    survey_entry: :class:`shared.entry.SurveyEntry`
        The survey entry that contains the student's name and answers.
    """

    def __init__(
        self,
        guild: discord.Guild | None = None,
        topic: str | None = "Empty",
        display_message: str | None = "Empty",
        views_queue: list | None = None,
        disable_after_interaction: bool | None = False,
    ):
        super().__init__(timeout=1800, disable_on_timeout=True)
        self.users_interacted_with_view = []
        self.type = "Score"
        self.guild = guild
        self.topic = topic
        self.display_message = display_message
        self.views_queue = views_queue
        self.disable_after_interaction = disable_after_interaction
        self.survey_entry = SurveyEntry()
        self.children.append(
            DynamicButton(label="20%", style=ButtonStyle.red, view_reference=self)
        )
        self.children.append(
            DynamicButton(label="40%", style=ButtonStyle.primary, view_reference=self)
        )
        self.children.append(
            DynamicButton(label="60%", style=ButtonStyle.primary, view_reference=self)
        )
        self.children.append(
            DynamicButton(label="80%", style=ButtonStyle.primary, view_reference=self)
        )
        self.children.append(
            DynamicButton(label="100%", style=ButtonStyle.green, view_reference=self)
        )
