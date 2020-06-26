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
        delimiter = self.config['delimiter'].get()
        position = self.config['comments_position'].get()

        if position == 'end':
            orig_comments = comments.split(delimiter)[-1].strip()
        elif position == 'start':
            orig_comments = comments.rsplit(delimiter)[0].strip()
        else:
            print('not a valid position for comments')  # TODO fetch original comments from the template position and not tacked on like this
            return

        tmpl = self.config['template'].get()
        template = Template(tmpl)
        import pdb; pdb.set_trace()
        new_comments = template.substitute(item, item._template_funcs())
        print('write')

        if position == 'end':
            item.comments = '{} {} {}'.format(new_comments, delimiter, orig_comments)
        elif position == 'start':
            item.comments = '{} {} {}'.format(orig_comments, delimiter, new_comments)
        

    def commands(self):
        return [StructuredCommentsCommand(self.config)]
