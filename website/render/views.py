from . import brokendown_jinja as jinj
import json
import pncommon.jsonhelpers as jsonhelp
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
        }
    ]}


def index(request):
    return render(request, 'render/index.html', navigation_map)


def inheritance_templates(request):
    latest_question_list = None
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'render/index.html', context=context)


def render_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
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
                # form = TemplateForm({'map_to_render_with': pretty_dumped,
                #                      'string_to_render': form.cleaned_data['string_to_render']})
                raise
            else:
                generated = jinj.render_string_with_jinja(form.cleaned_data['string_to_render'], env, jinja_map)
                generated_safe = jsonhelp.check_then_dump_json([generated])[0]
                # print(generated_safe)
                form = TemplateForm({'rendered_output': generated_safe,
                                     'map_to_render_with': pretty_dumped,
                                     'string_to_render': form.cleaned_data['string_to_render']})
    else:
        form = TemplateForm()
    final_map = ChainMap({'render_type': ['XML', 'JSON', 'NEITHER']}, {'form': form}, navigation_map)
    return render(request, 'render/name.html', final_map)


def input_template(request):
    if request.method == 'POST':
        form = InputTemplate(request.POST, request.FILES)
        if form.is_valid():
            handle_file_upload(request.FILES['filename'], request.FILES['file'])
    else:
        form = InputTemplate()
    return render(request, 'render/input.html', {'form': form})


def handle_file_upload(filename, file_contents):
    file_decoded = file_contents.decode('utf-8')
    file_db = Templates(filename=filename, file=file_decoded)
    file_db.save()