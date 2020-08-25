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

        self._command = ui.Subcommand(
            'structuredcomments', 
            help=u'structured comments for when you need beets data outside of beets'
        )

        self._command.parser.add_option(
            u'-d', u'--dry-run', dest='dry_run',
            action='store_true', default=None,
            help=u'Do not write or store any changes only print the result')

        if self.config['auto']:
            self.register_listener('write', self.process_item)
        
    def commands(self):

        def func(lib, opts, args):
            self.config.set_args(opts)

            for item in lib.items(ui.decargs(args)):
                self.process_item(item, dry_run)

        self._command.func = func
        return [self._command]

    def process_item(self, item, dry_run=False):
        """Write the new structured comments.
        """
        delimiter = self.config['delimiter'].get(str)
        dry_run = self.config['dry_run'].get(bool)
        write = ui.should_write()

        sc, comments = split_on_delimiter(item.comments, delimiter) 
        
        tmpl = self.config['template'].get()
        template = util.functemplate.Template(tmpl)
        new_sc = template.substitute(item, item._template_funcs())
        
        complete_comments = u'{} {} {}'.format(new_sc, delimiter, comments)
        if dry_run:
            self._log.info(u'{0} -> {1}'.format(util.displayable_path(item.path), complete_comments))
        else:
            item.update({'comments': complete_comments})
            if write:
                item.try_write()
            item.store()