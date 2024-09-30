from race import *
from runner import Runner
from custom_errors import *


class Competition:
    """
    Represents a competition with multiple rounds of short and marathon races.

    Attributes:
        MAX_ROUNDS (int): The maximum number of rounds allowed in a competition.
        runners (list): A list of Runner objects participating in the competition.
        rounds (int): The number of rounds in the competition.
        distances_short (list): A list of distances (in kilometers) for each short race round.
        distances_marathon (list): A list of distances (in kilometers) for each marathon race round.
        leaderboard (dict): A dictionary storing the current leaderboard of the competition.
            Keys are ordinal strings (e.g., "1st", "2nd") and values are tuples of 
            (runner_name, total_score).

    """
    MAX_ROUNDS = 3

    def __get_ordinal(self, n):
        """
        Returns the ordinal string for a given integer.

        Args:
            n (int): The integer to convert to an ordinal string.

        Returns:
            str: The ordinal string representation of the input integer (e.g., "1st", "2nd").

        """
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        if 11 <= n % 100 <= 13:
            suffix = 'th'
        else:
            suffix = suffixes.get(n % 10, 'th')
        return f"{n}{suffix}"

    def __init__(self, runners: list, rounds: int, distances_short: list, distances_marathon: list):
        """
        Initializes a Competition object with the given parameters.

        Args:
            runners (list): A list of Runner objects participating in the competition.
            rounds (int): The number of rounds in the competition.
            distances_short (list): A list of distances (in kilometers) for each short race round.
            distances_marathon (list): A list of distances (in kilometers) for each marathon race round.

        Raises:
            CustomTypeError: If any of the input arguments are not of the expected type.
            CustomValueError: If any of the input values are invalid (e.g., rounds out of range,
                             distances not positive).

        """
        if not (
            isinstance(runners, list) and
            all(isinstance(runner, Runner) for runner in runners) and
            isinstance(rounds, int) and
            isinstance(distances_short, list) and
            all(isinstance(distance, float) for distance in distances_short) and
            isinstance(distances_marathon, list) and
            all(isinstance(distance, float) for distance in distances_marathon)
        ):
            raise CustomTypeError("Invalid input type, please check the input types")
        if not (
            1 <= rounds <= self.MAX_ROUNDS and
            all(distance > 0 for distance in distances_short) and
            all(distance > 0 for distance in distances_marathon) and
            len(distances_short) == len(distances_marathon) == rounds
        ):
            raise CustomValueError("Invalid input value, please check the input values")

        self.runners = runners
        self.rounds = rounds
        self.distances_short = distances_short
        self.distances_marathon = distances_marathon

        # Initialize the leaderboard with None for each ranking position
        self.leaderboard = {}
        for i in range(1, len(self.runners) + 1):
            self.leaderboard[self.__get_ordinal(i)] = None

    def conduct_competition(self):
        """
        Conducts the competition by running all rounds of short and marathon races.

        This method simulates the entire competition, including:
            - Running each short and marathon race for each round.
            - Recovering energy for runners who did not finish (DNF) the marathon.
            - Updating the leaderboard after each round.

        Returns:
            dict: The final leaderboard after all rounds have been conducted.

        """
        current_round = 1
        i = 0
        while current_round <= self.rounds:
            # Conduct the short race with all runners
            short_race = ShortRace(self.distances_short[i], runners=self.runners)
            short_race.runners = self.runners
            short_result = self.conduct_race(short_race)

            # Conduct the Marathon race with all runners
            marathon = MarathonRace(self.distances_marathon[i], runners=self.runners)
            marathon.runners = self.runners  # Assign runners to the marathon race
            marathon_result = self.conduct_race(marathon)

            # Recover energy for all DNF runners
            for runner, taken_time in marathon_result:
                if taken_time == "DNF":
                    runner.recover_energy(1000)

            current_round += 1
            self.update_leaderboard(short_result)
            self.update_leaderboard(marathon_result)

        return self.leaderboard

    def conduct_race(self, race):
        """
        Conducts a single race (either short or marathon).

        Args:
            race (Race): The race object to conduct.

        Returns:
            list: The results of the race, as returned by the race's conduct_race() method.

        """
        return race.conduct_race()

    def update_leaderboard(self, results):
        """
        Updates the leaderboard based on the results of a race.

        This method calculates scores for each runner based on their finishing position in the race.
        Runners who did not finish (DNF) receive a score of 0. The leaderboard is then updated
        with the new scores, accumulating points over multiple rounds.

        Args:
            results (list): The results of a race, as a list of tuples (runner, taken_time).

        """
        # Sort the race results based on the taken time
        sorted_result = sorted(results, key=lambda x: x[1])
        
        # Get the list of leaderboard keys (e.g., "1st", "2nd")
        leaderboard_keys = list(self.leaderboard.keys())
        
        # Create a dictionary mapping runner names to their scores in the current race
        name2score = {runner.name: (len(results) - i - 1) if taken_time != "DNF" else 0 
                     for i, (runner, taken_time) in enumerate(sorted_result)}

        # Update scores based on previous leaderboard positions
        for key in leaderboard_keys:
            if self.leaderboard[key] is not None:
                name, score = self.leaderboard[key]
                name2score[name] += score
        
        # Sort the runners based on their accumulated scores
        sorted_result = sorted(name2score.items(), key=lambda x: -x[1])
        
        # Update the leaderboard with the new rankings
        for i, name_score in enumerate(sorted_result):
            self.leaderboard[leaderboard_keys[i]] = name_score

    def print_leaderboard(self):
        """
        Prints the current leaderboard to the console.

        The leaderboard is printed in the format:
        Leaderboard

        <ordinal> - <runner_name> (<total_score>)
        ...

        """
        print("Leaderboard\n\n")
        for key, value in self.leaderboard.items():
            print(f"{key} - {value[0]} ({value[1]})")

if __name__ == '__main__':
    # Example usage
    runners = [
        Runner("Elijah", 19, 'Australia', 6.4, 5.2),
        Runner("Rupert", 67, 'Botswana', 2.2, 1.8),
        Runner("Phoebe", 12, 'France', 3.4, 2.8),
        Runner("Lauren", 13, 'Iceland', 4.4, 5.1),
        Runner("Chloe", 21, 'Timor-Leste', 5.2, 1.9)
    ]

    competition = Competition(runners, 3, [0.5, 0.6, 1.2], [4.0, 11.0, 4.5])
    _ = (competition.conduct_competition())
    competition.print_leaderboard()
