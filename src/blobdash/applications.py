from dataclasses import dataclass, replace, asdict
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # We only need `AuthProvider` for type checking. Importing during runtime will result in
    # circular dependency badness.
    # See: https://mypy.readthedocs.io/en/stable/runtime_troubles.html#import-cycles
    from .auth import AuthProvider


@dataclass
class Application:
    name: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    desc: Optional[str] = None


class ApplicationProvider:
    # In the method signature, we define the type of the `auth_provider` parameter with a
    # "stringified" type definition. This prevents `AuthProvider` from being evaluated at runtime,
    # avoiding circular dependencies, as described in the comment above the import of `AuthProvider`
    # above.
    # See: https://typing.readthedocs.io/en/latest/spec/annotations.html#string-annotations
    def __init__(
        self, auth_provider: "Optional[AuthProvider]", overrides: dict[str, Application]
    ) -> None:
        self.auth_provider = auth_provider
        self.overrides = overrides

    def get_applications(self, username=""):
        apps = {}

        if self.auth_provider:
            apps = self.auth_provider.get_applications(username)

        for id, app in self.overrides.items():
            if id in apps:
                apps[id] = replace(
                    apps[id], **{k: v for k, v in asdict(app).items() if v is not None}
                )
            else:
                apps[id] = app

        return apps
