from itertools import izip

def chunks(li, n):
    """Yield successive n-sized chunks from li."""
    for i in xrange(0, len(li), n):
        yield li[i:i+n]

def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return izip(a, a)

def unique(seq):
   """Return sequence with duplicates removed (order preserving)"""
   seen = {}
   result = []
   for item in seq:
       if item in seen:
           continue
       seen[item] = 1
       result.append(item)
   return result
