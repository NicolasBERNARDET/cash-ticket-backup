from collections import defaultdict
from typing import Any, Dict, TypeVar

from pydantic import BaseSettings, SecretStr


class HashableSecretStr(SecretStr):
    def __hash__(self):
        return hash(self.get_secret_value())


KT = TypeVar('KT')
VT = TypeVar('VT')


class HashableDict(dict[KT, VT]):
    def __hash__(self):
        return hash(frozenset(self.items()))


class HashableSettings(BaseSettings):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def __eq__(self, o: object) -> bool:
        return isinstance(o, self.__class__) and self.dict() == o.dict()

    @classmethod
    def from_kwargs(cls, kwargs: Dict[str, Any]):
        settings_dict: Dict[str, Any] = defaultdict(dict)
        prefixes = {
            model.type_.__config__.env_prefix: name
            for name, model in cls.__fields__.items()
            if isinstance(model.type_, type(BaseSettings))
        }
        possible_prefixes = prefixes.keys()
        for name, value in kwargs.items():
            if value is None:
                continue
            matching_prefix = next(
                (prefix for prefix in possible_prefixes if name.startswith(prefix)),
                None,
            )
            if matching_prefix is None:
                settings_dict[name] = value
            else:
                settings_dict[prefixes[matching_prefix]][name[len(matching_prefix):]] = value
        return cls(**settings_dict)
