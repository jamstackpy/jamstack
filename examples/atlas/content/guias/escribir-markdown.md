+++
title = "Escribir Markdown"
template = "guide.html"
summary = "Front matter, rutas limpias y qué se puede escribir en cada archivo."
+++

Cada página es un archivo dentro de `content/`. La extensión decide cómo se procesa:

- **`.md`** pasa por MarkdownIt y el resultado se inyecta en la plantilla.
- **`.html`** se renderiza con Jinja, así que puede usar bucles y condicionales.

## Front matter

El bloque entre `+++` es TOML. Solo `title` es obligatorio; el resto tiene valores por
defecto razonables.

```toml
+++
title = "Escribir Markdown"
template = "guide.html"
summary = "Una línea para los índices."
date = 2026-11-07
draft = false
+++
```

## Rutas

La ruta del archivo se convierte en la URL:

- `index.md` → `/`
- `sobre.md` → `/sobre/`
- `guias/index.md` → `/guias/`
- `guias/avanzado/despliegue.md` → `/guias/avanzado/despliegue/`

Las tablas usan la sintaxis estándar de CommonMark:

| Clave | Tipo | Uso |
| --- | --- | --- |
| `title` | string | Título de la página |
| `date` | fecha ISO | Orden y feed |
| `draft` | boolean | Excluir del build |

Si necesitas algo que la tabla no cubra, escribe HTML directamente.

## Lo que sí funciona

Párrafos, **negrita**, *cursiva*, `código`, listas, enlaces, citas, bloques de código y
HTML crudo. Los encabezados generan anclas automáticas.

> El contenido se escribe una vez; el HTML se genera todas las veces que haga falta.
