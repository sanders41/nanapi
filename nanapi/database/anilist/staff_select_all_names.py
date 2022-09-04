from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Staff {
  id_al,
  name_user_preferred,
  name_alternative,
  name_native,
}
order by .favourites desc
"""


class StaffSelectAllNamesResult(BaseModel):
    id_al: int
    name_user_preferred: str
    name_alternative: list[str]
    name_native: str | None


adapter = TypeAdapter(list[StaffSelectAllNamesResult])


async def staff_select_all_names(
    executor: AsyncIOExecutor,
) -> list[StaffSelectAllNamesResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)
