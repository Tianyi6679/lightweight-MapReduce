import pickle

from functools4 import lru_cache
from lruCache import CacheData

@lru_cache(maxsize=16)
def fib(n):
    return n

# open a file, where you stored the pickled data
file = open('important', 'rb')

# dump information to that file
cacheData = pickle.load(file)

# close the file
file.close()

#fib.set_cache_dictionary(result)

print(fib.cache_info())


fib.set_cache_dictionary(cacheData.cache,cacheData.root,cacheData.hit,cacheData.full)


for x in range(16):
  fib(x)
print(fib.cache_info())
