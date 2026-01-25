"""JavaScript utilities."""
# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

import json
import textwrap
from pathlib import Path

import jinja2

from .config import Config

INDENT = " " * 4


def datatables_options_to_js(options: dict | str) -> str:
    """
    Convert a Python nested dictionary to a valid JS dictionary object as a str.

    If it's a string already, dedent and return. It will also append a comma at
    the end if not already present.
    """
    if isinstance(options, dict):
        obj = json.dumps(options, indent=INDENT)
    else:  # If it's not a dict, just return whatever it is (e.g., a string)
        obj = textwrap.dedent(options)
    # prepend an indent to each line
    obj = textwrap.indent(obj, indent).rstrip()
    if not obj.endswith(","):
        obj += ","
    return obj


def create_datatables_js(
    config: Config,
    *,
    emit_defaults: bool = True,
    emit_script_tag: bool = False,
) -> str:
    """Create the JS file to activate datatables."""
    custom_file = Path(__file__).parent.joinpath("activate_datatables.js.in")
    template = jinja2.Template(
        custom_file.read_text(encoding="utf-8"),
        undefined=jinja2.StrictUndefined,
    )
    rendered = template.render(
        datatables_options=datatables_options_to_js(config.datatables_options),
        datatables_class=config.datatables_class,
        emit_defaults=emit_defaults,
        emit_script_tag=emit_script_tag,
    )

    return rendered.replace(r"${datatables_version}", config.datatables_version)
