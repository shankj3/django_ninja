import time
import io
from collections import ChainMap
from jinja2 import Undefined, FileSystemLoader, environment
from jinja2.utils import missing, object_type_repr
from jinja2.exceptions import TemplateNotFound, TemplateSyntaxError
import os
import sqlite3


class PynetLoader(FileSystemLoader):
    """Loads template both from filesystem specified and from BytesIO.
        If the template isn't in the list of templates from FileSystemLoader
        and is not in BytesIO as pynet_test_builder will pass it, it will raise
        a TemplateNotFound exception"""
    def get_source(self, environment, template):
        # If template is of type BytesIO as set by PYNET test cases, decode it and return its value, with time
        # as current time, and a filename of None.
        if type(template) == io.BytesIO:
            template_str = template.getvalue().decode(self.encoding)
            contents = template_str
            mtime = time.time()
            filename = None  # could be a temp file name, None seemed apt enough. maybe the uid of test case?
            return contents, filename, mtime
        # If template is in the list of templates found by FileSystemLoader, render with its get_source
        elif template in super(PynetLoader, self).list_templates():
            return super(PynetLoader, self).get_source(environment, template)
        raise TemplateNotFound(template)


class Environment(environment.Environment):
    def _generate(self, source, name, filename, defer_init=False):
        # With a normal template with FileSystemLoader, the name is the name of the file. If it is BytesIO,
        # it's from the test case body, and will be named as such.
        # TODO: get the name from varmap.mapped.id somehow?
        if type(name) == io.BytesIO:
            name = 'Embedded Test Case Template'
        return super(Environment, self)._generate(source, name, filename, defer_init=defer_init)


class KeepUndefined(Undefined):
    # Jinja renders undefined variables to empty string by default. This overrides that behavior to have it
    # return the original {{ variable }} so it can be replaced by ninja, as with assigned variables through the
    # test run.
    def __str__(self):
        if self._undefined_hint is None:
            if self._undefined_obj is missing:
                return u'{{ %s }}' % self._undefined_name
            # here -- what to do here.. nested dictionary with a value that isn't originally in the varmap/testData.
            # TODO: be cleverer...
            return u'{{ %s[%r] }}' % (object_type_repr(self._undefined_obj), self._undefined_name)
        return u'{{ undefined value printed: %s }}' % self._undefined_hint


def render_string_with_jinja(string_value, jinja_env, jinja_map):
    bytes_template = io.BytesIO()
    bytes_template.write(string_value.encode('utf-8'))
    template = jinja_env.get_template(bytes_template)
    rendered_string = template.render(jinja_map)
    return rendered_string


def db_loader(template_name):

    pass


if __name__=='__main__':
    pass
