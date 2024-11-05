"""
Entry
~~~~~~~~

Contains a SurveyEntry class.

:copyright: (c) 2023-present Ivan Parmacli
:license: MIT, see LICENSE for more details.
"""


class SurveyEntry:
    """
    Represents a survey entry.

    Parameters
    ----------
    student_name :class:`str`
        Name of the student.
    selected_options :class:`dict`
        The dictionary that contains survey option key mapped to the student answer.
    """

    def __init__(
        self,
        student_name: str | None = "",
        selected_options: dict | None = None,
    ):
        self.student_name = student_name
        self.selected_options = {} if selected_options == None else selected_options
