# Tutorial: build a blog

This walks through a complete site: scaffold it, write two posts, add an about
page, change the look, and generate the feed. Every command is safe to run in
an empty directory.

## 1. Create the site

```bash
jamstack init my-blog --theme blog
cd my-blog
```

```
Created site in my-blog using the 'blog' theme
Next steps:
  cd my-blog
  jamstack build
```

You get a small tree:

```
my-blog/
  site.toml
  content/
    index.md
    posts/hello-world.md
  .gitignore
```

`site.toml` is the only configuration file. `content/` holds the pages. The
theme lives inside the package, so your project stays clean.

## 2. Build it

```bash
jamstack build
```

```
Built 2 page(s) into /home/you/my-blog/dist
```

Two pages: the home page and the example post. Now serve it:

```bash
jamstack serve
```

```
Built 2 page(s) into /home/you/my-blog/dist
Serving at http://127.0.0.1:8000/ (Ctrl+C to stop)
```

Open `http://127.0.0.1:8000/`. Leave it running: every time you save a file
under `content/`, `templates/`, `static/`, or `site.toml`, the site rebuilds.
If a template breaks, the terminal reports the error and the browser keeps
showing the last working build.

## 3. Write a post

Create `content/posts/second-post.md`:

```markdown
+++
title = "Why static sites"
date = 2026-11-07
summary = "No runtime, no database, no surprises."
template = "post"
+++

A static site is a folder of files. That is the whole trick.

- Nothing to patch at 3 a.m.
- Nothing to scale.
- Nothing to leak.
```

Save it and reload. The home page lists the post with its date and summary,
and the post is available at `/posts/second-post/`.

The front matter is TOML between `+++` lines. `title` and `date` are the ones
that matter here: the blog theme lists only dated pages, newest first, and the
feed only includes them.

## 4. Add an about page

Create `content/about.md`:

```markdown
+++
title = "About"
template = "page"
+++

I write about small tools and static sites.
```

It is published at `/about/`. Because it has no `date`, it does not appear in
the post list. Link it from the home page by editing `content/index.md`:

```markdown
+++
title = "Welcome"
+++

Notes on small tools.

[About this site](/about/)
```

## 5. Describe the site

Open `site.toml` and fill it in:

```toml
[site]
title = "Small Tools"
description = "Notes on small tools and static sites."
author = "Your Name"
base_url = "https://example.com"
language = "en"

[build]
output = "dist"

[theme]
name = "blog"
```

`base_url` is the public URL of the site. Set it to the real domain when you
deploy: it makes the links in `sitemap.xml` and `feed.xml` absolute. While it
is empty, both files are skipped instead of being written with relative URLs.

After saving, check `dist/sitemap.xml`, `dist/feed.xml`, and `dist/404.html`.

## 6. Change the look

For small changes, customize the theme's stylesheet. Files in the project's
`static/` are copied after the theme's and overwrite the same path, so the
theme's `/style.css` is the file to replace:

```bash
jamstack build
mkdir -p static
cp dist/style.css static/style.css
```

Now edit `static/style.css` and change the accent color:

```css
:root {
  --accent: #b45309;
}
```

Run `jamstack build` again and the site uses your copy. The rest of the theme
is untouched.

For structural changes, create a local copy of the theme:

```bash
mkdir -p themes
cp -r "$(python -c 'import jamstack, pathlib; print(pathlib.Path(jamstack.__file__).parent / "themes" / "blog")')" themes/blog
```

Edit `themes/blog/templates/` freely. Local themes take precedence over bundled
ones with the same name, so no configuration change is needed. See
[Themes](themes.md) for the template variables and the full format.

## 7. Publish

```bash
jamstack build --clean
```

Upload the contents of `dist/` to any static host. [Deployment](deployment.md)
has the settings for GitHub Pages, Netlify, and Cloudflare Pages.

## Next steps

- [Content](content.md) explains URL mapping, drafts, and HTML pages.
- [Configuration](configuration.md) lists every key in `site.toml`.
- [Command line](cli.md) covers the flags used above.
