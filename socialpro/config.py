"""Application configuration objects."""
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class PlatformConfig:
    """Configuration describing a supported marketing platform."""

    name: str
    enabled_tools: List[str]


@dataclass
class AppConfig:
    """Application-level configuration container."""

    default_language: str = "en"
    supported_languages: Dict[str, str] = None
    platforms: Dict[str, PlatformConfig] = None

    def __post_init__(self) -> None:
        if self.supported_languages is None:
            self.supported_languages = {"en": "English", "ar": "العربية"}
        if self.platforms is None:
            self.platforms = {
                "telegram": PlatformConfig(
                    name="Telegram",
                    enabled_tools=[
                        "account_management",
                        "messaging",
                        "group_management",
                        "analytics",
                    ],
                )
            }
