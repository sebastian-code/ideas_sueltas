""""Python script to handle exams grading, where I made some very opinonated changes,
everything was taken from Twitter user @Turint tweet here:
https://twitter.com/Turint/status/1309999286466342912

To improve code quality I used the following:
    - Black for code style.
    - PyLint for code syntax.
    - MyPy for type validation.

Kudos to Jaime for going with typing early on.
"""
# A list of lists with alumni data.
# TODO Import everything from an Excel/CSV file.
records = (
    ("nombre alumno", "codigo alumno", 39, 45, 76, 77, 98),
    ("nombre alumno", "codigo alumno", 99, 45, 76, 77, 98),
    ("nombre alumno", "codigo alumno", 12, 45, 76, 77, 98),
    ("nombre alumno", "codigo alumno", 5, 45, 76, 77, 98),
    ("nombre alumno", "codigo alumno", 45, 45, 76, 77, 98),
)

# This function handles an unknowk amount of grades per student.
# I dropped typing because the function takes no advantage of using it,
# and there is no standard way to do it in this case.
def alt_grader(*grades):
    lowest_grade = min(grades[0])
    first_average = sum(grades[0]) - lowest_grade / 4
    second_average = first_average / 20
    return round(second_average, 2)


if __name__ == "__main__":
    # Replaced a long for loop with nicer and faster list comprehension.
    [
        print(
            f"El promedio ajustado del estudiante {data[0]}, código {data[1]}, es de {alt_grader(data[2:])}"
        )
        for data in records
    ]
