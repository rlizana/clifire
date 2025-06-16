import os

from clifire import command, out


@command.fire
def doc_build(cmd):
    """
    Build the docs
    """
    bash = "rye run mkdocs build"
    cmd.app.shell(bash, path="./docs", capture_output=False)


@command.fire
def doc_serve(cmd):
    """
    Serve the docs
    """
    bash = "rye run mkdocs serve"
    cmd.app.shell(bash, path="./docs", capture_output=False)


@command.fire
def doc_record(cmd, filename: str, _force: bool = False):
    """
    Record terminal session

    Args:
        filename: name of the file with which you want to record the session
        -f, --force: remove files if already exists
    """
    result = cmd.app.shell("which asciinema")
    if not result.stdout:
        out.warn("You can install with `apt install asciinema`")
        out.critical("`asciinema` not found.")
    result = cmd.app.shell("which svg-term")
    if not result.stdout:
        out.warn("You can install with `npm install -g svg-term-cli`")
        out.critical("`svg-term` not found.", code=2)

    file_cast = cmd.app.path(f"./docs/docs/assets/records/{filename}.cast")
    if os.path.exists(file_cast) and _force is True:
        os.remove(file_cast)
    if os.path.exists(file_cast):
        msg = "File cast already exists, you can use --force for overwrite"
        out.critical(msg, code=3)
    out.info(f"Record file in {file_cast}")

    file_svg = cmd.app.path(f"./docs/docs/assets/records/{filename}.svg")
    if os.path.exists(file_svg) and _force is True:
        os.remove(file_svg)
    if os.path.exists(file_svg):
        msg = "File SVG already exists, you can use --force for overwrite"
        out.critical(msg, code=4)

    args = ""
    shell = os.environ.get("SHELL")
    if shell == "/bin/fish":
        args = '-c \'fish --private -C "function fish_prompt; echo -n \\" > \\"; end"\''
    bash = f"asciinema rec {file_cast} {args}"
    pwd = cmd.app.path("./docs/docs")
    out.info(f"You are now in {pwd}")
    cmd.app.shell(bash, path=pwd, shell=True, check=True, capture_output=False)

    with open(file_cast, "r") as f:
        lines = f.readlines()
    lines = [ln for ln in lines if "fish is running in private mode" not in ln]
    with open(file_cast, "w") as f:
        f.writelines(lines)

    cmd.app.shell(
        f"svg-term --in {file_cast} --out {file_svg} --window --padding 10"
    )
    out.success(f"File SVG created in {file_svg}")
    out.info("You can use it in doc with:")
    out.info(f"![{filename.title()}](assets/records/{filename}.svg)")


@command.fire
def doc_publish(cmd):
    """
    Publish docs in https://rlizana.github.io/clifire
    """
    bash = "mkdocs gh-deploy"
    cmd.app.shell(
        bash, path="./docs", shell=True, check=True, capture_output=False
    )
