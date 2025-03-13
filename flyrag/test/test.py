import unittest
from flyrag.module.document import DocumentParserContext

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
    def test_pdf_parser(self):
        print(DocumentParserContext.do_parse(f'C:/Users/niufe/Desktop/test.pdf'))
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
