from tdcreate.template import split_indent, parse_template, to_csv
import io

def test_split_indent():
    assert (0, 'Hello World!') == split_indent('Hello World!')
    assert (2, 'Hello World!') == split_indent('  Hello World!')
    assert (4, 'Hello World!') == split_indent('\tHello World!')

def test_parse_empty():
    template = io.StringIO('')
    template = parse_template(template)
    assert template.type == 'template'
    assert not template.properties
    assert not template.children

def test_parse_commend():
    template = io.StringIO('# foo')
    template = parse_template(template)
    assert template.type == 'template'
    assert not template.properties
    assert not template.children


def test_parse_template():
    template = io.StringIO('name = Project')
    template = parse_template(template)
    assert template.type == 'template'
    assert template.properties['name'] == 'Project'

def test_parse_task():
    template = io.StringIO('- an example task')
    result = parse_template(template).children
    assert len(result) == 1
    task = result[0]
    assert task.type == 'task'
    assert task.content == 'an example task'

def test_parse_task_with_description():
    template = io.StringIO('''
- an example task
    Here is a description''')
    result = parse_template(template).children
    assert len(result) == 1
    task = result[0]
    assert task.type == 'task'
    assert task.content == 'an example task'
    assert task.description == '''Here is a description'''


def test_parse_task_uncompletable():
    template = io.StringIO('* an example task which is uncompletable')
    result = parse_template(template).children
    assert len(result) == 1
    task = result[0]
    assert task.type == 'task'
    assert task.content == '* an example task which is uncompletable'

def test_parse_section():
    template = io.StringIO('Example Section:')
    result = parse_template(template).children
    assert len(result) == 1
    task = result[0]
    assert task.type == 'section'
    assert task.content == 'Example Section'

def test_parse_subtasks():
    template = io.StringIO('''
- three subtasks:
    - a
    - b
    - c
''')
    result = parse_template(template).children
    assert len(result) == 1
    task = result[0]
    assert task.type == 'task'
    assert task.content == 'three subtasks:'
    children = task.children
    assert len(children) == 3

def test_to_csv():
    template = io.StringIO('''
Section:
- an example task
    Here is a description 
    with text
- three items:
    - a
    - b 
    - c
''')
    result = parse_template(template)
    rows = []
    to_csv(rows, result)
    assert len(rows) == 6

