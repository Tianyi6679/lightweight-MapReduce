import pickle

from functools4 import lru_cache
from cacheData import CacheData

@lru_cache(maxsize=None)
def fib(key,url):
      return url
    
    
def checkCache(key):
    result=fib.checkCache(key);
    return result;
        
def writeToCache(key,url):
    fib(key,url)



# open a file, where you stored the pickled data
file = open('important', 'rb')

# dump information to that file
cacheData = pickle.load(file)

# close the file
file.close()

#fib.set_cache_dictionary(result)

#print(fib.cache_info())


fib.set_cache_dictionary(cacheData.cache,cacheData.root,cacheData.hit,cacheData.full)


cache=fib.get_cache_dictionary()

for x in range(54,65):
    result=checkCache(x)
    if result is None:
        print("Writing to Cache now")
        writeToCache(x,chr(x))
    else:
        print("hit---"+str(result) )

print("Stage 2")
for x in range(65,80):
    result=checkCache(x)
    if result is None:
        print("Writing to Cache now")
        writeToCache(x,chr(x))
    else:
        print("hit---"+str(result) )


print("Stage 3")
for x in range(54,80):
    result=checkCache(x)
    if result is None:
        print("Writing to Cache now")
        writeToCache(x,chr(x))
    else:
        print("hit---"+str(result) )
            

#for x in range(16):
#  fib(x)
#print(fib.cache_info())
