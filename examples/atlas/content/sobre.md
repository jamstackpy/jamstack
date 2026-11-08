+++
title = "Sobre este sitio"
template = "page.html"
+++

Atlas nació como un ejercicio: ¿cuánto se puede construir con tres dependencias?

## Lo que hay debajo

- **Motor:** jamstack 2.0, con Jinja para las plantillas y Markdown para el contenido.
- **Contenido:** doce archivos entre Markdown y HTML, incluyendo un borrador.
- **Tema:** `atlas`, una copia del tema `blog` que vive dentro del proyecto.
- **Salida:** HTML plano en `dist/`, sin runtime ni base de datos.

## Lo que no hay

Ni JavaScript de cliente, ni analítica, ni fuentes remotas. La página que estás leyendo
pesa menos que una foto de un gato.

> Un sitio estático no es un sitio sin movimiento: es un sitio que ya terminó de
> calcularse antes de que llegue el visitante.

## Cómo se genera

Cada archivo de `content/` se convierte en una página. `index.md` se vuelve la raíz;
`guias/index.md` se vuelve `/guias/`; y `guias/avanzado/despliegue.md` se vuelve
`/guias/avanzado/despliegue/`. Las plantillas deciden cómo se ve todo lo demás.
