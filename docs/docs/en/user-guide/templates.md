# Templates in CliFire

The `Template` module in CliFire allows you to render and save files using templates based on [Jinja2](https://jinja.palletsprojects.com/). This functionality helps you generate dynamic content easily, making it ideal for creating configuration files, reports, or other documents that require customization.

You can use the `Template` module independently, or you can use it within the `App` class to manage your CLI application's configuration.

The file `sample_template/hello.jinja2` is an example of a template that can be used with the `Template` module. Here is an example of what the template content might look like:

```jinja2
<h1>{{ title }}</h1>
<ul>
    {% for number in numbers %}
        <li>{{ number }}</li>
    {% endfor %}
</ul>
```

The CLI command will be called `app_template.py` and will look like this:
```python
from clifire import application, command, out


class HelloCommand(command.Command):
    _name = "hello"
    _help = "Create template"

    title = command.Field(
        pos=1,
        force_type=str,
    )

    def fire(self):
        print(self.title)
        content = self.app.template.render(
            'hello.jinja2', title=self.title, numbers=[1, 2, 3])
        out.success(content)


def main():
    app = application.App(template_folder="./sample_template")
    app.add_command(HelloCommand)
    app.fire()


if __name__ == "__main__":
    main()
```
Running this command will render the `hello.jinja2` template with the given title and a list of numbers, displaying the result in the terminal.

![Samplapp_Template](../../assets/records/samplapp_template.svg)


## Main Functions

- **`Template.render(template: str, **args) -> str`**
  Renders a specified template. It receives the template file name and additional parameters that will be used to substitute the variables defined in the template.

  Example:
  ```python
  from clifire import template

  # Create the Template object by specifying the folder where the templates are located.
  tpl = template.Template("templates")
  content = tpl.render("sample.jinja2", title="My Title", user="admin", items=["one", "two"])

  # 'content' will contain the HTML generated with the provided values.
  print(content)
  ```

- **`Template.write(template: str, filename: str, mark: Optional[str] = None, **args) -> str`**
  Renders the template and saves its content to a file.
  If a `mark` parameter is specified, the rendered content will be inserted or replaced between special markers in the file; this is useful for updating specific sections without overwriting the rest of the content.

  Example without a marker:
  ```python
  tpl = template.Template("templates")
  rendered = tpl.write("sample.jinja2", "output.html", title="My Title", user="admin", items=["one", "two"])
  ```

  Example with a marker:
  ```python
  tpl = template.Template("templates")
  # The marker '<<CONTENT>>' will delimit the section to update.
  rendered = tpl.write("sample.jinja2", "output.html", mark="<<CONTENT>>", title="My Title", user="admin", items=["one", "two"])
  ```

## How It Works

1. **Template Rendering:**
   The `render` method loads the template file using Jinja2 and processes it with the provided arguments. This allows you to generate dynamic content based on variables defined in your template.

2. **Saving and Updating Files:**
   With the `write` method, you can directly save the rendered content to a file.
   If you specify a `mark`:
   - The method searches within the file for the section delimited by that marker.
   - If it finds the section, it replaces it with the new rendered content.
   - If it does not exist, it appends the section at the end of the file.
   This enables you to update specific parts of the file without losing the original content that lies outside of the markers.

3. **Dynamic Integration:**
   The `Template` object integrates with the rest of CliFire, allowing you to utilize environment variables or any other business logic during rendering.

## Complete Example

```python
from clifire import template

def generate_report():
    # Initialize the template by specifying the template folder
    tpl = template.Template("templates")

    # Render the sample.jinja2 template with dynamic data
    content = tpl.render("sample.jinja2", title="Report", user="admin", items=["Item 1", "Item 2", "Item 3"])
    print("Rendered Content:")
    print(content)

    # Save the rendered content to output.html without using markers
    tpl.write("sample.jinja2", "output.html", title="Report", user="admin", items=["Item 1", "Item 2", "Item 3"])

    # Save the content to output_marked.html using a marker to update only a section
    tpl.write("sample.jinja2", "output_marked.html", mark="<<CONTENT>>", title="Report", user="admin", items=["Item 1", "Item 2", "Item 3"])

if __name__ == "__main__":
    generate_report()
```

## Conclusion

The `Template` module allows you to separate content logic from presentation, making it easier to generate dynamic files from templates. This improves the maintainability and flexibility of your CLI applications, as you can update specific sections of a file without affecting the rest of the content.

This functionality is especially useful for projects that require periodic creation or updating of reports, configuration files, or any other type of document based on templates.
