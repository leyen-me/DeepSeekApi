from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import requests
from constans import build_tool_response
from concurrent.futures import ThreadPoolExecutor
from constans import client, base_model
import json


def get_url(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(['script', 'style']):
        script.decompose()
    text = soup.get_text(separator=' ', strip=True)
    text = '\n'.join(text.split())
    return text


def fetch_urls(arr: list) -> list:

    # ai 总结
    def ai_summary(text: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的网页数据分析师，擅长从文本中提取有价值的信息，并进行总结。要求总结内容精炼，不要超过100字。"
            },
            {
                "role": "user",
                "content": "这是使用Python的requests库获取的网页信息，经过bs4库处理后的文本：" + text
            }
        ]
        response = client.chat.completions.create(
            model=base_model,
            messages=messages,
        )
        summary = response.choices[0].message.content

        print(Fore.GREEN + '--------ai_summary--------')
        print(Fore.CYAN + f'总结: {summary}')
        print(Fore.GREEN + '--------ai_summary--------' + Style.RESET_ALL)

        return summary

    def process_url(item):
        url = item["url"]
        try:
            text = get_url(url)
            summary = ai_summary(text)
            item["content"] = summary
        except Exception as e:
            print(Fore.RED + f'获取网页信息失败: {e}' + Style.RESET_ALL)
            item["content"] = '获取网页信息失败'
        return item

    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_url, arr))

    return results


def fetch_url(ctx, url: str):
    """
    查询指定URL的网页信息
    """
    print(Fore.GREEN + '--------fetch_url--------')
    print(Fore.CYAN + f'参数: url={url}')
    print(Fore.GREEN + '--------fetch_url--------' + Style.RESET_ALL)

    text = ''
    try:
        text = get_url(url)
    except Exception as e:
        print(Fore.RED + f'获取网页信息失败: {e}' + Style.RESET_ALL)
        error_msg = build_tool_response('获取网页信息失败')

        ctx['result'] = error_msg
        ctx['loading'] = False
        ctx['loading_text'] = error_msg
        yield f"__tool__:{json.dumps(ctx)}"
        return

    ctx['result'] = build_tool_response(text)
    ctx['loading'] = False
    ctx['loading_text'] = "完成"
    yield f"__tool__:{json.dumps(ctx)}"
