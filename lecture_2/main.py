import colorama
from datetime import datetime
from typing import Any


def generate_profile(age: int) -> str:
    """
    This function determines life stage based on its age.
    "Child" for 0-12, "Teenager" for 13-19, "Adult" for 20 and more
    :param age: user's age (int)
    :return: life stage (string)
    """
    if age >= 20:           # condition for adult
        return "Adult"
    if 13 <= age <= 19:     # condition for teenager
        return "Teenager"
    if 0 <= age <= 12:      # condition for child
        return "Child"


def count_age(birth_year_int: int) -> int:
    """
    Counts user's age on a basis of current year
    :param birth_year_int: user's birth year (int)
    :return: user's age (int)
    """
    # determining current year
    current_year = datetime.today().year

    # counting age
    age = current_year - birth_year_int

    return age


def validate_age(age: int) -> None:
    """
    Validates age to be positive and less than 150, otherwise raises ValueError
    :param age: user's age (int)
    :return: None
    """
    # checking lower border
    if age < 0:
        raise ValueError("Your age is less than 0")

    # checking upper border
    elif age > 150:
        raise ValueError("Your age is greater than 150")


# Get user input

current_age: int = 0
user_name: str = input("Hey! Enter your full name: ").strip()  # asking user's full name and removing whitespaces
print("Great! ", end='')
while True:
    birth_year_str: str = input("Enter your birth year: ")  # asking user's birth year

    try:
        birth_year: int = int(birth_year_str)  # converting birth year from string into integer
    except ValueError:
        print("Error! You should type your birth year only with digits. Let's do it again")
        continue  # if check failed, asking again birth year

    current_age: int = count_age(birth_year)  # calculating user's current age

    try:
        validate_age(current_age)  # checking if age value is valid
        break  # if no errors occurred, exit from the loop and move on
    except ValueError as e:
        print("Error! " + str(e) + ". Let's do it again")
        continue  # if check failed, asking again birth year
print("Wonderful! ", end='')

hobbies: list[str] = []  # list for user's hobbies
stop_input: str = "stop"  # if user inputs that, loop stops
print('Please enter your favourite hobby or type "stop" to finish: ', end='')  # Asking user to type hobbies

while True:
    hobby: str = input().strip()  # saving user's input into 'hobby', removing whitespaces

    if hobby.lower() == stop_input:  # check if user typed stop (case-insensitive)
        break  # exit the loop (stop asking)

    hobbies.append(hobby)  # if loop is continuing, add saved hobby into the hobbies list
    print('Great! Now you can add another your hobby or type "stop" to finish: ', end='')  # asking user for new input
    # end of iteration


# Process and generate the Profile

life_stage: str = generate_profile(current_age)  # determining user's current life stage
user_profile: dict[str: Any] = {  # creating dictionary for user's info
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies
}


# Display the output

colorama.init()  # Initializing colorama for cross-platform colored terminal output

print("-" * 3)  # begin summary
print(f"{colorama.Fore.MAGENTA}Profile summary: {colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.GREEN}Full name: {colorama.Fore.CYAN}{user_profile['name']}{colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.GREEN}Age: {colorama.Fore.CYAN}{user_profile['age']}")
print(f"{colorama.Fore.GREEN}Life stage: {colorama.Fore.CYAN}{user_profile['stage']}")

if len(user_profile['hobbies']) == 0:  # check if hobbies were filled
    print(f"{colorama.Fore.YELLOW}You didn't mention any hobbies.{colorama.Style.RESET_ALL}")

else:
    print(f"{colorama.Fore.GREEN}Favourite hobbies ({len(user_profile['hobbies'])}): ")

    for user_hobby in hobbies:  # display user hobbies
        print(f"{colorama.Fore.CYAN}• {user_hobby}{colorama.Style.RESET_ALL}")

print(f"-" * 3)  # end summary
