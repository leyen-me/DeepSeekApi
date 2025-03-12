from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import requests
from constans import build_tool_response


def fetch_url(url: str) -> str:
    """
    查询指定URL的网页信息
    """
    print(Fore.GREEN + '--------fetch_url--------')
    print(Fore.CYAN + f'参数: url={url}')
    print(Fore.GREEN + '--------fetch_url--------' + Style.RESET_ALL)

    text = ''
    try:
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
        print(text)
    except Exception as e:
        print(Fore.RED + f'获取网页信息失败: {e}' + Style.RESET_ALL)
        return build_tool_response('获取网页信息失败')

    return build_tool_response(text)