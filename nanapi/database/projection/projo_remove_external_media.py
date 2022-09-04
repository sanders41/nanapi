from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  external_media_id := <uuid>$external_media_id,
update projection::Projection
filter .id = id
set {
  external_medias -= (select .external_medias filter .id = external_media_id),
}
"""


class ProjoRemoveExternalMediaResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ProjoRemoveExternalMediaResult | None)


async def projo_remove_external_media(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    external_media_id: UUID,
) -> ProjoRemoveExternalMediaResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        external_media_id=external_media_id,
    )
    return adapter.validate_json(resp, strict=False)
