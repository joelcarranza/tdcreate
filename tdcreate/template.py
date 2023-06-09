import os
import io
import csv
from dataclasses import dataclass, field
import re

@dataclass
class TemplateItem:
    type: str
    content: str = ''
    description: str = None
    children: list = field(default_factory=list)
    properties: dict = None

def split_indent(line):
    "strip whitespace from line and return tuple of (indent level, content)"
    indent = 0
    while line:
        if line[0] == ' ':
            indent += 1
            line = line[1:]
        elif line[0] == '\t':
            indent += 4
            line = line[1:]
        else:
            break
    return indent, line.rstrip()

def parse_template(f):
    item_stack = list()
    item_stack.append((TemplateItem(type='template', properties=dict()), -1))
    line_no = 0

    def add_task(item, child):
        if item.type not in ('template', 'task'):
            raise ValueError('Cannot add sub-task to '+item.type+' at line '+str(line_no))
        item.children.append(child)

    def add_section(item, child):
        if item.type != 'template':
            raise ValueError('Cannot add section to '+item.type+' at line '+str(line_no))
        item.children.append(child)

    def set_property(item, key, value):
        if item.type != 'template':
            raise ValueError('Cannot set property on '+item.type+' at line '+str(line_no))
        item.properties[key] = value

    def add_description_line(item, line):
        if item.type != 'task':
            raise ValueError('Cannot add description to '+item.type+' at line '+str(line_no))
        if item.description is None:
            item.description = line
        else:
            item.description = item.description + '\n' + line

    for line in f:
        line_no += 1
        indent_level, content = split_indent(line)

        while True:
            last_item, last_item_indent = item_stack[-1]
            if indent_level <= last_item_indent:
                item_stack.pop()
            else:
                break

        if indent_level == 0 and content.startswith('#'):
            pass
        elif content.startswith('-'):
            task = TemplateItem('task', content[1:].strip())
            add_task(last_item, task)
            item_stack.append((task, indent_level))            
        elif content.startswith('*'): # special extension for uncompletable items
            task = TemplateItem('task', "* " + content[1:].strip())
            add_task(last_item, task)
            item_stack.append((task, indent_level))
        elif indent_level == 0 and content.endswith(':'):
            section = TemplateItem('section', content[0:-1].strip())
            add_section(last_item, section)
        elif indent_level == 0 and re.match(r'^\w+\s*=',line):
            key,value = content.split('=', 1)
            set_property(last_item, key.strip(), value.strip())
        elif indent_level > 0:
            add_description_line(last_item, content)
        elif content:
            raise ValueError(content+ " line "+str(line_no))
    return item_stack[0][0]

CSV_FIELDNAMES = ['TYPE', 'CONTENT', 'DESCRIPTION','PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE']

def to_csv(rows, ti, indent=0):
    if ti.type == 'template':
        pass
    else:
        row = dict(TYPE=ti.type, CONTENT=ti.content, PRIORITY='4')
        if ti.description:
            row['DESCRIPTION'] = ti.description
        row['INDENT'] = str(indent)
        rows.append(row)
    for child in ti.children:
        to_csv(rows, child, indent + 1) 

def template_csv(t):
    rows = []
    to_csv(rows, t)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDNAMES)
    writer.writeheader()
    for x in rows:
        writer.writerow({f: x.get(f, '') for f in CSV_FIELDNAMES})
    return buffer.getvalue()