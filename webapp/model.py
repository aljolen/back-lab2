import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass
class Category:
    name: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass
class Record:
    name: str
    user_id: str
    category_id: str
    created: datetime.datetime
    sum: int
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
