from typing import Optional

from app import models


def userinfo_update(
    *,
    id: int,
    first_name: str,
    last_name: str,
    phone: str,
    country: Optional[int],
    province: str,
    city: str,
):
    userinfo = models.UserInfo.objects.get(user_id=id)

    userinfo.first_name = first_name
    userinfo.last_name = last_name
    userinfo.country_id = country
    userinfo.province = province
    userinfo.phone = phone
    userinfo.city = city

    userinfo.save()
    return userinfo.user
