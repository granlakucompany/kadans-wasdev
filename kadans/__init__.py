"""Kadans WASDEV — videos written as code: a JSON spec -> HTML scenes -> MP4.

By Getho Guerrier · GRAN LAKU COMPANY · https://wasdev.ai · MIT
"""
from . import _fresh  # noqa: F401 — referans tan chajman motè a (fresh_engine), anvan tout lòt modil
from .spec import (
    RATIOS,
    SCENE_TYPES,
    TICKS_PER_SECOND,
    SpecError,
    frames_to_ticks,
    json_schema,
    parse_timecode,
    quantize_time,
    sec_to_ticks,
    ticks_to_frames,
    ticks_to_sec,
    timecode,
    timeline,
    total,
    validate,
)
from .compose import build_html
from .hyperframes import (
    export_kadans_html,
    export_to_hyperframes,
    import_hyperframes,
    import_kadans_html,
)
from .interchange import (
    export_edl,
    export_fcp7_xml,
    export_timeline,
    import_edl,
    import_fcp7_xml,
    import_timeline,
)
from .lint import measure_loudness


def render(*a, **kw):
    """spec -> MP4 (see kadans.renderer.render)."""
    from .renderer import render as _r
    return _r(*a, **kw)


__version__ = "0.6.0"
NAME = "Kadans WASDEV"
AUTHOR = "Getho Guerrier"
COMPANY = "GRAN LAKU COMPANY"

__all__ = [
    "RATIOS", "SCENE_TYPES", "SpecError", "json_schema", "timeline", "total", "validate",
    "build_html", "render",
    "import_kadans_html", "export_kadans_html", "import_hyperframes", "export_to_hyperframes",
    "export_fcp7_xml", "import_fcp7_xml", "export_edl", "import_edl", "export_timeline", "import_timeline",
    "TICKS_PER_SECOND", "sec_to_ticks", "ticks_to_sec", "frames_to_ticks", "ticks_to_frames",
    "quantize_time", "timecode", "parse_timecode", "measure_loudness",
    "__version__", "NAME", "AUTHOR", "COMPANY"
]
