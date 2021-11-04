from nltk.corpus import wordnet as wn
import spacy

class WordnetBasedSimilarity:

    def __init__(self):
        self.NOMATCH = 0
        self.OVERLAPEXAM = 1
        self.OVERLAPDEFIN = 1
        self.COMMONPARENTS = 2
        self.MERONYM = 3
        self.HOLONYM = 3
        self.HYPONYM = 4
        self.HYPERNYM = 4
        self.SYNONYM = 5
        self.EXACT = 6

    def compareString(self, word1, word2, nlp):
        review = word1
        submission = word2
        print("compareString")

        revTok = nlp(review)
        print(f"revTok: {revTok[0].pos_}")
        posRev = revTok[0].pos_
        print(f"revPos: {posRev}")

        reviewPos = self.determinePos(posRev)

        if review == "n't":
            review = "not"

        subTok = nlp(review)
        print(f"subTok: {subTok[0].pos_}")
        subRev = subTok[0].pos_
        print(f"subPos: {subRev}")

        subPos = self.determinePos(posRev)

        if subPos == -1 or reviewPos == -1:
            return -1

        print(f"review:{review}")
        print(f"reviewPos: {reviewPos}")
        print(f"submission: {submission}")
        try:
            revSynset = wn.synset(review+"."+reviewPos+".01")
        except:
            return 0

        try:
            subSynset = wn.synset(submission+"."+subPos+".01")
        except:
            return 0
        print(f"revSynset: {revSynset}")

        print(f"Lch similarity: {wn.lch_similarity(revSynset, subSynset, simulate_root=False)}")
        print(f"Wup similarity: {wn.wup_similarity(revSynset, subSynset)}")
        print(f"Path similarity: {wn.path_similarity(revSynset, subSynset)}")


        match = 0
        count = 0

        #print(wn.synsets("cat"))
        return match

    def determinePos(self, str_pos):
        pos = ""
        if "NOUN" in str_pos or "CD" in str_pos or "NN" in str_pos or "PR" in str_pos or "IN" in str_pos or "EX" in str_pos or "WP" in str_pos:
            pos = "n"
        elif "JJ" in str_pos:
            pos = "a"
        elif "TO" in str_pos or "VB" in str_pos or "MD" in str_pos:
            pos = "v"
        elif "RB" in str_pos:
            pos = "r"
        elif "DET" in str_pos:
            pos = -1
        else:
            pos = "n"

        return pos
