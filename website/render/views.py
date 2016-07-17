from . import brokendown_jinja as jinj
import json
# import pncommon.jsonhelpers as jsonhelp
from django.shortcuts import render
from collections import ChainMap
from .forms import TemplateForm, InputTemplate
from .models import Templates
from jinja2 import FunctionLoader


# Create your views here.
navigation_map = {
    "navigation":[
        {
            "href": "/render/list_templates",
            "caption": "List Templates to extend/include in your template"
        },
        {
            "href": "/render/render_template",
            "caption": "Render your own template"
        },
        {
            "href": "/render/upload",
            "caption": "Upload files to use for extending"
        }
    ]}


def index(request):
    return render(request, 'render/index.html', navigation_map)


def inheritance_templates(request):
    context = {"templates": Templates.objects.all()}
    return render(request, 'render/list_templates.html', context=ChainMap(context, navigation_map))

def specific_templates(request, template_name):
    context = {"templates": Templates.objects.all()}
    data = vars(Templates.objects.get(template_name=template_name))
    print(data)
    return render(request, 'render/list_templates.html', context=ChainMap(data, context, navigation_map))

def render_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print('FORM IS VALID')
            env = jinj.Environment(loader=FunctionLoader(jinj.db_loader),
                                   undefined=jinj.KeepUndefined,
                                   block_start_string='{~',
                                   block_end_string='~}',
                                   comment_start_string='{!',
                                   comment_end_string='!}')
            try:
                jinja_map = json.loads(form.cleaned_data['map_to_render_with'])
                pretty_dumped = json.dumps(jinja_map, indent=4)
            except ValueError:
                # pretty_dumped = 'Invalid JSON! \n %s' \
                #                 % jsonhelp.return_line_no_of_json_value_exc(form.cleaned_data['map_to_render_with'])
                form = TemplateForm({'map_to_render_with': pretty_dumped,
                                     'string_to_render': form.cleaned_data['string_to_render']})
                raise
            else:
                # print('cleaned data',form.cleaned_data['string_to_render'])
                generated = jinj.render_string_with_jinja(form.cleaned_data['string_to_render'], env, jinja_map)
                # generated_safe = jsonhelp.check_then_dump_json([generated])[0]
                # print(generated_safe)
                form = TemplateForm({'rendered_output': generated,
                                     'map_to_render_with': pretty_dumped,
                                     'string_to_render': form.cleaned_data['string_to_render']})
        else:
            print(form.errors)
    else:
        form = TemplateForm()
    final_map = ChainMap({'render_type': ['XML', 'JSON', 'NEITHER']}, {'form': form}, navigation_map)
    return render(request, 'render/name.html', final_map)


def input_template(request):
    from pprint import pprint
    ## http://stackoverflow.com/questions/15323880/how-to-take-data-from-textboxes-in-django-without-using-the-automated-model-form
    if request.method == 'POST':
        pprint(vars(request))
        form = InputTemplate(request.POST, request.FILES)
        # print(request.FILES)
        if form.is_valid():
            handle_file_upload(form.cleaned_data['filename'], request.FILES['file'].read().decode())
            print(request.FILES['file'].read().decode())
    else:
        form = InputTemplate()
    return render(request, 'render/input.html', ChainMap({'form': form},navigation_map))


def handle_file_upload(filename, file_contents):
    print(type(file_contents))
    file_br = file_contents.replace('\n', '<br>')
    file_db = Templates(template_name=filename, template_body=file_contents.encode())
    file_db.save()