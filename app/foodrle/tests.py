from django.test import TestCase
from .models import Country, Puzzle, Dishes
from .game import distance, direction
import itertools
import random
import re


class CountryHintsTests(TestCase):
    fixtures = ['foodrle.yml']

    def setUp(self):
        self.random_countries = random.choices(list(Country.objects.all()), k=10)
        self.opposite_directions = [
            ('north', 'south'),
            ('east', 'west'),
            ('northwest', 'southeast'),
            ('northeast', 'southwest')
        ]

    def test_dist_equality(self):
        """Test to ensure the distance from Country A to Country B
            is the same as the distance from B to A
        """
        for country_a, country_b in itertools.product(self.random_countries, repeat=2):
            if country_a != country_b:
                self.assertEqual(distance(country_a, country_b), distance(country_b, country_a))

    def test_dir_parity(self):
        """
            Checks that there is parity in direction computation
            (e.g., if a is north of b, b must be south of a)
        """
        for country_a, country_b in itertools.product(self.random_countries, repeat=2):
            a_b_direction = direction(country_a, country_b)
            b_a_direction = direction(country_b, country_a)
            if country_a != country_b:
                for direction1, direction2 in self.opposite_directions:
                    if a_b_direction == direction1:
                        self.assertEqual(b_a_direction, direction2)
                    if a_b_direction == direction2:
                        self.assertEqual(b_a_direction, direction1)
            else:
                self.assertEqual(a_b_direction, b_a_direction)


class PuzzleModelTests(TestCase):
    def test_dict_contents(self):
        dish = Dishes(name="foo", calories=200)
        puzzle = Puzzle(ans_dish=dish)

        test_dict = puzzle.get_guesses_as_dict()
        for k, v in test_dict.items():
            self.assertTrue(re.match('guess[1-6]', k), msg=f'{k} does not match guess[1-6] pattern')
