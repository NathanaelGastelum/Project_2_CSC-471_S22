from cgi import test
import simplify_cfg    # The code to test
import unittest   # The test framework
import shelve

class Test_TestSearchFilter(unittest.TestCase):

    def test_e_rules(self):
        test_file = 
        with shelve.open(test_file) as input:
            actual = simplify_cfg.remove_e_rules(simplify_cfg.get_input())
            self.assertEqual(actual, 
                )

if __name__ == '__main__':
    unittest.main()