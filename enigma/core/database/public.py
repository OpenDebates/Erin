import urllib.parse

from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient(AsyncIOMotorClient):
    def __init__(self, config, logger, bot=None, *args, **kwargs):
        # Internal
        self.conn = None
        self.logger = logger

        # Config
        self.host = config["database"]["host"]
        self.port = config["database"]["port"]
        self.database = config["database"]["database"]
        self.username = urllib.parse.quote_plus(config["database"]["username"])
        self.password = urllib.parse.quote_plus(config["database"]["password"])
        self.replica_set = config["database"]["replica_set"]

        # URI Building
        if len(self.host) == 1:
            self.uri = f"mongodb://{self.username}:{self.password}" \
                       f"@{self.host[0]}:{self.port}"
            super(MongoClient, self).__init__(self.uri, *args, **kwargs)
        elif len(self.host) > 1:
            host_list = []
            for replica_host in self.host:
                host = f"mongodb://{self.username}:{self.password}"\
                                     f"@{replica_host}"
                host_list.append(host)

            super(MongoClient, self).__init__(
                host_list, replicaSet=f"{self.replica_set}", *args, **kwargs
            )
