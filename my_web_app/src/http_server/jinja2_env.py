from jinja2 import Environment, FileSystemLoader
import pathlib

env = Environment(loader=FileSystemLoader(pathlib.Path(__file__).parent / "templates"))


def render_template(template_name, context=None):
    template = env.get_template(template_name)
    return template.render(context or {})
