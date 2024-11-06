import flask as f


def create_app():
    app = f.Flask(__name__)

    @app.route("/")
    def index():
        return f.render_template("index.html")

    return app
