import unittest

from flyrag.llm import LLM

class MyTestCase(unittest.TestCase):
    def test_rag(self):
        # add assertion here
        query = "我的案件结案了吗"
        llm = LLM()
        response = llm.rag(query)
        print(response)

if __name__ == '__main__':
    unittest.main()
