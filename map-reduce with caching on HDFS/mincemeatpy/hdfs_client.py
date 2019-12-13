import subprocess

class HDFSClient:
    """ 
    This is a class for for interacting with HDFS.
    """
    def __init__(self):
        """ 
        The constructor for HDFSClient class. 
        """

    def test(self, path: str) -> bool:
        """
        Check if file exists.
      
        Parameters: 
        path (str): path of file.
      
        Returns: 
        bool: returns if operation succeeded
        """
        result = subprocess.run(["hdfs", "dfs", "-test", "-e", path, "/dev/null"], capture_output=True)
        return not result.returncode

    def put(self, local_file: str, remote_file: str) -> bool:
        """
        Copy from local to remote.
      
        Parameters: 
        local_file (str): local file.
        remote_file (str): remote file.
      
        Returns: 
        bool: returns if operation succeeded
        """
        result = subprocess.run(["hdfs", "dfs", "-put", local_file, remote_file, "/dev/null"], capture_output=True)
        return not result.returncode

    def get(self, remote_file: str, local_file: str) -> bool:
        """
        Copy from remote to local.
      
        Parameters: 
        remote_file (str): remote file.
        local_file (str): local file.
      
        Returns: 
        bool: returns if operation succeeded
        """
        result = subprocess.run(["hdfs", "dfs", "-get", remote_file, local_file, "/dev/null"], capture_output=True)
        return not result.returncode

    def rmr(self, path: str) -> bool:
        """
        Remove file.
      
        Parameters: 
        path (str): path of file.
      
        Returns: 
        bool: returns if operation succeeded
        """
        result = subprocess.run(["hdfs", "dfs", "-rmr", path, "/dev/null"], capture_output=True)
        return not result.returncode