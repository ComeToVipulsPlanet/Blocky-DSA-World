"""
Unit Tests for Manual Binary Search Tree (BST)
----------------------------------------------
Tests Node creation, insertion, duplicate rejection, search, deletion (all 3 cases),
Inorder, Preorder, Postorder traversals, height, min, max, and layout calculations.
"""

import unittest
from src.bst import Node, BinarySearchTree


class TestBST(unittest.TestCase):

    def setUp(self):
        self.bst = BinarySearchTree()

    def test_node_creation(self):
        """Verify Node attributes value, left, right."""
        node = Node(50)
        self.assertEqual(node.value, 50)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertTrue(node.is_leaf())

    def test_sample_tree_insertion_and_traversals(self):
        """
        Verify the exact sample tree specified in the requirements:
        Values inserted: 50, 30, 70, 20, 40, 60, 80
        Structure:
                      50
                    /    \\
                  30      70
                 /  \\    /  \\
                20  40  60  80
        Expected:
        - Inorder: [20, 30, 40, 50, 60, 70, 80]
        - Preorder: [50, 30, 20, 40, 70, 60, 80]
        - Postorder: [20, 40, 30, 60, 80, 70, 50]
        """
        values = [50, 30, 70, 20, 40, 60, 80]
        for val in values:
            success, steps, path = self.bst.insert(val)
            self.assertTrue(success)

        self.assertEqual(self.bst.size(), 7)
        self.assertEqual(self.bst.height(), 3)
        self.assertEqual(self.bst.root.value, 50)

        # Inorder traversal
        inorder_result = self.bst.inorder()
        self.assertEqual(inorder_result, [20, 30, 40, 50, 60, 70, 80])

        # Preorder traversal
        preorder_result = self.bst.preorder()
        self.assertEqual(preorder_result, [50, 30, 20, 40, 70, 60, 80])

        # Postorder traversal
        postorder_result = self.bst.postorder()
        self.assertEqual(postorder_result, [20, 40, 30, 60, 80, 70, 50])

    def test_duplicate_rejection(self):
        """Verify duplicate values are rejected with appropriate message and path."""
        self.bst.insert(50)
        self.bst.insert(30)
        success, steps, path = self.bst.insert(50)
        self.assertFalse(success)
        self.assertIn("Duplicate rejected", steps[-1])
        self.assertEqual(self.bst.size(), 2)

        # Duplicate of non-root
        success2, steps2, path2 = self.bst.insert(30)
        self.assertFalse(success2)
        self.assertIn("Duplicate rejected", steps2[-1])
        self.assertEqual(self.bst.size(), 2)

    def test_search_existing_and_missing(self):
        """Verify search for root, inner nodes, leaves, and non-existent values."""
        for v in [50, 30, 70, 20, 40]:
            self.bst.insert(v)

        # Search existing
        found, steps, path = self.bst.search(40)
        self.assertTrue(found)
        self.assertEqual(path, [50, 30, 40])
        self.assertIn("Match found", steps[-1])

        # Search missing
        found_miss, steps_miss, path_miss = self.bst.search(99)
        self.assertFalse(found_miss)
        self.assertEqual(path_miss, [50, 70])
        self.assertIn("not found", steps_miss[-1])

        # Search in empty tree
        empty_bst = BinarySearchTree()
        found_emp, steps_emp, path_emp = empty_bst.search(10)
        self.assertFalse(found_emp)

    def test_delete_leaf_node(self):
        """Case 1: Delete a leaf node."""
        for v in [50, 30, 70, 20, 40]:
            self.bst.insert(v)

        success, steps, path = self.bst.delete(20)
        self.assertTrue(success)
        self.assertEqual(self.bst.inorder(), [30, 40, 50, 70])
        self.assertIsNone(self.bst.root.left.left)

    def test_delete_single_child_node(self):
        """Case 2: Delete a node with one child."""
        for v in [50, 30, 70, 20]:
            self.bst.insert(v)
        # 30 has only left child (20)
        success, steps, path = self.bst.delete(30)
        self.assertTrue(success)
        self.assertEqual(self.bst.inorder(), [20, 50, 70])
        self.assertEqual(self.bst.root.left.value, 20)

    def test_delete_two_children_node(self):
        """Case 3: Delete a node with two children (inorder successor replacement)."""
        values = [50, 30, 70, 20, 40, 60, 80]
        for v in values:
            self.bst.insert(v)

        # Delete root (50) with two children
        success, steps, path = self.bst.delete(50)
        self.assertTrue(success)
        # Inorder successor of 50 is 60
        self.assertEqual(self.bst.root.value, 60)
        self.assertEqual(self.bst.inorder(), [20, 30, 40, 60, 70, 80])

        # Delete 70 which has two children (none and 80? wait, 60 was removed from right, so 70 has right 80)
        # Let's delete 30 which still has two children (20 and 40)
        success2, steps2, path2 = self.bst.delete(30)
        self.assertTrue(success2)
        # Inorder successor of 30 is 40
        self.assertEqual(self.bst.inorder(), [20, 40, 60, 70, 80])

    def test_clear_tree(self):
        """Verify clear resets tree to empty state."""
        for v in [50, 30, 70]:
            self.bst.insert(v)
        self.assertFalse(self.bst.is_empty())
        self.bst.clear()
        self.assertTrue(self.bst.is_empty())
        self.assertEqual(self.bst.size(), 0)
        self.assertEqual(self.bst.height(), 0)
        self.assertEqual(self.bst.inorder(), [])

    def test_min_and_max(self):
        """Verify min and max computations."""
        self.assertIsNone(self.bst.get_min())
        self.assertIsNone(self.bst.get_max())

        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(v)

        self.assertEqual(self.bst.get_min(), 20)
        self.assertEqual(self.bst.get_max(), 80)

    def test_layout_calculation_non_overlapping(self):
        """Verify layout calculation positions all nodes without overlapping."""
        values = [50, 30, 70, 20, 40, 60, 80]
        for v in values:
            self.bst.insert(v)

        layout = self.bst.calculate_layout(canvas_width=800, canvas_height=500)
        self.assertEqual(len(layout), 7)

        # Check all nodes have coordinates
        for v in values:
            self.assertIn(v, layout)
            x, y, depth = layout[v]
            self.assertGreater(x, 0)
            self.assertGreater(y, 0)

        # Check horizontal monotonicity of inorder keys:
        # 20 < 30 < 40 < 50 < 60 < 70 < 80
        inorder = self.bst.inorder()
        for i in range(len(inorder) - 1):
            curr_x = layout[inorder[i]][0]
            next_x = layout[inorder[i + 1]][0]
            self.assertLess(curr_x, next_x, f"Node {inorder[i]} should be strictly left of {inorder[i+1]}")


if __name__ == "__main__":
    unittest.main()
