students: list[dict] = []  # stores student's data
menu_options: list[str] = [
    "Add a new student",
    "Add grades for a student",
    "Show report (all students)",
    "Find top performer",
    "Exit"
]
forbidden_names: list[str] = [
    "1",
    "2",
    "3",
    "4",
    "5"
]
sep_line = "-" * 10  # line to print to separate menu views


def get_student_index(stud_name: str) -> int:
    """
    Search a student list for a student name
    :param stud_name: student's name to search
    :return: student's index in the list, if student have not been found returns -1
    """
    stud_name = stud_name.strip().capitalize()
    for cur_index, stud in enumerate(students):
        if stud['name'] == stud_name:
            return cur_index
    else:
        return -1


def check_grade(grade: int) -> bool:
    """
    Checks if grade is valid (in range of [0;100]
    :param grade: student's grade
    :return: True if grade is valid, else False
    """
    return 0 <= grade <= 100


while True:
    print(sep_line)
    for i, menu_option in enumerate(menu_options):
        print(f"{i + 1}. {menu_option}")
    user_choice: str = input("Your choice: ")

    match user_choice:
        #  "Add a new student"
        case '1':
            print(sep_line)
            print("Add a new student")
            new_name: str = input("Enter new student's name: ")
            new_name = new_name.strip().capitalize()

            if new_name in forbidden_names:
                print("Sorry, you cannot use that name")
                continue

            i = get_student_index(new_name)
            if i != -1:  # check if student's name already exists
                print("Sorry, a student with that name already exists")
                continue

            new_student: dict = {
                "name": new_name,
                "grades": []
            }
            students.append(new_student)
            print(f"Student {new_student['name']} successfully added")
            continue

        case '2':
            # "Add grades for a student"
            print(sep_line)
            print("Add grades for a student")

            if len(students) == 0:
                print("There are no students. Firstly you should add a student")
                continue

            student_name: str = input("Enter a student's name: ")
            student_index: int = get_student_index(student_name)
            if student_index == -1:  # check if student's name exists
                print("Cannot find a student with that name")
                continue

            while True:
                try:
                    user_input: str = input("Enter a grade (or 'done' to finish): ").strip().lower()
                    if user_input == 'done':
                        break

                    student_grade = int(user_input)
                    if not check_grade(student_grade):
                        print("Error! Wrong grade value, it must be from 0 to 100")
                    else:
                        students[student_index]['grades'].append(student_grade)
                except ValueError:
                    print("Error! Invalid input, please enter a number")

        case "3":
            # "Show report (all students)"
            print(sep_line)
            print("Show report")

            if len(students) == 0:
                print("There are no students at the moment")
                continue

            avg_grades: list[int] = []  # list to store all avg grades
            for student in students:
                try:
                    avg: int = sum(student['grades']) / len(student['grades'])
                    print(f"{student['name']}'s average grade is {avg}")
                    avg_grades.append(avg)
                except ZeroDivisionError:
                    print(f"{student['name']}'s average grade is N/A")

            if len(avg_grades) == 0:
                print("There are no students with grades")
                continue

            print(f"\nMax average: {max(avg_grades)}")
            print(f"Min average: {min(avg_grades)}")
            print(f"Overall average: {sum(avg_grades) / len(avg_grades)}")

        case "4":
            # "Find top performer"
            print(sep_line)
            print("Find top performer")

            if len(students) == 0:
                print("There are no students added")
                continue

            top_student: dict = max(
                students, key=lambda x: 0 if len(x['grades']) == 0 else (sum(x['grades']) / len(x['grades']))
            )

            if not top_student['grades']:
                print("No one student has grades")
                continue

            print(f"Top student: {top_student['name']} "
                  f"with average grade of {sum(top_student['grades']) / len(top_student['grades'])}")

        case "5":
            # "Exit"
            break
