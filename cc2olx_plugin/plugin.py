import os

import importlib_resources
from tutor import hooks

import cc2olx_plugin.commands.cli
from cc2olx_plugin.constants import CONVERTER_IMAGE_NAME

config = {
    'defaults': {
        'BRANCH': 'master',
    },
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f'CC2OLX_{key}', value) for key, value in config.get('defaults', {}).items()]
)

hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(str(importlib_resources.files('cc2olx_plugin') / 'templates'))

hooks.Filters.ENV_TEMPLATE_TARGETS.add_item(('cc2olx/build', 'plugins'))

hooks.Filters.IMAGES_BUILD.add_item(
    (
        CONVERTER_IMAGE_NAME,
        os.path.join('plugins', 'cc2olx', 'build', 'cc2olx'),
        CONVERTER_IMAGE_NAME,
        (),
    )
)
