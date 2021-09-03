import spacy
from PorterStemmer import PorterStemmer
from stopwords import Stopwords

def replaceStopWords(text):

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

            nlp = spacy.load('en_core_web_trf')
            doc = nlp(seg)
            doc = [tok.text for tok in doc]

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

            nlp = spacy.load('en_core_web_trf')
            doc = nlp(seg)
            doc = [tok.text for tok in doc]

            stemmer = PorterStemmer()

            for tok in doc:
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
    if (text in Stopwords.CLOSED_CLASS_WORDS or text in Stopwords.FREQUENT_WORDS
        or text in Stopwords.suffixes):
        return True

    return False
