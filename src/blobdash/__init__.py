import flask as f
from click import secho
import jinja2
import tomllib

def create_app():
    app = f.Flask(__name__)

    try:
        with open("blobdash.toml", "rb") as settings_file:
            app.settings = tomllib.load(settings_file)
    except FileNotFoundError:
        secho("Config file `blobdash.toml` wasn't found!", bold=True, fg="bright_red")
        raise SystemExit(1)

    @app.route("/")
    def index():
        return f.render_template("index.html.jinja", settings=app.settings)

    return app
