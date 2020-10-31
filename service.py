import attr
import time
from twisted.internet import protocol
import datetime
import json

@attr.s(auto_attribs=True)
class Stats:
    _launched: datetime.datetime = attr.ib(factory=datetime.datetime.now)
    _requests: int = attr.ib(init=False, default=0)

    def get(self):
        return dict(launched=self._launched.isoformat(), requests=self._requests)

    def ding(self):
        self._requests += 1


@attr.s(auto_attribs=True)
class DayTimeCounterFactory(protocol.ServerFactory):
    _stats: Stats

    def buildProtocol(self, addr):
        self._stats.ding()
        ret_value = Daytime()
        ret_value.factory = self
        return ret_value
    

class StatsLine(protocol.Protocol):
    def connectionMade(self):
        data =json.dumps(self.factory.stats.get()).encode("ascii") + b"\n"
        self.transport.write(data)
        self.transport.loseConnection()

class Daytime(protocol.Protocol):

    def connectionMade(self):
        self.transport.write(time.asctime(time.gmtime(time.time())).encode("ascii") + b'\r\n')
        self.transport.loseConnection()



def main():
    from twisted.internet import reactor
    stats = Stats()
    f = protocol.ServerFactory()
    f.stats = stats
    f.protocol = StatsLine
    reactor.listenTCP(1111, f)
    c = DayTimeCounterFactory(stats)
    reactor.listenTCP(1113, c)
    reactor.run()

if __name__ == '__main__':
    main()
