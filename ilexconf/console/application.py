try:
    import cleo
except ImportError:
    cleo = None


class Application:
    def __init__(self):
        if cleo is not None:
            self.application = cleo.Application()
            # Add commands here
        else:
            self.application = None

    def run(self):
        if cleo is not None:
            self.application.run()
        else:
            print((
                "CLI application is not supported in ilexconf\n"
                "when 'console' extra is not installed.\n"
                "Install the console with\n"
                "    pip install ilexconf[console]\n"
                "or for development\n"
                "    poetry install -E console;'"
            ))


if __name__ == "__main__":
    Application().run()
