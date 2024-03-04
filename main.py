from typing import Callable, Generic, Iterable, Optional, TypeVar, Union

_T = TypeVar('_T')
class SegmentTree(Generic[_T]):
    
    def __init__(self, l:Iterable[_T], f:Callable[[_T, _T], _T]) -> None:
        
        l_:list[_T] = list(l)
        length = 1 << (len(l_)-1).bit_length()  # smallest power of 2 greater than or equal to len(l)
        
        def f_(x:Optional[_T], y:Optional[_T]) -> Optional[_T]:
            if x is None:
                return y
            if y is None:
                return x
            return f(x, y)
        
        self._l:list[Optional[_T]] = [None] * ((length << 1) - 1)  # segment tree
        self.f = f_
        self._len = length
        
        self._l[length-1:length-1+len(l_)] = l_
        for i in range(length-2, -1, -1):
            self._l[i] = self.f(self._l[2*i+1], self._l[2*i+2])
    
    def __str__(self) -> str:
        return str(list(filter(lambda x: x is not None, self._l[self._len-1:])))
    
    def _get_index(self, start:int, interval:int) -> int:
        return self._len // interval - 1 + start // interval
    
    def __getitem__(self, item:Union[int, slice]) -> _T:
        match item:
            case int():
                if item < 0:
                    item += self._len
                if item < 0 or self._len <= item:
                    raise IndexError('index out of range')
                item += self._len - 1
                ret = self._l[item]
                if ret is None:
                    raise IndexError('index out of range')
                return ret
            case slice():
                start, stop, step = item.indices(self._len)
                if (step != 1) or (start < 0) or (stop < 0) or (self._len < start) or (self._len < stop) or (start > stop):
                    raise IndexError(f'slice({start}, {stop}, {step}) not supported')
                if start == stop:
                    return self[start]
                max_interval = start & -start if start != 0 else self._len
                interval = 1 << (min(stop - start, max_interval).bit_length() - 1)
                id = self._get_index(start, interval)
                ret = self._l[id]
                assert ret is not None
                start += interval
                if start < stop:
                    ret = self.f(ret, self[start:stop])
                    assert ret is not None
                return ret


if __name__ == '__main__':
    st = SegmentTree([1, 2, 3, 4, 5], lambda x, y: x+y)
    print(st) # [1, 2, 3, 4, 5]
    print(st[0]) # 1
    print(st[0:3]) # 6