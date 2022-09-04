from typing import Literal
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  custom_position := <optional waicolle::CollagePosition>$custom_position,
  custom_position_waifu_id := <optional uuid>$other_waifu_id,
  custom_position_waifu := (
    (select waicolle::Waifu filter .id = custom_position_waifu_id)
    if exists custom_position_waifu_id
    else <waicolle::Waifu>{}
  ),
update waicolle::Waifu
filter .id = id
set {
  custom_position := custom_position ?? waicolle::CollagePosition.DEFAULT,
  custom_position_waifu := custom_position_waifu,
}
"""


WAIFU_REPLACE_CUSTOM_POSITION_CUSTOM_POSITION = Literal[
    'DEFAULT',
    'LEFT_OF',
    'RIGHT_OF',
]


class WaifuReplaceCustomPositionResult(BaseModel):
    id: UUID


adapter = TypeAdapter(WaifuReplaceCustomPositionResult | None)


async def waifu_replace_custom_position(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    custom_position: WAIFU_REPLACE_CUSTOM_POSITION_CUSTOM_POSITION | None = None,
    other_waifu_id: UUID | None = None,
) -> WaifuReplaceCustomPositionResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        custom_position=custom_position,
        other_waifu_id=other_waifu_id,
    )
    return adapter.validate_json(resp, strict=False)
