import sys
import csv
from collections import defaultdict
import string

class Document():
    """
        A class used to represent a Document

        Attributes:
            id : str
                The document ID
            title : str
                The title of the document
            body : str
                The text in the body of the document
    """

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body

class DocumentDataBase():
    """
        A class used to represent the Document Database

        Attributes:
            docDataBase : Dictionary
                The database stored as a key value pair, with the ID's as the keys, and the titles as the value

        Methods:
            AddFile()
                Adds a file to the database. Raises valueError if id already exists
                @Param - document: Document
            GetFile()
                Returns the title for the given ID
                @Param - id: str
    """

    def __init__(self):
        self.docDataBase = {}

    def AddFile(self, document):
        if document.id in self.docDataBase.keys():
            print ("Duplicate Key")
            raise ValueError
        else:
            self.docDataBase[document.id] = document.title

    def GetFile(self, id):
        return self.docDataBase[id]

class Index():
    """
        A class used to represent the Search Index (Inverted Index)

        Attributes:
            index : Dictionary
                The index stored as a key value pair, with the words as the keys, and a set of document id's as the value
            db : DocumentDataBase
                The database representing the documents indexed

        Methods:
            IndexDocument()
                Splits the document title and body by whitespace, and removes all punctuation.
                Adds the word to the keys of the index if it doesn't exist, and the id to the value set
                Updates the document database.
                @Param - document: Document
            LookUp()
                Returns the list of document ID's for any word. Returns an empty list if word not found
                @Param - searchTerm: str
    """

    def __init__(self, dataBase):
        self.index = defaultdict(set)
        self.db = dataBase

    def IndexDocument(self, document):
        words = document.title+ " " + document.body
        for word in words.split():
            self.index[word.lower().translate(str.maketrans(dict.fromkeys(string.punctuation)))].add(document.id)
        self.db.AddFile(document)

    def LookUp(self, searchTerm):
        if searchTerm.lower() in self.index.keys():
            return self.index[searchTerm.lower()]
        else:
            return []


def createIndex(inputFilePath, searchIndex):
    """
        A function to iterate on a csv file, and index each one of them.

        Attributes:
            inputFilePath : str
                The path to the csv file
            searchIndex : Index
                The index representing the search index
    """

    with open(inputFilePath) as inputFile:
        reader = csv.reader(inputFile, delimiter = ',')
        for row in reader:
            doc = Document(row[0], row[1], row[2])
            searchIndex.IndexDocument(doc)

def main(argv):
    """
        The main function which creates the index, and returns the list of document id's for each search term.
    """

    try:
        inputFilePath = argv[0]
        searchTerms = argv[1:]
    except:
        print ("Please enter at least one search term")

    documentDataBase = DocumentDataBase()
    searchIndex = Index(documentDataBase)

    createIndex(inputFilePath, searchIndex)

    for term in searchTerms:
        results = searchIndex.LookUp(term.lower())
        if len(results) == 0:
            print ("{0} - Term not found".format(term))
        else:
            print("The search results for the term - {0} are:".format(term))
            for result in results:
                print(result + ", " + documentDataBase.docDataBase[result])

if __name__ == '__main__':
    main(sys.argv[1:])