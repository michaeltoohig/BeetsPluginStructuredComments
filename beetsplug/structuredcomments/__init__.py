#  Copyright: Copyright (c) 2020., Michael Toohig
#  Author: Michael Toohig <michael dot toohig at gmail>
#  License: See LICENSE.txt

import os

from beets.plugins import BeetsPlugin
from beets.util.confit import ConfigSource, load_yaml
from beets.util.functemplate import Template

from beetsplug.structuredcomments.command import StructuredCommentsCommand


class StructuredCommentsPlugin(BeetsPlugin):
    _default_plugin_config_file_name_ = 'config_default.yml'

    def __init__(self):
        super(StructuredCommentsPlugin, self).__init__()
        config_file_path = os.path.join(os.path.dirname(__file__), self._default_plugin_config_file_name_)
        source = ConfigSource(load_yaml(config_file_path) or {}, config_file_path)
        self.config.add(source)
        self.register_listener('write', self.write)
        self.register_listener('import_task_files', self._import_task_files)

    def _import_task_files(self, session, task):
        print('import task files')
        # Just testing which event occurs first and I notice `scrub` plugin uses this hook

    def write(self, item, path, tags):
        comments = item.comments
        import pdb; pdb.set_trace()
        tmpl = self.config['template'].get()
        template = Template(tmpl)
        new_comments = template.substitute(item, item._template_funcs())
        print('write')
        item.comments = new_comments + ' ::: ' + comments
        

    def commands(self):
        return [StructuredCommentsCommand(self.config)]
