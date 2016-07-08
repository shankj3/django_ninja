from . import brokendown_jinja as jinj
from django.shortcuts import render
from django.http import HttpResponse

from .forms import TemplateForm
from .models import Rendered


# Create your views here.


def index(request):
    return HttpResponse("hello, world. you're at the render index.")


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
            env = jinj.Environment(loader=jinj.PynetLoader('.'),
                                   undefined=jinj.KeepUndefined,
                                   block_start_string='{~',
                                   block_end_string='~}',
                                   comment_start_string='{!',
                                   comment_end_string='!}')

    return HttpResponse("Insert template here, and see it rendered fully.")

