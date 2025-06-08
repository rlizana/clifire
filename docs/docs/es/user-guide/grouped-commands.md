# Comandos Agrupados en CliFire

CliFire permite organizar los comandos en grupos utilizando una convención de nomenclatura basada en puntos. Esto es especialmente útil cuando tu aplicación CLI tiene muchas funcionalidades, ya que mejora la legibilidad y la organización.

## ¿Cómo funciona?

Para agrupar comandos, simplemente define el nombre del comando utilizando un punto (`.`) para separar el nombre del grupo y el comando específico. Por ejemplo, para agrupar comandos relacionados a la base de datos, puedes usar nombres como `db.create` y `db.drop`.

Cuando se registra el comando, la funcionalidad de ayuda de CliFire (por ejemplo, en el comando de ayuda) detecta el carácter `.` y agrupa automáticamente los comandos bajo el mismo grupo.

## Ejemplo de definición de comandos agrupados
Quien define el grupo es la variable  `_name` de la clase `Command`, o el nombre del método en los decoradores.

Aquí tienes un ejemplo de cómo definir comandos agrupados utilizando clases:
```python
from clifire import command, out

class DbCreateCommand(command.Command):
    _name = "db.create"
    _help = "Create the database"

    def run(self):
        out.info("Database created.")

class DbDropCommand(command.Command):
    _name = "db.drop"
    _help = "Drop a database"

    def run(self):
        out.info("Database removed.")
```

## Registro y ejecución

Registra los comandos en tu aplicación:

```python
from clifire import application

app = application.App(name="MyApp CLI", version="1.0")
app.add_command(CommandDbCreate)
app.add_command(CommandDbDrop)
```

Luego, al ejecutar el comando de ayuda:

```bash
$ fire help
```

La salida mostrará los comandos agrupados, por ejemplo:

```
Available Commands:

  db
    create          Create the database
    drop            Drop the database
```

## Uso de los comandos agrupados en los decoradores
Puedes usar la misma convención de agrupación con los decoradores para agrupar
los comandos, en este caso, los grupos se obtienen del nombre del método usando
el carácter `_`:

```python
from clifire import command

@command.fire
def db_create(cmd):
    """
    Create the database
    """
    out.info("Database created.")

@command.fire
def db_drop(cmd):
    """
    Drop the database.
    """
    out.info("Database removed.")

```

## Consejos adicionales

- **Consistencia en los nombres:** Asegúrate de seguir una convención coherente al nombrar tus comandos (por ejemplo, `grupo.comando`) para que el agrupamiento sea intuitivo.
- **Subgrupos:** Si lo necesitas, puedes definir más niveles de agrupación utilizando más de un punto (por ejemplo, `db.table.create`).
- **Personalización de la ayuda:** Puedes extender la funcionalidad del comando de ayuda para modificar cómo se muestran los grupos si fuera necesario.

Con esta estructura, podrás organizar tus comandos de forma clara y brindar una mejor experiencia a los usuarios de tu aplicación CLI.
