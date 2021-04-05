# tg-bot
[![Build Status](https://travis-ci.com/daveusa31/tg-bot.svg?branch=master)](https://travis-ci.com/daveusa31/tg-bot)
[![codecov](https://codecov.io/gh/daveusa31/tg-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/daveusa31/tg-bot)
[![repository size](https://img.shields.io/github/repo-size/daveusa31/tg-bot)](https://github.com/daveusa31/tg-bot)
## Установка
```sh
pip3 install https://github.com/daveusa31/tg-bot/archive/master.zip
```

## Использование
```python
import tg_bot
```

### Как использовать автобекапы?
1. Закидываем себе в проект файл settings. [Пример](https://github.com/daveusa31/tg-bot/blob/master/examples/settings.py) 
можно увидеть
2. Устанавливаем переменную до того, как подключим библиотеку 
    ```python
    import os
    os.environ.setdefault("TG_BOT_SETTINGS_MODULE", "settings")  # Путь до файла с настройками
    ```
3.  Запускаем шедулер
    ```python
    from tg_bot.etc import schedule
    schedule.setup()
    ```
4. Теперь ждите бекапы



