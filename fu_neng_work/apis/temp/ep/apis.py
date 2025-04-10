from typing import List, Optional
from attrs import define, field
from .models import SaveResponse, PostSaveAPIRequestBodyTemplateParamsItem
from aomaker.core.api_object import BaseAPIObject
from aomaker.core.router import router

__ALL__ = ["PostSaveAPI"]


@define(kw_only=True)
@router.post("/ep/v2/sms/template/save")
class PostSaveAPI(BaseAPIObject[SaveResponse]):
    """捕获于 2025-04-07 11:15:12"""

    @define
    class RequestBodyModel:
        name: Optional[str] = field(default=None)
        businessType: Optional[int] = field(default=None)
        signatureId: Optional[str] = field(default=None)
        template: Optional[str] = field(default=None)
        templateParams: Optional[
            List[PostSaveAPIRequestBodyTemplateParamsItem]
        ] = field(default=None)
        status: Optional[int] = field(default=None)
        objId: Optional[str] = field(default=None)
        subject: Optional[str] = field(default=None)

    request_body: RequestBodyModel
    response: Optional[SaveResponse] = field(default=SaveResponse)
    endpoint_id: Optional[str] = field(default="post_save")
