import json
import urllib.parse
from datetime import datetime
import aiohttp
import os
import asyncio
from mitmproxy import http
from mitmproxy.script import concurrent

# 全局配置
CONFIG = {
    "LOG_DIR": "mitmproxy_apis",
    "MAX_RESPONSE_SIZE": 1024 * 1024  # 1MB
}

# ================= 网络请求层 =================

async def fetch_response(session, url, headers, data=None):
    """向指定URL发送请求并获取响应"""
    try:
        async with session.request("POST" if data else "GET", url, headers=headers, data=data) as response:
            if response.status == 200:
                content_type = response.headers.get("Content-Type", "")
                if content_type.startswith("application/json"):
                    return await response.json()
                else:
                    text = await response.text()
                    if text and len(text) > CONFIG["MAX_RESPONSE_SIZE"]:
                        return text[:CONFIG["MAX_RESPONSE_SIZE"]] + "... [截断]"
                    else:
                        return text
            else:
                return f"请求失败，状态码: {response.status}"
    except Exception as e:
        return f"无法获取响应: {str(e)}"

async def get_response_async(url, headers, method, params=None):
    """异步获取响应"""
    async with aiohttp.ClientSession() as session:
        if method == "POST":
            return await fetch_response(session, url, headers, data=params)
        else:
            return await fetch_response(session, url, headers)

async def get_response_sync(url, headers, method, params=None):
    """异步获取响应（通过事件循环包装异步函数）"""
    return await get_response_async(url, headers, method, params)

# ================= 数据处理层 =================

def extract_request_params(flow):
    """提取请求参数"""
    method = flow.request.method
    
    if method == "GET":
        return flow.request.query  # GET 请求的参数
    elif method == "POST":
        if flow.request.headers.get("Content-Type", "").startswith("application/json"):
            return flow.request.text  # JSON 格式的 POST 请求体
        else:
            return flow.request.urlencoded_form  # 表单格式的 POST 请求体
    else:
        return None

def extract_response_body(flow):
    """从响应中提取响应体"""
    if not flow.response:
        return None
        
    try:
        if flow.response.headers.get("Content-Type", "").startswith("application/json"):
            return flow.response.json()
        else:
            response_text = flow.response.text
            if response_text and len(response_text) > CONFIG["MAX_RESPONSE_SIZE"]:
                return response_text[:CONFIG["MAX_RESPONSE_SIZE"]] + "... [截断]"
            else:
                return response_text
    except Exception as e:
        return f"无法解析响应体: {str(e)}"


def should_save_response(response_body):
    """判断响应是否应该保存（包含errcode=200或code=200）"""
    # 定义需要检查的成功代码字段和值
    success_codes = [
        ("errcode", 200),
        ("code", 200),
        ("ret_code", 200)
    ]

    # 检查字典类型响应
    if isinstance(response_body, dict):
        for field, value in success_codes:
            if response_body.get(field) == value:
                print(f"找到成功状态码: {field}={value}")
                return True, response_body

    # 检查字符串类型响应
    elif isinstance(response_body, str):
        # 尝试解析字符串为JSON
        try:
            json_body = json.loads(response_body)
            if isinstance(json_body, dict):
                for field, value in success_codes:
                    if json_body.get(field) == value:
                        print(f"从JSON字符串中找到成功状态码: {field}={value}")
                        return True, json_body
        except json.JSONDecodeError:
            # 如果无法解析为JSON，检查字符串是否包含成功代码
            for field, value in success_codes:
                if f'"{field}": {value}' in response_body or f"'{field}': {value}" in response_body:
                    print(f"从字符串中找到成功状态码: {field}={value}")
                    return True, response_body

    # 都不符合条件
    print("未找到匹配的成功状态码")
    return False, response_body

# ================= OpenAPI 生成层 =================

def generate_schema_from_data(data):
    """根据数据生成 OpenAPI schema"""
    if not isinstance(data, dict):
        return {"type": "string", "example": str(data)}
    
    schema = {
        "type": "object",
        "properties": {}
    }
    
    for key, value in data.items():
        if value is None:
            schema["properties"][key] = {"type": "null"}
        elif isinstance(value, bool):
            schema["properties"][key] = {"type": "boolean", "example": value}
        elif isinstance(value, int):
            schema["properties"][key] = {"type": "integer", "example": value}
        elif isinstance(value, float):
            schema["properties"][key] = {"type": "number", "example": value}
        elif isinstance(value, str):
            schema["properties"][key] = {"type": "string", "example": value}
        elif isinstance(value, list):
            if value and all(isinstance(x, dict) for x in value):
                # 如果是字典列表，尝试基于第一项生成模式
                item_schema = generate_schema_from_data(value[0])
                schema["properties"][key] = {
                    "type": "array",
                    "items": item_schema,
                    "example": value[:2]  # 最多包含前两项作为示例
                }
            else:
                schema["properties"][key] = {
                    "type": "array",
                    "items": {"type": "string"},
                    "example": value[:2] if value else []
                }
        elif isinstance(value, dict):
            schema["properties"][key] = generate_schema_from_data(value)
    
    return schema

