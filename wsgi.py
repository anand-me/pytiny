from pytiny.web import create_app

app = create_app()

if __name__ == "__main__":
    from pytiny.config import Config
    config = Config.load()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
