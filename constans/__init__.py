import os
from openai import OpenAI

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1/',
    api_key=os.getenv('MODEL_SCOPE_API_KEY'),
)

base_model = "deepseek-ai/DeepSeek-V3"

def build_tool_response(tool_result):
    return f"tool:\n{tool_result}"