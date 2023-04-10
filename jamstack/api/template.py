import builtins
import copy
import datetime
import string
import uuid

from jinja2 import Environment, FileSystemLoader


def base_context():
    """
    Get a dictionary of built-in functions and variables.

    Returns
    -------
    dict
        Dictionary of built-in functions and variables.
    """
    defaults = [_ for _ in dir(builtins)
                if _[0] in string.ascii_lowercase and
                _ not in ['copyright', 'credits']
                ]
    attrs = [getattr(builtins, _) for _ in defaults]

    builtins_dict = dict(zip(defaults, attrs))
    return copy.deepcopy(builtins_dict)


def generate(file_in_templates, out_path, template_dir='templates', assets_path_append='', **kwargs):
    """
    Generates necessary file(s) from a Jinja2 template.

    Parameters
    ----------
    file_in_templates: str
        Template file to work with.
    out_path: str
        Output path to save the generated file to.
    template_dir: str, optional
        Templates directory. Default is 'templates'.
    assets_path_append: str, optional
        Path to append to assets. Default is ''.
    kwargs: dict
        Variables to pass to the template.

    Returns
    -------
    None
    """
    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)
    template = env.get_template(file_in_templates)

    build_id = str(uuid.uuid4())

    output = template.render(
        kwargs,
        year=datetime.datetime.now().year,
        build_id=build_id,
        assets_path_append=assets_path_append)

    with open(out_path, 'w+', encoding="utf8") as f:
        f.write(output)
