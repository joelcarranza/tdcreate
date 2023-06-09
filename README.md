# tdcreate

Author your templates for Todoist in a simple plain text format instead of their gross CSV format. 

Example template file:

```
# template.txt
name = My Packing List
favorite = true

# Template for when I need to pack on a trip

* "The Journey Not The Arrival Matters" 
    by T.S Elliot
- phone
- charger

Clothes:

- shirts 
    one for each day you are planning to be gone
- shoes
    left and right
- If you expect it to rain
    - rain jacket
    - galoshes

Toiletries:

- toothbrush
- toothpaste
- vitamins
```

You can then create a project from the command line using:

    tdcreate template.txt

OR by passing content via stdin

    curl "https://gist.githubusercontent.com/joelcarranza/3f2562eeb02528c38d17bb31c02dd665/raw/e60d9a9a66ae76b605ef74dd21dd6ff3bcba68e2/example.txt" | tdcreate - 

## Installation

Recommended usage is with [pipx](https://pypa.github.io/pipx/)

    pipx install git+https://github.com/joelcarranza/tdcreate

## Usage

To use this tool, you must define the environment variable `TODOIST_API_TOKEN` with your Todoist API token. 

## Template Text Format

At the start of a template file, project properties can be defined using the syntax

    name = value

Current properties:

- `name` name of project to create. If not specified, will use the name of file 
- `favorite` if "true" then the created project will be set as a favorite
- `color` See [color names](https://developer.todoist.com/guides/#colors)
- `view` either board or list (the default)
- `parentid` an id of a todoist project to create the new project under
- `parent` a name of a todoist project to create the new project under

**Tasks** are defined with a prefix of either `-` or `*`. If a task is idented it becomes a subtask of previously defined task. Non-task text indented following a task is interpreted as a description. Tasks that start with `*` are created as uncompletable

```
- example task
    - subtask 1
    - subtask 2
        description for subtask 2 
    - subtask 3
* uncompletable task
```

**Sections** are defined by a single line with a trailing `:`. Leading space is not permitted

```
Example Section:

- task in section 1
- task in section 2
```

Any line that starts with `#` is interpreated as a **comment** 


