# pythonによるセグメント木の実装

競プロ勉強用
mypy推奨

## コンストラクタ

インスタンスの生成には、元となる配列`l:Iterable[T]`と、二項演算`f:Callable[[T, T], T]`が必要である。
なお、`f`は`Callable[[Optional[T], Optional[T]], Optional[T]]`に変換され、`None`を単位元として扱うため、初期化の際に単位元が求められることはない。
以下の例は、最大値を管理したい場合。

```python
l = [1, 2, 3, 4, 5, 6]
st = SegmentTree(l, max)
```

文字列の長さの最大値を管理したい場合は以下の通り。

```python
l = ["a", "aaa", "ab", "abcd", "d"]
st = SegmentTree(l, lambda x, y: x if len(x) >= len(y) else y)
```

以下の通りにすれば、最大値とその個数を管理することも可能。

```python
l:list[tuple[int, int]] = [(1, 1), (1, 5), (1, 3), (1, 4), (1, 5), (1, 4), (1, 5), (1, 7)]

def f(x:tuple[int, int], y:tuple[int, int]) -> tuple[int, int]:
    if x[1] > y[1]:
        return x
    elif y[1] > x[1]:
        return y
    else:
        return (x[0] + y[0], x[1])

st = SegmentTree(l, f)
```

## 表示

`print`で元の配列に対応する配列を表示

```python
l = [1, 2, 3, 4, 5, 6]
st = SegmentTree(l, max)
print(st) # [1, 2, 3, 4, 5, 6]
```

## 値の更新

元の配列の`i`番目の要素を`x`に書き換える場合、以下の通り

```python
l = [1, 2, 3, 4, 5, 6]
st = SegmentTree(l, max)
st[0] = 7
print(st) # [7, 2, 3, 4, 5, 6]
```

## 値の取得

元の配列の`i`番目の要素を取得する場合は以下の通り

```python
l = [1, 2, 3, 4, 5, 6]
st = SegmentTree(l, max)
print(st[3]) # 4
```

元の配列の`[l, r)`での関数`f`による値の取得は以下の通り。

```python
l = [1, 2, 3, 4, 5, 6]
st = SegmentTree(l, max)
print(st[:]) # 6
print(st[0:0]) # 1
print(st[2:6]) # 6
```
