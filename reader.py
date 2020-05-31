# -*- coding: UTF-8 -*-

import os
import string
import re
from basic import TokenType, Gram, Dictionary, Sentence

class HistoryReader():

    def __init__(self, filePath):
        self.filePath = filePath
        self.sentenceList = list()
        if not os.path.isfile(self.filePath):
            raise Exception("File \"{}\" Not Found".format(self.filePath))

    def readAndProcess(self, maxSentenceLength = 30, dictionaryToUse = None):
        messageList = list()
        with open(self.filePath, "r") as fin:
            for line in fin:
                splited = line.split("\t")
                # skip invalid lines
                if len(splited) != 3:
                    continue
                message = splited[2]
                # skip invalid content including calls, pictures and stickers
                if re.match("^☎ ", message):
                    continue
                if re.match("^\[.+\]", message):
                    continue
                # reaplce invalid symbols and combine spaces
                for punc in string.punctuation:
                    message = message.replace(punc, " ")
                message = re.sub("\s+", " ", message).strip()
                # keep the message
                messageList.append(message)
        if not messageList:
            raise Exception("No Available Messages")
        if not dictionaryToUse:
            dictionaryToUse = Dictionary("".join(messageList))
        self.sentenceList = list()
        for message in messageList:
            sentence = Sentence()
            sentence.addGram(Dictionary.BOS)
            for tokenIdx, token in enumerate(message):
                if tokenIdx >= maxSentenceLength:
                    continue
                sentence.addGram(dictionaryToUse.convertTokenToGram(token))
            if sentence.length() < maxSentenceLength:
                sentence.addGram(Dictionary.EOS)
            self.sentenceList.append(sentence)
        return dictionaryToUse

    def getNumberOfSentences(self):
        return len(self.sentenceList)

    def getSentence(self, index):
        if index >= self.getNumberOfSentences():
            raise Exception("Unexpcted Behavior")
        return self.sentenceList[index]

