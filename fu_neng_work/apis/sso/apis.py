from typing import Optional
from attrs import define, field
from .models import GetByTokenResponse
from aomaker.core.api_object import BaseAPIObject
from aomaker.core.router import router

__ALL__ = ["PostGetByTokenAPI"]


@define(kw_only=True)
@router.post("/sso/platform/login/info/get-by-token")
class PostGetByTokenAPI(BaseAPIObject[GetByTokenResponse]):
    """捕获于 2025-03-27 10:21:10"""

    @define
    class RequestBodyModel:
        token: Optional[str] = field(default=None)

    request_body: RequestBodyModel
    response: Optional[GetByTokenResponse] = field(default=GetByTokenResponse)
    endpoint_id: Optional[str] = field(default="post_get-by-token")
