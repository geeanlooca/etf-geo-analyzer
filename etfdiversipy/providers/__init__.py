from abc import ABC, abstractmethod
from enum import Enum
from etfdiversipy.fund import Fund


class Provider(ABC):
    @abstractmethod
    def get_available_funds(self, *args, **kwargs) -> list[Fund]:
        pass


class Providers(Enum):
    BLACKROCK = "blackrock"
    ISHARES = "ishares"
    LYXOR = "lyxor"
    VANGUARD = "vanguard"


class BlackRock(Provider):
    def get_available_funds(self, *args, **kwargs):
        pass


def get_provider(provider: Providers) -> Provider:
    if provider == "blackrock":
        return BlackRock()
    else:
        raise ValueError(f"Provider {provider} not supported")


def get_providers() -> list[Provider]:
    ...
