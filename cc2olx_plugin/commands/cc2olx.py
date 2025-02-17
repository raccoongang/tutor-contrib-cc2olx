import os
import subprocess
from contextlib import closing
from pathlib import Path
from typing import Generator, List, Tuple
from uuid import uuid4

import click

from cc2olx_plugin.constants import CONVERTER_IMAGE_NAME, DEFAULT_OUTPUT_ARG_VALUE
from cc2olx_plugin.enums import AsciiEscapeCode
from cc2olx_plugin.utils.cli import is_command_line_argument_name
from cc2olx_plugin.utils.docker import (
    build_container_data_directory_path_mapped_to_host_path,
    build_host_path_to_container_data_path_bind_mount,
)
from cc2olx_plugin.utils.filesystem import create_directory_if_not_exists

OUTPUT_ARGS = ('-o', '--output')
LOGS_DIR_ARGS = ('--logs_dir',)
PATH_ARGS = (*OUTPUT_ARGS, *LOGS_DIR_ARGS, '-i', '--inputs', '-f', '--link_file', '-p', '--passport-file')


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.pass_context
def cc2olx(context: click.Context) -> None:
    """
    Run Common Cartridge to OLX converter.
    """
    args = context.args

    if not (set(args).intersection(OUTPUT_ARGS)):
        args.extend(['-o', DEFAULT_OUTPUT_ARG_VALUE])
    _create_path_argument_ancestors_if_not_exist(OUTPUT_ARGS, args)

    if set(args).intersection(LOGS_DIR_ARGS):
        _create_path_argument_ancestors_if_not_exist(LOGS_DIR_ARGS, args)

    command = _build_cc2olx_run_command(args)

    _run_cc2olx_converter(command)


def _create_path_argument_ancestors_if_not_exist(path_argument_names: Tuple[str, ...], args: List[str]) -> None:
    """
    Create the path argument ancestors if they do not exist.

    Allows to avoid the situation when the ancestors corresponding to the path
    argument value don't exist and Docker creates them on behalf of the root,
    so the current host user has no access to them. Such function should be run
    before the Docker command to create the path ancestors on behalf of the
    current host user if they don't exist.
    """
    for argument_name in path_argument_names:
        for argument_index in _generate_argument_indexes(argument_name, args):
            argument_value_index = argument_index + 1

            if argument_value_index < len(args):
                directory_path = args[argument_value_index]

                if not is_command_line_argument_name(directory_path):
                    create_directory_if_not_exists(Path(directory_path).parent)


def _build_cc2olx_run_command(args: List[str]) -> List[str]:
    """
    Provide the CLI command to run Common Cartridge to OLX converter.

    Run the Docker container with pre-installed converter under the hood.
    """
    bind_mounts = []

    for argument in PATH_ARGS:
        _process_path_argument(argument, args, bind_mounts)

    user_id = os.getuid()

    return ['docker', 'run', '--user', str(user_id), '--rm', *bind_mounts, CONVERTER_IMAGE_NAME, *args]


def _run_cc2olx_converter(command: List[str]) -> None:
    """
    Runs the converter CLI command and capture the output.
    """
    command_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    click.echo(f'{AsciiEscapeCode.CYAN}The converter output:{AsciiEscapeCode.END}')
    try:
        with closing(command_process.stdout):
            for line in command_process.stdout:
                click.echo(line, nl=False)
    except KeyboardInterrupt:
        command_process.terminate()
    finally:
        command_process.wait()


def _process_path_argument(argument: str, argument_list: List[str], bind_mount_args: List[str]) -> None:
    """
    Process the CLI filesystem path-related argument.
    """
    for argument_index in _generate_argument_indexes(argument, argument_list):
        _process_argument_value(argument_index + 1, argument_list, bind_mount_args)


def _generate_argument_indexes(argument: str, argument_list: List[str]) -> Generator[int, None, None]:
    """
    Generate tne indexes of an argument occurrences.
    """
    search_start_index = 0

    while True:
        try:
            argument_index = argument_list.index(argument, search_start_index)
        except ValueError:
            break

        yield argument_index

        search_start_index = argument_index + 1


def _process_argument_value(argument_value_index: int, argument_list: List[str], bind_mount_args: List[str]) -> bool:
    """
    Process the CLI argument if it is possible and return such possibility status.
    """
    if argument_value_index < len(argument_list):
        path_argument = argument_list[argument_value_index]

        if is_command_line_argument_name(path_argument):
            return False

        _process_path_argument_value(path_argument, argument_value_index, argument_list, bind_mount_args)

        return True
    return False


def _process_path_argument_value(
    path_argument: str,
    path_argument_index: int,
    argument_list: List[str],
    bind_mount_args: List[str],
) -> None:
    """
    Process a CLI argument value that is a filesystem path.

    Replace the argument in arguments list by the mapped path inside the
    converter container. Populate binding mounts by filesystem path to the
    mapped path inside the converter container binding mount.
    """
    absolute_path_argument = Path(path_argument).resolve()
    argument_mapped_directory = str(uuid4())

    argument_list[path_argument_index] = build_container_data_directory_path_mapped_to_host_path(
        absolute_path_argument,
        argument_mapped_directory,
    )

    bind_mount_args.extend([
        '-v',
        build_host_path_to_container_data_path_bind_mount(absolute_path_argument, argument_mapped_directory),
    ])
