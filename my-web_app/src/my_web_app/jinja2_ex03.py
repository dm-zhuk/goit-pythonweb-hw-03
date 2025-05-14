from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))

template = env.get_template("persons.html")


persons = [
    {'name': 'Andrej', 'age': 34},
    {'name': 'Mark', 'age': 17},
    {'name': 'Thomas', 'age': 44},
    {'name': 'Lucy', 'age': 14},
    {'name': 'Robert', 'age': 23},
    {'name': 'Dragomir', 'age': 54}
]

output = template.render(persons=persons, )

with open("new_persons.html", "w", encoding='utf-8') as fh:
    fh.write(output)