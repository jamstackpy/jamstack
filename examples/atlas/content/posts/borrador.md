+++
title = "Notas sin publicar"
template = "post.html"
date = 2026-11-01
draft = true
summary = "Este post no debe aparecer en el build normal."
+++

Si estás leyendo esto en el sitio publicado, algo salió mal.

Este archivo existe para comprobar tres cosas:

- Que `jamstack build` lo excluye.
- Que `jamstack build --drafts` lo incluye.
- Que el sitemap y el feed respetan la misma decisión.

## Borradores

Un borrador es una página con `draft = true` en el front matter. No se renderiza, no
entra en los índices y no se publica. Es la forma de escribir sin que el mundo lo vea.
