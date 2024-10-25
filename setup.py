from setuptools import setup

from utils import load_about, load_readme, load_requirements

ABOUT = load_about()

setup(
    name='cc2olx-tutor-plugin',
    version=ABOUT['__version__'],
    license='GNU Affero General Public License',
    description='cc2olx plugin for Tutor',
    long_description=load_readme(),
    long_description_content_type='text/x-rst',
    packages=[
        'cc2olx_plugin',
    ],
    include_package_data=True,
    install_requires=load_requirements('requirements/base.txt'),
    extras_require={'dev': ['tutor[dev]>=17.0.0']},
    entry_points={'tutor.plugin.v1': ['cc2olx = cc2olx_plugin.plugin']},
)
