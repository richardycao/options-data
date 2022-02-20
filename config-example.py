
env = 'prod' # sandbox or prod

UPDATE_INTERVAL = 3000 # how often the graphs update, in milliseconds
GRAPH_CAPACITY = 1500 # number of most recent data points to show on the graph
MA_WINDOW_SIZE = 100 # how wide is the moving average
STATS_WINDOW_SIZE = 100 # number of most recent data points to show stats for

PROD_ACCOUNT_ID = ''
PROD_ACCESS_TOKEN = ''
SANDBOX_ACCOUNT_ID = ''
SANDBOX_ACCESS_TOKEN = ''

##################### Don't change anything below here #########################

PROD_URL = 'https://api.tradier.com'
SANDBOX_URL = 'https://sandbox.tradier.com'

ACCOUNT_ID = ''
ACCESS_TOKEN = ''
BASE_URL = ''
if env == 'prod':
    ACCOUNT_ID = PROD_ACCOUNT_ID
    ACCESS_TOKEN = PROD_ACCESS_TOKEN
    BASE_URL = PROD_URL
if env == 'sandbox':
    ACCOUNT_ID = SANDBOX_ACCOUNT_ID
    ACCESS_TOKEN = SANDBOX_ACCESS_TOKEN
    BASE_URL = SANDBOX_URL

HEADERS = {'Authorization': f'Bearer {ACCESS_TOKEN} ', 'Accept': 'application/json'}
