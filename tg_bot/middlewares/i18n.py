from typing import Any, Tuple
from dataclasses import dataclass, field
from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware

from .. import config


@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):
    AVAILABLE_LANGUAGES = {
        "en": LanguageData("🇺🇸", "English"),
        "ru": LanguageData("🇷🇺", "Русский"),
        "uk": LanguageData("🇺🇦", "Українська"),
    }

    def __init__(self, user_profile):
        self.user_profile = user_profile
        super().__init__("bot", path="locales")

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        chat_id = args[0].chat.id
        data: dict = args[-1]

        if "chat" in data:
            language = data["chat"].language
        else:
            language = self.user_profile(chat_id).language
        return language
