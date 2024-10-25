from pathlib import Path

from cc2olx_plugin.constants import CC2OLX_CONTAINER_DATA_ROOT_DIRECTORY_PATH


def build_container_data_directory_path_mapped_to_host_path(
    host_absolute_path: Path,
    mapped_data_directory_name: str,
) -> str:
    """
    Provide the container data directory path mapped to the host absolute path.

    For example, there is a host machine absolute path
    /home/admin/cc_courses/english_b1.imscc. The function will return the path
    inside a container like
    /data/d52e4439-f09d-4288-bc67-dd1e6590c6a5/english_b1.imscc to which the
    host machine path is mapped.
    """
    return str(CC2OLX_CONTAINER_DATA_ROOT_DIRECTORY_PATH / mapped_data_directory_name / host_absolute_path.name)


def build_host_path_to_container_data_path_bind_mount(host_absolute_path: Path, mapped_data_directory_name: str) -> str:
    """
    Build host path to the container mapped data directory path bind mount.
    """
    container_mapped_data_directory_path = CC2OLX_CONTAINER_DATA_ROOT_DIRECTORY_PATH / mapped_data_directory_name
    return f'{host_absolute_path.parent.resolve()}:{container_mapped_data_directory_path}'
