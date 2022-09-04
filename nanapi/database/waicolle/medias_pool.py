from enum import StrEnum

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  ids_al := <array<int32>>$ids_al,
  discord_id := <optional int64>$discord_id,
  genred := <optional bool>$genred ?? false,
  player := (select waicolle::Player filter .client = global client and .user.discord_id = discord_id),
  medias := (select anilist::Media filter .id_al in array_unpack(ids_al)),
  pool := (
    select anilist::Character
    filter .edges.media in medias and .image_large not ilike '%/default.jpg'
  ),
genred := (
    select pool
    filter (
      re_test(r"(?i)\y(?:female|non-binary)\y", .fuzzy_gender)
      if player.game_mode = waicolle::GameMode.WAIFU else
      re_test(r"(?i)\y(?:male|non-binary)\y", .fuzzy_gender)
      if player.game_mode = waicolle::GameMode.HUSBANDO else
      true
    )
  ) if genred and exists player else pool
group genred {
  id_al,
}
by .rank
"""


class WaicolleRank(StrEnum):
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'


class MediasPoolResultElements(BaseModel):
    id_al: int


class MediasPoolResultKey(BaseModel):
    rank: WaicolleRank


class MediasPoolResult(BaseModel):
    key: MediasPoolResultKey
    grouping: list[str]
    elements: list[MediasPoolResultElements]


adapter = TypeAdapter(list[MediasPoolResult])


async def medias_pool(
    executor: AsyncIOExecutor,
    *,
    ids_al: list[int],
    discord_id: int | None = None,
    genred: bool | None = None,
) -> list[MediasPoolResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        ids_al=ids_al,
        discord_id=discord_id,
        genred=genred,
    )
    return adapter.validate_json(resp, strict=False)
