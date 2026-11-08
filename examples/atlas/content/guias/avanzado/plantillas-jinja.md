+++
title = "Plantillas con Jinja"
template = "guide.html"
summary = "El contexto site/page/pages y un cálculo real de tiempo de lectura."
+++

Toda plantilla recibe tres objetos:

- `site`: la configuración de `site.toml` (título, autor, idioma, URL base).
- `page`: la página actual (título, URL, fecha, contenido y metadatos).
- `pages`: todas las páginas publicadas, ordenadas por fecha descendente.

## Filtrar sin lógica en el contenido

El índice usa `pages` para separar posts de guías:

```jinja
{% set posts = pages | selectattr("date") | list %}
{% for item in pages if item.template == "guide.html" %}
  <a href="{{ item.url }}">{{ item.title }}</a>
{% endfor %}
```

## Un cálculo real

El tiempo de lectura se calcula en la plantilla. No hay campo extra en el contenido:

```jinja
{% set words = page.content | striptags | wordcount %}
{% set minutes = [(words / 200) | round(0, "ceil") | int, 1] | max %}
<span class="reading-time">{{ minutes }} min de lectura</span>
```

## Reglas del motor

Jinja corre en modo estricto: una variable inexistente es un error, no una cadena vacía.
Eso convierte los typos en fallos de build en lugar de huecos silenciosos.

Los archivos `.html` de `content/` también usan Jinja y el mismo contexto. `contacto.html`
recorre las guías publicadas para construir su lista.
