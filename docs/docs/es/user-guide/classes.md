# Comandos Basados en Clases

Además de usar decoradores, CliFire permite definir comandos mediante clases. Este enfoque es útil cuando necesitas mayor personalización o lógica compleja en tus comandos.

## Definiendo un Comando con Clases

Para crear un comando basado en clases, hereda de `command.Command` y establece las siguientes propiedades:

- **`_name`**: Nombre del comando. Si deseas agrupar comandos, usa puntos (por ejemplo, `db.create`).
- **`_help`**: Descripción breve que se mostrará en la ayuda.
- **Campos/Argumentos**: Define los argumentos y opciones como atributos de la clase utilizando `command.Field`.

Ejemplo básico:

```python
from clifire import command, out

class CommandGreet(command.Command):
    _name = "greet"
    _help = "Greets the user in a personalized way"

    # Define a field for the name (non-option argument)
    name = command.Field(
        pos=1,
        help="User's name",
        default="World",
        alias=[],
    )

    # Define a field to enable informal greeting (option)
    informal = command.Field(
        pos=None,
        help="Use informal greeting",
        default=False,
        alias=["-i"],
    )

    def fire(self):
        if self.informal:
            out.info(f"Hello, {self.name}! How's it going?")
        else:
            out.info(f"Good morning, {self.name}!")
```

## Registro y Ejecución

Al instanciar la aplicación, el comando se registra y se puede ejecutar desde la línea de comandos:

```bash
$ fire greet
Good morning, World!

$ fire greet Alice -i
Hello, Alice! How's it going?
```

## Ventajas del Enfoque basado en Clases

- **Mayor control y personalización:** Puedes definir métodos y atributos propios para manejar casos de uso complejos.
- **Herencia:** Puedes crear comandos base y extenderlos para compartir comportamientos comunes.
- **Organización:** Resultado en una estructura clara y modular cuando se tiene una gran cantidad de comandos.

## Detalles Internos

Cuando se instancia la aplicación, se registran los comandos definidos como clases. La aplicación llama al método `fire()` del comando correspondiente, luego de haber parseado los argumentos y opciones. Además:

- Los campos se actualizan automáticamente desde el parseo del comando.
- Los alias y conversiones de tipos se gestionan en la clase `Field` (ver [command.py](../../clifire/command.py)).

Con este mecanismo, puedes aprovechar al máximo la flexibilidad de Python y crear comandos con comportamientos avanzados sin complicar la sintaxis a nivel de función.

¡Explora y experimenta creando tus propios comandos personalizados!
