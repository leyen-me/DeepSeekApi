import json
import akshare as ak
import yfinance as yf
from colorama import init, Fore, Style
from constans import build_tool_response


def fetch_stock(ctx, symbol: str, type: str, date: str):
    """
    查询指定股票代码的股票信息
    """
    print(Fore.GREEN + '--------fetch_stock--------')
    print(Fore.CYAN + f'参数: symbol={symbol}, type={type}, date={date}')
    print(Fore.GREEN + '--------fetch_stock--------' + Style.RESET_ALL)

    stock_hist_df = None
    try:
        if type == 'HK':
            stock_hist_df = ak.stock_hk_hist(
                symbol=symbol, start_date=date, end_date=date)
        elif type == 'US':
            stock = yf.Ticker(symbol)
            stock_hist_df = stock.history(start=date, end=date)
        elif type == 'A':
            stock_hist_df = ak.stock_zh_a_hist(
                symbol=symbol, start_date=date, end_date=date)
        else:
            error_msg = build_tool_response(f'暂不支持查询该类型的股票，{type}')
            ctx['result'] = error_msg
            ctx['loading'] = False
            ctx['loading_text'] = error_msg
            yield f"__tool__:{json.dumps(ctx)}"
            return
    except Exception as e:
        print(Fore.RED + f'查询失败，{e}' + Style.RESET_ALL)

        error_msg = build_tool_response(f'查询失败，{e}')
        ctx['result'] = error_msg
        ctx['loading'] = False
        ctx['loading_text'] = error_msg
        yield f"__tool__:{json.dumps(ctx)}"
        return

    ctx['result'] = build_tool_response(json.dumps(stock_hist_df.to_json()))
    ctx['loading'] = False
    ctx['loading_text'] = "完成"
    yield f"__tool__:{json.dumps(ctx)}"
