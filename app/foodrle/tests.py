from django.test import TestCase
import re
from .models import Country, Puzzle, Dishes
from .game import distance, direction
from random import randint


def get_country(id):
    """
        SELECT * FROM country WHERE id=id;
    """
    return Country.objects.get(pk=id)


country_list = [get_country(randint(1, 244)) for i in range(10)]
# country_list = [get_country(i) for i in range(1, 245)]

class CountryHintsTests(TestCase):

    def test_dist_equality(self):
        """Test to ensure the distance from Country A to Country B
            is the same as the distance from B to A
        """
        # A = get_country(randint(1, 244))
        # B = get_country(randint(1, 244))

        for i in range(0, len(country_list)):
            A = country_list[i]
            for j in range(0, len(country_list)):
                B = country_list[j]
                self.assertEquals(distance(A, B), distance(B, A))

    def test_dir_parity(self):
        """
            Checks that there is parity in direction computation
            (e.g., if a is north of b, b must be south of a)
        """
        for i in range(0, len(country_list)):
            a = country_list[i]
            for j in range(0, len(country_list)):
                b = country_list[j]
                dir = direction(a, b)
                # try:
                if dir == 'same':
                    self.assertEqual(direction(b, a), 'same')
                if dir == 'north':
                    self.assertEqual(direction(b, a), 'south')
                elif dir == 'south':
                    self.assertEqual(direction(b, a), 'north')
                elif dir == 'east':
                    self.assertEqual(direction(b, a), 'west')
                elif dir == 'west':
                    self.assertEqual(direction(b, a), 'east')
                elif dir == 'northeast':
                    self.assertEqual(direction(b, a), 'southwest')
                elif dir == 'southwest':
                    self.assertEqual(direction(b, a), 'northeast')
                elif dir == 'northwest':
                    self.assertEqual(direction(b, a), 'southeast')
                elif dir == 'southeast':
                    self.assertEqual(direction(b, a), 'northwest')
                # except AssertionError as e:
                #     e.args += (a.name, b.name)


class PuzzleModelTests(TestCase):
    def test_dict_contents(self):
        dish = Dishes(name="foo", calories=200)
        puzzle = Puzzle(ans_dish=dish)

        test_dict = puzzle.get_guesses_as_dict()
        for k, v in test_dict.items():
            self.assertTrue(re.match('guess[1-6]', k), msg=f'{k} does not match guess[1-6] pattern')
        
