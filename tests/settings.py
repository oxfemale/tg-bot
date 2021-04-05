import peewee

DATABASE = {
    "peewee_engine": peewee.SqliteDatabase(":memory:", thread_safe=True),
}
