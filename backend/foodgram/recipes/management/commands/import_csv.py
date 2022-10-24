import csv
import os
from typing import List

from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from recipes import models

from foodgram.settings import BASE_DIR

CSV_FILES = [
    ['ingredients.csv', models.Ingredient],
    ]

FOREIGN_FIELD_NAMES = {
}


def check_fields(fields_name: List[str], model_fields: List[str], model):
    for i, _ in enumerate(fields_name):
        print(f'fields_name[{i}]: {fields_name[i]}')
        print(f'model_fields: {model_fields}')
        fields_name[i] = fields_name[i].lower()
        fields_name[i] = fields_name[i].replace('_id', '')
        if not fields_name[i] in model_fields:
            raise CommandError(
                f"{fields_name[i]} field doesn't exist "
                f"in {model} Model"
            )


def save_model(model, row, fields_name):
    try:
        obj = model()
        for i, field in enumerate(row):
            if fields_name[i] in FOREIGN_FIELD_NAMES.keys():
                foreign_model = FOREIGN_FIELD_NAMES[fields_name[i]]
                field = get_object_or_404(foreign_model, id=field)
            setattr(obj, fields_name[i], field)
        obj.save()
    # except Exception as e:
    #     raise CommandError(e)
    except IntegrityError:
        print(f'Ингридиет {row[0]} '
              f'{row[1]} уже есть в базе')


def process_file(csv_file, model):
    path = os.path.join(BASE_DIR, f'static/data/{csv_file}')
    model_fields = [f.name for f in model._meta.fields]
    fields_name = []
    with open(path, 'rt', encoding="utf8") as f:
        reader = csv.reader(f, dialect='excel')
        fields_name = next(reader)
        # check_fields(fields_name, model_fields, model)
        for row in reader:
            save_model(model, row, fields_name)


class Command(BaseCommand):
    help = 'Load csv files into the database'

    def handle(self, *args, **options):
        for csv_file, model in CSV_FILES:
            process_file(csv_file, model)
