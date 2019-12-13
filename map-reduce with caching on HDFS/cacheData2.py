from functools4 import lru_cache
import pickle
import copy

class CacheData:
  def __init__(self, cache=None, root=None,hit=None,full=None):
    self.cache = cache
    self.root = root
    self.hit = hit
    self.full = full
    
    

  def check(self):
        print(fib.cache_info())
        
  def test(self):
    for x in range(54,65):
        fib(x,chr(x))
    self.check();
    
@lru_cache(maxsize=None)
def fib(key,url):
      return url
