"""
Unit Tests for Queue Implementation (Singly Linked List)
--------------------------------------------------------
Tests:
- Initialization and capacity limits.
- Enqueue operations and size tracking.
- FIFO (First In, First Out) ordering on dequeue.
- Front and Rear pointers accuracy.
- Single element queue behaviour.
- Removing final element resets rear pointer to None.
- Reusing queue after it is emptied.
- Queue Underflow exceptions (dequeue, get_front, get_rear on empty queue).
- Queue Overflow (enqueue beyond capacity).
- Clear operation and pointer reset.
- Node structure verification.
"""

import unittest
from src.queue_linked_list import Queue, Node


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue(capacity=5)

    def test_node_creation(self):
        node = Node("Data", None)
        self.assertEqual(node.value, "Data")
        self.assertIsNone(node.next)

        node2 = Node("NextData", node)
        self.assertEqual(node2.value, "NextData")
        self.assertEqual(node2.next, node)

    def test_initial_state(self):
        self.assertTrue(self.queue.is_empty())
        self.assertFalse(self.queue.is_full())
        self.assertEqual(self.queue.size(), 0)
        self.assertIsNone(self.queue.front)
        self.assertIsNone(self.queue.rear)
        self.assertEqual(self.queue.to_list(), [])

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            Queue(capacity=0)
        with self.assertRaises(ValueError):
            Queue(capacity=-5)

    def test_enqueue_and_size(self):
        self.queue.enqueue(10)
        self.assertEqual(self.queue.size(), 1)
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.get_front(), 10)
        self.assertEqual(self.queue.get_rear(), 10)

        self.queue.enqueue(20)
        self.assertEqual(self.queue.size(), 2)
        self.assertEqual(self.queue.get_front(), 10)
        self.assertEqual(self.queue.get_rear(), 20)
        self.assertEqual(self.queue.to_list(), [10, 20])

    def test_fifo_order(self):
        """Verify that elements dequeue in the exact order they were enqueued (FIFO)."""
        items = ["First", "Second", "Third", "Fourth"]
        for it in items:
            self.queue.enqueue(it)

        self.assertEqual(self.queue.dequeue(), "First")
        self.assertEqual(self.queue.dequeue(), "Second")
        self.assertEqual(self.queue.dequeue(), "Third")
        self.assertEqual(self.queue.dequeue(), "Fourth")
        self.assertTrue(self.queue.is_empty())

    def test_front_and_rear_access(self):
        """Ensure get_front and get_rear do not remove elements."""
        self.queue.enqueue("A")
        self.queue.enqueue("B")
        self.queue.enqueue("C")

        self.assertEqual(self.queue.get_front(), "A")
        self.assertEqual(self.queue.get_rear(), "C")
        self.assertEqual(self.queue.size(), 3)
        self.assertEqual(self.queue.to_list(), ["A", "B", "C"])

    def test_single_element_removal_resets_rear(self):
        """
        CRITICAL TEST: When the final element in the queue is dequeued,
        both self.front and self.rear MUST be reset to None!
        """
        self.queue.enqueue("Solo")
        self.assertIsNotNone(self.queue.front)
        self.assertIsNotNone(self.queue.rear)
        self.assertEqual(self.queue.front, self.queue.rear)

        removed = self.queue.dequeue()
        self.assertEqual(removed, "Solo")
        self.assertEqual(self.queue.size(), 0)
        self.assertTrue(self.queue.is_empty())
        self.assertIsNone(self.queue.front, "Front pointer should be None after emptying")
        self.assertIsNone(self.queue.rear, "Rear pointer should be None after emptying")

    def test_reuse_after_empty(self):
        """Queue should be completely reusable after being drained to empty."""
        self.queue.enqueue(1)
        self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())

        # Re-populate
        self.queue.enqueue("New_A")
        self.queue.enqueue("New_B")
        self.assertEqual(self.queue.size(), 2)
        self.assertEqual(self.queue.get_front(), "New_A")
        self.assertEqual(self.queue.get_rear(), "New_B")
        self.assertEqual(self.queue.dequeue(), "New_A")
        self.assertEqual(self.queue.dequeue(), "New_B")
        self.assertTrue(self.queue.is_empty())
        self.assertIsNone(self.queue.front)
        self.assertIsNone(self.queue.rear)

    def test_empty_queue_exceptions(self):
        """Empty queue operations must raise IndexError."""
        with self.assertRaises(IndexError):
            self.queue.dequeue()

        with self.assertRaises(IndexError):
            self.queue.get_front()

        with self.assertRaises(IndexError):
            self.queue.get_rear()

    def test_queue_overflow(self):
        """Enqueuing past capacity must raise OverflowError."""
        for i in range(5):
            self.queue.enqueue(f"Item_{i}")
        self.assertTrue(self.queue.is_full())

        with self.assertRaises(OverflowError):
            self.queue.enqueue("Extra")

    def test_clear_and_pointers(self):
        self.queue.enqueue("P")
        self.queue.enqueue("Q")
        self.assertEqual(self.queue.size(), 2)

        self.queue.clear()
        self.assertEqual(self.queue.size(), 0)
        self.assertTrue(self.queue.is_empty())
        self.assertIsNone(self.queue.front)
        self.assertIsNone(self.queue.rear)
        self.assertEqual(self.queue.to_list(), [])

    def test_copy(self):
        self.queue.enqueue("Alpha")
        self.queue.enqueue("Beta")
        cloned = self.queue.copy()

        self.assertEqual(cloned.to_list(), ["Alpha", "Beta"])
        self.assertEqual(cloned.size(), 2)
        self.assertEqual(cloned.capacity, 5)

        self.queue.enqueue("Gamma")
        self.assertEqual(cloned.size(), 2)
        self.assertEqual(self.queue.size(), 3)


if __name__ == "__main__":
    unittest.main()
