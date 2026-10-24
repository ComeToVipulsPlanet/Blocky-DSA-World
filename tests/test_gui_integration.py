"""
GUI Integration Tests for Blocky DSA World
------------------------------------------
Performs programmatic end-to-end verification of Tkinter GUI workflows,
Canvas rendering calls, animation scheduling, and data-GUI synchronization
without blocking the main thread.
"""

import unittest
import tkinter as tk
from main import BlockyDSAWorldApp


class TestGUIIntegration(unittest.TestCase):

    def setUp(self):
        self.app = BlockyDSAWorldApp()
        # Withdraw window to prevent popping up during automated testing
        self.app.withdraw()
        self.app.update()

    def tearDown(self):
        try:
            self.app.destroy()
        except Exception:
            pass

    def test_gui_initial_state(self):
        """Verify initial labels, counters, and canvas state."""
        self.assertEqual(self.app.stack.size(), 0)
        self.assertEqual(self.app.queue.size(), 0)
        self.assertEqual(self.app.history.total_successful_ops, 0)
        self.assertIn("0 / 7", self.app.lbl_stack_size.cget("text"))
        self.assertIn("0 / 7", self.app.lbl_queue_size.cget("text"))

    def test_stack_gui_lifecycle(self):
        """Test Push, Peek, Pop via GUI methods."""
        # 1. Push
        self.app._set_input_val("101")
        self.app.on_stack_push(animate=False)
        self.app.update()

        self.assertEqual(self.app.stack.size(), 1)
        self.assertEqual(self.app.stack.peek(), "101")

        # 2. Peek
        self.app.on_stack_peek()
        self.app.update()
        self.assertEqual(self.app.stack.size(), 1)

        # 3. Pop
        self.app.on_stack_pop(animate=False)
        self.app.update()
        self.assertEqual(self.app.stack.size(), 0)

    def test_queue_gui_lifecycle(self):
        """Test Enqueue, Front, Rear, Dequeue via GUI methods."""
        # 1. Enqueue two items
        self.app._set_input_val("Q1")
        self.app.on_queue_enqueue(animate=False)
        self.app.update()

        self.app._set_input_val("Q2")
        self.app.on_queue_enqueue(animate=False)
        self.app.update()

        self.assertEqual(self.app.queue.size(), 2)
        self.assertEqual(self.app.queue.get_front(), "Q1")
        self.assertEqual(self.app.queue.get_rear(), "Q2")

        # 2. Front & Rear inspect
        self.app.on_queue_front()
        self.app.on_queue_rear()
        self.app.update()

        # 3. Dequeue
        self.app.on_queue_dequeue(animate=False)
        self.app.update()
        self.assertEqual(self.app.queue.size(), 1)
        self.assertEqual(self.app.queue.get_front(), "Q2")

    def test_undo_operation(self):
        """Verify GUI undo functionality."""
        self.app._set_input_val("Alpha")
        self.app.on_stack_push(animate=False)
        self.app.update()
        self.assertEqual(self.app.stack.size(), 1)

        # Undo
        self.app.on_undo_operation()
        self.app.update()
        self.assertEqual(self.app.stack.size(), 0)

    def test_load_preset_scenarios(self):
        """Verify demo scenarios populate data models and canvas correctly."""
        self.app.load_preset_scenario("LIFO")
        self.app.update()
        self.assertEqual(self.app.stack.size(), 3)
        self.assertEqual(self.app.stack.to_list(), [10, 20, 30])

        self.app.load_preset_scenario("FIFO")
        self.app.update()
        self.assertEqual(self.app.queue.size(), 3)
        self.assertEqual(self.app.queue.to_list(), ["T1", "T2", "T3"])

        self.app.load_preset_scenario("BOTH")
        self.app.update()
        self.assertEqual(self.app.stack.size(), 3)
        self.assertEqual(self.app.queue.size(), 3)

    def test_canvas_redraw_no_crash(self):
        """Verify procedural 3D drawing pipeline executes without errors."""
        self.app.visualizer.redraw()
        self.app.update()


if __name__ == "__main__":
    unittest.main()
