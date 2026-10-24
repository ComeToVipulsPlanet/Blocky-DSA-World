"""
Unit Tests for Stack Implementation
-----------------------------------
Tests:
- Initialization and capacity limits.
- Push operations and size tracking.
- LIFO (Last In, First Out) ordering on pop.
- Peek operation non-destructive behavior.
- Stack Underflow (pop and peek on empty stack).
- Stack Overflow (push beyond capacity).
- Clear operation and reuse after clear.
- Copy functionality.
"""

import unittest
from src.stack import Stack


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack(capacity=5)

    def test_initial_state(self):
        self.assertTrue(self.stack.is_empty())
        self.assertFalse(self.stack.is_full())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(self.stack.to_list(), [])

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            Stack(capacity=0)
        with self.assertRaises(ValueError):
            Stack(capacity=-3)

    def test_push_and_size(self):
        self.stack.push("Block_A")
        self.assertEqual(self.stack.size(), 1)
        self.assertFalse(self.stack.is_empty())

        self.stack.push("Block_B")
        self.assertEqual(self.stack.size(), 2)
        self.assertEqual(self.stack.to_list(), ["Block_A", "Block_B"])

    def test_lifo_order(self):
        """Verify that items pop in reverse order of insertion (Last In, First Out)."""
        items = [10, 20, 30, 40]
        for x in items:
            self.stack.push(x)

        self.assertEqual(self.stack.pop(), 40)
        self.assertEqual(self.stack.pop(), 30)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)
        self.assertTrue(self.stack.is_empty())

    def test_peek_behavior(self):
        """Peek must inspect the top element without removing it or altering size."""
        self.stack.push("Alpha")
        self.stack.push("Beta")

        self.assertEqual(self.stack.peek(), "Beta")
        self.assertEqual(self.stack.size(), 2)
        self.assertEqual(self.stack.peek(), "Beta")  # Repeated peek should return same
        self.assertEqual(self.stack.size(), 2)

    def test_empty_stack_exceptions(self):
        """Pop or peek on empty stack must raise IndexError (Stack Underflow)."""
        with self.assertRaises(IndexError):
            self.stack.pop()

        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_stack_overflow(self):
        """Pushing beyond capacity must raise OverflowError."""
        for i in range(5):
            self.stack.push(i)
        self.assertTrue(self.stack.is_full())

        with self.assertRaises(OverflowError):
            self.stack.push(999)

    def test_clear_and_reuse(self):
        self.stack.push("X")
        self.stack.push("Y")
        self.assertEqual(self.stack.size(), 2)

        self.stack.clear()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

        # Ensure stack is fully reusable after clearing
        self.stack.push("Z")
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), "Z")
        self.assertEqual(self.stack.pop(), "Z")
        self.assertTrue(self.stack.is_empty())

    def test_copy(self):
        self.stack.push(1)
        self.stack.push(2)
        cloned = self.stack.copy()

        self.assertEqual(cloned.to_list(), [1, 2])
        self.assertEqual(cloned.capacity, 5)

        # Mutating original should not affect clone
        self.stack.push(3)
        self.assertEqual(cloned.size(), 2)
        self.assertEqual(self.stack.size(), 3)


if __name__ == "__main__":
    unittest.main()
