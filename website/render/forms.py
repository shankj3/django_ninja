from django import forms


class TemplateForm(forms.Form):
    string_to_render = forms.CharField(label='Template to Render', max_length=10000, widget=forms.Textarea)
    map_to_render_with = forms.CharField(label='Map to render Jinja with', max_length=10000, widget=forms.Textarea)
    rendered_output = forms.CharField(label='Rendered Form', max_length=10000, required=False, widget=forms.Textarea)
    render_type = forms.ChoiceField(label='content type', choices=['XML', 'JSON', 'Neither'])

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['string_to_render'].widget.attrs['cols'] = 100
        self.fields['string_to_render'].widget.attrs['rows'] = 20
        self.fields['map_to_render_with'].widget.attrs['cols'] = 100
        self.fields['map_to_render_with'].widget.attrs['rows'] = 20
        self.fields['rendered_output'].widget.attrs['cols'] = 100
        self.fields['rendered_output'].widget.attrs['rows'] = 20