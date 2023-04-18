<div align="center">
  <img alt="Jamstack logo" src="https://i.imgur.com/sXUAdYJ.png" height="217" />
</div>

![](https://img.shields.io/pypi/v/jamstack)

Also known as Jamstackpy, is a tool that allows you to create static websites using the power of **Python** hand in hand
with the [Flask](https://github.com/pallets/flask) library. Its operation is based on templates which are rendered with
the powerful Jinja engine generating your website with all its dependencies.

## Installation

```bash
python -m pip install jamstack
```

## Create basic project

```bash
jamstack plain <foldername>
```

## Templates

Jamstack has templates available courtesy of [html5up](https://html5up.net).

| Template                                   | Command           | Tutorial                                                                 |
|--------------------------------------------|-------------------|--------------------------------------------------------------------------|
| [Massively](https://html5up.net/massively) | html5up/massively |                                                                          |
| [Phantom](https://html5up.net/phantom)     | html5up/phantom   | [**HERE**](https://github.com/jamstackpy/jamstack/wiki/Phantom-template) |

The syntax is as follows:

```bash
jamstack t <template_command> <project_folder_name>
```

Use the `--existing` flag if you want the project to be created in an existing folder

```bash
jamstack t html5up/massively myproject --existing
```

By default, projects based in templates are created without the assets (stylesheets, images, etc...) to download them,
you must pass
the `--jamdo` option to the `static.py` file of the respective project.

## Build

To build the site run the file `static.py`.

```bash
python static.py
```

Your site will be generated in the **dist/** folder.

## Other project command-line options

| Argument  | Description                                                               |
|-----------|---------------------------------------------------------------------------|
| `--serve` | Optional. Start project livewatch (autoreload when files change).         |
| `--watch` | Optional. Specify files and folders to watch. Must be separated by comma. |
| `--port`  | Optional. Specify server port.                                            |

## Sites using jamstack

- [DeliciousPy Telegram Channel](https://deliciouspy.github.io/)
- [The Flask Community Work Group](https://flaskcwg.github.io/)
- [Abdur-Rahmaan Janhangeer](https://compileralchemy.github.io/)

# TODO

- [ ] Replace `python static.py --serve/--jamdo` by something like `jamstack --serve/--jamdo`
- [ ] Remove Flask as Main requirement and just use Jinja
