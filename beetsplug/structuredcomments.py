from beets import ui
from beets import util
from beets.plugins import BeetsPlugin


def split_on_delimiter(comments, delimiter):
    """Given the comments string, split the "original" comments from 
    any existing structured comments on the delimiter. Return the 
    original comments and the existing structured comments parts.
    """
    # split on the delimiter
    parts = [s.strip() for s in comments.split(delimiter, 1)]
    if len(parts) == 1:
        return None, parts[0]
    else:
        return tuple(parts)


class StructuredCommentsCommand(BeetsPlugin):
    def __init__(self):
        super(StructuredCommentsCommand, self).__init__()
        self.config.add({
            u'auto': False,
            u'dry_run': False,
            u'delimiter': ':::',
        })

        if self.config['auto']:
            self.import_stages = [self.imported]
            self.register_listener('write', self.write_structured_comment)
        
    def commands(self):
        cmd = ui.Subcommand('structuredcomments',
                            help=u'for when you need beets data outside of beets')

        cmd.func = self.command
        return [cmd]

    def command(self, lib, opts, args):
        items = lib.items(ui.decargs(args))
        dry_run = self.config['dry_run'].get(bool)
        write = ui.should_write()
        for item in items:
            if dry_run:
                self._log.info(self.build_structured_comment(itm))
            else:
                self.write_structured_comment(item, write)
        
    def imported(self, session, task):
        for item in task.imported_items():
            self.write_structured_comment(item)

    def build_structured_comment(self, item):
        delimiter = self.config['delimiter'].get(str)
        sc, comments = split_on_delimiter(item.comments, delimiter) 
        tmpl = self.config['template'].get()
        template = util.functemplate.Template(tmpl)
        new_sc = template.substitute(item, item._template_funcs())
        return u'{} {} {}'.format(new_sc, delimiter, comments)

    def write_structured_comment(self, item, write=False):
        complete_comments = self.build_structured_comment(item)
        item.update({'comments': complete_comments})
        if write:
            item.try_write()
        item.store()
