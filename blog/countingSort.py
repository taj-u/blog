def counting_sort(li):
    n = len(li)
    count = [0] * 10
    for i in range(n):
        count[li[i]] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]
    sorted_array = [0] * n
    for i in range(n):
        count[li[i]] -= 1
        sorted_array[count[li[i]]] = li[i]
    return sorted_array
li = [0, 5, 5, 4, 8, 2, 6, 3, 7, 7, 9]
print(counting_sort(li))

