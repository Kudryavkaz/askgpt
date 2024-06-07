import os
import time
from queue import Queue
from client.config import Config
from openai import OpenAI


class Client(object):
    def __init__(self):
        self.home = os.getenv("HOME")
        self.currentTime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

        self.output = self.home + "/.ag_history/"
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        self.history = self.output + self.currentTime + ".md"
        self.user = os.getenv("USER")
        self.display_user = "\033[0;34m" + self.user + "\033[0m"
        # get config from ~/.ag.yaml
        self.Config = Config(self.home + "/.ag.yaml")
        self.client = OpenAI(
            api_key=self.Config.api_key,
            base_url=self.Config.base_url
        )
        self.display_model = "\033[0;32m" + self.Config.model + "\033[0m"

        self.context = Queue(maxsize=self.Config.max_context_size)

    def put(self, msg):
        if self.context.full():
            self.context.get()
        self.context.put(msg)

    def get_context(self):
        return self.context.queue
