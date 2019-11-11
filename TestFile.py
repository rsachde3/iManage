import unittest
import SearchEngine

class TestSearchEngine(unittest.TestCase):

#Test cases for Document Database
    def test_DocumentDataBase(self):
        testDb = SearchEngine.DocumentDataBase()
        testDocument = SearchEngine.Document("testID", "testTitle", "testBody")
        testDocument2 = SearchEngine.Document("testID2", "testTitle2", "testBody2")
        testDb.AddFile(testDocument)
        testDb.AddFile(testDocument2)
        self.assertTrue(testDocument.id in testDb.docDataBase)
        with self.assertRaises(ValueError):
            testDb.AddFile(testDocument)
        res = testDb.GetFile(testDocument.id)
        self.assertEqual(res, testDocument.title)

#Test cases for Index
    def test_Index(self):
        testDb = SearchEngine.DocumentDataBase()
        testIndex = SearchEngine.Index(testDb)
        testDocument = SearchEngine.Document("testID", "testTitle", "testBody This is a test file without punctuation")
        testDocument2 = SearchEngine.Document("testID2", "testTitle2", "testBody2 this is a test file with punctuation.")
        testIndex.IndexDocument(testDocument)
        self.assertTrue(testDocument.title.lower() in testIndex.index.keys())
        self.assertTrue(testDocument.id in testIndex.index[testDocument.title.lower()])
        for i in testDocument.body.split():
            self.assertTrue(i.lower() in testIndex.index.keys())
            self.assertTrue(testDocument.id in testIndex.index[i.lower()])
        testIndex.IndexDocument(testDocument2)
        self.assertTrue(testDocument2.title.lower() in testIndex.index.keys())
        self.assertTrue(testDocument2.id in testIndex.index[testDocument2.title.lower()])
        for i in testDocument2.body.split():
            if i == "punctuation.":
                i = "punctuation"
            self.assertTrue(i.lower() in testIndex.index.keys())
            self.assertTrue(testDocument2.id in testIndex.index[i.lower()])
        res = testIndex.LookUp("This")
        self.assertEqual(res, {'testID', 'testID2'})
        res = testIndex.LookUp("this")
        self.assertEqual(res, {'testID', 'testID2'})
        res = testIndex.LookUp("testTitle")
        self.assertEqual(res, {'testID'})
        res = testIndex.LookUp("punctuation")
        self.assertEqual(res, {'testID', 'testID2'})
        res = testIndex.LookUp("with")
        self.assertEqual(res, {'testID2'})
        res = testIndex.LookUp("no")
        self.assertEqual(res, [])


if __name__ == '__main__':
    unittest.main()