from .base import LanguageModule
from .english import EnglishModule
from .hindi import HindiModule
from .telugu import TeluguModule
from .tamil import TamilModule
from .malayalam import MalayalamModule
from .kannada import KannadaModule
from .odia import OdiaModule
from .marathi import MarathiModule

LANGUAGE_REGISTRY: dict[str, LanguageModule] = {
    "en": EnglishModule(),
    "hi": HindiModule(),
    "te": TeluguModule(),
    "ta": TamilModule(),
    "ml": MalayalamModule(),
    "kn": KannadaModule(),
    "or": OdiaModule(),
    "mr": MarathiModule(),
}

LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "hi": "हिंदी",
    "te": "తెలుగు",
    "ta": "தமிழ்",
    "ml": "മലയാളം",
    "kn": "ಕನ್ನಡ",
    "or": "ଓଡ଼ିଆ",
    "mr": "मराठी",
}

__all__ = [
    "LanguageModule", "LANGUAGE_REGISTRY", "LANGUAGE_NAMES",
    "EnglishModule", "HindiModule", "TeluguModule", "TamilModule",
    "MalayalamModule", "KannadaModule", "OdiaModule", "MarathiModule",
]
