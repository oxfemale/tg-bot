import peewee_migrate
from cached_property import cached_property


class Router(peewee_migrate.Router):
    @cached_property
    def migrator(self):
        migrator = peewee_migrate.migrator.Migrator(self.database)
        return migrator
