import csv
import os

from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from foodgram.settings import BASE_DIR
from recipes import models

CSV_FILES = [
    ['ingredients.csv', models.Ingredient],
]

FOREIGN_FIELD_NAMES = {
}


def save_model(model, row, fields_name):
    try:
        obj = model()
        for i, field in enumerate(row):
            if fields_name[i] in FOREIGN_FIELD_NAMES.keys():
                foreign_model = FOREIGN_FIELD_NAMES[fields_name[i]]
                field = get_object_or_404(foreign_model, id=field)
            setattr(obj, fields_name[i], field)
        obj.save()
    except IntegrityError:
        print(f'Ингридиет {row[0]} '
              f'{row[1]} уже есть в базе')


def process_file(csv_file, model):
    path = os.path.join(BASE_DIR, f'data/{csv_file}')
    fields_name = []
    with open(path, 'rt', encoding="utf8") as f:
        reader = csv.reader(f, dialect='excel')
        fields_name = next(reader)
        for row in reader:
            save_model(model, row, fields_name)


class Command(BaseCommand):
    help = 'Load csv files into the database'

    def handle(self, *args, **options):
        for csv_file, model in CSV_FILES:
            process_file(csv_file, model)
