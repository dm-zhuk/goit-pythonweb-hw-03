from jinja2 import Template

persons = [
    {'name': 'Andrej', 'age': 34},
    {'name': 'Mark', 'age': 17},
    {'name': 'Thomas', 'age': 44},
    {'name': 'Lucy', 'age': 14},
    {'name': 'Robert', 'age': 23},
    {'name': 'Dragomir', 'age': 54}
]

rows_tmp = Template("""{% for person in persons -%}
    {{ person.name }} {{ person.age }}
{% endfor %}""")

print(rows_tmp.render(persons=persons))
