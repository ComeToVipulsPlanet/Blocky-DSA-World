"""
Stack Data Structure Implementation
-----------------------------------
A pure Python Stack implementation adhering to the Last In, First Out (LIFO) principle.

Key Characteristics:
- LIFO (Last In, First Out): The most recently added element is the first one removed.
- Underlying storage: Python standard list (`self._items`).
- Time Complexity:
  * push(item): O(1) amortized
  * pop():      O(1)
  * peek():     O(1)
  * is_empty(): O(1)
  * size():     O(1)
  * clear():    O(1)
"""

from typing import Any, List, Optional


class Stack:
    """
    A bounded Stack data structure using an internal Python list.
    
    Attributes:
        capacity (int): Maximum number of elements allowed in the stack.
    """

    def __init__(self, capacity: int = 7):
        """
        Initialize an empty Stack with an optional capacity limit.
        
        Args:
            capacity: Maximum number of elements allowed (default is 7 for GUI clarity).
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity: int = capacity
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        """
        Push an element onto the top of the stack.
        
        Time Complexity: O(1) amortized.
        
        Args:
            item: The element to add.
            
        Raises:
            OverflowError: If the stack has reached its maximum capacity.
        """
        if self.is_full():
            raise OverflowError(f"Stack Overflow! Maximum capacity of {self.capacity} reached.")
        self._items.append(item)

    def pop(self) -> Any:
        """
        Remove and return the element at the top of the stack.
        
        Time Complexity: O(1).
        
        Returns:
            The element popped from the top of the stack.
            
        Raises:
            IndexError: If the stack is empty (Stack Underflow).
        """
        if self.is_empty():
            raise IndexError("Stack Underflow! Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> Any:
        """
        Return the element at the top of the stack without removing it.
        
        Time Complexity: O(1).
        
        Returns:
            The top element.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Check if the stack contains no elements.
        
        Time Complexity: O(1).
        
        Returns:
            True if empty, False otherwise.
        """
        return len(self._items) == 0

    def is_full(self) -> bool:
        """
        Check if the stack has reached its maximum capacity.
        
        Time Complexity: O(1).
        
        Returns:
            True if full, False otherwise.
        """
        return len(self._items) >= self.capacity

    def size(self) -> int:
        """
        Return the current number of elements in the stack.
        
        Time Complexity: O(1).
        
        Returns:
            Current count of elements.
        """
        return len(self._items)

    def clear(self) -> None:
        """
        Remove all elements from the stack.
        
        Time Complexity: O(1).
        """
        self._items.clear()

    def to_list(self) -> List[Any]:
        """
        Return a copy of the stack elements from bottom (index 0) to top (last index).
        Useful for visualization and snapshotting.
        
        Returns:
            A shallow copy of the internal items list.
        """
        return list(self._items)

    def copy(self) -> "Stack":
        """
        Create a clone of this stack with the same capacity and elements.
        
        Returns:
            A new Stack instance containing the same elements.
        """
        cloned = Stack(capacity=self.capacity)
        cloned._items = list(self._items)
        return cloned

    def __repr__(self) -> str:
        return f"Stack(items={self._items}, size={self.size()}/{self.capacity})"
