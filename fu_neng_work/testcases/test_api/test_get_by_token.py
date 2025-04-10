import sys
import os

import pytest

# 获取项目根目录（fu_neng_work 的父目录）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT_DIR)

from fu_neng_work.apis.sso.apis import PostGetByTokenAPI
from aomaker.storage import cache

token = cache.get('token')

@pytest.mark.mock_api
@pytest.mark.parametrize("token", [token])
def test_case_get_by_token(token):
    query_params = PostGetByTokenAPI.RequestBodyModel(token=token)
    resp = PostGetByTokenAPI(request_body=query_params).send()
    assert resp.response_model.errcode == 200




