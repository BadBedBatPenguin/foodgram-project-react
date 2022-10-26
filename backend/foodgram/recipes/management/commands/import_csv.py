import csv
import os

from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from foodgram.settings import BASE_DIR
from recipes import models

CSV_FILES = [
    ['ingredients.csv', models.Ingredient],
]


def save_model(model, row):
    try:
        obj = model()
        setattr(obj, 'name', row[0])
        setattr(obj, 'measurement_unit', row[1])
        obj.save()
    except IntegrityError:
        print(f'Ингридиет {row[0]} '
              f'{row[1]} уже есть в базе')


def process_file(csv_file, model):
    path = os.path.join(BASE_DIR, f'data/{csv_file}')
    with open(path, 'rt', encoding="utf8") as f:
        reader = csv.reader(f, dialect='excel')
        next(reader)
        for row in reader:
            save_model(model, row)


class Command(BaseCommand):
    help = 'Load csv files into the database'

    def handle(self, *args, **options):
        for csv_file, model in CSV_FILES:
            process_file(csv_file, model)
