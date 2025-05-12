# Copyright 2017-2020 Palantir Technologies, Inc.
# Copyright 2021- Python Language Server Contributors.

import logging

from pylsp import _utils, hookimpl


log = logging.getLogger(__name__)


def lsp_location(name, uri=None):
    """Reference jedi_language_server/jedi_utils.py"""
    if uri is None:
        module_path = name.module_path
        if module_path is None:
            return None
        uri = module_path.as_uri()
    if name.line is None or name.column is None:
        return None
    return {
        "uri": str(uri),
        "range": {
            "start": {"line": name.line - 1, "character": name.column},
            "end": {"line": name.line - 1, "character": name.column + len(name.name)},
        },
    }


@hookimpl
def pylsp_type_definition(config, document, position):
    log.debug("HOB!! pylsp_type_definition %s:%s", document, position)
    kwargs = _utils.position_to_jedi_linecolumn(document, position)
    try:
        script = document.jedi_script()
        names = script.infer(**kwargs)
        definitions = [
            definition
            for definition in (lsp_location(name) for name in names)
            if definition is not None
        ]
        return definitions
    except Exception as e:
        raise e
