+++
title = "Despliegue"
template = "guide.html"
summary = "De dist/ a producción: URL base, sitemap, feed y caché."
+++

`jamstack build` deja todo en `dist/`. Ese directorio es el sitio completo: se puede
subir a cualquier hosting estático sin instalar Python en el servidor.

## Antes de publicar

Configura `base_url` en `site.toml`:

```toml
[site]
title = "Atlas"
base_url = "https://atlas.example.com"
```

Sin `base_url` el motor no genera `sitemap.xml` ni `feed.xml`, porque no puede construir
URLs absolutas. Es una decisión deliberada: mejor no publicar un sitemap roto.

## GitHub Pages

```yaml
- uses: actions/checkout@v7
- uses: actions/setup-python@v7
- run: pip install jamstack
- run: jamstack build
- uses: actions/upload-pages-artifact@v3
  with:
    path: dist
```

Añade un `.nojekyll` vacío en `dist/` si tu hosting ignora carpetas que empiezan por
guion bajo. Las URLs limpias (`/sobre/` en vez de `/sobre.html`) funcionan porque cada
página se escribe como `index.html` dentro de su carpeta.

## Caché

Los assets no llevan hash. Para un sitio pequeño, un `Cache-Control: max-age=3600`
sobre `dist/` es suficiente; si cambias el CSS, sube el número de versión en el nombre
o invalida la caché del hosting.
