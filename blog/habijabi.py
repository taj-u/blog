class Solution:
    def heapify(self, arr, n, i):
        max_index = i
        left, right = (2 * i) + 1, (2 * i) + 2
        if left < n and arr[left] > arr[max_index]:
            max_index = left
        if right < n and arr[right] > arr[max_index]:
            max_index = right
        if i != max_index:
            arr[i], arr[max_index] = arr[max_index], arr[i]
            self.heapify(arr, n, max_index)
    def buildHeap(self, arr, n):
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i)
    def heapSort(self, arr, n):
        print(str(arr) + 'Given array')
        self.buildHeap(arr, n)
        print(str(arr) + 'Builded Heap')
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(arr, i, 0)
        # print(arr)
arr = [932, 66, 777 ,426 ,127 ,404 ,63 ,281 ,426, 317, 735 ,628, 543 ,78 ,31 ,811 ,626 ,104 ,389 ,412 ,687 ,296 ,35 ,252, 441, 675 ,604 ,770]
Solution().heapSort(arr, len(arr))
print(arr)

    #             5
    #     4               4
    # 3       0       2       3
    #     2