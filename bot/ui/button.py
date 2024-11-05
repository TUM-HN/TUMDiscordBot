"""
Contains various buttons used when interacting with the bot.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""

import discord

from datetime import date
from utility import save_survey_entry_to_csv
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji


class DynamicButton(discord.ui.Button):
    """Represents a custom UI button.

    Parameters
    ----------
    style: :class:`discord.ButtonStyle`
        The style of the button.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
    url: Optional[:class:`str`]
        The URL this button sends you to.
    disabled: :class:`bool`
        Whether the button is disabled or not.
    label: Optional[:class:`str`]
        The label of the button, if any. Maximum of 80 chars.
    emoji: Optional[Union[:class:`.PartialEmoji`, :class:`.Emoji`, :class:`str`]]
        The emoji of the button, if available.
    row: Optional[:class:`int`]
        The relative row this button belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    view_reference :class:`discord.ui.View`
        The reference to the parent view, required to update the state and correct data processing.
    """

    def __init__(
        self,
        *,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | Emoji | PartialEmoji | None = None,
        row: int | None = None,
        view_reference: discord.ui.View,  # DifficultyView or ScoreView
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self.view_reference = view_reference

    async def callback(self, interaction: Interaction):
        # Verify if the user has already interacted with the view.
        def can_interact() -> bool:
            if (
                interaction.user.id
                not in self.view_reference.users_interacted_with_view
            ):
                self.view_reference.users_interacted_with_view.append(
                    interaction.user.id
                )
                return True
            return False

        async def disable_after_interaction() -> None:
            if self.view_reference.disable_after_interaction:
                self.view_reference.disable_all_items()
                await interaction.message.edit(view=self.view_reference)

        def save_student_name() -> None:
            # Get the student name.
            if self.view_reference.survey_entry.student_name == "":
                self.view_reference.survey_entry.student_name = (
                    self.view_reference.guild.get_member(
                        interaction.user.id
                    ).display_name
                )

        # Save the answer to the file if no other elements are in the views queue.
        if (
            self.view_reference.views_queue == None
            or not self.view_reference.views_queue
        ):
            # User can interact with the view only once
            if can_interact():
                # Respond to the user.
                await interaction.response.defer()
                await interaction.user.send(
                    content="```Thank you for your feedback!```"
                )

                # Disable view elements if necessary.
                await disable_after_interaction()

                # Get the student name.
                save_student_name()
                # Get the student answer.
                self.view_reference.survey_entry.selected_options.update(
                    {f"{self.view_reference.type}": self.label}
                )

                # Save the student answer to the file.
                save_survey_entry_to_csv(
                    path=f"./data/exercise_feedback/{self.view_reference.topic}_{str(date.today())}.csv",
                    entry=self.view_reference.survey_entry,
                )
            else:
                # Ignore the current interaction attempt.
                await interaction.response.defer()
        else:
            if can_interact():
                # Disable view elements if necessary.
                await disable_after_interaction()

                # Get the next view
                index = len(self.view_reference.views_queue)
                next_view = self.view_reference.views_queue.pop(0)

                # Get the student name.
                save_student_name()
                # Get the student answer.
                self.view_reference.survey_entry.selected_options.update(
                    {f"{self.view_reference.type}{index}": self.label}
                )

                # Pass the current survey_entry to the next view.
                next_view.survey_entry = self.view_reference.survey_entry

                await interaction.response.send_message(
                    content=f"```{next_view.display_message}```", view=next_view
                )
            else:
                # Ignore the current interaction attempt.
                await interaction.response.defer()
