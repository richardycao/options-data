


UPDATE_INTERVAL = 3000 # how often the graphs update, in milliseconds

PROD_ACCESS_TOKEN = ''

##################### Don't change anything below here #########################

realm = 'prod'

PROD_URL = 'https://api.tradier.com'
SANDBOX_URL = 'https://sandbox.tradier.com'

ACCOUNT_ID = ''
ACCESS_TOKEN = ''
BASE_URL = ''
if realm == 'prod':
    ACCOUNT_ID = PROD_ACCOUNT_ID
    ACCESS_TOKEN = PROD_ACCESS_TOKEN
    BASE_URL = PROD_URL
if realm == 'sandbox':
    ACCOUNT_ID = SANDBOX_ACCOUNT_ID
    ACCESS_TOKEN = SANDBOX_ACCESS_TOKEN
    BASE_URL = SANDBOX_URL

HEADERS = {'Authorization': f'Bearer {ACCESS_TOKEN} ', 'Accept': 'application/json'}
