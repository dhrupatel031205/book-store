class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        """Push an item onto the stack."""
        self.stack.append(item)

    def pop(self):
        """Pop the top item off the stack."""
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        """View the top item on the stack."""
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.stack) == 0

    def to_list(self):
        """Return a list representation of the stack."""
        return self.stack.copy()


    def delete(self, item):
        """
        Delete a particular item from the stack.
        If the item is not found, raise a ValueError.
        """
        if item not in self.items:
            raise ValueError(f"Item {item} not found in stack")

        # Create a temporary stack to hold elements
        temp_stack = []
        while not self.is_empty():
            top_item = self.pop()
            if top_item == item:
                break
            temp_stack.append(top_item)

        # Push back remaining items to the original stack
        while temp_stack:
            self.push(temp_stack.pop())
