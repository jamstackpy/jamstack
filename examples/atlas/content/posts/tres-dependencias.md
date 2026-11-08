+++
title = "Tres dependencias"
template = "post.html"
date = 2026-09-30
summary = "Click, Jinja y MarkdownIt: el presupuesto completo del motor."
+++

Un generador de sitios estáticos tiene un trabajo acotado: leer archivos, renderizar
plantillas y escribir HTML. No necesita un framework web, ni un ORM, ni un bundler.

## El presupuesto

- **Click** para la línea de comandos.
- **Jinja** para las plantillas.
- **MarkdownIt** para el contenido.

Eso es todo. El resto es biblioteca estándar: `tomllib`, `http.server`, `pathlib`,
`shutil`, `xml.etree`.

## Lo que se evitó

`livereload` parecía cómodo hasta que dejó de importar en Python 3.12. Un watcher de
`mtime` con `threading` hace lo mismo que necesitamos y no arrastra un árbol de
dependencias.

No hay plugins, ni temas descargables, ni un marketplace. Cada cosa que no existe es una
cosa que no se puede romper en una actualización.
