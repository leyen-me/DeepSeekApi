import json
import requests
from constans import build_tool_response
from colorama import init, Fore, Style
from .url import fetch_urls

def search_web(query: str) -> list:
    SEARXNG_URL = "https://search.leyen.me/search"
    params = {'q': query, 'format': 'json'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(SEARXNG_URL, params=params, headers=headers)
    if response.status_code != 200:
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
        raise Exception(
            f"Search query failed with status code {response.status_code}")
    return response.json().get("results", [])


def format_search_results(results: list, max_results: int = 10) -> str:
    """  
    Format the top search results into a context string.  
    """
    formatted = []
    for result in results[:max_results]:
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "No content")
        formatted.append({
            "title": title,
            "url": url,
            "content": content
        })
    results = fetch_urls(formatted)
    return results


def fetch_web(ctx, keyword: str):
    """
    查询指定关键词的网页信息
    """
    print(Fore.GREEN + '--------fetch_web--------')
    print(Fore.CYAN + f'参数: keyword={keyword}')
    print(Fore.GREEN + '--------fetch_web--------' + Style.RESET_ALL)

    try:
        results = format_search_results(search_web(keyword), max_results=10)

        ctx['result'] = build_tool_response(json.dumps(results, ensure_ascii=False))
        ctx['loading'] = False
        ctx['loading_text'] = "完成"
        yield f"__tool__:{json.dumps(ctx)}"
    except Exception as e:
        print(Fore.RED + f'查询失败，{e}' + Style.RESET_ALL)

        error_msg = build_tool_response(f'查询失败，{e}')
        ctx['result'] = error_msg
        ctx['loading'] = False
        ctx['loading_text'] = error_msg
        yield f"__tool__:{json.dumps(ctx)}"
