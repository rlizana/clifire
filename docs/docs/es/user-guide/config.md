# Configuration (Configuración)

El módulo `Config` de CliFire se encarga de gestionar la configuración de la aplicación a través de archivos YAML. Permite leer y escribir la configuración, asegurándose de excluir automáticamente los campos privados (aquellos cuyo nombre comienza con `_`).

## Características Principales

- **Exclusión automática de campos privados:**
  Cuando se escribe la configuración, se excluyen las propiedades cuyo nombre inicia con `_`, asegurando que la información sensible o interna no se almacene en el archivo.

- **Carga flexible de archivos de configuración:**
  El método de clase `get_config` permite especificar una lista de posibles archivos de configuración. Se carga el primer archivo existente o, si ninguno existe, se puede crear uno si se indica con la opción `create`.

- **Gestión dinámica de atributos:**
  Los valores de configuración se asignan como atributos de la instancia de `Config`, permitiendo acceder a ellos de forma dinámica mediante el método `get`.

## Ejemplo de Uso

Puede usar el módulo `Config` de manera independiente, o puede usarlo dentro de la clase `App` para manejar la configuración de su aplicación CLI.

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

Ahora podemos ejecutarlo

![Samplapp_Config](../../assets/records/samplapp_config.svg)

### Leer la Configuración

Para cargar la configuración de la aplicación, utiliza el método `get_config`. Por ejemplo:

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

En este ejemplo, si el archivo de configuración existe, se actualizan los atributos de la instancia `cfg`. Si no, `read()` retorna `False`.

### Escribir la Configuración

Para guardar la configuración actual en un archivo, utiliza el método `write()`. Observa cómo se excluyen los campos privados:

```python
from clifire import config

cfg = config.Config(config_file="config.yaml")
cfg.name = "MyApp"
cfg.version = "1.0.0"
cfg._secret_key = "my-secret-key"  # This will not be saved
cfg.write()
```

> **Exclusión de Campos Privados**

> Todas las variables que comienzan con `_` no se guardarán en el archivo YAML. Esto es útil para mantener la privacidad de los datos sensibles o internos de la aplicación.

## Resumen

El módulo `Config` proporciona una forma sencilla y segura de administrar la configuración de tu aplicación CLI mediante archivos YAML. Al leer y escribir la configuración, se excluyen automáticamente los campos privados, lo que ayuda a mantener la seguridad y la limpieza de los datos almacenados.

Esta funcionalidad robusta facilita la centralización y el manejo de la configuración en CliFire, contribuyendo a la flexibilidad y mantenibilidad de tus aplicaciones.
