from typing import Optional
from attrs import define, field
from .models import QueryallResponse
from aomaker.core.api_object import BaseAPIObject
from aomaker.core.router import router

__ALL__ = ["PostQueryAllAPI"]


@define(kw_only=True)
@router.post("/ep/sms/them/queryAll")
class PostQueryAllAPI(BaseAPIObject[QueryallResponse]):
    """捕获于 2025-04-02 14:17:56"""

    @define
    class RequestBodyModel:
        formKey: Optional[str] = field(default=None)
        subjectCode: Optional[str] = field(default=None)

    request_body: RequestBodyModel
    response: Optional[QueryallResponse] = field(default=QueryallResponse)
    endpoint_id: Optional[str] = field(default="post_queryAll")

if __name__ == '__main__':
    request_body = PostQueryAllAPI.RequestBodyModel()
    RES = PostQueryAllAPI(request_body=request_body).send(formKey = "", subjectCode = "")
    RES.cached_response

