import os
import click
import io
from .todoist import TodoistAPI
from .template import parse_template, template_csv

def extract_project_name(template):
    # when file passed in, is io.TextWrapper with name attribute as path
    name, ext = os.path.splitext(os.path.basename(template.name))
    if name == '<stdin>':
        raise ValueError("project name must be specified")
    return name

def create_project_properties(t):
    project_name = t.properties.get('name', None)
    project_properties = dict(name=project_name)
    if t.properties.get('favorite') == 'true':
        project_properties['is_favorite'] = True
    if 'color' in t.properties:
        project_properties['color'] = t.properties['color']
    if 'view' in t.properties:
        project_properties['view_style'] = t.properties['view']
    if 'parentid' in t.properties:
        project_properties['parent_id'] = t.properties['parentid']
    return project_properties

@click.command()
@click.argument('template',type=click.File('r', encoding='utf-8'))
@click.option('--token',type=str, envvar='TODOIST_API_TOKEN')
@click.option('--name',type=str)
def main(template, token, name):
    api = TodoistAPI(token)

    tt = parse_template(template)

    # construct project properties
    project_properties = create_project_properties(tt)
    if name:
        project_properties['name'] = name        
    elif not project_properties.get('name'):
        project_properties['name'] = extract_project_name(template)
    # assign parent if needed
    if 'parent' in tt.properties:
        projects = api.get_projects()
        for p in projects: 
            if p.get('name') == tt.properties['parent']:
                project_properties['parent_id'] = p['id']

    csv_content = template_csv(tt)

    project = api.create_project(**project_properties)
    api.import_template(project_id=project['id'], file=io.StringIO(csv_content))
    click.echo(f"Created project {project['name']}")

if __name__ == '__main__':
    main()