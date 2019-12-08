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

    def generate_key(self, function, data):
        """
        The function to generate a unique key from a function and data.
  
        Parameters: 
            function: The function to be serialized.
            data: The data to be hashed.
          
        Returns: 
            Str: Returns unique key generated from function and data.
        """
        return self.serialize(function) + self.__hash_data(data)

    def generate_key_from_file(self, function, filename):
        """
        The function to generate a unique key from a function and file.
  
        Parameters: 
            function: The function to be serialized.
            filename: The name of file to be hashed.
          
        Returns: 
            Str: Returns unique key generated from function and file.
        """
        return self.serialize(function) + self.__hash_file(filename)

    def generate_key_from_files(self, function, filenames):
        """
        The function to generate a unique key from a function and files.
  
        Parameters: 
            function: The function to be serialized.
            filename: The name of files to be hashed.
          
        Returns: 
            Str: Returns unique key generated from function and files.
        """
        result = list(map(self.__hash_file, filenames))
        result.sort()
        return self.serialize(function) + "".join(result)

    def __hash_file(self, filename):
        """
        The function to hash a file.
  
        Parameters: 
            filename: The name of file to be serialized.
          
        Returns: 
            Str: Returns hash generated from file.
        """
        hasher = hashlib.md5()
        print(filename)
        with open(filename, 'r', encoding='latin1') as file:
            buf = file.read()
            hasher.update(buf.encode('latin1'))
        return hasher.hexdigest()

    def __hash_data(self, data):
        """
        The function to hash a file.
  
        Parameters: 
            filename: The name of file to be serialized.
          
        Returns: 
            Str: Returns hash generated from file.
        """
        return hashlib.md5(data.encode('utf-8')).hexdigest()

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
