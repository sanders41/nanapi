with
  code := <str>$code,
select waicolle::Coupon {
  code,
  claimed_by: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
}
filter .client = global client and .code = code
