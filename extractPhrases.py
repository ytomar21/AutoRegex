from graphGenerator import GraphGenerator


class ExtractPhrase:

    def __init__(self, text):
        self.phrases = None
        self.text = text

    def extractPhrasesFromText(self):
        #print(f'ExtractPhrasesFromText: {self.text}')

        #Constructing the word order graph
        graphGen = GraphGenerator()
        graphGen.generateGraph(self.text)

        rubricPhrases = []

        for edge in graphGen.edges:
            if edge != None:
                rubricPhrases.append(edge.inVertex.name + " " + edge.outVertex.name)
                print(f"Edge: {[edge.inVertex.name, edge.outVertex.name, edge.name, edge.label]}")

        print(f'Num of Phrases: {len(rubricPhrases)}')

        return rubricPhrases