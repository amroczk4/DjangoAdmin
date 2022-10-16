from django.test import TestCase

from .models import Country
from random import randint


def get_country(id):
    """
        SELECT * FROM country WHERE id=id;
    """
    return Country.objects.get(pk=id)


country_list = [get_country(randint(1, 244)) for i in range(10)]


class CountryModelTests(TestCase):

    def test_dist_equality(self):
        """Test to ensure the distance from Country A to Country B
            is the same as the distance from B to A
        """
        # A = get_country(randint(1, 244))
        # B = get_country(randint(1, 244))

        for i in range(0, 9):
            A = country_list[i]
            for j in range(i+1, 10):
                B = country_list[j]
                self.assertEquals(A.distance(B), B.distance(A))

    def test_dir_parity(self):
        """
            Checks that there is parity in direction computation
            (e.g., if a is north of b, b must be south of a)
        """
        for i in range(0, 9):
            a = country_list[i]
            for j in range(i+1, 10):
                b = country_list[j]
                direction = a.direction(b)
                # try:
                if direction == '':
                    self.assertEqual(b.direction(a), '')
                if direction == 'north':
                    self.assertEqual(b.direction(a), 'south')
                elif direction == 'south':
                    self.assertEqual(b.direction(a), 'north')
                elif direction == 'east':
                    self.assertEqual(b.direction(a), 'west')
                elif direction == 'west':
                    self.assertEqual(b.direction(a), 'east')
                elif direction == 'northeast':
                    self.assertEqual(b.direction(a), 'southwest')
                elif direction == 'southwest':
                    self.assertEqual(b.direction(a), 'northeast')
                elif direction == 'northwest':
                    self.assertEqual(b.direction(a), 'southeast')
                elif direction == 'southeast':
                    self.assertEqual(b.direction(a), 'northwest')
                # except AssertionError as e:
                #     e.args += (a.name, b.name)


