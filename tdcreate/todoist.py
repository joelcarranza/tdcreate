import requests
import uuid

class TodoistAPI():
    def __init__(self, api_token):
        self.api_token = api_token

    def get_projects(self, **data):
        headers = {'X-Request-Id': str(uuid.uuid1()), 'Authorization': 'Bearer ' + self.api_token}
        response = requests.get('https://api.todoist.com/rest/v2/projects', data=data, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            response.raise_for_status()


    def create_project(self, **data):
        headers = {'X-Request-Id': str(uuid.uuid1()), 'Authorization': 'Bearer ' + self.api_token}
        response = requests.post('https://api.todoist.com/rest/v2/projects', data=data, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            response.raise_for_status()

    def import_template(self, project_id, file):
        data = dict(project_id=project_id)
        files = dict(file=file)
        headers = {'X-Request-Id': str(uuid.uuid1()), 'Authorization': 'Bearer ' + self.api_token}
        response = requests.post('https://api.todoist.com/sync/v9/templates/import_into_project', data=data, files=files, headers=headers)
        response.raise_for_status()