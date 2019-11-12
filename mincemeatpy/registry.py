import dill
import hashlib
from os import path

class Registry:
    """ 
    This is a Singleton class for "registering" functions and data. 
    """
    __instance = None

    def get_instance():
        """
        The function returns an instance of Registry.
          
        Returns: 
            Registry
        """
        if Registry.__instance == None:
            Registry()
        return Registry.__instance

    def __init__(self):
        """ 
        The constructor for Registry class. 
        """
        if Registry.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Registry.__instance = self

    def serialize(self, function):
        """
        The function to serialize a function.
  
        Parameters: 
            function: The function to be serialized.
          
        Returns: 
            str: A hexstring representing function.
        """
        return dill.dumps(function).hex()
    
    def deserialize(self, hex_string):
        """
        The function to deserialize a string into a function.
  
        Parameters: 
            hex_string: The string to be deserialized.
          
        Returns: 
            Function: Returns the a deserialized function.
        """
        return dill.loads(bytes.fromhex(hex_string))

    def generate_key(self, function, filename):
        """
        The function to generate a unique key from a function and file.
  
        Parameters: 
            function: The function to be serialized.
            filename: The name of file to be serialized.
          
        Returns: 
            Str: Returns unique key generated from function and file.
        """
        return self.serialize(function) + self.__hash_file(filename)

    def __hash_file(self, filename):
        """
        The function to hash a file.
  
        Parameters: 
            filename: The name of file to be serialized.
          
        Returns: 
            Str: Returns hash generated from file.
        """
        hasher = hashlib.md5()
        with open(filename, 'r') as file:
            buf = file.read()
            hasher.update(buf.encode('utf-8'))
        return hasher.hexdigest()

    # def register(self, function):
    #     ser = self.serialize(function)
    #     write(ser)
    #     ln = sum(1 for line in open(self.functions_file))
    #     functions_map["ser"] = ln

    # def read(self, function)

    # def write(self, input):
    #     mode = 'a' if path.exists(self.functions_file) else 'w'
    #     file = open(self.functions_file, mode)
    #     f.write(input)
    #     f.close()

    # def __hash_string(self, input):
    #     return hashlib.md5(input.encode()).hexdigest()
