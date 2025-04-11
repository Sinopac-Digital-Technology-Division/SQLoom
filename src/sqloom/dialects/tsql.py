import typing as t
from contextlib import contextmanager
from functools import partial

import more_itertools as mit
import pymssql
from lxml import etree
from parse import parse

from ..utils import Connection, Relation
from .types import QueryPlanAnalyzer, QueryPlanFormat


@contextmanager
def _activate_query_plan(cursor):
    cursor.execute("set showplan_xml on")
    yield
    cursor.execute("set showplan_xml off")


class TSQL(QueryPlanAnalyzer):
    def __init__(
        self,
        conn: Connection,
        use_db: str = "",
    ):
        self._host = conn.host
        self._conn = pymssql.connect(
            host=conn.host,
            user=conn.username,
            password=conn.password,
            port=conn.port,
            database=use_db,
        )

    def get_query_plan(
        self,
        raw_sql: str,
    ) -> t.Tuple[QueryPlanFormat, str]:
        cursor = self._conn.cursor()
        with _activate_query_plan(cursor):
            cursor.execute(raw_sql)
            if plan := cursor.fetchone():
                return QueryPlanFormat.XML, mit.one(plan)
            raise ValueError("There is no query plan output from DB")

    def get_relations(
        self,
        raw_sql: str,
    ) -> t.Set[Relation]:
        _, query_plan = self.get_query_plan(raw_sql)
        root = etree.fromstring(
            query_plan,
            etree.XMLParser(ns_clean=True),
        )
        namespace = mit.one(root.nsmap.values())
        lineages = mit.map_except(
            self._unwrap_xml_tag,
            root.findall(
                ".//default_ns:ColumnReference",
                namespaces={"default_ns": namespace},
            ),
            KeyError,
        )
        return set(map(lambda lineage: Relation(**lineage), lineages))

    def _unwrap_xml_tag(
        self,
        tag: etree._Element,
    ):
        scan_bracket = partial(parse, "[{}]")
        attrib = tag.attrib
        try:
            host = mit.first(scan_bracket(attrib["Server"]))  # pyright: ignore
        except KeyError:
            host = self._host

        return {
            "database": mit.first(scan_bracket(attrib["Database"])),  # pyright: ignore
            "schema": mit.first(scan_bracket(attrib["Schema"])),  # pyright: ignore
            "table": mit.first(scan_bracket(attrib["Table"])),  # pyright: ignore
            "column": attrib["Column"],
            "host": host,
        }
