import requests
from constans import build_tool_response
from colorama import init, Fore, Style

def fetch_weather(city: str) -> str:
    """
    查询指定城市的天气
    """

    print(Fore.GREEN + '--------fetch_weather--------')
    print(Fore.CYAN + f'参数: city={city}')
    print(Fore.GREEN + '--------fetch_weather--------' + Style.RESET_ALL)

    url = f"https://wttr.in/{city}?format=j1&lang=zh"
    response = requests.get(url)
    return build_tool_response(response.text)