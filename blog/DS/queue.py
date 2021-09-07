class Queue:
    def __init__(self, size):
        self.max_size = size
        self.head, self.tail, self.size = 0, 0, 0
        self.li = [0] * size
    def enqueue(self, x):
        self.li[self.tail] = x
        self.tail = (self.tail + 1) % self.max_size
        self.size += 1
    def dequeue(self):
        item = self.li[self.head]
        self.head = (self.head + 1) % self.max_size
        self.size -= 1
        return item
    def __str__(self):
        return str(self.li[self.head:self.tail])
q = Queue(3)
q.enqueue('T')
q.enqueue('x')
q.enqueue('T')
print(q.dequeue())
print(q)
