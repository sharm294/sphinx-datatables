"""A directive for inline DataTables configuration."""
# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

import json
from typing import Any

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from .config import get_config
from .js import create_datatables_js


class datatables_selector_options(nodes.raw):  # noqa: N801
    """A vanity node we can ``traverse`` for during ``html-page-context``."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Create a new options node."""
        super().__init__(*args, **kwargs, format="html")


class JSONOptionsDirective(SphinxDirective):
    """Emit DataTables script tag for tables on the page."""

    has_content = True

    def run(self) -> list[nodes.Node]:
        """Generate a single options ``<script>``."""
        config = get_config(self.state.document.settings.env.config)
        config.datatables_options = {}
        config.datatables_class = ""
        config.datatables_selector_options = json.loads("\n".join(self.content))
        html = create_datatables_js(config, emit_defaults=False, emit_script_tag=True)
        return [datatables_selector_options("", html)]
