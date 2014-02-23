import unittest, os
import DiffLibrary2

class MyTest(unittest.TestCase):
    
    def setUp(self):
        self.diff = DiffLibrary2.keywords()
        self.badFile = (os.path.join(os.path.dirname(__file__), "resources", "data","loremipsu.txt"))     
        self.testFile1 = (os.path.join(os.path.dirname(__file__), "resources", "data","loremipsum.txt"))
        self.testFile3 = (os.path.join(os.path.dirname(__file__), "resources", "data","loremipsum3.txt"))
        self.testFile2 = (os.path.join(os.path.dirname(__file__), "resources", "data","loremipsum2.txt"))
        
        print self.badFile
        
    def testFileNotExists(self):
        ExpectedException = ("%s doesn't exist" % (self.badFile))
        
        with self.assertRaises(AssertionError) as context:
            self.diff.diff_files(self.badFile,self.testFile2)
            
        self.assertEqual(context.exception.message, ExpectedException)   
    
    def testMissMatchRight(self):
        ExpectedException = ("differences found between %s and %s" % (self.testFile1,self.testFile2))
        
        with self.assertRaises(AssertionError) as context:
            self.diff.diff_files(self.testFile1,self.testFile2)
        
        self.assertEqual(context.exception.message, ExpectedException)

    def testMissMatchLeft(self):
        ExpectedException = ("differences found between %s and %s" % (self.testFile1,self.testFile3))
        
        with self.assertRaises(AssertionError) as context:
            self.diff.diff_files(self.testFile1, self.testFile3)
        
        self.assertEqual(context.exception.message, ExpectedException)
        
    def testMatch(self):
        self.assertIsNone(self.diff.diff_files(self.testFile1,self.testFile1))     
    
    def testMatchWithOptions(self):
        """
        Options being passed:
            -i  --ignore-case  Consider upper- and lower-case to be the same.
            -w  --ignore-all-space  Ignore all white space.
            -B  --ignore-blank-lines  Ignore changes whose lines are all blank.
        """
        self.assertIsNone(self.diff.diff_files(self.testFile1,self.testFile3,"-i -w -B"))
        
if __name__ == "__main__":
    unittest.main()