from typing import Optional
from attrs import define, field

__ALL__ = ["SaveResponse"]


@define(kw_only=True)
class SaveResponse:
    errcode: Optional[int] = field(default=None)
    errmsg: Optional[str] = field(default=None)
    requestId: Optional[str] = field(default=None)
