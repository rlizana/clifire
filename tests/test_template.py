import os
import tempfile

import pytest

from clifire import application


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_app_template(temp_dir):
    folder = os.path.join(os.path.dirname(__file__), "sample", "template")
    app = application.App(template_folder=folder)
    kwargs = {
        "title": "sample",
        "user": "root",
        "items": ["test1", "test2"],
    }
    content = app.template.render("sample.jinja2", **kwargs)
    assert "sample" in content
    assert "Hi root" in content
    assert "test1" in content
    assert "test2" in content

    temp_file = os.path.join(temp_dir, "output.html")
    app.template.write("sample.jinja2", temp_file, **kwargs)
    with open(temp_file, "r") as f:
        content = f.read()
    assert "sample" in content
    assert "Hi root" in content

    temp_file_mark = os.path.join(temp_dir, "output_mark.html")
    mark = "<!-- MARK -->"
    content = app.template.write(
        "sample.jinja2", temp_file_mark, mark=mark, **kwargs
    )
    assert mark in content
    assert content.count(mark) == 2

    with open(temp_file_mark, "w") as f:
        f.write(f"Header\n{mark}\nOld content\n{mark}\nFooter\n")
    content = app.template.write(
        "sample.jinja2", temp_file_mark, mark=mark, **kwargs
    )
    assert "Header" in content
    assert "Footer" in content
    assert "Old content" not in content
