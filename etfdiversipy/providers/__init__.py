from abc import ABC, abstractmethod
from enum import Enum
from etfdiversipy.fund import Fund


class Provider(ABC):
    @abstractmethod
    def get_available_funds(self, *args, **kwargs) -> list[Fund]:
        pass


class Providers(Enum):
    ISHARES = "ishares"
    LYXOR = "lyxor"
    BLACKROCK = "blackrock"
    VANGUARD = "vanguard"


class iShares(Provider):
    def get_available_funds(self, *args, **kwargs):
        raise NotImplementedError("iShares not implemented yet")


class BlackRock(Provider):
    def get_available_funds(self, *args, **kwargs):
        raise NotImplementedError("BlackRock not implemented yet")


class Lyxor(Provider):
    def get_available_funds(self, *args, **kwargs):
        raise NotImplementedError("Lyxor not implemented yet")


class Vanguard(Provider):
    def get_available_funds(self, *args, **kwargs):
        raise NotImplementedError("Vanguard not implemented yet")


def get_provider(provider: Providers) -> Provider:
    if provider == Providers.ISHARES:
        return iShares()
    if provider == Providers.BLACKROCK:
        return BlackRock()
    if provider == Providers.LYXOR:
        return Lyxor()
    if provider == Providers.VANGUARD:
        return Vanguard()

    raise ValueError("Invalid provider")


def get_providers() -> list[Provider]:
    ...


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the setup of a provider")
    parser.add_argument("provider", help="Provider to use", type=Providers)
    args = parser.parse_args()

    try:
        provider = get_provider(args.provider)
        print(provider.get_available_funds())
    except NotImplementedError as e:
        print(e)
        exit(1)
    except ValueError as e:
        print(e)
        exit(1)
