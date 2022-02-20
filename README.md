# options-data

Shows real-time graphs and stats for options data.

## How to use:

### Getting API Access (only need to do this once)

1. Go to Tradier's website (https://brokerage.tradier.com/) and create a free account.

2. Once your account has been created and approved, go the home page (https://dash.tradier.com/account/<your account id>).

3. Click on the your profile dropdown in the top-right corner and click "API Access". 

4. Scroll down to the "Brokerage Account Access" and create an acccess token. Don't share this token with anyone. 

### Setting up dependencies for macOS (only need to do this once)

1. Open the terminal.

2. Go to https://brew.sh/ and copy this command `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. Run the command in the terminal to install Homebrew.

3. Run `brew install python` to install python.

4. Run `git clone https://github.com/richardycao/options-data.git` to download this code.

5. Run `cd options-data`.

6. Run `cp config-example.py config.py` to create your personal config file.

7. Open `config.py` in a text editor and paste your access token for `PROD_ACCESS_TOKEN`. This is the access token that was created on Tradier above.

8. Run `python3 -m pip install requirements.txt` to install required python libraries.

### Using the tool

To use the tool, run `python3 main.py <mode> <space-separated symbols>` in the terminal.

Example: `python3 main.py mock SPY220222C00435000 SPY220222P00435000`. This will start the tool in `mock` mode, and will have graphs for two options. The black line is the average of bid and ask. The red line is the moving average.

`<mode>` can be `mock` or `live`. `mock` is for fake data. `live` is for real data.

Example: `python3 main.py live SPY220222C00435000 SPY220222P00435000`. This won't show data when the market is closed.
