import io
from pathlib import Path


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip() for line in open(path).readlines()
            if is_requirement(line)
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, or editable.
    """
    # Remove whitespace at the start/end of the line
    line = line.strip()

    # Skip blank lines, comments, and editable installs
    return not (
        line == ''
        or line.startswith('-r')
        or line.startswith('#')
        or line.startswith('-e')
        or line.startswith('git+')
        or line.startswith('-c')
    )


def load_readme():
    """
    Provides README file content.
    """
    return Path('README.rst').read_text()


def load_about():
    """
    Provides __about__ file content.
    """
    about = {}
    with io.open(
        Path('cc2olx_plugin/__about__.py'),
        'rt',
        encoding='utf-8',
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about
