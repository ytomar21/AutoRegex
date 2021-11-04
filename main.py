# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import csv

from extractPhrases import ExtractPhrase
from util import elimStopWords, replaceStopWords, tokenizeText, frequentToken
from EquivalenceClass import GenerateEquivalenceClass

#import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet

def main():
    # Initialize word net library, pos tagger, parser for graph generation

    # Step 1: Get Rubric Text and Top Scorer Text
    with open('Data/Data Set #1--ReadMeFirst.txt', newline='', encoding="latin-1") as rubricFile:
        #rubricReader = csv.reader(rubricFile)
        rubricSegments = [row for row in rubricFile]

    print(f'rubricSegments: {rubricSegments}')

    with open('Data/topscorers.csv', newline='') as topScorerFile:
        topScorerReader = csv.reader(topScorerFile)
        topScorerSegments = [row[0] for row in topScorerReader]

    #print(f'topScorerSegment: {topScorerSegment}')

    # Step 2: Extract Long Phrases from the Text (Generate edges for word order graph)
    phraseExtractor = ExtractPhrase(rubricSegments)
    rubricPhrases = phraseExtractor.extractPhrasesFromText()

    print("Rubric Segments: ", rubricSegments)
    print("Rubric Phrases: ", rubricPhrases)

    # Step 3: Eliminate Stop-Words
    rubricSegments = elimStopWords(rubricSegments)
    #topScorerSegment = elimStopWords(topScorerSegments)
    rubricPhrases = replaceStopWords(rubricPhrases)

    print("Rubric Segments: ", rubricSegments)
    print("Rubric Phrases: ", rubricPhrases)

    # Step 4: Tokenize Rubric and Top-Scorer Text
    rubricTok = tokenizeText(rubricSegments)
    topScorerTok = tokenizeText(topScorerSegments)

    # Step 5: Select Most Frequent Words Among the Top-Scorer Text and Prompt Texts' Token
    #frquencyMap = frequentToken(topScorerTok)
    topScoringTokens = frequentToken(topScorerTok)

    # Step 6: Identify equivalence classes for the tokens in the rubric text
    equivalenceClassGen = GenerateEquivalenceClass()
    finalListOfTokenClasses = []
    for tokens in rubricTok:
        finalListOfTokenClasses = equivalenceClassGen.identifyClassOfWords(tokens, topScoringTokens, finalListOfTokenClasses)
    print("equivalence class generated")

    #Step 7: Write out results and convert into Perl regex format
    with open("output.txt", 'w') as csvfile:
        #csvwriter = csv.writer(csvfile)
        for phrase in finalListOfTokenClasses:
            csvfile.write(phrase + "\n")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
