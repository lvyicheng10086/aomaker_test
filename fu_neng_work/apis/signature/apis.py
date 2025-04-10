from typing import Optional
from attrs import define, field
from .models import SaveResponse
from aomaker.core.api_object import BaseAPIObject
from aomaker.core.router import router

__ALL__ = ["SignatureSaveAPI"]


@define(kw_only=True)
@router.post("/signature/save")
class SignatureSaveAPI(BaseAPIObject[SaveResponse]):
    """捕获于 2025-04-07 11:15:06"""

    @define
    class RequestBodyModel:
        name: Optional[str] = field(default=None)
        subject: Optional[str] = field(default=None)

    request_body: RequestBodyModel
    response: Optional[SaveResponse] = field(default=SaveResponse)
    endpoint_id: Optional[str] = field(default="post_save")
