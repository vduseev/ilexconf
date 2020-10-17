try:
    import cleo
except ImportError:
    cleo = None

if cleo:
    from ilexconf.console.commands.config import ConfigCommand

    class Application:
        def __init__(self):
            self._app = cleo.Application(name="ilexconf", version="0.6")
            self._app.add(ConfigCommand())

        def run(self):
            self._app.run()

else:
    import argparse

    class Application:
        def __init__(self):
            self._parser = argparse.ArgumentParser()

        def run(self):
            self._parser.parse_args()


if __name__ == "__main__":
    Application().run()
