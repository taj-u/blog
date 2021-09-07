def insertionSort(li):
    n = len(li)
    for i in range(1, n):
        x = li[i]
        j = i - 1
        while j >= 0 and li[j] > x:
            li[j + 1] = li[j]
            j -= 1
        li[j + 1] = x
    return li
li = list(map(int, input().split()))
print(insertionSort(li))