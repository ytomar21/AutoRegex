import spacy
from PorterStemmer import PorterStemmer
from stopwords import Stopwords

def replaceStopWords(text):

    print("replaceStopWords()")

    outList = []
    for seg in text:
        stemmedDoc = ""
        if seg != None:
            seg = seg.replace(";", "")
            seg = seg.replace(",", "")
            seg = seg.replace(":", "")
            seg = seg.replace("\"", "")
            seg = seg.replace("\\.", " ")
            seg = seg.replace("\\/", " ")
            seg = seg.replace("\\:", " ")
            seg = seg.replace("[?()]", "")
            seg = seg.replace("!", "")
            seg = seg.replace("[(]", "")
            seg = seg.replace("[)]", "")

            seg.strip()
            doc = seg.split()

            stemmer = PorterStemmer()

            for tok in doc:
                temp = stemmer.stem(tok)

                if isStopWordOrFrequentWord(temp) and stemmedDoc != "":
                    stemmedDoc += "(\\\\w{0-4}\\\\s) "
                else:
                    stemmedDoc += temp + " "

        j = 1
        #print(stemmedDoc)
        #Why does Lakshmi only loop 11 times?
        while (j < 11):
            if "(\\\\w{0-4}\\\\s) (\\\\w{0-4}\\\\s)" in stemmedDoc:
                stemmedDoc = stemmedDoc.replace("(\\\\w{0-4}\\\\s) (\\\\w{0-4}\\\\s)", "(\\\\w{0-4}\\\\s)");
            else:
                break

            j += 1

        repString = "(\\\\w{0-4}\\\\s){0-" + str(j) + "}"
        stemmedDoc = stemmedDoc.replace("(\\\\w{0-4}\\\\s)", repString) # num of stopwords
        stemmedDoc = stemmedDoc.strip();

        if stemmedDoc != "" or stemmedDoc == "(\\\\w{0-4}\\\\s){0-" + j + "}":
            outList.append(stemmedDoc)

    return outList

def elimStopWords(text):

    print("elimStopWords()")
    outList = []
    nlp = spacy.load('en_core_web_trf')
    print(f'nlp: {nlp}')

    for seg in text:
        print(f"seg: {seg}")
        stemmedDoc = ""
        if seg != None:
            seg = seg.replace(";", "")
            seg = seg.replace(",", "")
            seg = seg.replace(":", "")
            seg = seg.replace("\"", "")
            seg = seg.replace("\\.", " ")
            seg = seg.replace("\\/", " ")
            seg = seg.replace("\\:", " ")
            seg = seg.replace("[?()]", "")
            seg = seg.replace("!", "")
            seg = seg.replace("[(]", "")
            seg = seg.replace("[)]", "")

            seg.strip()
            doc = seg.split()
            print(f'doc: {doc}')

            stemmer = PorterStemmer()
            print("stemmer")

            for tok in doc:
                print(f"tok: {tok}")
                temp = stemmer.stem(tok)

                if (not isStopWordOrFrequentWord(temp)):
                    stemmedDoc += temp + " "


        j = 1
        #print(stemmedDoc)
        #Why does Lakshmi only loop 11 times?
        while (j < 11):
            if "(\\\\w{0-4}\\\\s) (\\\\w{0-4}\\\\s)" in stemmedDoc:
                stemmedDoc = stemmedDoc.replace("(\\\\w{0-4}\\\\s) (\\\\w{0-4}\\\\s)", "(\\\\w{0-4}\\\\s)");
            else:
                break

            j += 1

        repString = "(\\\\w{0-4}\\\\s){0-" + str(j) + "}"
        stemmedDoc = stemmedDoc.replace("(\\\\w{0-4}\\\\s)", repString) # num of stopwords
        stemmedDoc = stemmedDoc.strip()

        if stemmedDoc != "" or stemmedDoc == "(\\\\w{0-4}\\\\s){0-" + str(j) + "}":
            outList.append(stemmedDoc)

    return outList

def isStopWordOrFrequentWord(text):
    print("isStopWordOrFrequentWord()")
    if (text in Stopwords.CLOSED_CLASS_WORDS or text in Stopwords.FREQUENT_WORDS
        or text in Stopwords.suffixes):
        return True

    return False

def tokenizeText(text):
    print("tokenize()")
    #nlp = spacy.load('en_core_web_trf')
    tokText = []

    for seg in text:
        seg.strip()
        doc = seg.split()

        tokText.append(doc)

    return tokText

def frequentToken(text):
    print("frequentToken()")
    tokenMap = {}
    freqToken = []

    for tok in text:
        if(tokenMap.get(tok) != None):
            #print("HI")
            tokenMap[tok] += 1
            #print("hi 2")
        else:
            #print("Bye")
            tokenMap[tok] = 1
            #print("bye 2")

    tokenMap = dict(sorted(tokenMap.items(), key=lambda x: -x[1]))
    avgCount = sum(tokenMap.values())/len(tokenMap)

    for tok in tokenMap:
        if tokenMap[tok] >= avgCount:
            freqToken.append(tok)

    return freqToken

