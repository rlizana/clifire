# Guía Rápida - Empezando con CliFire

Bienvenido a la guía rápida de CliFire, un framework minimalista para crear interfaces de línea de comandos en Python de forma sencilla y elegante.

## Instalación

Puedes instalar CliFire desde PyPI o directamente usando Poetry:

### Desde PyPI

```bash
pip install clifire
```

### Usando Poetry

```bash
poetry add clifire
```

## Uso Básico

CliFire te permite definir comandos mediante decoradores o clases. Aquí tienes un ejemplo utilizando un decorador para saludar al usuario:

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

### Ejecutando el Comando

Guarda el archivo como `fire.py` o crea un directorio `fire` y coloca el archivo dentro con extensión `.py`.

La ayuda se construye automáticamente a partir del docstring, lo que permite a los usuarios entender rápidamente cómo usar el comando:

![Help](../assets/records/help.svg)

Puedes ejecutar el comando `greet` directamente:
![Greet](../assets/records/greet.svg)

## Características Principales

- **Definición Sencilla de Comandos:** Usa decoradores o clases para crear comandos dinámicos.
- **Manejo de Argumentos y Opciones:** Define argumentos y opciones para personalizar el comportamiento de tus comandos.
- **Salida formateada:** Utiliza el módulo `out` para mostrar mensajes con estilos y colores usando la libreria `Rich`.
- **Configuración centralizada:** Administra la configuración de tu aplicación mediante la clase `Config`.
- **Plantillas de ficheros:** Crea archivos con plantillas Jinja2 usando la clase `Template`.

## Próximos Pasos

- Para más detalles sobre la API y configuración, consulta la [Documentación de Usuario](user-guide/basics.md).
- Revisa la [API Reference](api/index.md) para ver todas las funciones y clases disponibles.
- Mira ejemplos prácticos en la sección [Ejemplos](examples.md).

¡Empieza a crear tus comandos y disfruta de una experiencia minimalista y potente con CliFire!
