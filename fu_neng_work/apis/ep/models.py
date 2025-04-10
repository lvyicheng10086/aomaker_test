from typing import Optional, Any, List
from attrs import define, field

__ALL__ = ["QueryallResponseDataItem", "QueryallResponse"]


@define(kw_only=True)
class QueryallResponseDataItem:
    id: Optional[str] = field(default=None)
    subjectCode: Optional[str] = field(default=None)
    subjectName: Optional[str] = field(default=None)
    subjectWideTable: Optional[str] = field(default=None)
    formKey: Optional[str] = field(default=None)
    biUrl: Optional[Any] = field(default=None)
    spId: Optional[str] = field(default=None)
    spCode: Optional[str] = field(default=None)
    accountCode: Optional[str] = field(default=None)
    createTime: Optional[str] = field(default=None)
    updateTime: Optional[Any] = field(default=None)


@define(kw_only=True)
class QueryallResponse:
    errcode: Optional[int] = field(default=None)
    errmsg: Optional[str] = field(default=None)
    data: Optional[List[QueryallResponseDataItem]] = field(default=None)
    requestId: Optional[str] = field(default=None)
