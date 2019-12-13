from functools4 import lru_cache
import pickle

class CacheData:
  def __init__(self, cache=None, root=None,hit=None,full=None):
    self.cache = cache
    self.root = root
    self.hit = hit
    self.full = full

@lru_cache(maxsize=None)
def cache(key, url):
    return url

def dumpCacheToDisk():
    result=cache.get_cache_dictionary()
    result_1=cache.get_cache_1()
    result_2=cache.get_cache_2()
    result_3=cache.get_cache_3()

    cacheData1= CacheData(result,result_1,result_2,result_3)

    
    
    file = open('cacheFile', 'wb')

    #dump information to that file
    pickle.dump(cacheData1, file)
    # close the file
    file.close()
    
    
def loadCacheFromDisk():

    try:
      file = open('cacheFile', 'rb')
      cacheData1 = pickle.load(file)
      cache.set_cache_dictionary(cacheData1.cache,cacheData1.root,cacheData1.hit,cacheData1.full)
      file.close()
    except:
      print("No Cache File")
      

def checkCache1(key):
    return cache.checkCache(key)



