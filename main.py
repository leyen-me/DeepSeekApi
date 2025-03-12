import datetime
import os
import re
from flask import Flask, Response, request, stream_with_context
from openai import OpenAI
from flask_cors import CORS
from constans.v3_prompt import build_v3_prompt
from tools import tools
from enum import Enum, auto

class TokenizerState(Enum):
    NORMAL = auto()          # 正常文本状态
    TOOL_START = auto()      # 可能是<tool>的开始
    IN_TOOL = auto()         # 在<tool>标签内
    TOOL_END = auto()        # 可能是</tool>的开始
    EMPTY_START = auto()     # 可能是<empty/>的开始

def parse_tool_call(tool_content):
    """解析工具调用内容，返回函数名和参数"""
    pattern = r'(\w+)\((.*)\)'
    match = re.match(pattern, tool_content)
    if not match:
        return None, None
    
    func_name = match.group(1)
    args_str = match.group(2)
    
    # 简单解析参数（假设参数是字符串形式）
    args = [arg.strip().strip('"\'') for arg in args_str.split(',') if arg.strip()]
    return func_name, args

def execute_tool(func_name, args):
    try:
        for tool in tools:
            if tool['name'] == func_name:
                tool_func = tool['function']
                result = tool_func(*args)
                return str(result)
        return f"Error: Tool {func_name} not found"
    except Exception as e:
        return f"Error: {e}"
class StreamTokenizer:
    def __init__(self):
        self.buffer = ""
        self.state = TokenizerState.NORMAL
        self.token_buffer = ""
        self.position = 0
        
    def process_char(self, char):
        """处理单个字符，返回(输出文本, 是否需要输出)"""
        if self.state == TokenizerState.NORMAL:
            if char == '<':
                self.state = TokenizerState.TOOL_START
                self.token_buffer = char
                return None, False, False
            return char, True, False
            
        elif self.state == TokenizerState.TOOL_START:
            self.token_buffer += char
            if self.token_buffer == "<tool>":
                self.state = TokenizerState.IN_TOOL
                self.token_buffer = ""  # 清空buffer准备接收函数调用内容
                return None, False, False
            elif self.token_buffer == "<empty":
                self.state = TokenizerState.EMPTY_START
                return None, False, False
            elif len(self.token_buffer) >= 6:  # 不是特殊标记
                self.state = TokenizerState.NORMAL
                result = self.token_buffer
                self.token_buffer = ""
                return result, True, False
            return None, False, False
            
        elif self.state == TokenizerState.IN_TOOL:
            if char == '<' and not self.token_buffer.endswith('</'):
                # 可能是结束标签的开始
                self.token_buffer += char
                return None, False, False
            elif self.token_buffer.endswith('</') and char == 't':
                self.token_buffer += char
                return None, False, False
            elif self.token_buffer.endswith('</t') and char == 'o':
                self.token_buffer += char
                return None, False, False
            elif self.token_buffer.endswith('</to') and char == 'o':
                self.token_buffer += char
                return None, False, False
            elif self.token_buffer.endswith('</too') and char == 'l':
                self.token_buffer += char
                return None, False, False
            elif self.token_buffer.endswith('</tool') and char == '>':
                # 完整的工具调用结束，执行函数
                tool_content = self.token_buffer[:-6].strip()  # 移除</tool>
                func_name, args = parse_tool_call(tool_content)
                if func_name:
                    result = execute_tool(func_name, args)
                    self.state = TokenizerState.NORMAL
                    self.token_buffer = ""
                    return result, True, True
                self.state = TokenizerState.NORMAL
                self.token_buffer = ""
                return None, False, False
            else:
                self.token_buffer += char
                return None, False, False
            
        elif self.state == TokenizerState.EMPTY_START:
            self.token_buffer += char
            if self.token_buffer == "<empty/>":
                self.state = TokenizerState.NORMAL
                self.token_buffer = ""
                return None, False, False
            elif len(self.token_buffer) >= 8:  # 不是<empty/>
                self.state = TokenizerState.NORMAL
                result = self.token_buffer
                self.token_buffer = ""
                return result, True, False
            return None, False, False
            
        return None, False, False

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1/',
    api_key=os.getenv('MODEL_SCOPE_API_KEY'),
)

app = Flask(__name__)
print_mode = False
CORS(app)


def process_stream_response(response, messages, tokenizer):
    output_buffer = ""
    all_buffer = ""
    
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            continue
        
        for char in content:
            text, should_output, is_tool = tokenizer.process_char(char)
            if text is not None:
                output_buffer += text

                if not is_tool:
                    all_buffer += text
            
            if should_output and output_buffer:
                if not is_tool:
                    if print_mode:
                        print('------normal------')
                        print(text)
                    yield output_buffer
                output_buffer = ""
            
            if is_tool:
                if print_mode:
                    print('------tool------')
                    print(text)
                messages.append({
                    "role": "assistant",
                    "content": all_buffer
                })
                messages.append({
                    "role": "user",
                    "content": text
                })
                # 创建新的响应流并继续处理
                new_response = client.chat.completions.create(
                    model='deepseek-ai/DeepSeek-V3',
                    messages=messages,
                    stream=True
                )
                yield from process_stream_response(new_response, messages, tokenizer)
                return  # 结束当前生成器
    
    if output_buffer:
        yield output_buffer


@app.route("/v1/stream", methods=["POST"])
def stream():
    body = request.json
    v3_prompt = build_v3_prompt(tools)
    messages = body.get('messages', [])
    messages.insert(0, {
        "role": "system",
        "content": v3_prompt
    })
    
    def generate(messages):
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V3',
            messages=messages,
            stream=True
        )
        tokenizer = StreamTokenizer()
        yield from process_stream_response(response, messages, tokenizer)

    return Response(
        stream_with_context(generate(messages)),
        mimetype='text/event-stream'
    )

if __name__ == '__main__':
    print("="*50)
    print("🚀 服务启动成功!")
    print(f"📡 服务运行在: http://0.0.0.0:5000")
    # 当前时间
    print(f"⏰ 当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)