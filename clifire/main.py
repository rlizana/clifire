import importlib.util
import os

from clifire import application, out


def load(path):
    if not os.path.exists(path):
        out.debug2("Not exist, skipping")
        return False
    if os.path.isdir(path):
        load_folder(path)
    else:
        load_file(path)
    return True


def load_folder(path):
    for file in os.listdir(path):
        if file.endswith(".py"):
            load_file(os.path.join(path, file))


def load_file(filename):
    out.debug2(f"Loading {os.path.relpath(filename)}")
    module_name = os.path.basename(filename)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    app = application.App(name="CliFire", version="1.0")
    out.debug("Search commands in ./fire folder")
    load(os.path.join(os.getcwd(), "fire"))
    out.debug("Search commands in ./file.py file")
    load(os.path.join(os.getcwd(), "fire.py"))
    app.fire()


if __name__ == "__main__":
    main()
