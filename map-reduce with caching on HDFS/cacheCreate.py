from functools4 import lru_cache
import pickle
import copy
from cacheData import CacheData


# get keys from Thomas
#get serilalized function from Thomos
#get input from  Tianyi
#call the deserialized function, get the result, call the writeToCache Function
#in TaskManager we need to dump the cache into hdd and initialize the master with the cache data from hdd

@lru_cache(maxsize=None)
def fib(key,url):
      return url



for x in range(54,65):
  fib(x,chr(x))
print(fib.cache_info())

# for x in range(16):
#   fib(x)
# print(fib.cache_info())
#
result=fib.get_cache_dictionary()
result_1=fib.get_cache_1()
result_2=fib.get_cache_2()
result_3=fib.get_cache_3()

cacheData= CacheData(result,result_1,result_2,result_3)
#
#
file = open('important', 'wb')

#dump information to that file
pickle.dump(cacheData, file)

# close the file
file.close()