def generate_openapi_document(url, method, params, token, response_body):
    """生成符合 OpenAPI 3.1.0 规范的文档"""
    parsed_url = urllib.parse.urlparse(url)
    endpoint_path = parsed_url.path
    
    # 创建 schema 名称，基于路径
    schema_name = f"{endpoint_path.split('/')[-1].title().replace('-', '')}Response"
    
    # 生成响应 schema
    response_schema = generate_schema_from_data(response_body)
    
    # 创建基本的 OpenAPI 文档结构
    openapi_data = {
        "openapi": "3.1.0",
        "info": {
            "title": f"API Documentation for {parsed_url.netloc}",
            "description": f"自动生成的 API 文档",
            "version": "1.0.0"
        },
        "paths": {
            f"{endpoint_path}": {
                method.lower(): {
                    "tags": [endpoint_path.split('/')[1] if len(endpoint_path.split('/')) > 1 else "default"],
                    "summary": f"{endpoint_path.split('/')[-1]}",
                    "description": f"捕获于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "operationId": f"{method.lower()}_{endpoint_path.split('/')[-1]}",
                    "parameters": [],
                    "responses": {
                        "200": {
                            "description": "成功响应",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": f"#/components/schemas/{schema_name}"
                                    }
                                }
                            }
                        },
                        "401": {
                            "$ref": "#/components/schemas/UnauthorizedError"
                        },
                        "422": {
                            "$ref": "#/components/schemas/HTTPValidationError"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                f"{schema_name}": response_schema,
                "UnauthorizedError": {
                    "type": "object",
                    "properties": {
                        "errcode": {
                            "type": "integer",
                            "example": 401
                        },
                        "message": {
                            "type": "string",
                            "example": "Unauthorized"
                        }
                    }
                },
                "HTTPValidationError": {
                    "type": "object",
                    "properties": {
                        "errcode": {
                            "type": "integer",
                            "example": 422
                        },
                        "message": {
                            "type": "string",
                            "example": "Validation Error"
                        }
                    }
                }
            }
        }
    }
    
    # 处理 GET 参数
    if method == "GET" and params:
        for key, value in params.items():
            param_info = {
                "name": key,
                "in": "query",
                "required": True,
                "schema": {
                    "type": "string",
                    "example": value
                },
                "description": f"查询参数: {key}"
            }
            openapi_data["paths"][endpoint_path][method.lower()]["parameters"].append(param_info)
    
    # 处理 POST 请求体
    elif method == "POST" and params:
        request_body = {
            "required": True,
            "content": {}
        }
        
        if isinstance(params, str):
            try:
                # 尝试解析 JSON 字符串
                json_params = json.loads(params)
                request_schema = generate_schema_from_data(json_params)
                request_body["content"]["application/json"] = {
                    "schema": request_schema
                }
            except:
                # 非 JSON 格式
                request_body["content"]["application/x-www-form-urlencoded"] = {
                    "schema": {
                        "type": "string",
                        "example": params
                    }
                }
        else:
            # 表单数据
            form_schema = {
                "type": "object",
                "properties": {}
            }
            
            for key, value in params.items():
                form_schema["properties"][key] = {
                    "type": "string",
                    "example": value
                }
            
            request_body["content"]["application/x-www-form-urlencoded"] = {
                "schema": form_schema
            }
        
        openapi_data["paths"][endpoint_path][method.lower()]["requestBody"] = request_body
    
    # 添加 token 参数
    if token:
        token_param = {
            "name": "TOKEN",
            "in": "header",
            "required": True,
            "schema": {
                "type": "string",
                "example": token
            },
            "description": "身份验证令牌"
        }
        openapi_data["paths"][endpoint_path][method.lower()]["parameters"].append(token_param)
    
    return openapi_data

# ================= 文件存储层 =================

