import os
from openai import OpenAI

client = OpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    api_key=os.getenv('ALIYUN_API_KEY'),
)

base_model = "deepseek-v3"

def build_tool_response(tool_result):
    return f"tool:\n{tool_result}"