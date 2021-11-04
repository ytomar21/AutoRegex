from WordnetBasedSimilarity import WordnetBasedSimilarity
import spacy
from PorterStemmer import PorterStemmer
from util import tokenizeText

class GenerateEquivalenceClass:

    def __init__(self):
        self.treshold = .8
        self.wn = WordnetBasedSimilarity()
        self.nlp = spacy.load('en_core_web_sm')

    #def identifyClassOfWords(self, rubricTokens, topScoringTokens):
    def identifyClassOfWords(self, rubricTokens, topScoringTokens, finalListOfTokenClasses):
        tokenClass = []
        wn = WordnetBasedSimilarity()
        sizes = 0
        stemmer = PorterStemmer()

        for rubric in rubricTokens:
            tempToken = rubric
            stemText = stemmer.stem(tempToken)

            classOfWords = self.getClassOfWords(stemText, topScoringTokens)

            if not classOfWords in tokenClass:
                tokenClass.append(classOfWords)
                #print("tokenClass: ", tokenClass)

        concatListOfTok = ""
        grams = 0

        for tokClass in tokenClass:
            #print("tokClass: ", tokenClass)
            if not tokClass in finalListOfTokenClasses:
                if len(tokClass) > 1:
                    finalListOfTokenClasses.append(tokClass)
                if grams < 5:
                    concatListOfTok += " @@ " + tokClass
                    grams += 1
                elif grams == 5:
                    if not concatListOfTok.strip() in finalListOfTokenClasses:
                        finalListOfTokenClasses.append(concatListOfTok.strip())

                    grams = 0
                    concatListOfTok = ""

        return finalListOfTokenClasses

    def identifyClassOfPhrases(self, rubricPhrase, topScoringTokens, posTagger):
        wn = WordnetBasedSimilarity()
        outputPhrase = ""
        tokText = tokenizeText(rubricPhrase)
        stemmer = PorterStemmer()

        for tok in tokText:

            if not "(\\\\w{0-4}\\\\s)" in tok:
                tempToken = tok
                stemTok = stemmer.stem(tempToken)

                tokClass = self.getClassOfWords(stemTok, topScoringTokens)

                if len(tokClass) > 0:
                    outputPhrase += " " + tokClass
            else:
                outputPhrase += " " + tok

        return outputPhrase.strip()

    def getClassOfWords(self, token, topscorers):
        tokenClass = []

        if token.strip() == "$$$":
            tokenClass.append("$$$")
            return tokenClass

        #print("token: ", token)
        #print("topscorers: ", topscorers)
        tokenClass = token
        #print("updated tokenClass: ", tokenClass)
        wn = WordnetBasedSimilarity()
        s = PorterStemmer()
        #tokenSyns = [] - doesn't even use synonyms

        for token in topscorers:
            if token != None:
                sttop = tokenizeText(token)

                for tok in sttop:
                    match = wn.compareString(token, tok, self.nlp)

                    if match >= self.treshold:
                        stemText = s.stem(tok)
                        #print("stemText: ", stemText)

                        if not (stemText in tokenClass):
                            tokenClass += " " + stemText

        #print("tokenClass: ", tokenClass)
        return tokenClass

