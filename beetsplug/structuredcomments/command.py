#  Copyright: Copyright (c) 2020., Michael Toohig
#  Author: Michael Toohig <michael dot toohig at gmail>
#  License: See LICENSE.txt

from optparse import OptionParser

from beets.library import Library, Item, parse_query_string
from beets.ui import Subcommand, decargs
from beets.util.confit import Subview

from beetsplug.structuredcomments import common


class StructuredCommentsCommand(Subcommand):
    config: Subview = None
    lib: Library = None
    query = None
    parser: OptionParser = None

    cfg_force = False
    cfg_dry_run = False

    def __init__(self, cfg):
        self.config = cfg.flatten()
        
        self.cfg_force = self.config.get('force')
        self.cfg_dry_run = self.config.get('dry-run')
        self.cfg_format = self.config.get('format')
        self.cfg_comments_delimiter = self.config.get('delimiter')
        self.cfg_comments_position = self.config.get('comments_position')

        self.parser = OptionParser(
            usage='beet {plg} [options] [QUERY...]'.format(
                plg=common.plg_ns['__PLUGIN_NAME__']
            ))

        self.parser.add_option(
            '-f', '--force',
            action='store_true', dest='force', default=self.cfg_force,
            help=u'[default: {}] force re-writing of items with existing '
                 u'comments'.format(self.cfg_force)
        )

        self.parser.add_option(
            '-d', '--dry-run',
            action='store_true', dest='dryrun', default=self.cfg_dry_run,
            help=u'[default {}] display the structured comments but do not '
                 u'update the library items'.format(self.cfg_dry_run)
        )

        self.parser.add_option(
            '-v', '--version',
            action='store_true', dest='version', default=False,
            help=u'show plugin version'
        )

        # keep this at the end
        super(StructuredCommentsCommand, self).__init__(
            parser=self.parser,
            name=common.plg_ns['__PLUGIN_NAME__'],
            aliases=[common.plg_ns['__PLUGIN_ALIAS__']] if common.plg_ns['__PLUGIN_ALIAS__'] else [],
            help=common.plg_ns['__PLUGIN_SHORT_DESCRIPTION__']
        )

    def func(self, lib: Library, options, arguments):
        self.cfg_force = options.force
        self.cfg_dry_run = options.dryrun

        self.lib = lib
        self.query = decargs(arguments)

        if options.version:
            self.show_version_information()
            return

        self.handle_main_task()

    def handle_main_task(self):
        # Setup the query
        query = self.query
        if not self.cfg_force:
            query_element = 'comments:""'
            query.append(query_element)

        # Get the library items
        items = self.lib.items(self.query)
        if not items:
            self._say("Your query did not produce any results", log_only=False)
            return
        
        for item in items:
            if self.process_item(item):
                if not self.cfg_dry_run:
                    # item.try_write()  # write to file
                    # item.store()      # write to database
                    pass
                pass
            
    def process_item(self, item: Item):
        self._say('Building structured comments for item: {}'.format(item), log_only=False)
        
        if self.cfg_comments_position == 'end':
            comments = item.comments.split(self.cfg_comments_delimiter)[-1]
        elif self.cfg_comments_position == 'start':
            comments = item.comments.split(self.cfg_comments_delimiter, 1)[0]
        else:
            self._say('Invalid configuration for comments position: {}'.format(self.cfg_comments_position))
            return
        
        print(comments)


    def show_version_information(self):
        self._say("{pt}({pn}) plugin for Beets: v{ver}".format(
            pt=common.plg_ns['__PACKAGE_TITLE__'],
            pn=common.plg_ns['__PACKAGE_NAME__'],
            ver=common.plg_ns['__version__']
        ), log_only=False)

    @staticmethod
    def _say(msg, log_only=True, is_error=False):
        common.say(msg, log_only, is_error)
