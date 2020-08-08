_register = {}


def singleton(cls):
    def wrapper(*args, **kw):
        if cls not in _register:
            instance = cls(*args, **kw)
            _register[cls] = instance
        return _register[cls]

    wrapper.__name__ = cls.__name__
    return wrapper


@singleton
class ChannelSingleton:
    channelsMap = {}

    def getChannelId(self, channel_name):
        return self.channelsMap[channel_name]

    def createMap(self, channel_list):
        for channel in channel_list:
            self.channelsMap[channel["name"]] = channel["id"]
