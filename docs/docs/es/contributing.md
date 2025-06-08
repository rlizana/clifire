# Contribuir a CliFire

¡Gracias por tu interés en contribuir a CliFire!

Las contribuciones son bienvenidas y ayudan a mejorar este proyecto minimalista para construir aplicaciones CLI en Python.

## ¿Cómo Contribuir?

Existen varias maneras de ayudar:

- **Reportando errores:** Si encuentras un bug o comportamiento inesperado, por favor abre un *issue* en GitHub con una descripción detallada y, si es posible, pasos para reproducirlo.
- **Solicitando nuevas funcionalidades:** Si tienes una idea para mejorar CliFire, abre un *issue* o propone un *pull request*.
- **Código y mejoras:** Si deseas enviar código, asegúrate de seguir las pautas de estilo y añade pruebas unitarias para respaldar tus cambios.
- **Documentación:** Ayuda a mejorar la documentación, ya sea corrigiendo errores, ampliando secciones o añadiendo ejemplos de uso.

## Flujo de Contribución

#### **Fork del repositorio**
   Haz un fork del proyecto en GitHub.

#### **Clona tu fork en local:**
   ```bash
   git clone https://github.com/your-user/clifire.git
   cd clifire
   ```

#### **Crea una rama para tus cambios:**
   ```bash
   git checkout -b my-changes
   ```

#### **Realiza tus cambios:**

   Realiza los cambios necesarios en el código. Asegúrate de que:

   * Sigue las convenciones de estilo del proyecto.
   * Añade pruebas unitarias, el proyecto tiene el 100% de coverage!.
   * Actualiza o añade documentación si fuera necesario.

#### **Ejecuta los tests:**
   Asegúrate de que todos los tests pasan con:
   ```bash
   poetry run pytest
   ```
   Comprueba la cobertura:
   ```bash
   poetry run coverage run -m pytest && poetry run coverage html
   ```

   También puedes usar `poetry run fire coverage` para ejecutar los tests y generar el informe de cobertura.

#### **Realiza un Pull Request:**
   Una vez que estés satisfecho con tus cambios, realiza un *pull request* a la rama principal del repositorio. Describe detalladamente lo que has cambiado y la motivación detrás de ello.

## Buenas Prácticas

- Escribe mensajes de *commit* claros y descriptivos.
- Sigue el formato de [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) para documentar tus cambios.
- Asegúrate de que las nuevas funcionalidades o arreglos no rompan la compatibilidad existente.
- Respeta el formato y la estructura de la documentación existente.

## Revisión y Feedback

Tu *pull request* será revisado por mantenedores del proyecto. Es posible que te pidan ajustes o aclaraciones, ¡así que estate atento a los comentarios!

---

Para más detalles, consulta la [Guía de Contribución Completa](CONTRIBUTING.md) en el repositorio.

¡Gracias por ayudar a que CliFire crezca y mejore!
