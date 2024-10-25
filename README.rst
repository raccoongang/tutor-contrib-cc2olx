Common Cartridge to OLX plugin for `Tutor <https://docs.tutor.edly.io>`__
=========================================================================

Overview
########

The Tutor plugin simplifies the `cc2olx <https://github.com/openedx/cc2olx>`__
converter usage. It allows eliminate the converter script and related Python
version installation, makes the solution platform-independent.

Installation
############

Common Cartridge to OLX plugin was specially developed to be used with
`Tutor <https://docs.tutor.edly.io>`__. So, you need to have the Tutor
installed before the plugin usage.

Also, it uses the Docker under the hood, so you need to have the Docker
installed on your machine.

When the prerequisites described above are met, clone the repository and
install the plugin in the same environment with Tutor as follows::

    pip install -e /path/to/tutor-contrib-cc2olx

Then, to enable this plugin, run::

    tutor plugins enable cc2olx

Then, build the cc2olx converter image::

    tutor images build cc2olx

**Note**: After changing the converter branch configuration you need to
re-enable the plugin and rebuild the image to apply the changes.

Configuration
#############

- ``CC2OLX_BRANCH`` (default: "master")

Usage
#####

To use the converter, you need to run the CLI command as follows::

    tutor cc2olx [ARGS...]

where `[ARGS...]` are the `cc2olx <https://github.com/openedx/cc2olx>`__ converter
arguments.

For, example::

    tutor cc2olx -r zip -i /home/admin/cc_courses/english_b1.imscc -o olx_courses/english_b1

will take the course in Common Cartridge format from the host absolute path
*/home/admin/cc_courses/english_b1.imscc* and produce the OLX zip archive with
*english_b1* name in the relative *olx_courses* directory.
