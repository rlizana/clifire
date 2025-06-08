import os
import re

import jinja2


class Template:
    def __init__(self, template_folder: str):
        self.jinja2 = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_folder)
        )

    def render(self, template, **args):
        args["os"] = os
        return self.jinja2.get_template(template).render(**args)

    def write(self, template, filename, mark=None, **args):
        template_content = self.render(template, **args)

        if not mark:
            with open(filename, "w") as file:
                file.write(template_content)
            return template_content

        content = ""
        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
        mark_escaped = re.escape(mark)
        pattern = f"({mark_escaped})[\\s\\S]*?\\1"
        if re.search(pattern, content):
            content = re.sub(
                pattern, f"{mark}\n{template_content}\n{mark}", content
            )
        else:
            content += f"\n{mark}\n{template_content}\n{mark}\n"
        with open(filename, "w") as file:
            file.write(content)
        return content
