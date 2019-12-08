from functools4 import lru_cache
import pickle
import copy


class CacheData:
  def __init__(self, cache=None, root=None,hit=None,full=None):
    self.cache = cache
    self.root = root
    self.hit = hit
    self.full = full


# @lru_cache(maxsize=16)
# def fib(n):
#     return n
#
# for x in range(16):
#   fib(x)
# print(fib.cache_info())
#
# for x in range(16):
#   fib(x)
# print(fib.cache_info())
#
# result=fib.get_cache_dictionary()
# result_1=fib.get_cache_1()
# result_2=fib.get_cache_2()
# result_3=fib.get_cache_3()
#
# cacheData= CacheData(result,result_1,result_2,result_3)
#
#
# file = open('important', 'wb')
#
# #dump information to that file
# pickle.dump(cacheData, file)
#
# # close the file
# file.close()
#


# var1=copy.deepcopy(result)
# var2=copy.deepcopy(result_1)
# var3=copy.deepcopy(result_2)
# var4=copy.deepcopy(result_3)
#
#
#
# print(var1)
# print(var2)
# print(result_2)
# print(result_3)

# fib.set_cache_dictionary(var1,var2,result_2,result_3)
# #print(var1 )
#
#
# result10=fib.get_cache_dictionary()
#
# #print(fib.cache_info())
# print(result10)



#for x in range(16):
#  fib(x)
#print(fib.cache_info())
