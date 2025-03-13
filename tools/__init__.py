from .weather import fetch_weather
from .stock import fetch_stock
from .web import fetch_web
from .url import fetch_url
from .net import get_ip_info

tools = [
    {
        "name": "fetch_weather",
        "description": "查询指定城市的天气",
        "use_time": "当用户需要今天（当前日期）的天气信息时，使用此工具。非今天，请勿使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称", "example": "北京"}
            },
            "required": ["city"]
        },
        "function": fetch_weather
    },
    {
        "name": "fetch_stock",
        "description": "查询指定股票代码股票信息，支持港股、美股、A股",
        "use_time": "当用户需要具体某一天的股票信息时，使用此工具。非必要时，请勿使用。",
        "enum": {
            "type": ["HK", "US", "A"]
        },
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码", "example": "000001"},
                "type": {"type": "string", "description": "股票类型", "example": "HK"},
                "date": {"type": "string", "description": "查询日期", "example": "2023-01-01"},
            },
            "required": ["symbol", "type", "date"]
        },
        "function": fetch_stock
    },
    {
        "name": "fetch_web",
        "description": "查询指定关键词的网页信息, 类似于搜索引擎",
        "use_time": "当用户需要查询指定关键词的网页信息时，使用此工具。非必要时，请勿使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "关键词", "example": "热点新闻"}
            },
            "required": ["keyword"]
        },
        "function": fetch_web
    },
    {
        "name": "fetch_url",
        "description": "查询指定URL的网页信息",
        "use_time": "当用户需要查询指定URL的网页信息时，使用此工具。非必要时，请勿使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL", "example": "https://www.baidu.com"}
            },
            "required": ["url"]
        },
        "function": fetch_url
    },
    {
        "name": "get_ip_info",
        "description": "获取用户的IP信息",
        "use_time": "当用户需要获取自己的IP信息时，使用此工具。非必要时，请勿使用。",
        "function": get_ip_info
    }
]
