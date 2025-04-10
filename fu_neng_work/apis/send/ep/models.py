from typing import Optional
from attrs import define, field

__ALL__ = ["CreatResponse"]


@define(kw_only=True)
class CreatResponse:
    errcode: Optional[int] = field(default=None)
    data: Optional[str] = field(default=None)
    requestId: Optional[str] = field(default=None)
