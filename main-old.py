import tradier, json, asyncio
import numpy as np
import matplotlib.pyplot as plt
import threading
from collections import deque
import matplotlib.animation as animation
from datetime import datetime

# {
#     "symbol":"",
#     "mv": 100,
#     "position": (0,0)
# }

##### websocket
resp = tradier.create_streaming_session()
session_id = resp['stream']['sessionid']

params = {
    "symbols": ["SPY220222C00436000"],
    "sessionid": session_id,
    "linebreak": True
}

queue = []
queue_avg = []
times = []
interval = 0

def trunc(x, decimals):
    return int(x * 10**decimals) / 10**decimals

def on_msg(msg):
    global queue
    global interval
    print(msg)
    if msg['type'] == 'quote':
        queue_cap = 2460 # cap 164 ~= 60 seconds. 2460
        window_size = 100

        mid = (msg['bid'] + msg['ask']) / 2
        now = datetime.now()
        queue.append(mid)
        window = queue[-window_size:]
        queue_avg.append(np.mean(window))
        times.append(now)

        
        if len(queue) > queue_cap:
            queue.pop(0)
        if len(queue_avg) > queue_cap:
            queue_avg.pop(0)
        if len(times) > queue_cap:
            times.pop(0)
        
        interval = (interval + 1) % 5
        if interval == 0:
            print("===")
            print('mean:', trunc(np.mean(window), 2), ', std:', trunc(np.std(window), 2))
            print('low:', trunc(np.min(window), 2), ', high:', trunc(np.max(window), 2))
            print('bid:', trunc(msg['bid'], 2), ', ask:', trunc(msg['ask'], 2))
        
def run_ws():
    asyncio.run(tradier.ws_connect(params, on_msg=on_msg))

t = threading.Thread(target=run_ws)
t.start()

##### plots

def animate(i):
    global queue
    global times
    ax.relim()
    ax.autoscale_view()
    line.set_data(times, queue)
    line2.set_data(times, queue_avg)

# fig, ax = plt.subplots((2,2))

# ax[0, 0].yaxis.tick_right()
# ax[0, 0].set_title(params['symbols'][0])
# line_0_0 = ax[0, 0].plot(times, queue, c='black')

fig, ax = plt.subplots()
ax.yaxis.tick_right()
line, = plt.plot(times, queue, c='black')
line2, = plt.plot(times, queue_avg, c='red')

ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()
