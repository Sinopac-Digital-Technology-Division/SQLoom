from collections import namedtuple

Relation = namedtuple(
    "Relation",
    [
        "host",  # The field would be necessary in SQL Server linked db
        "database",
        "schema",
        "table",
        "column",
    ],
)


Connection = namedtuple(
    "Connection",
    ["host", "username", "password", "port"],
)
