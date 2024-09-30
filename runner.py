from custom_errors import *

class Runner:
    max_energy = 1000
    def __init__(self, name: str, age: int, country: str, sprint_speed: float, endurance_speed: float):
        """
        Initializes a Runner object with the provided attributes.

        Args:
            name (str): The name of the runner.
            age (int): The age of the runner.
            country (str): The country of the runner.
            sprint_speed (float): The sprint speed of the runner in meters per second.
            endurance_speed (float): The endurance speed of the runner in meters per second.

        Raises:
            CustomTypeError: If the input types are not valid.
            CustomValueError: If the input values are not valid.
        """
        # Checking input types
        if not (
            isinstance(name, str) and
            isinstance(age, int) and
            isinstance(country, str) and
            isinstance(sprint_speed, float) and
            isinstance(endurance_speed, float)
        ):
            raise CustomTypeError("Invalid input type, please check the input types")

        valid_countries = set()
        with open('countries.csv', 'r') as file:
            file.readline()
            for line in file:
                valid_countries.add(line.strip().split(',')[3])

        # Checking input values
        if not (
            name.replace(' ', '').isalnum() and
            5 <= age <= 100 and
            country in valid_countries and
            2.2 <= sprint_speed <= 6.8 and
            1.8 <= endurance_speed <= 5.4
        ):
            raise CustomValueError("Invalid input value, please check the input values")

        # Setting initial energy
        self.max_energy = 1000
        self.energy = self.max_energy

        # Setting attributes
        self.name = name
        self.age = age
        self.country = country
        self.sprint_speed = sprint_speed
        self.endurance_speed = endurance_speed

    def drain_energy(self, drain_points: int):
        """
        Drains the runner's energy by the specified amount.

        Args:
            drain_points (int): The amount of energy to drain.

        Raises:
            CustomTypeError: If the input type is not valid.
            CustomValueError: If the input value is not valid.
        """
        # Checking input type
        if not isinstance(drain_points, int):
            raise CustomTypeError("Invalid input type, please check the input types")

        # Checking input value
        if not 1 <= drain_points <= self.max_energy:
            raise CustomValueError("Invalid input value, please check the input values")

        # Draining energy
        self.energy -= drain_points
        if self.energy < 0:
            self.energy = 0

    def recover_energy(self, recovery_amount: int):
        """
        Recovers the runner's energy by the specified amount.

        Args:
            recovery_amount (int): The amount of energy to recover.

        Raises:
            CustomTypeError: If the input type is not valid.
            CustomValueError: If the input value is not valid.
        """
        # Checking input type
        if not isinstance(recovery_amount, int):
            raise CustomTypeError("Invalid input type, please check the input types")

        # Checking input value
        if not 1 <= recovery_amount <= self.max_energy:
            raise CustomValueError("Invalid input value, please check the input values")

        # Recovering energy
        self.energy += recovery_amount
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def run_race(self, race_type, distance):
        #raise ValueError(f'{race_type} {distance}')
        valid_race_types = ['short', 'long']
        if not isinstance(race_type, str):
            raise CustomTypeError(f"Invalid race type provided. Expected one of {valid_race_types}.")
        if not isinstance(distance,float):
            raise CustomTypeError("Distance must be a number (int or float).")
        if race_type not in valid_race_types:
            raise CustomValueError('')
        if distance <= 0:
            raise CustomValueError('')

        distance_meters = distance * 1000

        if race_type == 'short':
            time_taken = distance_meters / self.sprint_speed
        else:
            time_taken = distance_meters / self.endurance_speed

        return round(time_taken, 2)

    def __str__(self):
        """
        Returns a string representation of the Runner object.

        Returns:
            str: The string representation of the Runner object.
        """
        return f"Name: {self.name} Age: {self.age} Country: {self.country}"

if __name__ == '__main__':
    runner = Runner('Elijah', 18, 'Australia', 5.8, 4.4)
    
    # running a short race
    time_taken = runner.run_race('short', 2.0)
    print(f"Runner {runner.name} took {time_taken} seconds to run 2km!")

