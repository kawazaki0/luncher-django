import os
import unittest

from django.test import TestCase

from luncher.meals.models import MealImporter, Meal, Restaurant


class TestMealImporterParseLines(unittest.TestCase):
    def test_is_restaurant(self):
        mi = MealImporter(None)
        tests = [
            {
                'input': '# Flanders Bistro',
                'result': True,
            },
            {
                'input': '   # Flanders Bistro',
                'result': True,
            },
            {
                'input': '# Flanders Bistro            ',
                'result': True,
            },
            {
                'input': '#          Flanders Bistro            ',
                'result': True,
            },
            {
                'input': '06.02.2017',
                'result': False,
            },
            {
                'input': "",
                'result': False,
            },
            {
                'input': 'Z - Żurek z białą kiełbaską  sour rye soup with',
                'result': False,
            },
            {
                'input': 'P - (Danie mięsne) Pieczony udziec z indyka sosie kurkowym',
                'result': False,
            },
            {
                'input': 'E - Sushi zestaw 1 ',
                'result': False,
            },
        ]

        for t in tests:
            self.assertEqual(t['result'], mi.is_restaurant(t['input']), msg=t['input'])

    def test_is_meal(self):
        mi = MealImporter(None)
        tests = [
            {
                'input': '# Flanders Bistro',
                'result': False,
            },
            {
                'input': '06.02.2017',
                'result': False,
            },
            {
                'input': "",
                'result': False,
            },
            {
                'input': 'Z - Żurek z białą kiełbaską  sour rye soup with',
                'result': True,
            },
            {
                'input': 'P - (Danie mięsne) Pieczony udziec z indyka sosie kurkowym',
                'result': True,
            },
            {
                'input': 'E - Sushi zestaw 1 ',
                'result': True,
            },
        ]

        for t in tests:
            self.assertEqual(t['result'], mi.is_meal(t['input']), msg=t['input'])

    def test_is_date(self):
        mi = MealImporter(None)
        tests = [
            {
                'input': '# Flanders Bistro',
                'result': False,
            },
            {
                'input': '06.02.2017',
                'result': True,
            },
            {
                'input': "",
                'result': False,
            },
            {
                'input': 'Z - Żurek z białą kiełbaską  sour rye soup with',
                'result': False,
            },
            {
                'input': 'P - (Danie mięsne) Pieczony udziec z indyka sosie kurkowym',
                'result': False,
            },
            {
                'input': 'E - Sushi zestaw 1 ',
                'result': False,
            },
        ]

        for t in tests:
            self.assertEqual(t['result'], mi.is_date(t['input']), msg=t['input'])


class TestMealImporter(TestCase):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'testdata',
                             'menu.txt')

    def setUp(self):
        Restaurant.objects.bulk_create([
            Restaurant(name='Flanders Bistro', min_purchase=4),
            Restaurant(name='Dobry Obiad', min_purchase=4),
            Restaurant(name='Matsurisushi', min_purchase=4),
        ])

    def test_parse(self):
        mi = MealImporter(self.file_path)
        mi.parse()
        self.assertEqual(239, len(mi.meals))

        mi.bulk_create()

        result = Meal.objects.count()
        self.assertEqual(result, len(mi.meals))

        self.assertEqual(4, Meal.objects.filter(name__contains='Żurek z białą kiełbaską').count())
        self.assertEqual(1, Meal.objects.filter(name__contains='jarskie kotlety').count())
