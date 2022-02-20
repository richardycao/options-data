import tradier, asyncio
import numpy as np
import matplotlib.pyplot as plt
import threading
import matplotlib.animation as animation
from datetime import datetime
import time
import sys

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
                'data': [],
                'avg': [],
                'times': []
            } for symbol in self.params['symbols']
        }

        # Data collection
        self.queue_capacity = 2460
        self.window_size = 100
        self.log_interval = 5
        self.log_i = 0

        # Plot
        self.fig, self.axs = plt.subplots(len(self.params['symbols']))
        for i, symbol in enumerate(self.params['symbols']):
            self.axs[i].yaxis.tick_right()
            self.axs[i].title.set_text(symbol)
        self.lines = {
            symbol: {
                'data': self.axs[i].plot(self.queues[symbol]['times'], self.queues[symbol]['data'], c='black'),
                'avg': self.axs[i].plot(self.queues[symbol]['times'], self.queues[symbol]['avg'], c='red')
            } for i, symbol in enumerate(self.params['symbols'])
        }
        self.mock_vals = [np.random.normal(0,10) for _ in self.params['symbols']]
    
    def trunc(self, x, decimals):
        return int(x * 10**decimals) / 10**decimals

    def update_queue(self, msg):
        symbol = msg['symbol']
        mid = (msg['bid'] + msg['ask']) / 2
        window = self.queues[symbol]['data'][-self.window_size:]
        now = datetime.now()

        self.queues[symbol]['data'].append(mid)
        self.queues[symbol]['avg'].append(np.mean(window))
        self.queues[symbol]['times'].append(now)

        if len(self.queues[symbol]['data']) > self.queue_capacity:
            self.queues[symbol]['data'].pop(0)
            self.queues[symbol]['avg'].pop(0)
            self.queues[symbol]['times'].pop(0)
        
    def log_stats(self, msg):
        symbol = msg['symbol']
        window = self.queues[symbol]['data'][-self.window_size:]

        print("===")
        print('mean:', self.trunc(np.mean(window), 2), ', std:', self.trunc(np.std(window), 2))
        print('low:', self.trunc(np.min(window), 2), ', high:', self.trunc(np.max(window), 2))
        print('bid:', self.trunc(msg['bid'], 2), ', ask:', self.trunc(msg['ask'], 2))

    def on_msg(self, msg):
        if msg['type'] == 'quote':
            self.update_queue(msg)
            
            # self.log_i = (self.log_i + 1) % self.log_interval
            # if self.log_i == 0:
            #     self.log_stats(msg)

    def run_ws(self):
        asyncio.run(tradier.ws_connect(self.params, on_msg=self.on_msg))

    def mock_ws(self):
        for i in range(1000):
            for j in range(len(self.mock_vals)):
                self.mock_vals[j] += np.random.normal(0, 1)
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

    def run(self):
        t = threading.Thread(target=self.run_ws if self.mode == 'live' else self.mock_ws)
        t.start()

        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()

def main(symbols, mode):
    th = TradeHelper(symbols, mode=mode)
    th.run()

if __name__ == "__main__":
    args = sys.argv
    mode = args[0]
    symbols = args[1:]
    main(symbols, mode)
