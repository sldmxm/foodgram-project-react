import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            r_file = open('ingredients.csv', encoding='utf-8')
        except IOError as e:
            self.stdout.write(self.style.ERROR(e))
        else:
            upload_list = {}
            with r_file:
                data = csv.DictReader(
                    r_file,
                    fieldnames=['name', 'unit']
                )
                for row in data:
                    if not Ingredient.objects.filter(
                            name=row['name'],
                            measurement_unit=row['unit']
                    ).exists():
                        upload_list[str(
                            Ingredient(
                                name=row['name'],
                                measurement_unit=row['unit']
                            )
                        )] = Ingredient(
                            name=row['name'],
                            measurement_unit=row['unit']
                        )

                Ingredient.objects.bulk_create(
                    upload_list.values(),
                    ignore_conflicts=True,
                )
                if len(upload_list) > 0:
                    self.stdout.write(self.style.SUCCESS(
                        f'Загружено {len(upload_list)} '
                        f'новых записей в Ingredient.'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        'Нет новых записей для Ingredient.'
                    ))
