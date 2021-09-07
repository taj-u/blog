def selectionSort(li):
    n = len(li)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if li[min_index] > li[j]:
                min_index = j
        li[i] , li[min_index] = li[min_index], li[i]
    return li
li =list((map(int, input().split())))
print(selectionSort(li))