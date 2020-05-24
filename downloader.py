import discord
import asyncio
import json

# Channels that need to be traversed; List contains tuples: (CHANNEL_ID, LIMIT_OF_MESSAGES)
CHANNELS = [(00000000000000, 100000)]      # EXAMPLE

# Bot auth token string:
AUTH_TOKEN = ''


class MessageQueue:
    """
    This class temporalily stores last n messages,
    so that they can be processed.
    """
    def __init__(self, size: int = 7):
        self.queue = []
        self.size = size
    
    def push(self, msg: discord.Message) -> None:
        """Insert new message into queue"""
        if len(self.queue) == self.size: # If queue is full pop elem 0
            self.queue.pop(0)
        self.queue.append(msg)
    
    def get_neighbors(self) -> ("author", list):
        """
        Get a list of neighbors of the middle message;
        return author_id of the middle message + list.
        """
        if len(self.queue) != self.size:
            return (None, [])
        qcopy = self.queue.copy()
        author = qcopy[self.size // 2].author
        qcopy.pop(self.size // 2)
        return (author, qcopy)


class Results:
    """This class stores the results of traversal."""
    def __init__(self):
        self.message_data = {}
        self.username_data = {}

    def update_results(self, author_id: int, neighbor_id: int) -> None:
        if author_id == neighbor_id:
            return
        if not author_id in self.message_data:
            self.message_data[author_id] = {}
        sub_tree = self.message_data[author_id]
        if not neighbor_id in sub_tree:
            sub_tree[neighbor_id] = 0
        sub_tree[neighbor_id] += 1

    def update_username(self, user_id: int, username: str) -> None:
        if not user_id in self.username_data:
            self.username_data[user_id] = username

    def json(self) -> None:
        results = {}
        results["message_data"] = self.message_data
        results["username_data"] = self.username_data
        with open('result.json', 'w') as fp:
            json.dump(results, fp)
            

class MyClient(discord.Client):

    async def on_ready(self):
        print('Beginning download...')
        await self.collect_data()
        print('Finished.')

    async def download_channel(self, results: Results, channel: discord.TextChannel, limit: int, queue_size: int = 7):
        print("Beginning download of: {}".format(channel.name))
        queue = MessageQueue(queue_size)  # Message queue

        current_iteration = 0
        async for message in channel.history(limit=limit):
            queue.push(message)
            (author, neighbors) = queue.get_neighbors()
            if author:
                results.update_username(author.id, author.name)
            for n in neighbors:
                results.update_results(author.id, n.author.id)
                results.update_username(n.author.id, n.author.name)

            current_iteration += 1
            if (current_iteration % 10000) == 0:
                print("{}/{}".format(current_iteration, limit))

    
    async def collect_data(self):
        print("Downloading...")
        results = Results()
        channels_cls = []

        for (channel_id, limit) in CHANNELS:
            channel: discord.TextChannel = self.get_channel(channel_id)
            if channel:
                channels_cls.append((channel, limit))
            else:
                print("Channel {} not found! Skipping.".format(channel_id))

        for (channel, limit) in channels_cls:
            await self.download_channel(results, channel, limit)

        print("Download completed. Dumping data into JSON file.")
        results.json()


client = MyClient()
client.run(AUTH_TOKEN)