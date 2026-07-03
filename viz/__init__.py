"""Viz registry. Each viz function: render(data, options) -> html string."""
from . import kpi, bar, pie, funnel, progress, ranking, hierarchy, table

VIZ_REGISTRY = {
    "kpi": kpi.render,
    "bar": bar.render,
    "pie": pie.render,
    "funnel": funnel.render,
    "progress": progress.render,
    "ranking": ranking.render,
    "hierarchy": hierarchy.render,
    "table": table.render,
}
