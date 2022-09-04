from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  code := <str>$code,
  coupon := (
    insert waicolle::Coupon {
      client := global client,
      code := code,
    }
  ),
select coupon { code }
"""


class CouponInsertResult(BaseModel):
    code: str


adapter = TypeAdapter(CouponInsertResult)


async def coupon_insert(
    executor: AsyncIOExecutor,
    *,
    code: str,
) -> CouponInsertResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        code=code,
    )
    return adapter.validate_json(resp, strict=False)
