from dataclasses import dataclass


@dataclass
class Application:
    name: str
    id: str
    url: str
    icon: str
    desc: str
