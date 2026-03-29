import urllib.parse
from abc import ABC, abstractmethod

import authentik_client

from .applications import Application


class AuthProvider(ABC):
    @abstractmethod
    def get_applications(self, username) -> dict[str, Application]:
        pass


class AuthentikAuthProvider(AuthProvider):
    def __init__(self, host, token):
        # Base path for Authentik API
        self.host = urllib.parse.urljoin(host, "/api/v3")
        self.token = token

        # Set up API client. The `CoreAPI` is the only one we need to view users and applications
        self._api = authentik_client.CoreApi(
            authentik_client.ApiClient(
                authentik_client.Configuration(
                    host=self.host,
                    access_token=self.token,
                )
            )
        )

    def get_applications(self, username: str) -> dict[str, Application]:
        # `core_applications_list` requires a numeric user ID, so we need to find the user with the
        # given username first to pass it that ID (the `pk` attribute)
        user = self._api.core_users_list(username=username).results[0]
        list = self._api.core_applications_list(for_user=user.pk)

        return {
            app.slug: Application(
                name=app.name,
                url=app.launch_url,
                icon=urllib.parse.urljoin(self.host, app.meta_icon_url),
                desc=app.meta_description,
                hidden=(
                    (parsed_url := urllib.parse.urlparse(app.launch_url)).scheme == "blank"
                    and parsed_url.netloc == "blank"
                ),
            )
            for app in list.results
        }
