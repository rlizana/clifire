# Decoradores en CliFire

En CliFire, los *decorators* facilitan la creación y registro de comandos de manera simple y elegante. Gracias al decorador `@command.fire` puedes transformar fácilmente funciones regulares en comandos CLI.

## ¿Qué es un Decorator?

En Python, un *decorator* es una función que recibe otra función y la extiende o modifica sin alterar su estructura. En el contexto de CliFire, el decorador:

- **Registra el comando** en la aplicación.
- **Extrae información** (nombre, argumentos, docstring) necesaria para el comando.
- **Prepara la función** para invocarse desde la línea de comandos.

## Uso del Decorador `@command.fire`

El decorador `@command.fire` es la forma más sencilla de convertir una función en un comando dentro de CliFire. Por ejemplo, creamos el fichero `fire/greet.py` con el siguiente contenido:

```python
from clifire import command, out


@command.fire
def greet(cmd, name: str = "World", _end_char: str = "?"):
    """
    Greets the user.

    Args:
        name: Name of the user to greet. Defaults to "World".
        _end_char: Character to use at the end of the greeting. Defaults to "?".
    """
    result = cmd.app.shell("whoami")
    out.info(f"System user: {result.stdout}")
    out.success(f"Hello {name}{_end_char}")
```

Al aplicar `@command.fire`:

- La función `greet` se transforma en un objeto comando.
- Se extrae la información del nombre del comando y de los argumentos a partir del docstring.
- El comando queda registrado automáticamente para ser utilizado en la CLI.

## Ventajas de Usar Decorators

- **Simplicidad:** Define comandos con pocas líneas de código.
- **Organización:** Separa la lógica del comando de la configuración de la interfaz CLI.
- **Flexibilidad:** Permite definir argumentos y opciones mediante anotaciones de tipos y comentarios en el docstring.

## Registro Automático del Comando

Cuando defines una función con `@command.fire`, el decorador realiza las siguientes operaciones:

1. Obtiene el nombre del comando utilizando `func.__name__` o un atributo personalizado.
2. Procesa el docstring para extraer la descripción y detalles de cada argumento.
3. Crea dinámicamente una clase que hereda de `command.Command` y que representa el comando.
4. Registra este comando en la aplicación actual mediante `get_current_app().add_command(...)`.

## Ejecución de Comandos

La ayuda se construye automáticamente a partir del docstring, lo que permite a los usuarios entender rápidamente cómo usar el comando:

![Help](../../assets/records/help.svg)

Puedes ejecutar el comando `greet` directamente:
![Greet](../../assets/records/greet.svg)


## El comando `fire`

El comando `fire` es la entrada principal para interactuar con tu aplicación CLI. Permite ejecutar comandos y pasarles argumentos y opciones.

`fire` busca tus comandos o en un fichero `fire.py` o en la carpeta `fire/*.py` del directorio donde se lanza.


## Personalización

Si necesitas modificar el comportamiento de un comando:
- Puedes ajustar las opciones y argumentos en el decorador.
- Utiliza docstrings claros para definir la ayuda del comando.
- Explora la implementación de `@command.fire` en [`clifire/command.py`](clifire/command.py) para ver cómo se procesa la información.

Con este mecanismo basado en decoradores, CliFire te permite construir comandos de forma rápida, manteniendo el código limpio y organizado.

¡Empieza a usar decoradores para simplificar la creación de tus comandos y aprovecha la flexibilidad que ofrece CliFire!
