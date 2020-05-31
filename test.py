# -*- coding: UTF-8 -*-

import random
from basic import TermFrequency, Dictionary, Sentence
from reader import HistoryReader
from model import SequenceToSequenceModel

tokenList = "let's have a nice day."

dictionary = Dictionary(tokenList, maxSize = 10)
print(dictionary.size)
print(dictionary.mapping)
print(dictionary.convertTokenToGram("a"))

sentence = Sentence()
sentence.addGram(Dictionary.BOS)
for token in tokenList:
    sentence.addGram(dictionary.convertTokenToGram(token))
sentence.addGram(Dictionary.EOS)
print(sentence.length())
print(sentence)

historyReader = HistoryReader("./history.txt")
dictionary = historyReader.readAndProcess()
for i in range(50):
    print(dictionary.convertIndexToGram(i), end = "")
print(" - " + str(dictionary.size))
print(historyReader.getNumberOfSentences())
for i in range(50):
    print(historyReader.getSentence(i))

seqToSeqModel = SequenceToSequenceModel(dictionary.size)
seqToSeqModel.kerasOverallModel.summary()

seqToSeqModel.saveWeights()
seqToSeqModel.loadWeights()

while False:
    for t in range(5):
        questionSentence = random.choice(historyReader.sentenceList)
        answerSentence = seqToSeqModel.predict(questionSentence, dictionary)
        print("Preview #{}".format(t + 1))
        print("[Q] {}".format(questionSentence))
        print("[A] {}".format(answerSentence))
    #input("Press Enter To Train 1 Round...")
    seqToSeqModel.train(historyReader.sentenceList[:-1], historyReader.sentenceList[1:])

