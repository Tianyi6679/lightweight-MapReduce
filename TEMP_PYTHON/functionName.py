import sys
import hashlib
from lru import LRU
#import os

class CacheData:
  def __init__(self, key=None, resultPtr=None):
    self.key = key
    self.resultPtr = resultPtr

def whoami(  ):

    return sys._getframe().f_code.co_name

me  = whoami(  )



fileName="CertificateLabSafetyRustemCanAygunUCLA.pdf";

#fileSize=os.path.getsize(fileName)

digest=hashlib.md5(fileName).hexdigest()
key=me+digest



#record1=CacheData(key,None)
#dictionary
#cacheDictionary = {record1.key: record1}

#print(cacheDictionary[record1.key].key)

#print(key)
#fileSize=os.path.getsize(fileName)




## LRU

l = LRU(5)
for i in range(5):
   l[i] = str(i)

print (l.items())
