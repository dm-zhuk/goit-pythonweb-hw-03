from jinja2 import Template

name = "Bill"
age = 28

tm = Template("My name is {{ name }} and I am {{ age }}")
msg = tm.render(name=name, age=age)

print(msg)  # My name is Bill and I am 28
