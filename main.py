import tradier, asyncio
import numpy as np
import matplotlib.pyplot as plt
import threading
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime
import time
import sys
import config

class TradeHelper:
    def __init__(self, symbols, mode='mock'):
        self.mode = mode
        resp = tradier.create_streaming_session()
        session_id = resp['stream']['sessionid']

        self.params = {
            "symbols": symbols,
            "sessionid": session_id,
            "linebreak": True
        }
    
        self.queues = {
            symbol: {
                'last_bid': None,
                'last_ask': None,
                'data': [],
                'avg': [],
                'times': []
            } for symbol in self.params['symbols']
        }

        # Data collection
        self.queue_capacity = config.GRAPH_CAPACITY
        self.window_size = config.MA_WINDOW_SIZE

        # Plot
        num_graphs = max(len(self.params['symbols']), 2)
        self.fig, self.axs = plt.subplots(num_graphs)
        plt.subplots_adjust(
                    left=0.05, 
                    bottom=0.1,  
                    right=0.7,  
                    top=0.9,  
                    wspace=0.4,  
                    hspace=0.4)
        self.fig.set_size_inches(10, num_graphs * 2)
        self.fig.autofmt_xdate()
        self.lines = {
            symbol: {
                'data': self.axs[i].plot(self.queues[symbol]['times'], self.queues[symbol]['data'], c='black'),
                'avg': self.axs[i].plot(self.queues[symbol]['times'], self.queues[symbol]['avg'], c='red')
            } for i, symbol in enumerate(self.params['symbols'])
        }
        xfmt = mdates.DateFormatter('%H:%M:%S')
        for i, symbol in enumerate(self.params['symbols']):
            self.axs[i].yaxis.tick_right()
            self.axs[i].yaxis.set_label_coords(1.2, 1)
            self.axs[i].title.set_text(symbol)
            self.axs[i].xaxis.set_major_formatter(xfmt)
        self.mock_vals = [10 for _ in self.params['symbols']]

    def get_stats(self, symbol):
        window = self.queues[symbol]['data'][-self.window_size:]
        if len(window) == 0:
            return ""
        return f"""
        Stats for recent {config.STATS_WINDOW_SIZE} data points
        mean: {self.trunc(np.mean(window), 2)}, std: {self.trunc(np.std(window), 2)}
        low: {self.trunc(np.min(window), 2)}, high: {self.trunc(np.max(window), 2)}
        bid: {self.trunc(self.queues[symbol]['last_bid'], 2) or "-"}, ask: {self.trunc(self.queues[symbol]['last_ask'], 2) or "-"}
        """
    
    def trunc(self, x, decimals):
        return int(x * 10**decimals) / 10**decimals

    def update_queue(self, msg):
        symbol = msg['symbol']
        mid = (msg['bid'] + msg['ask']) / 2
        window = self.queues[symbol]['data'][-self.window_size:]
        now = datetime.now()

        self.queues[symbol]['last_bid'] = msg['bid']
        self.queues[symbol]['last_ask'] = msg['ask']
        self.queues[symbol]['data'].append(mid)
        self.queues[symbol]['avg'].append(np.mean(window) if len(window) > 0 else mid)
        self.queues[symbol]['times'].append(now)

        if len(self.queues[symbol]['data']) > self.queue_capacity:
            self.queues[symbol]['data'].pop(0)
            self.queues[symbol]['avg'].pop(0)
            self.queues[symbol]['times'].pop(0)

    def on_msg(self, msg):
        if msg['type'] == 'quote':
            self.update_queue(msg)

    def run_ws(self):
        asyncio.run(tradier.ws_connect(self.params, on_msg=self.on_msg))

    def mock_ws(self):
        for i in range(1000):
            for j in range(len(self.mock_vals)):
                self.mock_vals[j] += np.random.normal(0, 0.02)
            msgs = [{
                'type': 'quote',
                'symbol': symbol,
                'bid': mock_val,
                'ask': mock_val
            } for symbol, mock_val in zip(self.params['symbols'], self.mock_vals)]
            for msg in msgs:
                self.on_msg(msg)
            time.sleep(0.5)

    def animate(self, i):
        for i, symbol in enumerate(self.params['symbols']):
            self.axs[i].relim()
            self.axs[i].autoscale_view()
            self.lines[symbol]['data'][0].set_data(self.queues[symbol]['times'], self.queues[symbol]['data'])
            self.lines[symbol]['avg'][0].set_data(self.queues[symbol]['times'], self.queues[symbol]['avg'])
            self.axs[i].set_ylabel(self.get_stats(symbol), rotation=0)

    def run(self):
        t = threading.Thread(target=self.run_ws if self.mode == 'live' else self.mock_ws)
        t.start()

        ani = animation.FuncAnimation(self.fig, self.animate, interval=config.UPDATE_INTERVAL)
        plt.show()

def main(symbols, mode):
    th = TradeHelper(symbols, mode=mode)
    th.run()

if __name__ == "__main__":
    args = sys.argv[1:]
    mode = args[0]
    symbols = args[1:]
    main(symbols, mode)
