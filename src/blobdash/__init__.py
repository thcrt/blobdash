import flask as f
from click import secho
from pydantic import ValidationError

from .settings import Settings
from .auth import AuthentikAuthProvider


def create_app():
    app = f.Flask(__name__)

    try:
        settings = Settings()
        if app.debug:
            secho("Loaded configuration:", bold=True)
            print(settings.model_dump_json(indent=2))
    except ValidationError as e:
        secho("Configuration file was missing or had an error!", bold=True, fg="bright_red")
        secho(e)
        raise SystemExit(1)

    if settings.auth.apps.enabled:
        match settings.auth.apps.provider:
            case "authentik":
                auth = AuthentikAuthProvider(settings.auth.apps.host, settings.auth.apps.token)

    @app.route("/")
    def index():
        user = None
        apps = []

        if settings.auth.enabled:
            user = f.request.headers.get(settings.auth.header)
            user = settings.auth.default_user if user is None else user

            if settings.auth.apps.enabled:
                apps = auth.get_applications(user)

        return f.render_template("index.html.jinja", settings=settings, user=user, apps=apps)

    @app.route("/about")
    def about():
        return settings.about

    return app
