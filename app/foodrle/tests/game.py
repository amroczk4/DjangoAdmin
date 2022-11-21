import itertools
import pdb
import pprint
import random

from django.test import TestCase

from foodrle.game import distance, create_puzzle_answer, submit_guess, bearing, find_guess_cnt, main_ingredient_hint, \
    RED, YELLOW, GREEN, calorie_hint, taste_hint, Taste, Puzzle, is_guess_correct, collect_hints
from foodrle.models import Country, Dishes, User, MainIngredient


class TestCountryMethods(TestCase):
    fixtures = ['foodrle.yaml']

    def setUp(self):
        self.random_countries = random.choices(list(Country.objects.all()), k=10)
        self.opposite_bearings = [
            ('north', 'south'),
            ('east', 'west'),
            ('northwest', 'southeast'),
            ('northeast', 'southwest')
        ]

    def test_distance_equality(self):
        """Test to ensure the distance from Country A to Country B
            is the same as the distance from B to A
        """
        for country_a, country_b in itertools.product(self.random_countries, repeat=2):
            if country_a != country_b:
                self.assertEqual(distance(country_a, country_b), distance(country_b, country_a))

    def test_bearing_parity(self):
        """
            Checks that there is parity in direction computation
            (e.g., if a is north of b, b must be south of a)
        """
        for country_a, country_b in itertools.product(self.random_countries, repeat=2):
            a_b_bearing = bearing(country_a, country_b)
            b_a_bearing = bearing(country_b, country_a)
            if country_a != country_b:
                for bearing1, bearing2 in self.opposite_bearings:
                    if a_b_bearing == bearing1:
                        self.assertEqual(b_a_bearing, bearing2)
                    if a_b_bearing == bearing2:
                        self.assertEqual(b_a_bearing, bearing1)
            else:
                self.assertEqual(a_b_bearing, b_a_bearing)


class TestPuzzleMethods(TestCase):
    fixtures = ['foodrle.yaml']

    def test_create_puzzle_answer(self):
        user = User.objects.get(pk=1)
        puzzle = create_puzzle_answer(user)
        self.random_countries = random.choices(list(Country.objects.all()), k=10)

        possible_dishes = [d.name for d in Dishes.objects.all()]
        self.assertIn(puzzle.ans_dish.name, possible_dishes)

    def test_submit_guess_game_over(self):
        self.assertFalse(submit_guess(1, 'foo', 7))

    def test_submit_guess_invalid_dish(self):
        self.assertFalse(submit_guess(1, 'notafood', 1))

    def test_submit_guess_correct(self):
        self.assertTrue(submit_guess(1, 'pavlova', 1))


class TestGenericMethods(TestCase):
    fixtures = ['foodrle.yaml']

    def test_find_guess_cnt_no_guesses(self):
        guess_cnt = find_guess_cnt(1, 5)
        self.assertEqual(guess_cnt, 1)

    def test_find_guess_cnt_some_guesses(self):
        user = User.objects.get(pk=1)
        puzzle = create_puzzle_answer(user)
        beginning_guess_cnt = 1
        submit_guess(puzzle.id, 'slurm', beginning_guess_cnt)
        guess_cnt = find_guess_cnt(puzzle.id, beginning_guess_cnt + 1)
        submit_guess(puzzle.id, 'plumbus', beginning_guess_cnt)
        guess_cnt = find_guess_cnt(puzzle.id, guess_cnt + 1)
        submit_guess(puzzle.id, 'bingbong', guess_cnt)
        guess_cnt = find_guess_cnt(puzzle.id, guess_cnt + 1)
        self.assertEqual(guess_cnt, 3)

    # def test_is_guess_correct(self):
    #     user = User.objects.get(pk=1)
    #     answer = Dishes.objects.get(pk=1)
    #     puzzle = Puzzle(ans_dish=answer, player=user)
    #     submit_guess(puzzle.id, 'lumpia', 1)
    #     self.assertTrue(is_guess_correct(puzzle, guess_cnt=1))


class TestIngredientMethods(TestCase):
    fixtures = ['foodrle.yaml']

    def test_main_ingredient_hint(self):
        user = User.objects.get(pk=1)
        answer_ingredient = MainIngredient.objects.get(pk=1)  # red meat
        ingredient_dict = {
            1: GREEN,  # Correct
            2: YELLOW,  # Butter
            3: RED  # Wrong (refined grains)
        }
        for k, v in ingredient_dict.items():
            guess_ingredient = MainIngredient.objects.get(pk=k)
            self.assertEqual(main_ingredient_hint(answer_ingredient, guess_ingredient), {guess_ingredient.name: v})


class TestDishMethods(TestCase):
    fixtures = ['foodrle.yaml']

    def test_calorie_hint(self):
        answer_dish = Dishes.objects.get(pk=5)  # frankfurter
        greater_dish = Dishes.objects.get(pk=7)  # gyro
        lesser_dish = Dishes.objects.get(pk=1)  # pavlova
        same_dish = Dishes.objects.get(pk=29)  # fries
        self.assertEqual(calorie_hint(answer_dish, same_dish)['calories'], 0)
        self.assertLess(calorie_hint(answer_dish, greater_dish)['calories'], 0)
        self.assertGreater(calorie_hint(answer_dish, lesser_dish)['calories'], 0)

    def test_collect_hints_wrong(self):
        guess_dish = Dishes.objects.get(pk=1)
        answer_dish = Dishes.objects.get(pk=2)
        pprint.pprint(collect_hints(guess_dish, answer_dish))
        expected_hints = [
            ('guess', 'pavlova'),
            ('bitter', 0),
            ('sour', 0),
            ('sweet', 0),
            ('calories', 119),
            ('Fruits', 0)
        ]
        flattened_hints = {}
        for d in collect_hints(guess_dish, answer_dish):
            flattened_hints.update(d)

        for h in expected_hints:
            self.assertIn(h, flattened_hints.items())


class TestTasteMethods(TestCase):
    fixtures = ['foodrle.yaml']

    def test_guess_taste_hint(self):
        answer_taste = Taste.objects.get(pk=2) # sweet and salty
        guess_taste_1 = Taste.objects.get(pk=1) # sweet
        guess_taste_2 = Taste.objects.get(pk=12) # salty
        guess_taste_3 = Taste.objects.get(pk=19) # sour
        self.assertIn(('sweet', GREEN), taste_hint(answer_taste, guess_taste_1).items())
        self.assertIn(('salty', GREEN), taste_hint(answer_taste, guess_taste_2).items())
        self.assertIn(('sour', RED), taste_hint(answer_taste, guess_taste_3).items())

    def test_Taste_model(self):
        self.assertEqual(str(Taste.objects.get(pk=23)), 'Bitter ')
        self.assertEqual(str(Taste.objects.get(pk=21)), 'Sour Umami ')
        self.assertEqual(str(Taste.objects.get(pk=2)), 'Sweet Salty ')

