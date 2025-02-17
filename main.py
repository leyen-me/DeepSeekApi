import os
from flask import Flask, Response, request, stream_with_context
from openai import OpenAI
from flask_cors import CORS

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1/',
    api_key=os.getenv('API_KEY'),
)

app = Flask(__name__)
CORS(app)


@app.route("/stream", methods=["POST"])
def stream():
    messages = request.json
    def generate():
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-R1',
            messages=messages,
            stream=True
        )
        
        done_reasoning = False
        for chunk in response:
            reasoning_chunk = chunk.choices[0].delta.reasoning_content
            answer_chunk = chunk.choices[0].delta.content
            
            if reasoning_chunk:
                yield f"{reasoning_chunk}"
            elif answer_chunk:
                if not done_reasoning:
                    yield "=== Final Answer ==="
                    done_reasoning = True
                yield f"{answer_chunk}"
                
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream'
    )


@app.route("/v3/stream", methods=["POST"])
def stream_v3():
    messages = request.json
    def generate():
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V3',
            messages=messages,
            stream=True
        )
        for chunk in response:
            yield chunk.choices[0].delta.content
                
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)