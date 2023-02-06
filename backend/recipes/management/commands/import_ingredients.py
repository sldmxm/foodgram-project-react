import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('ingredients.csv', encoding='utf-8') as r_file:
            reader = csv.reader(r_file, delimiter=",")
            next(reader)
            upload_list = []
            for row in reader:
                if not Ingredient.objects.filter(
                        name=row[0], measurement_unit=row[1]).exists():
                    upload_list.append(
                        Ingredient(name=row[0], measurement_unit=row[1])
                    )
            Ingredient.objects.bulk_create(upload_list)
            print(f'Загружено {len(upload_list)} '
                  f'записей в Ingredient.')
