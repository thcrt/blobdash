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

## `auth`
Blobdash is built to play nicely behind an authentication system that operates a reverse proxy, such as Authentik. Such a reverse proxy can provide blobdash with an HTTP header to identify a logged-in user.

### `auth.header`
The name of a header that is passed by the reverse proxy, which should be set to the username or display name of the user currently logged in.

### `auth.logout_url`
The URL to which users should be redirected when logging out, in order to invalidate their SSO session.

## `dashdot`
Blobdash can integrate status dashboards from an existing [dashdot](https://getdashdot.com/) instance, displaying graphs on resource usage and availability.

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

## `services`
The core of blobdash is that it lets you display links to the various services you host. These links are displayed as wide 'cards' on desktop viewports, but scaled down to 'apps' on small mobile viewports. Clicking on one will redirect the user to the URL of the service.

Each service is its own entry under this top-level `services` key, where the key is an arbitrary identifier for the service and the value is another set of entries described below.

### `services.<service-name>.name`
The display name fo the service. 

### `services.<service-name>.desc`
A description of the service, shown on larger viewports.

### `services.<service-name>.icon`
The URL to an icon representing the service.

### `services.<service-name>.url`
The URL at which the service is hosted, to which the user will be redirected when clicking it.

### `services.<service-name>.domain` **(Optional)**

The base domain at which the service is hosted. For instance, if you host an instance of Paperless-ngx at `https://paperless.example.com`, you could set `services.paperless-ngx.name` to `"paperless"` and `services.paperless-ngx.domain` to `"example.com"`. 

This functionality is quite specific to my personal setup and may be subject to change in the future to make it more generally useful.

This will default to the value `service_domain`, but can be overridden here. If you don't want to display a full domain name, you can set it to the empty string `""`.
