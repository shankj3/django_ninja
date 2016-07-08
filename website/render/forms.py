from django import forms


class TemplateForm(forms.Form):
    string_to_render = forms.CharField(label='Template to Render', max_length=10000)
    map_to_render_with = forms.CharField(label='Map to render Jinja with', max_length=10000)