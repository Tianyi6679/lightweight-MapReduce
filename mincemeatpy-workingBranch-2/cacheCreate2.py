from functools4 import lru_cache
import pickle
import copy
import cacheData2


# get keys from Thomas
#get serilalized function from Thomos
#get input from  Tianyi
#call the deserialized function, get the result, call the writeToCache Function
#in TaskManager we need to dump the cache into hdd and initialize the master with the cache data from hdd



#cache=CacheData();
#cache.test();
#print(cache.fib.cache_info())
for x in range(54,65):
  cacheData2.fib(x,chr(x))

#cache.check();
print(cacheData2.fib.cache_info())

# for x in range(16):
#   fib(x)
# print(fib.cache_info())
#
#result=cache.fib.get_cache_dictionary()
#result_1=cache.fib.get_cache_1()
#result_2=cache.fib.get_cache_2()
#result_3=cache.fib.get_cache_3()
#
#cacheData= CacheData(result,result_1,result_2,result_3)
##
##
#file = open('important2', 'wb')
#
##dump information to that file
#pickle.dump(cacheData, file)
#
## close the file
#file.close()

