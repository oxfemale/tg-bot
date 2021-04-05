import math
from wrapcache.adapter.MemoryAdapter import MemoryAdapter


AUTO_BACKUP = {
    "code": False,
    "database": False,
    "sql_database": False,
    "interval": 86400,  # Раз в сутки
    "last_backups_save": math.inf,
}

NEED_BITCOIN_CONFIRMATIONS = 1  # Нужно подтверждений сети биткоин, для пополнения
DEFAULT_FIAT_CURRENCY = "rub"


BOT_ID = 1


wrapcache_adapter = MemoryAdapter
