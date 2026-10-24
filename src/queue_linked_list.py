"""
Queue Data Structure Implementation (Singly Linked List)
--------------------------------------------------------
A pure Python Queue implementation adhering to the First In, First Out (FIFO) principle,
built manually using a Singly Linked List with explicit front and rear pointers.

Key Characteristics:
- FIFO (First In, First Out): The earliest inserted element is the first one removed.
- Underlying structure: Linked nodes (no Python list or deque).
- Pointers:
  * `front`: References the head node where elements leave (dequeue).
  * `rear`:  References the tail node where elements enter (enqueue).
- Time Complexity:
  * enqueue(item): O(1) (tail pointer allows direct insertion)
  * dequeue():     O(1) (head pointer allows direct removal)
  * get_front():   O(1)
  * get_rear():    O(1)
  * is_empty():    O(1)
  * size():        O(1) (tracked with count attribute)
  * clear():       O(1)
"""

from typing import Any, List, Optional


class Node:
    """
    A single node in a Singly Linked List.
    
    Attributes:
        value (Any): The payload or data stored in this node.
        next (Optional[Node]): Pointer to the subsequent node in the list.
    """

    def __init__(self, value: Any, next_node: Optional["Node"] = None):
        self.value: Any = value
        self.next: Optional["Node"] = next_node

    def __repr__(self) -> str:
        return f"Node({self.value})"


class Queue:
    """
    A bounded Queue implemented using a Singly Linked List with front and rear pointers.
    
    Attributes:
        capacity (int): Maximum capacity limit.
        front (Optional[Node]): Head pointer (exit point).
        rear (Optional[Node]): Tail pointer (entry point).
    """

    def __init__(self, capacity: int = 7):
        """
        Initialize an empty Queue with an optional capacity limit.
        
        Args:
            capacity: Maximum capacity limit (default is 7 for GUI clarity).
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity: int = capacity
        self.front: Optional[Node] = None
        self.rear: Optional[Node] = None
        self._count: int = 0

    def enqueue(self, item: Any) -> None:
        """
        Insert an element at the rear of the queue.
        
        Time Complexity: O(1).
        
        Args:
            item: The element to add.
            
        Raises:
            OverflowError: If the queue is at maximum capacity.
        """
        if self.is_full():
            raise OverflowError(f"Queue Overflow! Maximum capacity of {self.capacity} reached.")

        new_node = Node(item)
        if self.is_empty():
            # When empty, both front and rear point to the single new node
            self.front = new_node
            self.rear = new_node
        else:
            # Link current rear to new node, then advance rear pointer
            assert self.rear is not None
            self.rear.next = new_node
            self.rear = new_node

        self._count += 1

    def dequeue(self) -> Any:
        """
        Remove and return the element from the front of the queue.
        
        Time Complexity: O(1).
        
        Returns:
            The element removed from the front.
            
        Raises:
            IndexError: If the queue is empty (Queue Underflow).
        """
        if self.is_empty():
            raise IndexError("Queue Underflow! Cannot dequeue from an empty queue.")

        assert self.front is not None
        removed_value = self.front.value
        self.front = self.front.next
        self._count -= 1

        # CRITICAL POINTER INVARIANT:
        # If the queue has just become empty, rear must also be reset to None!
        if self.front is None:
            self.rear = None

        return removed_value

    def get_front(self) -> Any:
        """
        Return the element at the front of the queue without removing it.
        
        Time Complexity: O(1).
        
        Returns:
            The front element value.
            
        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot read front of an empty queue.")
        assert self.front is not None
        return self.front.value

    def get_rear(self) -> Any:
        """
        Return the element at the rear of the queue without removing it.
        
        Time Complexity: O(1).
        
        Returns:
            The rear element value.
            
        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot read rear of an empty queue.")
        assert self.rear is not None
        return self.rear.value

    def is_empty(self) -> bool:
        """
        Check if the queue contains no elements.
        
        Time Complexity: O(1).
        
        Returns:
            True if empty, False otherwise.
        """
        return self.front is None or self._count == 0

    def is_full(self) -> bool:
        """
        Check if the queue has reached its maximum capacity.
        
        Time Complexity: O(1).
        
        Returns:
            True if full, False otherwise.
        """
        return self._count >= self.capacity

    def size(self) -> int:
        """
        Return the current number of elements in the queue.
        
        Time Complexity: O(1).
        
        Returns:
            Current element count.
        """
        return self._count

    def clear(self) -> None:
        """
        Remove all elements from the queue and reset pointers.
        
        Time Complexity: O(1).
        """
        self.front = None
        self.rear = None
        self._count = 0

    def to_list(self) -> List[Any]:
        """
        Traverse the singly linked list from front to rear and return a list of values.
        
        Time Complexity: O(N) where N is queue size.
        
        Returns:
            List of values ordered from front (index 0) to rear (index -1).
        """
        values: List[Any] = []
        current = self.front
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def copy(self) -> "Queue":
        """
        Create a clone of this queue with identical elements and capacity.
        
        Returns:
            A new Queue instance containing duplicates of the elements in the same order.
        """
        cloned = Queue(capacity=self.capacity)
        for item in self.to_list():
            cloned.enqueue(item)
        return cloned

    def __repr__(self) -> str:
        return f"Queue(items={self.to_list()}, size={self.size()}/{self.capacity})"
