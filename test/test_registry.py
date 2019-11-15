import unittest
import os
import shutil
from mincemeatpy.registry import Registry

def identity(n):
    return n

class TestRegistry(unittest.TestCase):

    def setUp(self):
        self.reg = Registry.get_instance()

    def test_get_instance(self):
        new_reg = Registry.get_instance()
        self.assertTrue(type(self.reg) is Registry)
        self.assertEqual(self.reg, new_reg)

    def test_serialize(self):
        ser = self.reg.serialize(identity)
        self.assertTrue(type(ser) is str)

    def test_deserialize(self):
        before = identity(10)
        ser = self.reg.serialize(identity)
        new_identity = self.reg.deserialize(ser)
        after = new_identity(10)
        self.assertTrue(before, after)

    def test_generate_key(self):
        content = "hello world"
        key = self.reg.generate_key(identity, content)
        self.assertTrue(type(self.reg) is Registry)
        self.assertTrue(type(key) is str)

    def test_generate_key_from_file(self):
        content = "hello world"
        directory = "temp"
        filename = "temp/temp1.txt"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file = open(filename, 'w')
        file.write(content)
        file.close()
        key = self.reg.generate_key_from_file(identity, filename)
        self.assertTrue(type(self.reg) is Registry)
        self.assertTrue(type(key) is str)
        shutil.rmtree(directory)

if __name__ == '__main__':
    unittest.main()