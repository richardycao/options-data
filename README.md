# options-data

Shows real-time graphs and stats for options data.

![image](https://user-images.githubusercontent.com/56094002/154863664-203508a2-37f2-4342-921f-e2b023583c73.png)

## How to use:

### Getting API Access (only need to do this once)

1. Go to Tradier's website (https://brokerage.tradier.com/) and create a free account.

2. Once your account has been created and approved, go the home page (https://dash.tradier.com/account/<your account id>).

3. Click on the your profile dropdown in the top-right corner and click "API Access". 

4. Scroll down to the "Brokerage Account Access" and create an acccess token. Don't share this token with anyone. 

### Setting up dependencies for macOS (only need to do this once)

1. Open the terminal.

2. Install homebrew: Go to https://brew.sh/ and copy this command `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. Run the command in the terminal.

3. Install python: Run `brew install python`.

4. Download this code: Run `git clone https://github.com/richardycao/options-data.git`.

5. Change direction: `cd options-data`.

6. Create personal config: Run `cp config-example.py config.py`.

7. Set access token: Open `config.py` in a text editor and paste your access token for `PROD_ACCESS_TOKEN`. This is the access token that was created on Tradier above.

8. Run `python3 -m pip install requirements.txt` to install required python libraries.

### Using the tool

To start the tool, run `python3 main.py <mode> <space-separated symbols>` in the terminal.

To stop the tool, right-click on the python graph icon (looks like a rocket) at the bottom of the screen and click "Quit".

`<mode>` can be `mock` or `live`. `mock` is for fake data. `live` is for real data.

Example: `python3 main.py mock SPY220222C00435000 SPY220222P00435000`. This will start the tool in `mock` mode, and will have graphs for two options. The black line is the average of bid and ask. The red line is the moving average.

Example: `python3 main.py live SPY220222C00435000 SPY220222P00435000`. This will only show data when the market is open.
