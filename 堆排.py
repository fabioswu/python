import random

class heapSort:
    def __init__(self, heap):
        self.heap = heap
        self.length = len(self.heap)

    def heapify(self, length, i):
        left = i*2 + 1
        right = i*2 + 2
        larger = i
        #print(self.heap, left, right)
        if left < length and self.heap[left] > self.heap[larger]:
            larger = left
        if right < length and self.heap[right] > self.heap[larger]:
            larger = right
        if larger != i:
            self.heap[larger], self.heap[i] = self.heap[i], self.heap[larger]
            self.heapify(length, larger)

    def build_heap(self):
        for i in range((self.length-2) // 2, -1, -1):
            self.heapify(self.length, i)
        #print(self.heap)
        #print('')

    def sort(self):
        self.build_heap()
        for i in range(self.length-1, -1, -1):
            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]
            self.heapify(i, 0)
            #print('')
        return self.heap

a = []
for i in range(101):
    a.append(random.randint(-10000, 10000))
print(a)
a = heapSort(a)
print(a.sort())