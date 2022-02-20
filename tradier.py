# References: 
# intro: https://www.youtube.com/watch?v=jLwBnhabVdU

import config, requests, json
import websockets

def create_streaming_session():
    response = requests.post(f'{config.BASE_URL}/v1/markets/events/session',
        data = {},
        headers = config.HEADERS)

    json_response = response.json()
    return json_response

def get_option_chain(params):
    response = requests.post(f'{config.BASE_URL}/v1/markets/options/chains',
        params = params,
        headers = config.HEADERS)

    json_response = response.json()
    return json_response

async def ws_connect(params, on_msg):
    uri = "wss://ws.tradier.com/v1/markets/events"
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = json.dumps(params)
        await websocket.send(payload)

        print(f">>> {payload}")

        async for msg in websocket:
            msg = json.loads(msg)
            on_msg(msg)
