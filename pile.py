class Stack:
    """Simple stack used by the maze generation algorithm."""

    def __init__(self):
        """Create an empty stack backed by a Python list."""
        self.items = []

    def is_empty(self):
        """Return True when the stack has no elements."""
        return self.items == []

    def push(self, value):
        """Push a value onto the top of the stack."""
        self.items.append(value)

    def pop(self):
        """Remove and return the top value of the stack."""
        if not self.is_empty():
            return self.items.pop()
        print("Stack is empty!")

    def size(self):
        """Return the number of elements in the stack."""
        return len(self.items)

    def top(self):
        """Return the top value without removing it."""
        if not self.is_empty():
            return self.items[-1]
        print("Stack is empty!")
