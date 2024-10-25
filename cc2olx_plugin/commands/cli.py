from tutor import hooks

from cc2olx_plugin.commands.cc2olx import cc2olx

hooks.Filters.CLI_COMMANDS.add_item(cc2olx)
