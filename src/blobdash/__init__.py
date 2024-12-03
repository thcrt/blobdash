import flask as f
from click import secho
from pydantic import ValidationError

# import authentik_client

from .settings import Settings


def create_app():
    app = f.Flask(__name__)

    try:
        app.settings = Settings()
        if app.debug:
            secho("Loaded configuration:", bold=True)
            print(app.settings.model_dump_json(indent=2))
    except ValidationError as e:
        secho("Configuration file was missing or had an error!", bold=True, fg="bright_red")
        secho(e)
        raise SystemExit(1)

    @app.route("/")
    def index():
        if app.settings.auth.enabled:
            user = f.request.headers.get(app.settings.auth.header)
            user = app.settings.auth.default_user if user is None else user

        return f.render_template("index.html.jinja", settings=app.settings, user=user)

    @app.route("/about")
    def about():
        return app.settings.about

    return app
