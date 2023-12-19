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
    owner_id: str = field(default=None)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass
class Record:
    user_id: str
    category_id: str
    sum: int
    created: datetime.datetime = field(default_factory=datetime.datetime.now)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
