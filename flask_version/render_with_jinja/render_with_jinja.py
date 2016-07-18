import os
import sqlite3
from flask import Flask, request, session, g, redirect, render_template, flash
from werkzeug import secure_filename

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'render.db'), 
    SECRET_KEY='dev key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list-templates', methods=['GET'])
def show_entries():
    db = get_db()
    cur = db.execute('select filename, contents from templates order by id desc')
    entries = cur.fetchall()
    render_dict = {"templates": entries}
    return render_template('list_templates.html', entries=render_dict)


@app.route('/list-templates/<template_name>')
def show_template(template_name):
    db = get_db()
    cur = db.execute('select filename, contents from templates order by id desc')
    entries = cur.fetchall()
    cur = db.execute("select filename, contents from templates where filename = '{0}'".format(template_name))
    file_contents = cur.fetchone()['contents']
    render_dict = {"templates": entries, "template_contents": file_contents}
    
    return render_template('list_templates.html', entries=render_dict)


@app.route('/upload', methods=['GET', 'POST'])
def add_entry():
    error = None
    print(request.files)
    if request.method == 'GET':
        return render_template('input.html')
    elif request.method == 'POST':
        file = request.files['file']
        if file and secure_filename(file.filename):
            filename = secure_filename(file.filename)
            db = get_db()
            db.execute('insert into templates (filename, contents) values (?, ?)',
                       [secure_filename(filename), file.stream.read().decode()])
            db.commit()
            flash('New template {0} was successfully added'.format(filename))
        else:
            flash('Not loaded')
        return render_template('input.html')


# @app.route('/render', methods=['GET', 'POST'])
# def render_template(request):
#     if request.method == 'POST':
#         form = TemplateForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             print('FORM IS VALID')
#             print(request.POST.get('choices'))
#             env = jinj.Environment(loader=FunctionLoader(jinj.db_loader),
#                                    undefined=jinj.KeepUndefined,
#                                    block_start_string='{~',
#                                    block_end_string='~}',
#                                    comment_start_string='{!',
#                                    comment_end_string='!}')
#             try:
#                 if form.cleaned_data['map_to_render_with']:
#                     jinja_map = json.loads(form.cleaned_data['map_to_render_with'])
#                     pretty_dumped = json.dumps(jinja_map, indent=4)
#                 else:
#                     jinja_map = {}
#                     pretty_dumped = ''
#             except (ValueError, json.decoder.JSONDecodeError):
#                 # pretty_dumped = 'Invalid JSON! \n %s' \
#                 #                 % jsonhelp.return_line_no_of_json_value_exc(form.cleaned_data['map_to_render_with'])
#                 form = TemplateForm({'map_to_render_with': form.cleaned_data['map_to_render_with'],
#                                      'string_to_render': form.cleaned_data['string_to_render']})
#                 raise
#             else:
#                 # print('cleaned data',form.cleaned_data['string_to_render'])
#                 generated = jinj.render_string_with_jinja(form.cleaned_data['string_to_render'], env, jinja_map)
#                 # generated_safe = jsonhelp.check_then_dump_json([generated])[0]
#                 # print(generated_safe)
#                 form = TemplateForm({'rendered_output': generated,
#                                      'map_to_render_with': pretty_dumped,
#                                      'string_to_render': form.cleaned_data['string_to_render']})
#         else:
#             print(form.errors)
#     else:
#         form = TemplateForm()
#     final_map = ChainMap({'render_type': ['XML', 'JSON', 'NEITHER']}, {'form': form}, navigation_map)
#     return render(request, 'render/name.html', final_map)




# def render_string_with_jinja(string_value, jinja_env, jinja_map):
#     # print(string_value)
#     if isinstance(string_value, str):
#         bytes_template = io.BytesIO()
#         bytes_template.write(string_value.encode('utf-8'))
#     # print(bytes_template.read())
#         bytes_template.seek(0)
#     else:
#         print(type(string_value))
#         bytes_template = string_value
#     template = jinja_env.get_template(bytes_template)
#     rendered_string = template.render(jinja_map)
#     return rendered_string

##http://flask.pocoo.org/docs/0.11/patterns/wtforms/
## http://flask.pocoo.org/docs/0.11/tutorial/templates/#tutorial-templates