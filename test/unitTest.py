import unittest

class utestPDF_Sorter(unittest.TestCase):
    """docstring for utestPDF_Sorter."""
    def __init__(self, arg):
        super(utestPDF_Sorter, self).__init__()
        self.arg = arg

    def setUp(self):
        print("SetUp")

if __name__ == '__main__':
    unittest.main()
