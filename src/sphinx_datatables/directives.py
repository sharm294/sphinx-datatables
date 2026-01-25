# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""A directive for inline DataTables configuration."""

import abc
import contextlib
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst.directives import uri
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective

from .config import SphinxDatatablesConfig
from .js import create_datatables_js

HAS_TOML = False

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib

    HAS_TOML = True
else:  # pragma: no cover
    with contextlib.suppress(ImportError):
        import tomli as tomllib

        HAS_TOML = True


class datatables_options(nodes.raw):  # noqa: N801
    """A vanity node we can ``traverse`` for during ``html-page-context``."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Create a new options node."""
        super().__init__(*args, **kwargs, format="html")


class OptionsBase(SphinxDirective):
    """Emit ``DataTables`` script tag for tables on the page."""

    has_content = True
    required_arguments = 1

    option_spec: ClassVar[dict[str, Callable[[Any], Any]]] = {
        "path": uri,
    }

    def run(self) -> list[nodes.Node]:
        """Generate a single options ``<script>``."""
        config = SphinxDatatablesConfig.from_sphinx_config(
            self.state.document.settings.env.config
        )
        content = self.get_path_or_content()
        config.datatables_options = self.parse_datatables_options(content)
        config.datatables_class = self.arguments[0]
        html = create_datatables_js(config, emit_defaults=False, emit_script_tag=True)
        return [datatables_options("", html)]

    @abc.abstractmethod  # pragma: no cover
    def parse_datatables_options(self, content: str) -> dict[str, Any] | str:
        """Parse the datatables options from the directive."""

    def get_path_or_content(self) -> str:
        """Load the content from a given path or the directive content."""
        path_option = self.options.get("path")
        current_source = self.state.document.current_source

        if path_option and current_source:
            here = Path(current_source).parent
            path = (here / f"{path_option}").resolve()
            content = path.read_text(encoding="utf-8")
            self.state.document.settings.env.note_dependency(f"{path}")
        else:
            content = "\n".join(self.content)

        return content


class OptionsJSON(OptionsBase):
    """Build a ``DataTables`` script tag from JSON for tables on the page."""

    def parse_datatables_options(self, content: str) -> dict[str, Any]:
        """Load options from the directive content JSON."""
        return json.loads(content) if content else {}


class OptionsJS(OptionsBase):
    """Build a ``DataTables`` script tag from JavaScript for tables on the page."""

    def parse_datatables_options(self, content: str) -> str:
        """Load options from the directive content JSON."""
        return content


class OptionsTOML(OptionsBase):
    """Build a ``DataTables`` script tag from TOML for tables on the page."""

    def parse_datatables_options(self, content: str) -> dict[str, Any]:
        """Load options from the directive content TOML."""
        if not HAS_TOML:  # pragma: no cover
            msg = "``datatables-toml`` requires python 3.11+ or `tomli`"
            raise ExtensionError(msg)
        return tomllib.loads(content) if content else {}


def add_directives(app: Sphinx) -> None:
    """Add all directives to the application."""
    app.add_directive("datatables-json", OptionsJSON)
    app.add_directive("datatables-toml", OptionsTOML)
    app.add_directive("datatables-js", OptionsJS)
