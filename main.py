from typing import Callable, Generic, Iterable, Optional, TypeVar, Union

_T = TypeVar('_T')
class SegmentTree(Generic[_T]):
    
    def __init__(self, l:Iterable[_T], f:Callable[[_T, _T], _T]) -> None:
        
        l_:list[_T] = list(l)
        length = 1 << (len(l_)-1).bit_length()  # smallest power of 2 greater than or equal to len(l)
        
        # use None as a unit element
        def f_(x:Optional[_T], y:Optional[_T]) -> Optional[_T]:
            if x is None:
                return y
            if y is None:
                return x
            return f(x, y)
        
        # initialize segment tree
        self._l:list[Optional[_T]] = [None] * ((length << 1) - 1)  # segment tree
        self.f = f_
        self._len = length
        
        # build segment tree
        self._l[length-1:length-1+len(l_)] = l_
        for i in range(length-2, -1, -1):
            self._l[i] = self.f(self._l[2*i+1], self._l[2*i+2])
    
    
    def __str__(self) -> str:
        return str(list(filter(lambda x: x is not None, self._l[self._len-1:])))
    
    
    def _get_index(self, start:int, interval:int) -> int:
        # get the index of the segment tree that corresponds to the interval [start, start+interval)
        return self._len // interval - 1 + start // interval
    
    
    def __getitem__(self, item:Union[int, slice]) -> _T:
        match item:
            case int():
                # convert negative index to positive
                if item < 0:
                    item += self._len
                    
                # check if item is out of range
                if item < 0 or self._len <= item:
                    raise IndexError('index out of range')
                
                # get item-th element
                ret = self._l[item - self._len + 1]
                
                if ret is None:
                    raise IndexError('index out of range')
                return ret
            
            case slice():
                start, stop, step = item.indices(self._len)
                
                # check if slice is valid
                if (step != 1) or (start < 0) or (stop < 0) or (self._len < start) or (self._len < stop) or (start > stop):
                    raise IndexError(f'slice({start}, {stop}, {step}) not supported')
                
                if start == stop:
                    return self[start]
                
                
                max_interval = start & -start if start != 0 else self._len  # largest power of 2 that divides start
                interval = 1 << (min(stop - start, max_interval).bit_length() - 1)  # largest power of 2 that is less than or equal to stop - start
                id = self._get_index(start, interval)
                ret = self._l[id]
                assert ret is not None
                start += interval
                
                # if needed to get the value of the right end of the slice
                if start < stop:
                    ret = self.f(ret, self[start:stop])
                    assert ret is not None
                    
                return ret
    
    def __setitem__(self, id:int, value:_T) -> None:
        # convert negative index to positive
        if id < 0:
            id += self._len
            
        # check if id is out of range
        if id < 0 or self._len <= id:
            raise IndexError('index out of range')
        
        # set id-th element
        id += self._len - 1
        self._l[id] = value
        
        # update the segment tree
        while id > 0:
            id = (id - 1) // 2
            self._l[id] = self.f(self._l[id*2+1], self._l[id*2+2])


if __name__ == '__main__':
    l1 = [1, 2, 3, 4, 5, 6]
    st1 = SegmentTree(l1, max)
    print(st1) # [1, 2, 3, 4, 5, 6]
    print(st1[3]) # 4
    print(st1[:]) # 6
    print(st1[0:0]) # 1
    print(st1[2:6]) # 6
    st1[0] = 7
    print(st1) # [7, 2, 3, 4, 5, 6]
    print(st1[:]) # 7
    print(st1[2:6]) # 6
    
    l2 = ["a", "aaa", "ab", "abcd", "d"]
    st2 = SegmentTree(l2, lambda x, y : x if len(x) >= len(y) else y)
    print(st2) # ['a', 'aaa', 'ab', 'abcd', 'd']
    print(st2[3]) # abcd
    print(st2[:]) # abcd