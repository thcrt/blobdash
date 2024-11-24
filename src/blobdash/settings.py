from typing import Tuple, Type

from pydantic import BaseModel
from pydantic_extra_types import color
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class AuthSettings(BaseModel):
    header: str = "X-App-User"
    logout_url: str = "https://example.com"


class DashdotSettings(BaseModel):
    enabled: bool = True
    host: str = "https://dash.mauz.dev"
    show_values: bool = True
    widgets: list = [
        "cpu",
        "ram",
        "network",
    ]


class Service(BaseModel):
    name: str = "service"
    desc: str = "a cool service"
    icon: str = "https://www.pngmart.com/files/11/Rickrolling-PNG-Pic.png"
    url: str = "https://google.com"


class Settings(BaseSettings):
    name: str = "exampledash"
    logo: str = "https://www.pngmart.com/files/11/Rickrolling-PNG-Pic.png"
    accent_color: color.Color = "#dc2626"
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

    services: dict[str, Service] = {
        "example1": Service(),
        "example2": Service(),
        "example3": Service(),
    }

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
