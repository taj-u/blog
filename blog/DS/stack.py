class Stack:
    def __init__(self):
        self.items = list()
    def push(self, x):
        self.items.append(x)
    def pop(self):
        self.items.pop()
    def __repr__(self):
        return str(self.items)
s = Stack()
s.push('x')
s.push('y')
s.push('z')
s.pop()
s.push('t')
print(f'{s}')