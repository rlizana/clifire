# Opciones y Argumentos en CliFire

En CliFire, los comandos pueden recibir datos tanto como **argumentos posicionados** como **opciones**. Estos se definen mediante la clase `Field` en el módulo `command`.

## Definición de Campos

Cada campo que se declara como atributo en un comando se reconoce como:

- **Argumento Posicionado:**
  Si el campo tiene un valor de `pos` definido (por ejemplo, `pos=1`), se trata de un argumento que se espera en un orden determinado.
  Los argumentos se asignan en base a su posición en la línea de comandos.

- **Opción:**
  Si `pos` es `False` o `None`, el campo se interpreta como una opción.
  Estas se indican en la línea de comandos con un guión simple o doble (por ejemplo, `-v` o `--verbose`).
  Además, se pueden definir alias para facilitar su uso.

## Ejemplo de Definición en un Comando

```python
from clifire import command, out

class CommandTest(command.Command):
    _name = "test"
    _help = "Example command using options and arguments"

    # Argumento posicionado (por ejemplo, el primer argumento luego del nombre del comando)
    filename = command.Field(
        pos=1,
        help="Name of the file to process",
        default="default.txt",  # default value if not specified
    )

    # Opción que se activa con bandeja (por ejemplo, -v para verbose)
    verbose = command.Field(
        pos=False,
        help="Detailed mode",
        default=False,
        alias=["v"],
    )

    # Opción que espera un valor (por ejemplo, --level=3)
    level = command.Field(
        pos=False,
        help="Level of detail",
        default=1,
        alias=["l"],
        force_type=int,
    )

    def run(self):
        out.info(f"File: {self.filename}")
        out.info(f"Verbose: {self.verbose}")
        out.info(f"Level: {self.level}")
```

En este ejemplo:
- **`filename`** es un argumento posicionado: se asigna el primer valor no asociado a una opción.
- **`verbose`** es una opción booleana: se activa con `-v` o `--verbose`.
- **`level`** es una opción que espera un valor numérico, pudiendo usarse de la forma `--level=3` o `-l 3`.

## Proceso de Parseo y Conversión

Cuando se ejecuta un comando:
1. **Parseo:**
   CliFire lee la línea de comandos y separa los **argumentos** y **opciones** utilizando `shlex.split()`.
   Los argumentos posicionados se asignan según el orden definido en la propiedad `_argument_names` del comando.

2. **Conversión de Valores:**
   Cada campo utiliza su método `convert` para transformar el valor recibido de cadena a su tipo esperado.
   Por ejemplo:
   - Si se define el campo `level` con `force_type=int`, la cadena se convertirá a entero.
   - Si el campo es de tipo `list`, se puede usar una separación por comas para obtener una lista de elementos.

3. **Validaciones:**
   - Si un campo es obligatorio (sin valor por defecto), se comprueba que se haya proporcionado un valor.
   - Las opciones pueden tener alias; estos se normalizan (por ejemplo, eliminando guiones y reemplazando `-` por `_`) para evitar duplicados.

## Ejecución de un Comando con Opciones y Argumentos

Al ejecutar el comando anterior desde la terminal, podrías tener diferentes comportamientos:

```bash
$ fire test myfile.txt -v --level=5
```

- El valor `"myfile.txt"` se asignará a `filename`.
- La opción `-v` hará que `verbose` sea `True`.
- El argumento `--level=5` se convertirá a entero (`5`) y se asignará a `level`.

Si no se proporcionan algunos de estos valores, se utilizarán los valores por defecto definidos.

## Conclusión

Gracias a esta estructura flexible, CliFire permite definir de forma sencilla cómo se reciben y procesan los datos en tus comandos. Puedes combinar argumentos posicionados y opciones con alias, validación y conversión automática de tipos, lo que facilita la construcción de interfaces de línea de comandos robustas y fáciles de usar.

¡Experimenta creando tus propios comandos y ajustando las opciones según las necesidades de tu aplicación!
