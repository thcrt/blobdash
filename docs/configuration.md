# `blobdash.toml`

## `name`
The name of the dashboard, displayed throughout the application.

## `logo`
The URL to fetch a logo from. Ensure it's properly formed, including an `https://` prefix.

## `accent_color`
The color used as a secondary accent for various UI elements, including the title and graphs. This can be any [CSS color](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value), such as `#ff00ff`, `oklch(70% 0.3 330)` or `magenta`. 

## `service_domain`
The base domain name at which you host your services. This is used on larger viewports to display the full domain name for each service.

It can be overridden on a per-service level using `services.<service-name>.domain`.

This does not have any functional effect, and is only for appearance purposes. If you don't want full domain names to show up, you can set it to the empty string `""`.

## `about`
The HTML that will be shown to users who click the 'about' link in the sidebar. The TOML specification allows strings to span multiple lines by using three double-quotes (`"""`) at the beginning and end of the string, which may be useful for longer about sections.

## `dashdot`
blobdash can integrate status dashboards from an existing [dashdot](https://getdashdot.com/) instance, displaying graphs on resource usage and availability.

Note that graphs are displayed [using `iframe`s](https://getdashdot.com/docs/integration/widgets), and are not proxied, meaning that the user's device must be able to connect to the dashdot instance independently. Running a dashdot instance locally on your server in a way that only makes it available to blobdash and not externally visible will not work.

### `dashdot.enabled`
Whether to enable dashdot integration.

### `dashdot.host`
The hostname of the running dashdot instance. 

By default, this is set to `"https://dash.mauz.dev"`, a demo instance run by the developer of dashdot. Obviously, it doesn't reflect the actual status of your system when unchanged.

### `show_values`
Whether to display numerical values on the graphs.

### `split_view`
Whether to show storage devices in [split view](https://getdashdot.com/docs/integration/widgets#multiview). Doesn't apply to CPU cores.

### `widgets`
A list of the statistics that should be displayed as graphs. Allowed values can be seen at [dashdot's documentation](https://getdashdot.com/docs/integration/widgets#graph). At the time of writing, the list can contain:
- `"cpu"`
- `"storage"`
- `"ram"`
- `"network"`
- `"gpu"`

Because these values are passed directly to your dashdot instance, and future updates to dashdot may result in new options becoming available, this option is deliberately not validated by blobdash itself.

## `auth`
blobdash is built with authentication provider integration as a key goal. It supports header authentication to display a user menu and logout button, and can also query the provider's API to fetch applications that the current user has permission to access.

### `auth.enabled`
Whether to enable authentication functionality. 

A user menu with a button to log out will be displayed if this is set to `true` and the header specified in `auth.header` is present in the received request. If this is set to `false`, or if there is no such header, no user menu will be displayed.

### `auth.header`
The name of a header that is passed by the authentication provider's reverse proxy, containing the username of the currently logged in user.

### `auth.logout_url`
The URL to which users should be redirected when logging out, in order to invalidate their SSO session.

### `auth.default_user`
Requests that do not have the HTTP header specified by `auth.header` set will be treated as though there is a user logged in with the username set here. By default, this is unset, and requests without the appropriate header will be treated as unauthenticated.

### `auth.apps.enabled`
This determines whether blobdash should query the API of the authentication provider to get a list of apps to display.

Application fetching from the authentication provider's API will be enabled if both `auth.enabled` and `auth.apps.enabled` are set to `true`. If either is set to `false`, application fetching will be disabled. This is because querying the API requires a username to show applications available to that user.

If application fetching is disabled, blobdash can still be used in 'single-user mode' by manually adding applications under `apps`.

### `auth.apps.provider`
The software being used as an authentication provider. Right now, the only supported authentication provider is [authentik](https://goauthentik.io/), and hence the only allowed value is `"authentik"`. This is also the default value, and this field can be safely left out of your configuration. It exists for future expansion to accomodate other providers.

### `host`
The host at which the authentication provider can be reached, e.g. `"https://auth.example.com"`.

### `token`
The token to authenticate with the provider's API. The user for whom this token was generated must have access to view users and applications. For security, it's a good idea to create a service account with only the minimum permissions necessary. 

## `apps`
Manually specify apps to be displayed. Any apps configured here will be shown to all users, regardless of authentication. 

Each app is its own entry under this top-level `apps` key, where the key is an identifier for the app and the value is a set of entries described below.

If the key of an app entered here matches the ID of an app obtained from querying the authentication provider, the values specified will override those sourced from the authentication provider. Any values not overridden here will remain unchanged.

### `apps.<app-name>.name`
The display name for the app. 

### `apps.<app-name>.desc`
A description of the app, shown on larger viewports.

### `apps.<app-name>.icon`
The URL to an icon representing the app.

### `apps.<app-name>.url`
The URL at which the app is hosted, to which the user will be redirected when clicking it.
