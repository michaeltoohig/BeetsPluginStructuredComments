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
            u'delimiter': ':::',
        })

        if self.config['auto']:
            self.import_stages = [self.imported]
            self.register_listener('write', self.write_structured_comment)
        
    def commands(self):
        cmd = ui.Subcommand('structuredcomments',
                            help=u'for when you need beets data outside of beets')

        cmd.parser.add_option(
            u'-d', u'--dry-run', dest="dry_run",
            action="store_true", default=False,
            help=u'Print changes without writing to files'
        )
        cmd.parser.add_option(
            u'-f', u'--force', dest="force",
            action="store_true", default=False,
            help=u'Rewrite tags to file even if they are the same'
        )
        # XXX not sure how to ensure we come back to the next 100 if we do batch of 100, maybe a skip arg
        # cmd.parser.add_option(
        #     u'-b', u'--batch', dest="batch",
        #     action="store", default=None,
        #     help=u'Write comments in batches instead of all at once'
        # )
        cmd.func = self.command
        return [cmd]

    def command(self, lib, opts, args):
        write = ui.should_write()
        items = lib.items(ui.decargs(args))
        total_items = len(items)
        for num, item in enumerate(items):
            self._log.info(u'{0}/{1} {2}', num+1, total_items, util.displayable_path(item.path))
            new_comments = self.build_structured_comment(item)
            self._log.info(u'{0}', new_comments)
            if not opts.dry_run:
                if new_comments != item.comments or opts.force:
                    self.write_structured_comment(item, new_comments, write)

    def build_structured_comment(self, item):
        delimiter = self.config['delimiter'].get(str)
        sc, comments = split_on_delimiter(item.comments, delimiter) 
        tmpl = self.config['template'].get()
        template = util.functemplate.Template(tmpl)
        new_sc = template.substitute(item, item._template_funcs())
        return u'{} {} {}'.format(new_sc, delimiter, comments)
        
    def imported(self, session, task):
        for item in task.imported_items():
            new_comments = self.build_structured_comment(item)
            self.write_structured_comment(item, new_comments)

    def write_structured_comment(self, item, new_comments=None, write=False):
        if not new_comments:
            new_comments = self.build_structured_comment(item)
        item.update({'comments': new_comments})
        if write:
            item.try_write()
        item.store()
