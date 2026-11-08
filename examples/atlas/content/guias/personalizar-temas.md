+++
title = "Personalizar temas"
template = "guide.html"
summary = "Qué hay dentro de un tema y cómo pisarlo sin copiar todo el proyecto."
+++

Un tema es una carpeta con tres cosas:

```text
themes/atlas/
  theme.toml      # nombre y descripción
  templates/      # plantillas Jinja
  static/         # CSS, imágenes, fuentes
  scaffold/       # contenido inicial opcional
```

## Dónde se busca

1. `themes/<nombre>/` dentro del proyecto.
2. El tema empaquetado con el motor.

El proyecto siempre gana. Si creas `templates/colophon.html`, esa plantilla reemplaza a
la del tema sin tocar el resto.

## Estáticos

La copia va en dos pasadas: primero el tema, después el proyecto. Un
`static/atlas.css` en el proyecto sobrescribe el del tema.

Este sitio lo demuestra: el tema trae un logo verde, pero el proyecto publica uno ocre
con montañas. El CSS del proyecto cambia el acento y el colofón del pie.

## Copiar un tema empaquetado

Sirve para empezar con una base que ya funciona:

```bash
cp -r "$(python -c 'import jamstack, pathlib; print(pathlib.Path(jamstack.__file__).parent / "themes" / "blog")')" themes/atlas
```

Luego cambia el nombre en `theme.toml` y apunta `[theme] name` a la nueva carpeta.
