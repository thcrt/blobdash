import flask as f
from click import secho
import tomllib


def create_app():
    app = f.Flask(__name__)

    for path in ["blobdash.toml", "/blobdash.toml"]:
        try:
            with open(path, "rb") as file:
                app.settings = tomllib.load(file)
            secho(f"Loaded settings from {path} successfully.")
            break
        except FileNotFoundError:
            pass
    else:
        # `else` clause in `for` loop is called when the loop executed without `break`ing at least once
        # in this case, it means none of the files were found
        secho("Config file `blobdash.toml` wasn't found anywhere!", bold=True, fg="bright_red")
        raise SystemExit(1)

    @app.route("/")
    def index():
        return f.render_template(
            "index.html.jinja",
            settings=app.settings,
            user=f.request.headers.get(app.settings["auth"]["header"]),
        )

    @app.route("/about")
    def about():
        return app.settings["about"]

    return app
