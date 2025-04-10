from typing import Optional
from attrs import define, field

__ALL__ = [
    "PostSaveAPIRequestBodyTemplateParamsItem",
    "SaveResponseData",
    "SaveResponse",
]


@define(kw_only=True)
class PostSaveAPIRequestBodyTemplateParamsItem:
    paramId: Optional[str] = field(default=None)
    paramVal: Optional[str] = field(default=None)


@define(kw_only=True)
class SaveResponseData:
    id: Optional[str] = field(default=None)


@define(kw_only=True)
class SaveResponse:
    errcode: Optional[int] = field(default=None)
    errmsg: Optional[str] = field(default=None)
    data: Optional[SaveResponseData] = field(default=None)
    requestId: Optional[str] = field(default=None)
