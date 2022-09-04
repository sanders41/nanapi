from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  key := <str>$key,
  value := <str>$value,
insert redis::Data {
  key := key,
  value := value,
}
unless conflict on .key
else (
  update redis::Data set {
    value := value,
  }
)
"""


class DataMergeResult(BaseModel):
    id: UUID


adapter = TypeAdapter(DataMergeResult)


async def data_merge(
    executor: AsyncIOExecutor,
    *,
    key: str,
    value: str,
) -> DataMergeResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        key=key,
        value=value,
    )
    return adapter.validate_json(resp, strict=False)
