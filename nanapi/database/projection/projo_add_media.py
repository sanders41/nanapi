from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  _media := ( select anilist::Media filter .id_al = id_al )
update projection::Projection
filter .id = id
set { medias += _media }
"""


class ProjoAddMediaResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ProjoAddMediaResult | None)


async def projo_add_media(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    id_al: int,
) -> ProjoAddMediaResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        id_al=id_al,
    )
    return adapter.validate_json(resp, strict=False)
