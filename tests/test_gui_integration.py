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

    def test_infix_mode_switch(self):
        """Verify switching to Infix to Postfix Kingdom adjusts UI and visualizer."""
        self.app.switch_mode("INFIX")
        self.app.update()
        self.assertEqual(self.app.current_mode, "INFIX")
        self.assertEqual(self.app.visualizer.mode, "INFIX")
        self.assertEqual(self.app.btn_nav_infix.cget("bg"), "#D97706")
        self.assertEqual(self.app.frame_infix_ctrl.winfo_manager(), "pack")
        self.assertEqual(self.app.frame_infix_info.winfo_manager(), "pack")

    def test_infix_expression_conversion(self):
        """Verify converting custom expressions via GUI populates steps and result."""
        self.app.switch_mode("INFIX")
        self.app.on_infix_convert("A+B*C")
        self.app.update()
        self.assertEqual(self.app.infix_last_result, "A B C * +")
        self.assertGreater(len(self.app.infix_steps), 3)
        self.assertEqual(self.app.entry_infix_result.get(), "A B C * +")

    def test_infix_sample_buttons(self):
        """Verify loading all 6 university benchmark sample expressions."""
        self.app.switch_mode("INFIX")
        samples = [
            ("A+B*C", "A B C * +"),
            ("(A+B)*C", "A B + C *"),
            ("A+B*(C-D)", "A B C D - * +"),
            ("A^B^C", "A B C ^ ^"),
            ("(A+B)*(C-D)", "A B + C D - *"),
            ("A+B*C-D/E", "A B C * + D E / -"),
        ]
        for expr_str, expected in samples:
            self.app.on_infix_sample(expr_str)
            self.app.update()
            self.assertEqual(self.app.infix_last_result, expected)

    def test_infix_step_navigation(self):
        """Verify Next, Prev, Skip, and Reset operations in Infix Kingdom."""
        self.app.switch_mode("INFIX")
        self.app.on_infix_sample("A+B")
        self.app.update()
        self.assertEqual(self.app.infix_current_step_idx, 0)

        # Step forward
        self.app.infix_speed_ms = 0
        self.app.on_infix_next_step(from_play=False)
        self.app.update()
        self.assertEqual(self.app.infix_current_step_idx, 1)

        # Step backward
        self.app.on_infix_prev_step()
        self.app.update()
        self.assertEqual(self.app.infix_current_step_idx, 0)

        # Skip to end
        self.app.on_infix_skip_to_end()
        self.app.update()
        self.assertEqual(self.app.infix_current_step_idx, len(self.app.infix_steps) - 1)

        # Reset
        self.app.on_infix_reset()
        self.app.update()
        self.assertEqual(self.app.infix_current_step_idx, 0)

    def test_infix_challenge_mode(self):
        """Verify Challenge Mode random generation and answer evaluation."""
        self.app.switch_mode("INFIX")
        self.app.challenge_difficulty = "easy"
        self.app.on_challenge_new()
        self.app.update()

        target = self.app.challenge_target_expr
        expected = self.app.challenge_expected_postfix
        self.assertTrue(len(target) > 0)
        self.assertTrue(len(expected) > 0)

        # Correct answer submission
        self.app.entry_challenge_answer.delete(0, tk.END)
        self.app.entry_challenge_answer.insert(0, expected)
        self.app.on_challenge_submit()
        self.app.update()
        self.assertEqual(self.app.challenge_correct, 1)
        self.assertEqual(self.app.challenge_attempts, 1)

        # Incorrect answer submission
        self.app.entry_challenge_answer.delete(0, tk.END)
        self.app.entry_challenge_answer.insert(0, "WRONG ANSWER")
        self.app.on_challenge_submit()
        self.app.update()
        self.assertEqual(self.app.challenge_correct, 1)
        self.assertEqual(self.app.challenge_attempts, 2)

    def test_infix_portals_and_scenarios(self):
        """Verify portal interactions and scenario switching."""
        self.app.load_preset_scenario("INFIX")
        self.app.update()
        self.assertEqual(self.app.current_mode, "INFIX")
        self.assertEqual(self.app.infix_last_result, "A B C D - * +")

        # Portal Return callback
        self.app.visualizer.on_portal_return()
        self.app.update()
        self.assertEqual(self.app.current_mode, "STACK_QUEUE")


if __name__ == "__main__":
    unittest.main()

