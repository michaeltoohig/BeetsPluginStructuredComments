#  Copyright: Copyright (c) 2020., Michael Toohig
#  Author: Michael Toohig <michael dot toohig at gmail>
#  License: See LICENSE.txt

import os
import ast

from beets.plugins import BeetsPlugin
from beets.util.confit import ConfigSource, load_yaml
from beets.util import functemplate

from beetsplug.structuredcomments.command import StructuredCommentsCommand


class MyTemplate(functemplate.Template):
    def __init__(self, template):
        super(MyTemplate, self).__init__(template)
        self.compiled = self.translate()
        
    def translate(self):
        """Compile the template to a Python function."""
        expressions, varnames, funcnames = self.expr.translate()

        argnames = []
        for varname in varnames:
            argnames.append(functemplate.VARIABLE_PREFIX + varname)
        for funcname in funcnames:
            argnames.append(functemplate.FUNCTION_PREFIX + funcname)
            
        #import pdb; pdb.set_trace()
        
        func = functemplate.compile_func(
            argnames,
            [ast.Return(ast.List(expressions, ast.Load()))],
        )

        def wrapper_func(values={}, functions={}):
            args = {}
            for varname in varnames:
                args[functemplate.VARIABLE_PREFIX + varname] = values[varname]
            for funcname in funcnames:
                args[functemplate.FUNCTION_PREFIX + funcname] = functions[funcname]
            parts = func(**args)
            return u''.join(parts)

        return wrapper_func


class StructuredCommentsPlugin(BeetsPlugin):
    _default_plugin_config_file_name_ = 'config_default.yml'

    def __init__(self):
        super(StructuredCommentsPlugin, self).__init__()
        config_file_path = os.path.join(os.path.dirname(__file__), self._default_plugin_config_file_name_)
        source = ConfigSource(load_yaml(config_file_path) or {}, config_file_path)
        self.config.add(source)
        self.register_listener('write', self.write)

    def write(self, item, path, tags):
        # NOTE nearly same as the `process_item` method; could both be extracted to `common.py`?
        comments = item.comments
        delimiter = self.config['delimiter'].get()
        orig_comments = comments.split(delimiter)[-1].strip()
        tmpl = self.config['template'].get()
        template = functemplate.Template(tmpl)  # template = MyTemplate(tmpl)  # dev/exploring
        new_comments = template.substitute(item, item._template_funcs())
        item.comments = '{} {} {}'.format(new_comments, delimiter, orig_comments)
        #import pdb; pdb.set_trace()
        
    def commands(self):
        return [StructuredCommentsCommand(self.config)]
