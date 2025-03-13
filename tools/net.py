import json
from constans import build_tool_response

def get_ip_info(ctx):
    from flask import request
    client_ip = request.remote_addr
    # 如果使用了代理，可能需要从X-Forwarded-For头获取真实IP
    if request.headers.get('X-Forwarded-For'):
        client_ip = request.headers.get('X-Forwarded-For').split(',')[0]
    # 获取更多请求信息
    user_agent = request.headers.get('User-Agent')
    ip_info = {
        "client_ip": client_ip,
        "forwarded_for": request.headers.get('X-Forwarded-For'),
        "user_agent": user_agent,
        "headers": dict(request.headers)
    }

    ctx['result'] = build_tool_response(ip_info)
    ctx['loading'] = False
    ctx['loading_text'] = "完成"
    yield f"__tool__:{json.dumps(ctx)}"