def save_openapi_document(url, method, openapi_data):
    """保存 OpenAPI 文档到文件"""
    # 确保日志目录存在
    os.makedirs(CONFIG["LOG_DIR"], exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{CONFIG['LOG_DIR']}/{timestamp}_{method}_{url.split('/')[-1].split('?')[0]}.json"
    
    # 写入 JSON 文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, ensure_ascii=False, indent=2)
    
    print(f"已保存符合 OpenAPI 3.1.0 规范的文档到 {filename}")
    return filename

# ================= 主处理流程 =================

def process_request(flow):
    """处理请求的主要逻辑"""
    try:
        # 确保日志目录存在
        os.makedirs(CONFIG["LOG_DIR"], exist_ok=True)

        # 获取基本请求信息
        url = flow.request.pretty_url
        method = flow.request.method

        # 修改过滤逻辑，保留更多可能的API请求
        if url.endswith((".css", ".js", ".svg", ".gif", ".png", ".woff", ".ttf", ".eot")):
            # print(f"跳过静态资源: {url}")
            return

        # 打印调试信息
        print(f"捕获请求: {method} {url}")

        # 获取参数和令牌
        params = extract_request_params(flow)
        token = flow.request.headers.get("token", "") or flow.request.headers.get("TOKEN", "")

        # 日志记录
        print(f"URL: {url}")
        print(f"Method: {method}")
        print(f"Token: {token}")
        print(f"Params: {params}")

        # 添加此处理流程标记和时间戳用于调试
        flow.metadata["processed"] = True
        flow.metadata["process_time"] = datetime.now().strftime("%H:%M:%S.%f")

        # 将请求写入临时文件用于调试
        with open(f"{CONFIG['LOG_DIR']}/requests.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {method} {url}\n")
    except Exception as e:
        print(f"请求处理出错: {str(e)}")
        # 记录错误到文件
        try:
            with open(f"{CONFIG['LOG_DIR']}/errors.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 请求处理错误: {str(e)}, URL: {flow.request.pretty_url}\n")
        except:
            pass


@concurrent
def response(flow: http.HTTPFlow) -> None:
    """mitmproxy 响应处理入口"""
    try:
        # 检查该流是否已被请求处理过
        if not flow.metadata.get("processed"):
            return

        # 获取基本信息
        url = flow.request.pretty_url
        method = flow.request.method
        process_time = flow.metadata.get("process_time", "未知")

        # 过滤掉静态资源
        if url.endswith((".css", ".js", ".svg", ".gif", ".png", ".woff", ".ttf", ".eot")):
            return

        print(f"处理响应: {method} {url} (请求于 {process_time})")

        # 获取参数和令牌
        params = extract_request_params(flow)
        token = flow.request.headers.get("token", "") or flow.request.headers.get("TOKEN", "")

        # 获取响应体 - 添加原始响应文本的保存
        try:
            original_text = flow.response.text if flow.response else "无响应文本"
            with open(f"{CONFIG['LOG_DIR']}/raw_responses.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] {method} {url}\n")
                f.write(f"状态码: {flow.response.status_code if flow.response else '无响应'}\n")
                f.write(f"响应(前500字符): {original_text[:500]}\n")
                f.write("-" * 80 + "\n")
        except Exception as e:
            print(f"保存原始响应出错: {str(e)}")

        # 解析响应体
        response_body = extract_response_body(flow)
        print(
            f"获取到响应: {str(response_body)[:100]}{'...' if response_body and len(str(response_body)) > 100 else ''}")

        # 判断是否需要保存
        should_save_result, processed_response = should_save_response(response_body)

        if should_save_result:
            print(f"响应符合保存条件，准备生成OpenAPI文档...")
            # 生成 OpenAPI 文档
            openapi_data = generate_openapi_document(url, method, params, token, processed_response)

            # 保存文档
            filename = save_openapi_document(url, method, openapi_data)
            print(f"已保存到文件: {filename}")
        else:
            print(f"响应不符合保存条件，不保存文件")
            # 记录不符合保存条件的响应以供分析
            try:
                with open(f"{CONFIG['LOG_DIR']}/skipped_responses.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] {method} {url}\n")
                    f.write(f"不保存原因: 未找到成功状态码\n")
                    f.write(f"响应内容: {str(response_body)[:500]}\n")
                    f.write("-" * 80 + "\n")
            except Exception as e:
                print(f"记录跳过的响应出错: {str(e)}")
    except Exception as e:
        print(f"响应处理出错: {str(e)}")
        # 记录错误到文件
        try:
            with open(f"{CONFIG['LOG_DIR']}/errors.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 响应处理错误: {str(e)}, URL: {flow.request.pretty_url}\n")
        except:
            pass

# ================= 入口函数 =================

@concurrent
def request(flow: http.HTTPFlow) -> None:
    """mitmproxy 请求处理入口"""
    process_request(flow)

def run():
    """主程序入口（用于直接运行脚本）"""
    print("启动 mitmproxy API 捕获脚本")
    print(f"日志将保存到 {CONFIG['LOG_DIR']} 目录")
    print("等待请求...")
    # 当作为 mitmproxy 脚本运行时，由 mitmproxy 调用 request 函数
    # 此函数仅用于直接运行脚本时的提示

if __name__ == "__main__":
    run()