import json
import urllib.parse
from abc import ABC, abstractmethod

import authentik_client
from mantelo import KeycloakAdmin

from .applications import Application


class AuthProvider(ABC):
    @abstractmethod
    def get_applications(self, username):
        pass


class KeycloakAuthProvider(AuthProvider):
    def __init__(self, host, realm, auth_realm, id, secret):
        self.host = host
        self.realm = realm
        self.auth_realm = realm if auth_realm is None else auth_realm
        self.id = id
        self.secret = secret

        self._api = KeycloakAdmin.from_client_credentials(
            server_url=self.host,
            realm_name=self.realm,
            authentication_realm_name=self.auth_realm,
            client_id=self.id,
            client_secret=self.secret,
        )

    def get_applications(self, username):
        # Get user ID from username. Returns a list of user objects, so choose the first (and only)
        # entry and grab its ID.
        user = self._api.users.get(username=username, exact=True)[0]["id"]

        # Get a list of all clients the user has logged into, by cycling through consents for the
        # user ID and grabbing the client object associated with that client ID
        clients = [
            self._api.clients.get(clientId=consent["clientId"])[0]
            for consent in self._api.users(user).consents.get()
        ]

        return {
            client["clientId"]: Application(
                name=client["name"],
                url=client["baseUrl"],
                icon=client["attributes"]["logoUri"],
                desc=client["description"],
            )
            for client in clients
        }


class AuthentikAuthProvider(AuthProvider):
    def __init__(self, host, token):
        # Base path for Authentik API
        self.host = urllib.parse.urljoin(host, "/api/v3")
        self.token = token

        # Set up API client. The `CoreAPI` is the only one we need to view users and applications
        self._api = authentik_client.CoreApi(
            self._APIClient(
                authentik_client.Configuration(
                    host=self.host,
                    access_token=self.token,
                )
            )
        )

    def get_applications(self, username: str) -> list[Application]:
        # `core_applications_list` requires a numeric user ID, so we need to find the user with the
        # given username first to pass it that ID (the `pk` attribute)
        user = self._api.core_users_list(username=username).results[0]
        list = self._api.core_applications_list(for_user=user.pk)

        return {
            app.slug: Application(
                name=app.name,
                url=app.launch_url,
                icon=urllib.parse.urljoin(self.host, app.meta_icon),
                desc=app.meta_description,
                hidden=(
                    (parsed_url := urllib.parse.urlparse(app.launch_url)).scheme == "blank"
                    and parsed_url.netloc == "blank"
                ),
            )
            for app in list.results
        }

    # We need to subclass the `ApiClient` class from the official `authentik-client` library, to
    # avoid a bug that throws ValidationErrors due to unexpectedly returned None values. This is a
    # hacky workaround.
    # See https://github.com/goauthentik/authentik/issues/12164.
    class _APIClient(authentik_client.api_client.ApiClient):
        def deserialize(self, response_text, response_type):
            """Deserializes response into an object after preprocessing."""
            if response_text:
                try:
                    data = json.loads(response_text)
                except ValueError:
                    return super().deserialize(response_text, response_type)

                data = self.preprocess_data(data)
                response_text = json.dumps(data)

            return super().deserialize(response_text, response_type)

        def preprocess_data(self, data):
            """Recursively replace null or missing values with empty strings for specific fields."""
            if isinstance(data, dict):
                self.replace_null_fields(data)
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        data[key] = self.preprocess_data(value)
            elif isinstance(data, list):
                data = [self.preprocess_data(item) for item in data]
            return data

        def replace_null_fields(self, item):
            """Helper method to replace null or missing fields in a dictionary item."""
            for field in [
                "assigned_application_slug",
                "assigned_application_name",
                "assigned_backchannel_application_slug",
                "assigned_backchannel_application_name",
            ]:
                if item.get(field) is None:
                    item[field] = ""
            return item
