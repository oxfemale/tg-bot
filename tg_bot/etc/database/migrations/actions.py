import copy
import peewee
from playhouse.migrate import SchemaMigrator, migrate

from . import helper


def re_create_model_and_save_data(model):
    data = helper.save_data(model)
    helper.re_create_table_and_load_new_data_data(model, data, data)


def rename_field(model, old_field_name, new_field_name):
    data = helper.save_data(model)
    new_data = data.copy()
    for one_record in new_data:
        one_record[new_field_name] = one_record[old_field_name]
        del one_record[old_field_name]

    helper.re_create_table_and_load_new_data_data(model, data, new_data)


def create_field(database, model, field_name, field):
    table_name = model._meta.table_name

    migrator = SchemaMigrator.from_database(database)
    migrate(migrator.add_column(table_name, field_name, field))


def delete_field(database, model, field_name):
    table_name = model._meta.table_name

    migrator = SchemaMigrator.from_database(database)
    migrate(migrator.drop_column(table_name, field_name))
