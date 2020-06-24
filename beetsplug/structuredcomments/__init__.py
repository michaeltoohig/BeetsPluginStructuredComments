#  Copyright: Copyright (c) 2020., Michael Toohig
#  Author: Michael Toohig <michael dot toohig at gmail>
#  License: See LICENSE.txt

import os

from beets.plugins import BeetsPlugin
from beets.util.confit import ConfigSource, load_yaml
from beets.util.functemplate import Template

from beetsplug.structuredcomments.command import StructuredCommentsCommand


class MyTemplate(Template):
    def __init__(self, template, defaults):
        super(MyTemplate, self).__init__(template)
        self.defaults = defaults

    def translate(self):
        expressions, varnames, funcnames = self.expr.translate()

        argnames = []
        for varname in varnames:
            pass


class StructuredCommentsPlugin(BeetsPlugin):
    _default_plugin_config_file_name_ = 'config_default.yml'

    def __init__(self):
        super(StructuredCommentsPlugin, self).__init__()
        config_file_path = os.path.join(os.path.dirname(__file__), self._default_plugin_config_file_name_)
        source = ConfigSource(load_yaml(config_file_path) or {}, config_file_path)
        self.config.add(source)
        self.register_listener('write', self.write)

    def write(self, item):
        tmpl = self.config['template'].get()
        template = Template(tmpl)
        template.substitute(item)
        #import pdb; pdb.set_trace()
        print('write')

    def commands(self):
        return [StructuredCommentsCommand(self.config)]
