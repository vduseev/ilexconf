try:
    import cleo
except ImportError:
    cleo = None

if cleo:
    from .commands.list import ListCommand

    # from .commands.get import GetCommand
    # from .commands.set import SetCommand
    # from .commands.convert import ConvertCommand

    class Application:
        def __init__(self):
            self._app = cleo.Application(name="ilexconf", version="0.6")
            self._app.add(ListCommand())

        def run(self):
            # import debugpy
            # debugpy.listen(10001)
            # debugpy.wait_for_client()
            self._app.run()


else:  # pragma: no cover
    import argparse

    class Application:
        def __init__(self):
            self._parser = argparse.ArgumentParser()

        def run(self):
            self._parser.parse_args()


if __name__ == "__main__":
    Application().run()
