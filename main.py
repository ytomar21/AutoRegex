# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import csv

from extractPhrases import ExtractPhrase

#import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet

def main():
    # Initialize word net library, pos tagger, parser for graph generation
    #syns = wordnet.synsets("program")
    #print(syns[0].name())

    # Step 1: Get Rubric Text and Top Scorer Text
    with open('Data/rubric-data-temp.csv', newline='') as rubricFile:
        rubricReader = csv.reader(rubricFile)
        rubricSegments = [row[0] for row in rubricReader]

    #print(f'rubricSegments: {rubricSegments}')

    with open('Data/topscorers.csv', newline='') as topScorerFile:
        topScorerReader = csv.reader(topScorerFile)
        topScorerSegment = [row[0] for row in topScorerReader]

    #print(f'topScorerSegment: {topScorerSegment}')

    # Step 2: Extract Long Phrases from the Text (Generate edges for word order graph)
    phraseExtractor = ExtractPhrase(rubricSegments)
    phraseExtractor.extractPhrasesFromText()

    # Step 3: Eliminate Stop-Words

    # Step 4: Tokenize Rubric and Top-Scorer Text

    # Step 5: Select Most Frequent Words Among the Top-Scorer Text and Prompt Texts' Token

    # Step 6: Identify equivalence classes for the tokens in the rubric text

    #Step 7: Write out results and convert into Perl regex format



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
