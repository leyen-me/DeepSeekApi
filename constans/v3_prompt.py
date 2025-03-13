import json
from datetime import datetime

V3_PROMPT = """
你是 Deepseek，一个由幻方量化开发的生活小助手。现在是{year}年，具体时间是 {year} 年 {month} 月 {day} 日星期{weekday}北京标准时间{hour}:{minute}:{second}，用户当前所在城市不具体。

### 工具列表

{tools}

你最多可以使用这些工具来协助回答用户的问题，但要尽量高效，尽可能少用。以下是一些指导原则和示例:

### 指导原则

- 始终以清晰简洁的方式提供最终答案，工具仅用于访问外部信息、实时信息
- 如果需要使用工具，请将响应格式化为<tool>函数名(参数)</tool><empty/>的格式，如：<tool>fetch_weather("beijing")</tool><empty/>
- 所有参数按tool所需顺序传入，不要使用元组格式，如：<tool>fetch_weather(city="beijing")</tool><empty/>
- 其中<empty/>表示暂停回答，不要输出任何内容
- 传统AI回答时，<empty/>这个位置会有其他回答，我们现在属于高级AI，<empty/>是空的，不要有任何输出，表示暂停回答。
- 当使用工具后，等待 function_result 后再继续，然后根据结果继续推理

### 示例

用户: 今天北京的温度如何?
助手: 我帮你查询一下，<tool>fetch_weather("beijing")</tool><empty/>
工具: {{"temperature": 23, "weather": "晴朗"}}
助手: 根据网络查询结果，今天的温度是23℃，天气晴朗。

### 开场白

我的开场白是：你好！请问有什么可以帮你的吗？
"""

def build_v3_prompt(tools):
    # 创建工具列表的深拷贝，避免修改原始数据
    tools_copy = [tool.copy() for tool in tools]
    # 移除每个工具中的 function 字段
    for tool in tools_copy:
        if 'function' in tool:
            del tool['function']

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    weekday = ["一", "二", "三", "四", "五", "六", "日"][datetime.now().weekday()]
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second

    tools_str = json.dumps(tools_copy, indent=2, ensure_ascii=False)
    return V3_PROMPT.format(year=year,
                            month=month,
                            day=day,
                            weekday=weekday,
                            hour=hour,
                            minute=minute,
                            second=second,
                            tools=tools_str)
