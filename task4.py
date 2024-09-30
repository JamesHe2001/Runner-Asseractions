from runner import Runner
from competition import Competition
from custom_errors import *


def create_runner(runner_name: str, runner_age: str, runner_country: str, sprint_speed: str, endurance_speed: str):
    """Creates a Runner object with the given parameters, performing input validation.

    Args:
        runner_name (str): The name of the runner.
        runner_age (str): The age of the runner (to be converted to int).
        runner_country (str): The country of the runner.
        sprint_speed (str): The sprint speed of the runner (to be converted to float).
        endurance_speed (str): The endurance speed of the runner (to be converted to float).

    Returns:
        Runner: A Runner object if creation is successful, otherwise None.
    """
    runner_name = runner_name.strip()
    runner_country = runner_country.strip()
    try:
        runner_age = int(runner_age.strip())
        sprint_speed = float(sprint_speed.strip())
        endurance_speed = float(endurance_speed.strip())
    except ValueError:
        print("ERROR : runner_age should be an integer, sprint_speed and endurance_speed should be floats")
        return None
    try:
        runner = Runner(runner_name, runner_age, runner_country, sprint_speed, endurance_speed)
    except CustomTypeError as e:
        print("ERROR : ", e)
        return None
    except CustomValueError as e:
        print("ERROR : ", e)
        return None
    return runner

def create_competition(runners: list, rounds: str, distances_short: str, distances_long: str):
    """Creates a Competition object with the given parameters, performing input validation.

    Args:
        runners (list): A list of Runner objects participating in the competition.
        rounds (str): The number of rounds in the competition (to be converted to int).
        distances_short (str): A comma-separated string of sprint distances (to be converted to a list of floats).
        distances_long (str): A comma-separated string of marathon distances (to be converted to a list of floats).

    Returns:
        Competition: A Competition object if creation is successful, otherwise None.
    """
    try:
        rounds = int(rounds)
        distances_short = list(map(float, distances_short.strip().split(',')))
        distances_long = list(map(float, distances_long.strip().split(',')))
    except ValueError:
        print("ERROR : rounds should be an integer, distances should be floats")
        return None
    try:
        comp = Competition(runners, rounds, distances_short, distances_long)
    except CustomTypeError as e:
        print("ERROR : ", e)
        return None
    except CustomValueError as e:
        print("ERROR : ", e)
        print("Reminding you that the number of distances should be equal to the number of rounds")
        return None
    return comp


def main():
    # Ask the user to create runners (until they decide to add no more)
    runners = []

    while True:
        data = input("Add runner - name/age/country/sprint speed/marathon speed (blank line stops): ").strip().split('/')
        if len(data) == 0 or (len(data) == 1 and data[0] == ''):
            break
        if len(data) != 5:
            print("ERROR : Incorrect number of fields")
            continue
        runner = create_runner(data[0], data[1], data[2], data[3], data[4])
        if runner is not None:
            runners.append(runner)
    print("Done creating runners!\n")

    # Ask the user to create a competition
    comp = None
    while comp is None:
        data = input("Create competition - rounds/sprint distances/marathon distances: ").strip().split('/')
        if len(data) != 3:
            print("ERROR : Incorrect number of fields")
            continue
        comp = create_competition(runners, data[0], data[1], data[2])
    print("Done creating competition!\n")

    # Conduct the competition
    print("Executing the competition!")
    comp.conduct_competition()
    print("Competition concluded!\n")

    # Reveal the results!
    comp.print_leaderboard()

if __name__ == '__main__':
    main()
