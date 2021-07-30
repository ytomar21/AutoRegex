class Edge:

    def __init__(self, edgeName, edgeType):
        self.edgeId = None
        self.index = None
        self.degree = None
        self.inVertex = None
        self.outVertex = None
        self.label = None

        #1-verb, 2-adjective, 3-adverb
        self.type = edgeType
        self.name = edgeName
        #initializing match to -1
        self.averageMatch = 0.0
        self.frequency = 0

        #initializing the number of matches for each metric value to 0
        self.edgeMatch = [0,0,0,0,0]

class Vertex:

    def __init__(self, vertexName, vertexType, indexValue, lab, par, tag):
        self.nodeId = -1
        #1 - Noun, 2 - Adjective, 3 - Verb, 4 - Adverb
        self.type = vertexType
        self.name = vertexName
        #identifies the sentence number in which the vertex is present
        self.index = indexValue
        #number of relations the node has with other nodes
        self.degree = None
        #assuming that a vertex has only one property
        self.property = None
        #indicates the number of properties a vertex has
        self.propertyCount = 0
        #a vertex can have a max of 3 properties
        self.MAX = 50
        #number of times the vertex was repeatedly accessed
        self.frequency = 0
        #indicates if the word is negated or not - [true - not negated and false - negated]
        #self.state = State
        self.POStag = tag

        #for semantic role labelling
        self.label = lab
        self.parent = par


