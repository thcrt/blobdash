from typing import Tuple, Type, Optional, Literal

from pydantic import BaseModel
from pydantic_extra_types import color
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class AuthApplicationSettings(BaseModel):
    enabled: bool = False
    provider: Literal["authentik"] = "authentik"
    host: str = "https://auth.example.com"
    token: str = "changeme"


class AuthSettings(BaseModel):
    enabled: bool = False
    header: str = "X-App-User"
    logout_url: str = "/flows/-/default/invalidation"
    default_user: Optional[str] = None
    apps: AuthApplicationSettings = AuthApplicationSettings()


class DashdotSettings(BaseModel):
    enabled: bool = True
    host: str = "https://dash.mauz.dev"
    show_values: bool = True
    split_view: bool = False
    widgets: list = [
        "cpu",
        "ram",
        "network",
    ]


class Settings(BaseSettings):
    name: str = "mydash"
    logo: str = "/static/blobcat.png"
    accent_color: color.Color = "#fcc21b"
    service_domain: str = "example.com"

    about: str = """
<h4>Welcome to my dashboard</h4>
<p>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
    laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
    non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
</p>"""

    auth: AuthSettings = AuthSettings()
    dashdot: DashdotSettings = DashdotSettings()

    model_config = SettingsConfigDict(toml_file=["blobdash.toml", "/blobdash.toml"])

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
