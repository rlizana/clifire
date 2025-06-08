# Configuration

The `Config` module in CliFire is responsible for managing your application's configuration through YAML files. It allows you to read and write the configuration while automatically ensuring that private fields (those whose names begin with `_`) are excluded.

## Main Features

- **Automatic Exclusion of Private Fields:**
  When writing the configuration, properties whose names start with `_` are excluded, ensuring that sensitive or internal information is not stored in the file.

- **Flexible Loading of Configuration Files:**
  The class method `get_config` allows you to specify a list of possible configuration files. The first existing file is loaded or, if none exists, one can be created if the `create` option is enabled.

- **Dynamic Attribute Management:**
  Configuration values are assigned as attributes of the `Config` instance, allowing you to access them dynamically using the `get` method.

## Usage Example

You can use the `Config` module independently or within the `App` class to manage your CLI application's configuration.

```python
from clifire import application, command, out


class ConfigCommand(command.Command):
    _name = "config"
    _help = "Show config vars"

    def fire(self):
        self.app.config.my_new_var = "My new var"
        out.var_dump(self.app.config)


def main():
    app = application.App(config_files=["~/.myapp.yml"], config_create=True)
    app.add_command(ConfigCommand)
    app.fire()


if __name__ == "__main__":
    main()
```

Now we can run it:

![Samplapp_Config](../../assets/records/samplapp_config.svg)

### Reading the Configuration

To load your application's configuration, use the `get_config` method. For example:

```python
from clifire import config

# Attempt to load configuration from 'config.yaml' or 'default.yaml'
cfg = config.Config.get_config(["config.yaml", "default.yaml"])
if not cfg.read():
    print("Configuration file not found.")
else:
    print("Configuration loaded successfully.")
    print("Application Name:", cfg.get("name"))
```

In this example, if the configuration file exists, the attributes of the `cfg` instance are updated. If it does not exist, `read()` returns `False`.

### Writing the Configuration

To save the current configuration to a file, use the `write()` method. Note how private fields are excluded:

```python
from clifire import config

cfg = config.Config(config_file="config.yaml")
cfg.name = "MyApp"
cfg.version = "1.0.0"
cfg._secret_key = "my-secret-key"  # This will not be saved
cfg.write()
```

> **Private Field Exclusion**
>
> All variables that begin with `_` will not be saved in the YAML file. This is useful for keeping sensitive or internal application data private.

## Summary

The `Config` module provides a simple and secure way to manage your CLI application's configuration using YAML files. When reading and writing configuration data, private fields are automatically excluded, which helps maintain both security and cleanliness of the stored data.

This robust functionality facilitates centralized configuration management in CliFire, contributing to the flexibility and maintainability of your applications.
