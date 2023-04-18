import builtins
import copy
import datetime
import json
import string

from jinja2 import Environment, FileSystemLoader


def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)


def get_builtins_context() -> dict:
    """
    Get a dictionary of built-in functions and variables.

    Returns
    -------
    dict
        Dictionary of built-in functions and variables.
    """
    builtins_dict = {}
    for name in dir(builtins):
        if name[0] in string.ascii_lowercase and name not in ['copyright', 'credits']:
            value = getattr(builtins, name)
            builtins_dict[name] = value
    return copy.deepcopy(builtins_dict)


def generate(template_name: str, output_path: str, template_dir: str = 'templates', assets_path_append: str = '',
             context: dict = None) -> None:
    """
    Generates necessary file(s) from a Jinja2 template.

    Parameters
    ----------
    template_name: str
        Template file to work with.
    output_path: str
        Output path to save the generated file to.
    template_dir: str, optional
        Templates directory. Default is 'templates'.
    assets_path_append: str, optional
        Path to append to assets. Default is ''.
    context: dict, optional
        Variables to pass to the template. Additional context variables can be provided using this parameter.

    Returns
    -------
    None
    """
    if context is None:
        context = {}

    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)

    context.update({
        'year': datetime.datetime.now().year,
        'assets_path_append': assets_path_append,
        **get_builtins_context(),
    })

    output = template.render(context)

    with open(output_path, 'w+', encoding="utf8") as f:
        f.write(output)
