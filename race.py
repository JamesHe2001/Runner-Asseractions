from custom_errors import *  # Import custom exceptions
from abc import ABC, abstractmethod  # Import abstract base class tools
from runner import Runner  # Import the Runner class
import math  # Import math library for ceiling function

class Race(ABC):
    """
    Abstract base class for races.

    Attributes:
        distance (float): The distance of the race in kilometers.
        runners (list, optional): A list of Runner objects participating in the race. Defaults to an empty list.
        race_type (str, optional): The type of race, either "short" or "long". Defaults to "short".
        energy_per_km (float): The amount of energy drained per kilometer in long races. Defaults to 100.
        maximum_participants (int): The maximum number of participants allowed in the race. Defaults to 8 for short races and 16 for long races.
        time_multiplier (float): A multiplier applied to the time taken in short races. Defaults to 1.2.

    Methods:
        add_runner(runner): Adds a runner to the race.
        remove_runner(runner): Removes a runner from the race.
        conduct_race(): Conducts the race and returns the results.
    """
    def __init__(self, distance: float, runners: list | None = None, race_type: str = "short"):
        """
        Initializes a new Race object.

        Args:
            distance (float): The distance of the race in kilometers.
            runners (list, optional): A list of Runner objects participating in the race. Defaults to an empty list.
            race_type (str, optional): The type of race, either "short" or "long". Defaults to "short".

        Raises:
            CustomTypeError: If any of the input arguments are not of the correct type.
            CustomValueError: If the distance is not positive or if the race type is not "short" or "long".
        """
        if runners is None:
            runners = []
        if not (
            isinstance(distance, float)  # Check if distance is a float
            and isinstance(runners, list)  # Check if runners is a list
            and isinstance(race_type, str)  # Check if race_type is a string
            and all(isinstance(runner, Runner) for runner in runners)  # Check if all elements in runners are Runner objects
        ):
            raise CustomTypeError("Invalid input type, please check the input types")
        if not (
            distance > 0  # Check if distance is positive
            and race_type in ["short", "long"]  # Check if race_type is either "short" or "long"
        ):
            raise CustomValueError("Invalid input value, please check the input values")
        self.runners = runners  # Initialize runners attribute
        self.race_type = race_type  # Initialize race_type attribute
        self.distance = distance  # Initialize distance attribute
        self.energy_per_km = 100  # Initialize energy_per_km attribute
        self.maximum_participants = 8 if race_type == "short" else 16  # Initialize maximum_participants based on race_type
        self.time_multiplier = 1.2  # Initialize time_multiplier attribute
    
    def add_runner(self, runner):
        """
        Adds a runner to the race.

        Args:
            runner (Runner): The Runner object to add to the race.

        Raises:
            CustomTypeError: If the runner argument is not a Runner object.
            RaceIsFullError: If the race is already full.
            RunnerAlreadyExistsError: If the runner already exists in the race.
        """
        if not isinstance(runner, Runner):  # Check if runner is a Runner object
            raise CustomTypeError("Invalid input type, please check the input types")
        if len(self.runners) >= self.maximum_participants:  # Check if the race is full
            raise RaceIsFullError("Race is already full. Cannot add more runners.")
        if runner in self.runners:  # Check if runner already exists in the race
            raise RunnerAlreadyExistsError("Runner already exists in the race.")
        self.runners.append(runner)  # Add the runner to the race
    
    def remove_runner(self, runner):
        """
        Removes a runner from the race.

        Args:
            runner (Runner): The Runner object to remove from the race.

        Raises:
            CustomTypeError: If the runner argument is not a Runner object.
            RunnerDoesntExistError: If the runner does not exist in the race.
        """
        if not isinstance(runner, Runner):  # Check if runner is a Runner object
            raise CustomTypeError("Invalid input type, please check the input types")
        if runner not in self.runners:  # Check if runner exists in the race
            raise RunnerDoesntExistError("Runner does not exist in the race.")
        self.runners.remove(runner)  # Remove the runner from the race
    
    def conduct_race(self):
        """
        Conducts the race and returns the results.

        Returns:
            list: A list of tuples, where each tuple contains a Runner object and their finishing time or "DNF" if they did not finish.
        """
        result = []  # Initialize an empty list to store the results
        if self.race_type == "short":
            for i, runner in enumerate(self.runners):  # Iterate over each runner in the race
                time_taken = runner.run_race("short", self.distance) * self.time_multiplier  # Calculate the time taken for a short race
                result.append((runner, time_taken))  # Add the runner and their time to the results list
        elif self.race_type == "long":
            for i, runner in enumerate(self.runners):  # Iterate over each runner in the race
                time_taken = 0  # Initialize time taken to 0
                for km in range(math.ceil(self.distance)):  # Iterate over each kilometer in the race
                    if runner.energy > 0:  # Check if the runner has energy left
                        time_taken += runner.run_race("long", 1.0)  # Add the time taken for 1 km to the total time
                        runner.drain_energy(100)  # Drain the runner's energy by 100
                    else:
                        time_taken = 'DNF'  # If the runner runs out of energy, set time taken to "DNF"
                        break  # Exit the loop if the runner did not finish
                result.append((runner, time_taken))  # Add the runner and their time to the results list
        return result  # Return the results list

class ShortRace(Race):
    """
    A class representing a short race.

    Attributes:
        distance (float): The distance of the race in kilometers.
        runners (list, optional): A list of Runner objects participating in the race. Defaults to an empty list.

    Methods:
        __init__(distance, runners): Initializes a new ShortRace object.
    """
    def __init__(self, distance, runners = None):
        """
        Initializes a new ShortRace object.

        Args:
            distance (float): The distance of the race in kilometers.
            runners (list, optional): A list of Runner objects participating in the race. Defaults to an empty list.
        """
        super().__init__(distance, runners, "short")  # Initialize the ShortRace object by calling the Race class constructor with race_type="short"


class MarathonRace(Race):
    """
    A class representing a marathon race.

    Attributes:
        distance (float): The distance of the race in kilometers.
        runners (list, optional): A list of Runner objects participating in the race. Defaults to an empty list.

    Methods:
        __init__(distance, runners): Initializes a new MarathonRace object.
    """
    def __init__(self, distance, runners = None):
        """
        Initializes a new MarathonRace object.

        Args:
            distance (float): The distance of the race in kilometers.
            runners (list, optional): A list of Runner objects participating in the race. Defaults to an empty list.
        """
        super().__init__(distance, runners, "long")  # Initialize the MarathonRace object by calling the Race class constructor with race_type="long"
        
if __name__ == '__main__':
    short_race = ShortRace(0.5)  # Create a new ShortRace object with a distance of 0.5 kilometers
    long_race = MarathonRace(5.0)  # Create a new MarathonRace object with a distance of 5.0 kilometers

    # Create two Runner objects
    eli = Runner('Elijah', 18, 'Australia', 5.8, 4.4)
    rup = Runner('Rupert', 23, 'Australia', 2.3, 1.9)

    long_race.add_runner(eli)  # Add eli to the long race
    long_race.add_runner(rup)  # Add rup to the long race

    results = long_race.conduct_race()  # Conduct the long race and store the results
    for runner, time in results:  # Iterate over the results and print the runner's name and their time
        print(runner.name, time) 
