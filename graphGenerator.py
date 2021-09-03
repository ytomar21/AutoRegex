import time
import spacy
from graph import Vertex, Edge


class GraphGenerator:

    def __init__(self):
        self.WORDS = 10000
        self.NOUNS = 10000
        self.ALPHA_FREQ = 1
        self.BETA_FREQ = 10

        self.vertices = []
        self.edges = []

        self.numEdges = 0
        self.numVertices = 0
        self.numDoubleEdges = 0
        self.reviewStrLen = 0

        #POS enumeration
        self.NOUN = 1
        self.VERB = 2
        self.ADJ = 3
        self.ADV = 4

        self.POSITIVE = 0
        self.SUGGESTIVE = 1
        self.NEGATED = 2

        self.timeTaken = 0

        self.nounPhrases = 0
        self.prepPhrases = 0
        self.verbPhrases = 0
        self.progressVerbTenses = 0
        self.modalAuxPhrases = 0
        self.adjectiveCount = 0
        self.adverbialCount = 0


    #generateGraph():
    #   Input: Rubric Csv File
    #   Output: Word Order Graph
    def generateGraph(self, file):
        begin = round(time.time() * 1000)

        print("Inside generateGraph()")

        nlp = spacy.load('en_core_web_trf')

        ansCount = 0
        for ans in file:
            #Check is answer is not empty
            if ans.strip() or ans.strip() != "":
                ans = self.replaceApostrophes(ans)
                #print(f'ans: {ans}')
                doc = nlp(ans)

                # Create a POS tagger for the tokenized text
                tokenized = [tok for tok in doc]
                tagger = [tok.pos_ for tok in doc]
                labels = [tok.dep_ for tok in doc]
                parents = [tok.head for tok in doc]

                #print(f'tokenized: {tokenized}')
                #print(f'tagger: {tagger}')
                #print(f'labels: {labels}')
                #print(f'parents: {parents}')

                prevType = -1
                nouns = []
                nCount = 0
                verbs = []
                vCount = 0
                adjectives = []
                adjCount = 0
                adverbs = []
                advCount = 0

                labelCounter = 0
                parentCounter = 0

                #Loop through all tokens
                for tok in doc:
                    #print(f'Current Tok: {tok}')
                    text = tok.text
                    #If token is noun, personal pronoun, determiner, (preposition or subordinating conjunction), existential, Wh-pronoun
                    if tok.pos_ == "NOUN" or tok.pos_ == "PRON" or tok.pos_ == "PROPN" or tok.pos_ == "SCONJ":

                        nounVertex = None
                        appendedVertex = False

                        #If previous token was a noun append it to the current noun token
                        if prevType == self.NOUN:
                            self.nounPhrases += 1
                            nCount -= 1

                            prevVertex = self.searchVertices(self.vertices, nouns[nCount], ansCount)
                            #print(f'prevVertex: {prevVertex.name}')

                            nouns[nCount] = nouns[nCount] + " " + text
                            nounVertex = self.getVertex(self.vertices, nouns[nCount], ansCount)

                            if nounVertex == None:
                                #print(f'Previous noun vertex: {prevVertex.name} retrieved!')

                                prevVertex.name = prevVertex.name + " " + text
                                nounVertex = prevVertex

                                if nounVertex.label == "":
                                    nounVertex.label = labels[labelCounter]

                                if nounVertex.parent.text == "" or nounVertex.parent == None or nounVertex.parent.text.lower() == text:
                                    nounVertex.parent = parents[parentCounter]

                                if labels[labelCounter] != 'nmod' or labels[labelCounter] != "pmod":
                                    nounVertex.label = labels[labelCounter]

                                appendedVertex = True
                                #print(f'Noun Vertex: {nounVertex.name}')

                        else:
                            #Turn this piece of code into a function -- addVertex()
                            nouns.append(text)
                            nounVertex = Vertex(text, self.NOUN, ansCount, tok.dep_, tok.head, tok.pos_)
                            self.vertices.append(nounVertex)
                            #print(f'Vertex: {self.vertices[-1].name} added')
                            #print(f'Nount Vertex: {nounVertex.name}')

                            self.numVertices += 1

                        #If the previous token was an adj generate a noun-property edge linking the adj and noun
                        if prevType == self.ADJ:
                            #print(f'Previous tok is adjective!')
                            v1 = None
                            v2 = None
                            e = 0

                            if nCount >= 0:
                                if nCount == 0:
                                    v1 = self.searchVertices(self.vertices, nouns[nCount], ansCount)
                                else:
                                    v1 = self.searchVertices(self.vertices, nouns[nCount-1], ansCount)

                                v2 = self.searchVertices(self.vertices, adjectives[adjCount-1], ansCount)

                                e = self.searchEdgesToSetNull(self.edges, v1, v2, ansCount)
                                if v1 != None and v2 != None and e != -1:
                                    self.edges[e] = None

                            v1 = self.searchVertices(self.vertices, adjectives[adjCount-1], ansCount)
                            v2 = nounVertex

                            e = self.searchEdges(self.edges, v1, v2, ansCount)

                            if v1 != None and v2 != None and e == -1:
                                # Turn this piece of code into a funciton -- addEdge()
                                edge = Edge("noun-property", self.NOUN)
                                edge.inVertex = v1
                                edge.outVertex = v2
                                edge.index = ansCount
                                self.edges.append(edge)

                                #print(f'edge created!')
                                self.numEdges+=1

                        #If there has been a previous verb, and the current tok is not part of noun phrase
                        if vCount >= 1 and appendedVertex == False:
                            v1 = self.searchVertices(self.vertices, verbs[vCount-1], ansCount)
                            v2 = nounVertex
                            #print(f'v2.name: {v2.name}')

                            e = self.searchEdges(self.edges, v1, v2, ansCount)

                            if v1 != None and v2 != None and e == -1:
                                edge = Edge("verb", self.VERB)
                                edge.inVertex = v1
                                edge.outVertex = v2
                                edge.index = ansCount
                                self.edges.append(edge)
                                self.numEdges+=1

                        prevType = self.NOUN
                        nCount += 1

                    #If token is adjective
                    elif tok.pos_ == "ADJ":
                        adjVertex = None

                        #If previous token was also an adjective
                        if prevType == self.ADJ:
                            if adjCount >= 1:
                                adjCount -= 1

                            prevVertex = self.searchVertices(self.vertices, adjectives[adjCount], ansCount)
                            adjectives[adjCount] = adjectives[adjCount] + " " + text
                            adjVertex = self.getVertex(self.vertices, adjectives[adjCount], ansCount)

                            if adjVertex == None:
                                prevVertex.name = prevVertex.name + " " + text
                                adjVertex = prevVertex

                                if adjVertex.label == "":
                                    adjVertex.label = labels[labelCounter]

                                if adjVertex.parent.text == "" or adjVertex.parent == None or adjVertex.parent.text.lower() == text:
                                    adjVertex.parent = parents[parentCounter]

                                if labels[labelCounter] != 'nmod' or labels[labelCounter] != "pmod":
                                    adjVertex.label = labels[labelCounter]

                        else:
                            adjectives.append(text)
                            adjVertex = self.getVertex(self.vertices, text, ansCount)
                            if adjVertex == None:
                                adjVertex = Vertex(text, self.ADJ, ansCount, tok.dep_, tok.head, tok.pos_)
                                self.vertices.append(adjVertex)
                                self.numVertices += 1


                        if nCount > 0:

                            v1 = self.searchVertices(self.vertices, nouns[nCount-1], ansCount)
                            v2 = adjVertex

                            e = self.searchEdges(self.edges, v1, v2, ansCount)

                            if v1 != None and v2 != None and e == -1:
                                edge = Edge("noun-property", self.NOUN)
                                edge.inVertex = v1
                                edge.outVertex = v2
                                edge.index = ansCount
                                self.edges.append(edge)
                                self.numEdges +=1

                        prevType = self.ADJ
                        adjCount += 1


                    #If token is verb or auxilary verb
                    elif tok.pos_ == "VERB" or tok.pos_ == "AUX":
                        appendedVertex = False
                        verbVertex = None

                        if prevType == self.VERB:
                            #print(f'prev type was vertex')
                            self.verbPhrases += 1
                            vCount -= 1

                            prevVertex = self.searchVertices(self.vertices, verbs[vCount], ansCount)

                            if prevVertex.POStag == "AUX":
                                self.modalAuxPhrases += 1

                            verbs[vCount] = verbs[vCount] + " " + text

                            verbVertex = self.getVertex(self.vertices, verbs[vCount], ansCount)

                            if verbVertex == None:
                                prevVertex.name = prevVertex.name + " " + text
                                #print('appending prev verb vertex to current one')
                                verbVertex = prevVertex

                                if verbVertex.label == "":
                                    verbVertex.label = labels[labelCounter]

                                if verbVertex.parent.text == "" or verbVertex.parent == None or verbVertex.parent.text.lower() == text:
                                    verbVertex.parent = parents[parentCounter]

                                if labels[labelCounter] != 'nmod' or labels[labelCounter] != "pmod":
                                    verbVertex.label = labels[labelCounter]

                                appendedVertex = True
                        else:

                            verbs.append(text)
                            verbVertex = self.getVertex(self.vertices, text, ansCount)

                            if verbVertex == None:
                                #print('new verb vertex added')
                                verbVertex = Vertex(text, self.VERB, ansCount, tok.dep_, tok.head, tok.pos_)
                                self.vertices.append(verbVertex)
                                self.numVertices += 1

                            #print(f'verbVertex: {verbVertex.name}')

                        if prevType == self.ADV:
                            if vCount >= 0:
                                if vCount == 0:
                                    v1 = self.searchVertices(self.vertices, verbs[vCount], ansCount)
                                else:
                                    v1 = self.searchVertices(self.vertices, verbs[vCount], ansCount)

                                v2 = self.searchVertices(self.vertices, adverbs[advCount-1], ansCount)

                                e = self.searchEdgesToSetNull(self.edges, v1, v2, ansCount)

                                if v1 != None and v2 != None and e != -1:
                                    edge = Edge("verb-property", self.VERB)
                                    edge.inVertex = v1
                                    edge.outVertex = v2
                                    edge.index = ansCount

                                    self.edges.append(edge)
                                    self.numEdges += 1

                        if nCount >= 1 and appendedVertex == False:
                            v1 = self.searchVertices(self.vertices, nouns[nCount-1], ansCount)
                            v2 = verbVertex

                            e = self.searchEdges(self.edges, v1, v2, ansCount)

                            if v1 != None and v2 != None and e == -1:

                                edge = Edge("verb", self.VERB)
                                edge.inVertex = v1
                                edge.outVertex = v2
                                edge.index = ansCount

                                self.edges.append(edge)
                                self.numEdges += 1


                        appendedVertex = False
                        prevType = self.VERB
                        vCount += 1

                    #If token is adverb
                    elif tok.pos_ == "ADV":

                        if prevType == self.ADV:
                            if advCount >= 1:
                                advCount -= 1
                            prevVertex = self.searchVertices(self.vertices, adverbs[advCount], ansCount)
                            adverbs[advCount] = adverbs[advCount] + " " + text

                            adverbVertex = self.getVertex(self.vertices, adverbs[advCount], ansCount)

                            if adverbVertex == None:
                                prevVertex.name = prevVertex.name + " " + text
                                adverbVertex = prevVertex

                                if adverbVertex.label == "":
                                    adverbVertex.label = labels[labelCounter]
                                if adverbVertex.parent.text == "" or adverbVertex.parent == None or adverbVertex.parent.text.lower() == text:
                                    adverbVertex.parent = parents[parentCounter]
                                if labels[labelCounter] != 'nmod' or labels[labelCounter] != "pmod":
                                    adverbVertex.label = labels[labelCounter]

                        else:
                            adverbs.append(text)
                            adverbVertex = self.getVertex(self.vertices, text, ansCount)

                            if adverbVertex == None:
                                adverbVertex = Vertex(text, self.ADV, ansCount, tok.dep_, tok.head, tok.pos_)
                                self.vertices.append(adverbVertex)
                                self.numVertices += 1

                        if vCount > 0:

                            v1 = self.searchVertices(self.vertices, verbs[vCount-1], ansCount)

                            v2 = adverbVertex
                            e = self.searchEdges(self.edges, v1, v2, ansCount)

                            if v1 != None and v2 != None and e == -1:
                                edge = Edge("verb-property", self.VERB)
                                edge.inVertex = v1
                                edge.outVertex = v2
                                edge.index = ansCount

                                self.edges.append(edge)
                                self.numEdges += 1

                        prevType = self.ADV
                        advCount += 1

                    #If token coordinating conjunction
                    elif tok.pos_ == "CCONJ":

                        if prevType == self.VERB:
                            self.verbPhrases += 1
                            vCount -= 1

                            prevVertex = self.searchVertices(self.vertices, verbs[vCount], ansCount)

                            if prevVertex.POStag == "AUX":
                                self.modalAuxPhrases += 1

                            verbs[vCount] = verbs[vCount] + " " + text

                            verbVertex = self.getVertex(self.vertices, verbs[vCount], ansCount)

                            if verbVertex == None:
                                prevVertex.name = prevVertex.name + " " + text
                                # print('appending prev verb vertex to current one')
                                verbVertex = prevVertex

                                if verbVertex.label == "":
                                    verbVertex.label = labels[labelCounter]

                                if verbVertex.parent.text == "" or verbVertex.parent == None or verbVertex.parent.text.lower() == text:
                                    verbVertex.parent = parents[parentCounter]

                                if labels[labelCounter] != 'nmod' or labels[labelCounter] != "pmod":
                                    verbVertex.label = labels[labelCounter]

                            prevType = self.VERB
                            vCount+=1

                        if prevType == self.NOUN:

                            self.nounPhrases += 1
                            nCount -= 1

                            prevVertex = self.searchVertices(self.vertices, nouns[nCount], ansCount)
                            # print(f'prevVertex: {prevVertex.name}')

                            nouns[nCount] = nouns[nCount] + " " + text
                            nounVertex = self.getVertex(self.vertices, nouns[nCount], ansCount)

                            if nounVertex == None:
                                # print(f'Previous noun vertex: {prevVertex.name} retrieved!')

                                prevVertex.name = prevVertex.name + " " + text
                                nounVertex = prevVertex

                                if nounVertex.label == "":
                                    nounVertex.label = labels[labelCounter]

                                if nounVertex.parent.text == "" or nounVertex.parent == None or nounVertex.parent.text.lower() == text:
                                    nounVertex.parent = parents[parentCounter]

                                if labels[labelCounter] != 'nmod' or labels[labelCounter] != "pmod":
                                    nounVertex.label = labels[labelCounter]

                            prevType = self.NOUN
                            nCount += 1

                        appendedVertex = 0

                        #print(f'For conjunction check previous type.....')

                #print(f'Ans Count: {ansCount}')
                #print(f'Noun Count: {nCount}')
                #print(f'Verb Count: {vCount}')
                #print(f'Adjective Count: {adjCount}')
                #print(f'Adverb Count: {advCount}')

                ansCount+=1
                labelCounter+=1
                parentCounter+=1

                #print('\n\n')

        self.setSemanticLabelsForEdges(self.vertices, self.edges)

        print(f'Num of Edges: {len(self.edges)}')
        for edge in self.edges:
            if edge != None:
                print(f"Edge: {[edge.inVertex.name, edge.outVertex.name, edge.name]}")

        #print(f'Edges: {[(edge.inVertex.name, edge.outVertex.name) for edge in self.edges]}')




    #replaceApostrophes():
    #   Input: text
    #   Output: text with all contractions moved to their full form
    #           this removes the need of apostrophes
    def replaceApostrophes(self, text):
        text = text.replace("'s", " is")
        text = text.replace("'d", " could")
        text = text.replace("s'", "s")
        text = text.replace("'re", " are")

        if "can't" in text:
            text = text.replace("'t", " not")

        text = text.replace("n't", " not")

        return text


    # searchVertices():
    #   Input:  list of vertices
    #           token string of vertex you want to find
    #           sentence index (which sentence the vertex is in)
    #   Output: vertex with matching str and index
    def searchVertices(self, list, str, index):
        for vertex in list:
            #print(f'Vertex: {vertex.name.lower()} in vertex list')
            if vertex != None and str != "" and str != None:
                if vertex.name.lower() == str.lower() and vertex.index == index:
                    return vertex

        return None

    # getVertex()
    #   Input:  list of vertices
    #           token string of vertex you want to find
    #           sentence index (which sentence the vertex is in)
    #   Output: vertex with matching str and index
    #           unlike searchVertices(), getVertex() will nullify all vertices containing the token string
    def getVertex(self, list, str, index):
        pos = 0
        flag = 0

        if str == None:
            return None

        for i in range(self.numVertices):
            if list[i] != None and (list[i].name.lower() == str.lower()) and index == list[i].index:
                flag = 1
                pos = i
                list[i].frequency+=1

                #Nullify all vertices containing substrings of this vertex in the same sentence (index == list[j].index)
                for j in range(self.numVertices):
                    if list[j] != None and list[j].index == index and (not str.lower() == list[j].name.lower()) and list[j].name.lower() in str.lower():
                        self.vertices[j] = None

                break

        if flag == 1:
            return list[pos]
        else:
            return None

    # searchEdges()
    #   Input: list of edges
    #          inVertex of edge you want to find
    #          outVertex of edge you want to find
    #          sentence index
    #   Output: Returns the edge position
    def searchEdges(self, list, inVertex, outVertex, index):
        edgePos = -1

        #Loop through number of edges
        for i in range(self.numEdges):
            #Only loop through edges that exist
            if list[i] != None and list[i].inVertex != None and list[i].outVertex != None:
                inName = inVertex.name.lower()
                outName = outVertex.name.lower()
                #Check if the inVertex and outVertex names match what is in the edge
                if (((list[i].inVertex.name.lower() == inName or list[i].inVertex.name.lower() in inName) and
                    (list[i].outVertex.name.lower() == outName or list[i].outVertex.name.lower() in outName)) or
                    ((list[i].inVertex.name.lower() == outName or list[i].inVertex.name.lower() in outName) and
                     (list[i].outVertex.name.lower() == inName or list[i].outVertex.name.lower() in inName))):

                    edgePos = i

                    #Increase frequency of edge if it occurs in different sentence
                    if index != list[i].index:
                        list[i].frequency += 1

        #Nullify all edges that contain substrings of the in and out vertices

        for j in range(self.numEdges):
            i = self.numEdges - (j + 1)

            if list[i] != None and list[i].index == index:
                if (list[i].inVertex.name.lower() == inName and (not list[i].outVertex.name.lower() == outVertex) and
                    (list[i].outVertex.name.lower() in outName)):
                    self.edges[i] = None

                elif ((not list[i].inVertex.name.lower()) and (list[i].inVertex.name.lower() in inName) and
                      (list[i].outVertex.name.lower() == outName)):
                    self.edges[i] = None


        return edgePos

    # searchEdgesToSetNull()
    #   Input: list of edges
    #          inVertex of edge you want to find
    #          outVertex of edge you want to find
    #          sentence index
    #   Output: Returns the edge position
    def searchEdgesToSetNull(self, list, inVertex, outVertex, index):
        edgePos = -1

        for i in range(self.numEdges):
            if list[i] != None and list[i].inVertex != None and list[i].outVertex != None:
                inName = inVertex.name.lower()
                outName = outVertex.name.lower()
                if ((list[i].inVertex.name.lower() == inName and
                    list[i].outVertex.name.lower() == outName) or
                    (list[i].inVertex.name.lower() == outName and
                     list[i].outVertex.name.lower() == inName)):

                    edgePos = i

                    if index != list[i].index:
                        list[i].frequency+=1

        return edgePos

    # setSemanticLablesForEdges()
    #   Input: list of vertices
    #          list of edges
    #   Output: No output
    #           Function sets semantic labels for edges - copied implementation from Lakshmi, however it looks inefficient
    #           Also semantic labeling doesn't even seem to be used in the algorithm, what is the point of storing this info?
    def setSemanticLabelsForEdges(self, vertices, edges):

        for vertex in vertices:
            if vertex != None and vertex.parent != None:

                #Searches for a vertex, that is the parent of the current vertex
                for i in range(len(vertices)):
                    if vertices[i] != None and (vertices[i].name.lower() == vertex.parent.text or
                        vertex.parent.text.lower() in vertices[i].name.lower()):
                        parent = vertices[i]
                        break

                if parent != None:

                    for pos in range(len(edges)):
                        if edges[pos] != None and edges[pos].inVertex != None and edges[pos].outVertex != None:
                            #
                            if ((edges[pos].inVertex.name == vertex.name and edges[pos].outVertex.name == parent.name) or
                                (edges[pos].inVertex.name == parent.name and edges[pos].outVertex.name == vertex.name)):

                                if edges[pos].label == None or edges[pos].label == "":
                                    self.edges[pos].label = vertex.label
                                    print(f"Edge1: {[edges[pos].inVertex.name, edges[pos].outVertex.name, edges[pos].name, edges[pos].label]}")

                                elif (edges[pos].label == None and (edges[pos].label == "nmod" or edges[pos].label == "pmod") and
                                    (vertex.label != "" and vertex.label != "nmod" and vertex.label != "pmod")):
                                    self.edges[pos].label = vertex.label
                                    print(f"Edge2: {[edges[pos].inVertex.name, edges[pos].outVertex.name, edges[pos].name, edges[pos].label]}")



                parent = None

        for pos in range(len(edges)):
            if edges[pos] != None and (edges[pos].label == None or edges[pos].label == ""):

                if edges[pos].inVertex.label != "" and edges[pos].inVertex.label != None:
                    self.edges[pos].label = edges[pos].inVertex.label
                    print(f"Edge3: {[edges[pos].inVertex.name, edges[pos].outVertex.name, edges[pos].name, edges[pos].label]}")
                elif edges[pos].outVertex.label != "" and edges[pos].outVertex.label != None:
                    self.edges[pos].label = edges[pos].outVertex.label
                    print(f"Edge4: {[edges[pos].inVertex.name, edges[pos].outVertex.name, edges[pos].name, edges[pos].label]}")








