# Conceptos Básicos de CliFire

CliFire es un framework minimalista para crear aplicaciones de línea de comandos en Python de forma sencilla y elegante. Esta guía te introduce en los conceptos fundamentales para que puedas empezar a utilizarlo rápidamente.

Tenemos dos sabores para usar CliFire, por decoradores o por clases:

- **Decoradores:** Permiten definir comandos de forma rápida y sencilla, sin perder potencia ni flexibilidad.
- **Clases:** Ofrecen un control más detallado sobre el comportamiento de los comandos, ideal para aplicaciones más complejas.

La idea de CliFire es que puedas crear aplicaciones CLI (Command Line Interface) de forma rápida y sencilla, aprovechando las características de Python.

## 1. Comandos

Los comandos son la esencia de tu aplicación CLI. Puedes definirlos de dos formas:

- **Usando decoradores:**
  Se facilita la creación de comandos con el decorador `@command.fire`.

  ```python
  from clifire import command, out

  @command.fire
  def hello(cmd, name: str = "World"):
      """
      Greets the user.

      Args:
          name: Name of the user. Defaults to "World".
      """
      out.info(f"Hello, {name}!")
  ```

- **Usando clases:**
  Crear una clase que herede de `command.Command` para tener mayor control sobre el comportamiento del comando.

  ```python
  from clifire import command, out

  class CommandTest(command.Command):
      _name = "test"
      _help = "Test command"

      def fire(self):
          out.info("Executing test command")
  ```

## 2. Opciones y Argumentos

CliFire te permite definir:

- **Opciones Globales:** Configuraciones que afectan a toda la aplicación (por ejemplo, el modo verbose).
- **Opciones Locales:** Argumentos y opciones específicos para cada comando.

Estas opciones se pueden establecer con la clase `Field` del módulo `command`.

```python
from clifire import command

class CommandTest(command.Command):
    _name = "test"
    _help = "Test command"

    bool_option = command.Field(
        pos=1,
        help="Example boolean option",
        default=False,
        alias=["-v"],
    )

    def fire(self):
        if self.bool_option:
            print("Verbose option enabled")
        else:
            print("Verbose option disabled")
```

## 3. Configuración

La clase `Config` gestiona la configuración de tu aplicación. Permite leer datos de ficheros YAML y escribirlos, excluyendo campos privados (aquellos que comienzan con `_`).

```python
from clifire import config

conf = config.Config(config_file="config.yaml")
conf.name = "MyApp"
conf.version = "1.0.0"
conf.write()
```

*Nota:* Los campos privados (por ejemplo, `_secret`) no se guardan en el fichero de configuración.

## 4. Salida y Estilos

El módulo `out` utiliza la biblioteca Rich para mostrar mensajes con distintos estilos y colores:

- `out.info()`: Información.
- `out.success()`: Éxito.
- `out.warn()`: Advertencia.
- `out.error()`: Error.

```python
from clifire import out

out.info("This is an informational message")
```

## 5. Plantillas

La clase `Template` te permite generar archivos a partir de plantillas Jinja2. Esto es útil para crear ficheros con contenido dinámico de forma sencilla.

```python
from clifire import template

tpl = template.Template(template_folder="templates")
content = tpl.render(
    "sample.jinja2",
    title="My Title",
    user="admin",
    items=["data1", "data2"]
)
```

Además, la función `write` de la plantilla permite guardar el contenido renderizado en un fichero, con la opción de insertar o reemplazar contenido delimitado por marcas.

Esto es útil para generar archivos de configuración o scripts personalizados que se pueden actualizar fácilmente en el futuro sin afectar al resto del contenido del archivo.


## 6. Flujo de Ejecución

1. **Definición de Comandos:**
   Se definen mediante decoradores o clases.

2. **Registro de Comandos:**
   Al instanciar `App` se registran los comandos. Por defecto, se añade un comando de ayuda que muestra la información de todos los comandos disponibles.

3. **Parseo y Ejecución:**
   Al lanzar la aplicación se analiza la línea de comandos, se identifica el comando a ejecutar y se procesan sus opciones y argumentos.

## Conclusión

Con estos conceptos básicos, ya estás listo para empezar a usar CliFire en tus proyectos. La simplicidad y flexibilidad de este framework te permitirán construir aplicaciones CLI potentes y personalizadas sin complicaciones.

Para más detalles y ejemplos avanzados revisa la [Guía de Usuario](../user-guide/index.md) y la [API Reference](../api/index.md).
