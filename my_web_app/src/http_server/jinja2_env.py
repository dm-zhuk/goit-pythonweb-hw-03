from jinja2 import Environment, FileSystemLoader
import pathlib


def create_jinja_env():
    return Environment(
        loader=FileSystemLoader(str(pathlib.Path("src/http_server/templates")))
    )


def render_template(template_name, context=None):
    env = create_jinja_env()
    template = env.get_template(template_name)
    return template.render(context or {})
