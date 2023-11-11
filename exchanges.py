import json
import time
import terminal # Add ANSI terminal support https://pypi.org/project/terminal/
import colorama # Add ANSI terminal control https://pypi.org/project/colorama/
import ccxt # Add handling for crypto exchanges https://pypi.org/project/ccxt/
import requests


print('---< BitTrex >----------------------------')
exchange_id = 'bittrex'
exchange_class = getattr(ccxt, exchange_id)
exchbittrex = exchange_class({
    'apiKey': 'xxxxxxxxxxxxxxxx',
    'secret': 'xxxxxxxxxxxxxxxx',
    'timeout': 30000,
    'enableRateLimit': True,
    'rateLimit': 950
})
exchbittrex.load_markets()
balancebittrex = exchbittrex.fetch_balance()['total']
print('---< Binance >----------------------------')
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchbinance = exchange_class({
    'apiKey': 'xxxxxxxxxxxxxxxx',
    'secret': 'xxxxxxxxxxxxxxxx',
    'timeout': 30000,
    'enableRateLimit': True,
    'rateLimit': 950
})
exchbinance.load_markets()
balancebinance = exchbinance.fetch_balance()['total']
print('---< Binance Bot >------------------------')
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchbinbot = exchange_class({
    'apiKey': 'xxxxxxxxxxxxxxxx',
    'secret': 'xxxxxxxxxxxxxxxx',
    'timeout': 30000,
    'enableRateLimit': True,
    'rateLimit': 950
})
exchbinbot.load_markets()
balancebinbot = exchbinbot.fetch_balance()['total']
print('---< KuCoin >-----------------------------')
exchange_id = 'kucoin'
exchange_class = getattr(ccxt, exchange_id)
exchkucoin = exchange_class({
    'apiKey': 'xxxxxxxxxxxxxxxx',
    'secret': 'xxxxxxxxxxxxxxxx',
    'password': 'Weklom02',
    'timeout': 30000,
    'enableRateLimit': True,
    'rateLimit': 800
})
exchkucoin.load_markets()
balancekucoin = exchkucoin.fetch_balance()['total']
print('---< HuobiPro >---------------------------')
exchange_id = 'huobipro'
exchange_class = getattr(ccxt, exchange_id)
exchhuobi = exchange_class({
    'apiKey': 'xxxxxxxxxxxxxxxx',
    'secret': 'xxxxxxxxxxxxxxxx',
    'timeout': 30000,
    'enableRateLimit': True,
    'rateLimit': 800
})
exchhuobi.load_markets()
balancehuobi = exchhuobi.fetch_balance()['total']

print('---< EUR / USD >--------------------------')
eurbinance = exchbinance.fetchTicker('BTC/EUR')['last']
usdbinance = 1 / exchbinance.fetchTicker('EUR/USDT')['last']
btcusdbinance = exchbinance.fetchTicker('BTC/USDT')['last']
eurbittrex = exchbittrex.fetchTicker('BTC/EUR')['last']
usdbittrex = exchbittrex.fetchTicker('USDT/EUR')['last']
btcusdbittrex = exchbittrex.fetchTicker('BTC/USDT')['last']
btcusdkucoin = exchkucoin.fetchTicker('BTC/USDT')['last']
btcusdhuobi = exchhuobi.fetchTicker('BTC/USDT')['last']
btcusdhuobi = btcusdbinance
eur = (eurbinance + eurbittrex) / 2
usd = (usdbinance + usdbittrex) / 2 
print(btcusdbinance, btcusdbittrex, btcusdkucoin, btcusdhuobi)
btcusd = (btcusdbinance + btcusdbittrex + btcusdhuobi) / 3
print('BTC/EUR: {:.2f}'.format(eur))
print('BTC/USD: {:.2f}'.format(btcusd))
print('USD/EUR: {:.4f}'.format(usd))

totalassetsbtc = 0.0
export = { "BTCEUR": '{:.2f}'.format(eur), "BTCUSD": '{:.2f}'.format(btcusd), "USDEUR": '{:.2f}'.format(usd), "Wallet": [] }


def getAssets(market, balance, exchange):
    sumbtc = 0.0
    print()
    print(terminal.blue_bg(terminal.yellow(terminal.bold(market.ljust(60)))))
    expmarket = {}
    expmarket['Markets'] = []
    for asset in balance:
        symbol = asset
        amount = balance[asset]
        price = 0.0
        valuebtc = 0.0
        if amount > 0.00000001 and symbol != 'BTXCRD':
            if symbol == 'BTC':
                price = 1.0
                valuebtc = price * amount
            elif symbol == 'USDT' or symbol == 'USD':
                price = 1.0
                valuebtc = amount/ btcusd
            elif symbol == 'EUR':
                price = 1.0
                valuebtc = amount / eur
            elif symbol == 'BOSON' or symbol == 'SHIB' or symbol == 'RAY' or symbol == 'SLP' or symbol == 'VTHO' or symbol == 'XTM' or symbol == 'KAVA' or symbol == 'MTRG' or symbol == 'LUNC':
                hybrid = symbol+'/USDT'
                price = exchange.fetchTicker(hybrid)['last'] / btcusd
                valuebtc = price * amount
            else:
                hybrid = symbol+'/BTC'
                price = exchange.fetchTicker(hybrid)['last']
                valuebtc = price * amount
            print(symbol.ljust(6), '{:16.8f}'.format(amount), '{:14.10f}'.format(price), '{:12.8f}'.format(valuebtc),  terminal.yellow('{:8.2f}'.format(valuebtc * eur)))
            expasset = { "Exchange": market, "Symbol": symbol, "Amount": '{:.8f}'.format(amount), "Price": '{:.10f}'.format(price) }
            export['Wallet'].append(expasset)
            sumbtc += valuebtc
    print(terminal.cyan('Total asset value in BTC:          '), end='')
    print(terminal.cyan(terminal.bold('{:14.8f}'.format(sumbtc))))
    print(terminal.magenta('Total asset value in EUR:          '), end='')
    print(terminal.magenta(terminal.bold('{:8.2f}'.format(sumbtc * eur))))
    return(sumbtc)


totalassetsbtc += getAssets('BitTrex', balancebittrex, exchbittrex)
totalassetsbtc += getAssets('Binance', balancebinance, exchbinance)
totalassetsbtc += getAssets('Binance Bot', balancebinbot, exchbinbot)
totalassetsbtc += getAssets('KuCoin', balancekucoin, exchkucoin)
totalassetsbtc += getAssets('HuobiPro', balancehuobi, exchhuobi)

print()
print(terminal.yellow('Total asset value in BTC: '), end='')
print(terminal.yellow(terminal.bold('{:14.8f}'.format(totalassetsbtc))))
print(terminal.yellow('Total asset value in EUR: '), end='')
print(terminal.yellow(terminal.bold('{:8.2f}'.format(totalassetsbtc * eur))))

export["TotalBTC"] = '{:.8f}'.format(totalassetsbtc)
export["TotalEUR"] = '{:.2f}'.format(totalassetsbtc * eur)

headers = {'content-type': 'application/json'}
resp = requests.post('https://yourdomain.com/somefolder/process-json.php', data=dict(payload=json.dumps(export)))
print(resp)
