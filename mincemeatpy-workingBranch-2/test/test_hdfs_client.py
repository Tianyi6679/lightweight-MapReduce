import unittest
import os
import shutil
from mincemeatpy.hdfs_client import HDFSClient

class TestHDFSClient(unittest.TestCase):
    directory = "hdfs"
    content = "hello world"
    local_file = "hdfs/temp1.txt"
    remote_file = "/temp1.txt"

    # def setUp(self):
    #     self.hdfs_client = HDFSClient()

    @classmethod
    def create_files(cls):
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)
        file = open(cls.local_file, 'w')
        file.write(cls.content)
        file.close()

    @classmethod
    def delete_files(cls):
        shutil.rmtree(cls.directory)

    @classmethod
    def setUpClass(cls):
        cls.hdfs_client = HDFSClient()
        cls.create_files()

    @classmethod
    def tearDownClass(cls):
        cls.delete_files()

    # def test_test(self):
    #     self.assertFalse(self.hdfs_client.test(self.remote_file))

    # def test_put(self):
    #     self.assertTrue(self.hdfs_client.put(self.local_file, self.remote_file))

    # def test_get(self):
    #     path = "temp/temp2.txt"
    #     self.assertTrue(self.hdfs_client.get(cls.remote_file, path))

    # def test_rmr(self):
    #     path = "/temp1.txt"
    #     self.assertFalse(self.hdfs_client.test(path))

if __name__ == '__main__':
    unittest.main()