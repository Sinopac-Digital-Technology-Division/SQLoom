# SQLoom

SQLoom is a tool that make extracting data lineage from SQL statement easily. Please refer following code example to extract referenced column from query statement.

```python
from sqloom import TSQL, Connection

conn = Connection(
  "127.0.0.1",  # DB ip address
  "my_username",
  "my_password",
  1433,
)
query = "SELECT col_a, col_b from MyDB.dbo.MyTable"
TSQL(conn).get_relation(query)
# Output a set of relation instances, which is a namedtuple containing
# containing host, database, schema, table and column.
# {
#     Relation(host='127.0.0.1', database='MyDB', schema='dbo', table='MyTable', column='col_a'),
#     Relation(host='127.0.0.1', database='MyDB', schema='dbo', table='MyTable', column='col_b'),
# }
```

