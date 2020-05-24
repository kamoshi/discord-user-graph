# Generate a graph of user interactions in a discord servers!
This uses a very naive method: checking messages near each other to generate the model.


### Requirements:
- python 3.x (3.7+ preferred)
- discord.py
- matplotlib
- networkx


## How to use
### Downloading data:
1. Fill in channel_ids and your bot auth token.
2. Run downloader.py
3. Wait for completion
4. The script should output file result.json on completion

### Creating a graph:
1. Provide a valid result.json file in the same directory
2. Run grapher.py
3. Graphs should appear on your screen
