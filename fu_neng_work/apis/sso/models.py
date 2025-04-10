from typing import Optional, Any
from attrs import define, field

__ALL__ = [
    "GetByTokenResponseDataAccountInfo",
    "GetByTokenResponseData",
    "GetByTokenResponse",
]


@define(kw_only=True)
class GetByTokenResponseDataAccountInfo:
    id: Optional[str] = field(default=None)
    accountCode: Optional[str] = field(default=None)
    spId: Optional[str] = field(default=None)
    orgId: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    loginName: Optional[str] = field(default=None)
    mobile: Optional[str] = field(default=None)
    email: Optional[Any] = field(default=None)
    memberId: Optional[Any] = field(default=None)
    status: Optional[int] = field(default=None)
    createrId: Optional[str] = field(default=None)
    accType: Optional[int] = field(default=None)
    spCode: Optional[str] = field(default=None)
    realmCode: Optional[str] = field(default=None)
    spName: Optional[str] = field(default=None)


@define(kw_only=True)
class GetByTokenResponseData:
    userId: Optional[Any] = field(default=None)
    userName: Optional[str] = field(default=None)
    name: Optional[Any] = field(default=None)
    memberId: Optional[Any] = field(default=None)
    accountInfo: Optional[GetByTokenResponseDataAccountInfo] = field(default=None)
    terminalType: Optional[str] = field(default=None)
    identityId: Optional[str] = field(default=None)
    mobile: Optional[Any] = field(default=None)
    clientId: Optional[str] = field(default=None)
    token: Optional[str] = field(default=None)
    renew: Optional[bool] = field(default=None)
    ttl: Optional[int] = field(default=None)
    timeRatio: Optional[float] = field(default=None)
    grant_type: Optional[str] = field(default=None)
    operator: Optional[str] = field(default=None)
    expiration: Optional[str] = field(default=None)
    sessionId: Optional[str] = field(default=None)
    spId: Optional[str] = field(default=None)
    spName: Optional[str] = field(default=None)


@define(kw_only=True)
class GetByTokenResponse:
    data: Optional[GetByTokenResponseData] = field(default=None)
    errcode: Optional[int] = field(default=None)
    errmsg: Optional[str] = field(default=None)
    code: Optional[str] = field(default=None)
    msg: Optional[str] = field(default=None)
