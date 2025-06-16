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


def main(command_line: str = None):
    app = application.App(name="CliFire", version="1.0")
    current_dir = os.getcwd()
    out.debug(f"Search commands in {current_dir} folder and parents")
    loaded = False
    while True:
        fire_folder = os.path.join(current_dir, "fire")
        if load(fire_folder):
            loaded = True
            break
        fire_file = os.path.join(current_dir, "fire.py")
        if load(fire_file):
            loaded = True
            break
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    if not loaded:
        out.warn(
            "The file fire.py or folder fire is not in this directory or its "
            "parents"
        )
        out.critical("Fire not found!")
    app.fire(command_line)


if __name__ == "__main__":
    main()
