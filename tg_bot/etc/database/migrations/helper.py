import copy
import peewee


def save_data(model):
    created_fields = get_created_columns(model)
    need_fields = [field for _, field in created_fields.items()]

    columns_is_not_in_model = []
    for column in parse_columns_from_db(model):
        if column not in created_fields:
            columns_is_not_in_model = [column]

    data = []
    for _data in model.select(*need_fields):
        _data = _data.__data__
        for column in columns_is_not_in_model:
            _data[column] = select_from_db(model, column, _data["id"])
        data.append(_data)

    return data


def load_data(model, data):
    for record in data:
        model.create(**record)


def model_backup(model, data, backup_table_prefix="_backup"):
    model = copy.deepcopy(model)
    # noinspection PyProtectedMember
    model._meta.table.__name__ = "{}{}".format(model._meta.table.__name__, backup_table_prefix)
    model.create_table()

    load_data(model, data)
    return model


def re_create_table_and_load_new_data_data(model, old_data, new_data):
    # backup_model = model_backup(model, old_data)
    model.drop_table()
    model.create_table()
    load_data(model, new_data)
    # try:
    #     load_data(model, new_data)
    # except Exception:
    #     model_backup(model, old_data, backup_table_prefix="")
    #     raise Exception
    #
    # backup_model.drop_table()


def get_created_columns(model):
    # noinspection PyProtectedMember
    columns = model._meta.columns.copy()
    static_columns = columns.copy()

    for field_name, field_in_model in static_columns.items():
        try:
            model.select(field_in_model).first()
        except peewee.OperationalError:
            del columns[field_name]
    return columns


def parse_columns_from_db(model):
    # noinspection PyProtectedMember
    columns = [table.name for table in model._meta.database.get_columns(model._meta.table.__name__)]
    return columns


def select_from_db(model, column, record_id):
    # noinspection PyProtectedMember
    database = model._meta.database
    # noinspection PyProtectedMember
    table_name = model._meta.table.__name__
    response = database.execute_sql("SELECT {} FROM {} WHERE id = {}".format(column, table_name, record_id))
    value = response.fetchone()[0]
    return value
