from .bucket import Bucket


class Buckets:
    API_Buckets = {}

    @classmethod
    def Get_Buckets(cls, Name, rates):
        if Name in cls.API_Buckets:
            return cls.API_Buckets[Name]
        API = []
        for tokens, resetTime in rates:
            API.append(Bucket(tokens, resetTime))
        cls.API_Buckets[Name] = API
        return cls.API_Buckets[Name]

    @classmethod
    def reduce(cls, Name, TokenAmount=1):
        assert (Name in cls.API_Buckets), \
            "{} doesn't exist, create it with Get_Buckets".format(Name)

        def reduceAll(bucket): return bucket.reduce(TokenAmount)
        ReduceResult = False in list(map(reduceAll, cls.API_Buckets[Name]))
        return not ReduceResult

    @classmethod
    def nextRefill(cls, Name):
        refill_time = 0
        assert (Name in cls.API_Buckets), \
            "{} doesn't exist, create it with Get_Buckets".format(Name)
        for bucket in cls.API_Buckets[Name]:
            if bucket.get() == 0:
                refill_time = max(refill_time, bucket.next_refill())
        return refill_time
