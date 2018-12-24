import unittest


class TestIdataApi(unittest.TestCase):
    import idata

    def test_search(self):
        res = self.idata.search("中国")
        self.assertEqual(res['status'], 1)