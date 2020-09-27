""""Python script to handle exams grading, taken from Twitter user @Turint
tweet here https://twitter.com/Turint/status/1309999286466342912
"""


def grade_exams(
    first_note: int,
    second_note: int,
    third_note: int,
    fourth_note: int,
    fifht_note: int,
):
    lowest_grade = min(first_note, second_note, third_note, fourth_note, fifht_note)
    average_grade = (
        sum(first_note, second_note, third_note, fourth_note, fifht_note)
        - lowest_grade / 100
    )


if __name__ == "__main__":
    pass
