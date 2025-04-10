from typing import Optional
from attrs import define, field
from .models import CreatResponse
from aomaker.core.api_object import BaseAPIObject
from aomaker.core.router import router

__ALL__ = ["PostCreatAPI"]


@define(kw_only=True)
@router.post("/ep/sms/task/creat")
class PostCreatAPI(BaseAPIObject[CreatResponse]):
    """捕获于 2025-04-07 11:18:53"""

    @define
    class RequestBodyModel:
        them: Optional[str] = field(default=None)
        tid: Optional[str] = field(default=None)
        sendMsgNum: Optional[int] = field(default=None)
        senderNum: Optional[int] = field(default=None)
        type: Optional[int] = field(default=None)
        sendObj: Optional[str] = field(default=None)
        tmpTag: Optional[str] = field(default=None)
        businessType: Optional[int] = field(default=None)
        signatureId: Optional[str] = field(default=None)
        content: Optional[str] = field(default=None)

    request_body: RequestBodyModel
    response: Optional[CreatResponse] = field(default=CreatResponse)
    endpoint_id: Optional[str] = field(default="post_creat")
