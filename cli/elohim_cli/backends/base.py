from abc import ABC, abstractmethod


class BaseBackend(ABC):
    @abstractmethod
    def chat(self, messages: list[dict], system: str = "") -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...
