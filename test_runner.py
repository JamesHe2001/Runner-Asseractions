from custom_errors import *
from runner import Runner
import unittest

class TestRunner(unittest.TestCase):

    def setUp(self):
        """Setup method to create a Runner instance for testing."""
        self.runner = Runner('Elijah', 25, 'Australia', 6.5, 4.0)

    def test_init_valid_input(self):
        """Test case for valid input during initialization."""
        self.assertEqual(runner.name, 'Elijah')
        self.assertEqual(runner.age, 18)
        self.assertEqual(runner.country, 'Australia')
        self.assertEqual(runner.sprint_speed, 5.8)
        self.assertEqual(runner.endurance_speed, 4.4)
        self.assertEqual(runner.energy, 1000)

    def test_init_invalid_name(self):
        """Test case for invalid name input during initialization."""
        with self.assertRaises(CustomValueError):
            Runner('Elijah-123', 25, 'Australia', 6.5, 4.0)

    def test_init_invalid_country(self):
        """Test case for invalid country input during initialization."""
        with self.assertRaises(CustomValueError):
            Runner('Elijah', 25, 'Australia', 6.5, 4.0)

    def test_drain_energy_valid_input(self):
        """Test case for valid input to drain_energy method."""
        self.runner.drain_energy(200)
        self.assertEqual(self.runner.energy, 800)

    def test_drain_energy_full_drain(self):
        """Test case for draining all energy."""
        self.runner.drain_energy(1000)
        self.assertEqual(self.runner.energy, 0)

    def test_drain_energy_invalid_input_type(self):
        """Test case for invalid input type to drain_energy method."""
        with self.assertRaises(CustomTypeError):
            self.runner.drain_energy('200')

    def test_recover_energy_valid_input(self):
        """Test case for valid input to recover_energy method."""
        self.runner.drain_energy(300)
        self.runner.recover_energy(100)
        self.assertEqual(self.runner.energy, 800)

    def test_recover_energy_full_recovery(self):
        """Test case for recovering full energy."""
        self.runner.drain_energy(500)
        self.runner.recover_energy(500)
        self.assertEqual(self.runner.energy, 1000)

    def test_recover_energy_invalid_input_type(self):
        """Test case for invalid input type to recover_energy method."""
        with self.assertRaises(CustomTypeError):
            self.runner.recover_energy('100')

    def test_run_race_short_valid_input(self):
        """Test case for valid input to run_race method for a short race."""
        time_taken = self.runner.run_race('short', 2.0)
        self.assertAlmostEqual(time_taken, 307.69, places=2)

    def test_run_race_long_valid_input(self):
        """Test case for valid input to run_race method for a long race."""
        time_taken = self.runner.run_race('long', 5.0)
        self.assertAlmostEqual(time_taken, 1250.00, places=2)

    def test_run_race_invalid_race_type(self):
        """Test case for invalid race type input to run_race method."""
        with self.assertRaises(CustomValueError):
            self.runner.run_race('medium', 2.0)

    def test_str_representation(self):
        """Test case for the string representation of the Runner object."""
        expected_str = "Name: Elijah Age: 25 Country: Australia"
        self.assertEqual(str(self.runner), expected_str)

if __name__ == '__main__':
    unittest.main()
