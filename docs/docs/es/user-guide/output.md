# Módulo `out`: Salidas y Estilos

El módulo `out` de CliFire facilita la impresión de mensajes en la terminal con distintos estilos y colores, aprovechando la potencia de la biblioteca [Rich](https://rich.readthedocs.io/). Con estas funciones podrás mostrar información, advertencias, errores, mensajes de éxito, depuraciones y hasta actualizaciones en vivo.

## Funciones Principales

Importa el módulo `out` en tu aplicación de la siguiente manera:

```python
from clifire import out
```
A continuación, se describen las funciones más utilizadas:

- **`out.info(text: str) -> None`**
  Muestra un mensaje informativo.
  ```python
  out.info("This is an informational message")
  ```

- **`out.success(text: str) -> None`**
  Muestra un mensaje de éxito, ideal para indicar que una operación se completó correctamente.
  ```python
  out.success("Operation completed successfully")
  ```

- **`out.warn(text: str) -> None`**
  Imprime un mensaje de advertencia, útil cuando se requiere precaución en la ejecución.
  ```python
  out.warn("Warning: check your configuration")
  ```

- **`out.error(text: str) -> None`**
  Muestra un mensaje de error de forma destacada para indicar fallos críticos en el proceso.
  ```python
  out.error("Critical error occurred")
  ```

- **`out.debug(text: str) -> None`**
  Imprime mensajes de depuración, lo que resulta útil durante el desarrollo para rastrear el comportamiento interno.
  ```python
  out.debug("Debug: variable x = 42")
  ```

- **`out.var_dump(var) -> None`**
  Imprime de manera legible el contenido de una variable, resaltando su estructura para facilitar su inspección.
  ```python
  sample_dict = {"key": "value", "numbers": [1, 2, 3]}
  out.var_dump(sample_dict)
  ```

- **`out.LiveText`**
  Es una clase que permite actualizar en vivo la salida de texto en la terminal. Es útil para mostrar barras de progreso o contadores que se actualizan dinámicamente.
  ```python
  live_text = out.LiveText("Starting...")
  live_text.info("Process running")
  live_text.warn("Retrying operation")
  live_text.success("Operation completed", end=False)
  ```


## Uso General

El módulo `out` está diseñado para integrarse de forma transparente en tus comandos y aplicaciones creadas con CliFire, brindando un formato estándar y estilizado para la salida en la terminal. Cada función aplica estilos predefinidos para mantener una experiencia consistente y atractiva.

A continuación, se muestra un ejemplo completo:

```python
import time

from clifire import application, command, out


class OutCommand(command.Command):
    _name = 'out'

    def fire(self):
        print('Text colors')
        print('-' * 80)
        out.info("This is an informational message")
        out.success("Operation completed successfully")
        out.warn("Warning: check your configuration")
        out.error("Critical error occurred")

        print('')
        print('Debug')
        print('-' * 80)
        out.debug("Debug: variable x = 42")
        sample_dict = {"key": "value", "numbers": [1, 2, 3]}
        out.var_dump(sample_dict)

        print('')
        print('Tables')
        print('-' * 80)
        data = [
            {"name": "Luke", "age": 18, "is_student": True},
            {"name": "Elizabeth", "age": 101, "is_student": False},
        ]
        out.table(data, border=True, title="Contacts")

        print('')
        print('Live text')
        print('-' * 80)
        live_text = out.LiveText("Starting...")
        time.sleep(1)
        live_text.info("Process running")
        time.sleep(1)
        live_text.warn("Retrying operation")
        time.sleep(1)
        live_text.success("Operation completed", end=False)
        time.sleep(1)


def main():
    app = application.App()
    app.add_command(OutCommand)
    app.fire("out -v")


if __name__ == "__main__":
    main()

```

![Sample_Out](../../assets/records/sample_out.svg)

## Personalización

El módulo `out` utiliza un objeto de consola de Rich (`out.CONSOLE`) que puede ser personalizado. Si necesitas cambiar los estilos o modificar el comportamiento visual, puedes configurar dicho objeto o consultar la documentación de Rich para más opciones.

---

Con esta guía tendrás una visión general de cómo utilizar el módulo `out` para mejorar la presentación de mensajes en tus aplicaciones CLI creadas con CliFire.
