from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  ids_al := <array<int32>>$ids_al,
  medias := (select anilist::Media filter .id_al in array_unpack(ids_al)),
  pool := (
    select anilist::Character
    filter .edges.media in medias and .image_large not ilike '%/default.jpg'
  ),
select pool {
  id_al,
  image := str_split(.image_large, '/')[-1],
  favourites,
}
"""


class MediasPoolExportResult(BaseModel):
    id_al: int
    image: str
    favourites: int


adapter = TypeAdapter(list[MediasPoolExportResult])


async def medias_pool_export(
    executor: AsyncIOExecutor,
    *,
    ids_al: list[int],
) -> list[MediasPoolExportResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        ids_al=ids_al,
    )
    return adapter.validate_json(resp, strict=False)
