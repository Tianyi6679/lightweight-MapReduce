import unittest
from registry import Registry

class TestRegistry(unittest.TestCase):

    def test_get_instance(self):
        reg1 = Registry.get_instance()
        reg2 = Registry.get_instance()
        self.assertTrue(type(reg) is Registry)
        self.assertEqual(reg1, reg2)


    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()