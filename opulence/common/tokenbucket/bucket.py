import time


class Bucket(object):
    def __init__(self, maxToken, resetTime):
        self.rate = str(maxToken) + "/" + str(resetTime)
        self.MaxToken = maxToken
        self.resetTime = resetTime
        self.reset()
        self.info()

    def info(self):
        print('Rate: {}, amount {}, Maxtoken: {}, resetTime: {}'.format(
            self.rate, self.amount, self.MaxToken, self.resetTime))

    def reset(self):
        self.amount = self.MaxToken
        self.lastUpdate = time.time()

    def _refill_count(self):
        return int(((time.time() - self.lastUpdate) / self.resetTime))

    def get(self):
        return min(
          self.MaxToken,
          self.amount + self._refill_count() * self.MaxToken)

    def next_refill(self):
        return self.resetTime + self.lastUpdate - time.time()

    def reduce(self, tokens):
        refill_count = self._refill_count()
        self.amount += refill_count * self.MaxToken
        self.lastUpdate += refill_count * self.resetTime

        if self.amount >= self.MaxToken:
            self.reset()
        if tokens > self.amount:
            return False

        self.amount -= tokens
        return True
