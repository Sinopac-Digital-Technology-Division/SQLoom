import typing as t
from enum import StrEnum

from ..utils import Relation


class QueryPlanFormat(StrEnum):
    XML = "xml"
    JSON = "json"


@t.runtime_checkable
class QueryPlanAnalyzer(t.Protocol):

    def get_query_plan(self, raw_sql: str) -> t.Tuple[QueryPlanFormat, str]: ...

    def get_relations(self, raw_sql: str) -> t.Set[Relation]: ...
