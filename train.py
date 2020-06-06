# -*- coding: UTF-8 -*-

import random
from reader import HistoryReader
from model import SequenceToSequenceModel

historyReader = HistoryReader("./history.txt")
dictionary = historyReader.readAndProcess()

seqToSeqModel = SequenceToSequenceModel(dictionary.size)

while True:

    for previewIdx in range(5):
        sentence = random.choice(historyReader.sentenceList)
        response = seqToSeqModel.predict(sentence, dictionary)
        print("\nPreview #{}".format(previewIdx + 1))
        print("[Sample Sentence] {}".format(sentence))
        print("[Sample Response] {}\n".format(response))

    input("Press any key to train one more epoch, or CTRL-C to stop...")

    seqToSeqModel.train(historyReader.sentenceList[:-1], historyReader.sentenceList[1:])
    seqToSeqModel.saveWeights()

