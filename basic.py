from enum import Enum

class TermFrequency():

    def __init__(self, tokenList):
        self.countingMap = dict()
        self.rankingMap = dict()
        for token in tokenList:
            if token in self.countingMap:
                self.countingMap[token] += 1
            else:
                self.countingMap[token] = 1
        rankingList = sorted(self.countingMap.items(), key = lambda item: item[1], reverse = True)
        for rank, item in enumerate(rankingList):
            token = item[0]
            self.rankingMap[token] = rank

    def getTermFrequency(self, token):
        if token in self.countingMap:
            return self.countingMap[token]
        return 0

    def isTokenRecognized(self, token):
        if token in self.countingMap:
            return True
        return False

    def getTermRank(self, token):
        if not self.isTokenRecognized(token):
            raise Exception("Token \"{}\" Not Recognized".format(token))
        return self.rankingMap[token]

class TokenType(Enum):
    EOS = 0
    UNKNOWN = 1
    NONGRAMCOUNT = 2
    GRAM = 3

class Gram():

    def __init__(self, tokenType, index, token = ""):
        self.tokenType = tokenType
        self.index = index
        self.token = token

    def __repr__(self):
        if self.tokenType == TokenType.EOS:
            return "<EOS>"
        if self.tokenType == TokenType.UNKNOWN:
            return "<UNKNOWN>"
        if self.tokenType == TokenType.NONGRAMCOUNT:
            raise Exception("Unexpcted Behavior")
        return self.token

class Dictionary():

    def __init__(self, tokenList, maxSize = 5000):
        self.EOS = Gram(TokenType.EOS, TokenType.EOS)
        self.UNKNOWN = Gram(TokenType.UNKNOWN, TokenType.UNKNOWN)
        self.mapping = dict()
        termFrequency = TermFrequency(tokenList)
        for token in tokenList:
            termRank = termFrequency.getTermRank(token)
            indexToApply = termRank + TokenType.NONGRAMCOUNT.value
            if indexToApply >= maxSize:
                continue
            self.mapping[token] = Gram(TokenType.GRAM, indexToApply, token)
        self.size = len(self.mapping) + TokenType.NONGRAMCOUNT.value

    def convertTokenToGram(self, token):
        if token in self.mapping:
            return self.mapping[token]
        return self.UNKNOWN

class Sentence():

    def __init__(self):
        self.length = 0
        self.gramList = list()

