'''
Created on Jan 2, 2018

@author: KSH
'''
import os
import unittest
from cast.analysers.test import UATestAnalysis


class TibcoTest(unittest.TestCase):
    def test_RegisterPlugin(self):
        print (os.getcwd())
        #print("Hello Test")
        analysis = UATestAnalysis('Tibco')
        analysis.add_selection("Tibco_Sample")
        analysis.set_verbose()
        analysis.run()
if __name__ == "__main__":
    unittest.main();
