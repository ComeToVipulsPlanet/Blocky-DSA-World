"""
Binary Search Tree (BST) Module — Pure Python Implementation
-----------------------------------------------------------
Implements a manual Binary Search Tree (BST) using Python classes, objects,
and references. Strictly no third-party or built-in tree data structure libraries.

Classes:
    Node: Represents a single node with `value`, `left`, and `right` references.
    BinarySearchTree: Manual BST operations (insert, search, delete, traversals,
                      depth/height calculation, layout coordinates for 3D rendering).
"""

from typing import Any, Dict, List, Optional, Tuple


class Node:
    """
    Represents a single node in the Binary Search Tree.

    Attributes:
        value (int): Integer key stored in the node.
        left (Optional[Node]): Reference to left child (contains keys < value).
        right (Optional[Node]): Reference to right child (contains keys > value).
    """

    def __init__(self, value: int):
        self.value: int = int(value)
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

    def is_leaf(self) -> bool:
        """Return True if this node has neither left nor right child."""
        return self.left is None and self.right is None

    def __repr__(self) -> str:
        return f"Node({self.value})"


class BinarySearchTree:
    """
    Manual Binary Search Tree implementation with educational telemetry
    and 3D layout calculation.
    """

    def __init__(self):
        self.root: Optional[Node] = None

    # -------------------------------------------------------------------------
    # CORE OPERATIONS: INSERT, SEARCH, DELETE
    # -------------------------------------------------------------------------
    def insert(self, value: int) -> Tuple[bool, List[str], List[int]]:
        """
        Manually inserts an integer value into the BST.
        Duplicates are strictly rejected.

        Returns:
            Tuple of:
                - success (bool): True if inserted, False if duplicate.
                - comparison_steps (List[str]): Step-by-step decision trail.
                - path_values (List[int]): Sequence of node values visited.
        """
        val = int(value)
        steps: List[str] = []
        path: List[int] = []

        if self.root is None:
            self.root = Node(val)
            steps.append(f"Tree is empty. Created root node with value {val}.")
            path.append(val)
            return True, steps, path

        curr = self.root
        while True:
            path.append(curr.value)
            steps.append(f"Comparing {val} with {curr.value}")

            if val == curr.value:
                steps.append(f"Value {val} already exists! Duplicate rejected.")
                return False, steps, path

            elif val < curr.value:
                steps.append(f"{val} is smaller than {curr.value} — move left")
                if curr.left is None:
                    curr.left = Node(val)
                    path.append(val)
                    steps.append(f"Found empty left position. Node {val} inserted successfully!")
                    return True, steps, path
                curr = curr.left

            else:  # val > curr.value
                steps.append(f"{val} is greater than {curr.value} — move right")
                if curr.right is None:
                    curr.right = Node(val)
                    path.append(val)
                    steps.append(f"Found empty right position. Node {val} inserted successfully!")
                    return True, steps, path
                curr = curr.right

    def search(self, value: int) -> Tuple[bool, List[str], List[int]]:
        """
        Manually searches for an integer value in the BST.

        Returns:
            Tuple of:
                - found (bool): True if value exists, False otherwise.
                - comparison_steps (List[str]): Decision trail for each step.
                - path_values (List[int]): Nodes visited during search.
        """
        val = int(value)
        steps: List[str] = []
        path: List[int] = []

        if self.root is None:
            steps.append("Tree is empty. Value not found.")
            return False, steps, path

        curr = self.root
        while curr is not None:
            path.append(curr.value)
            steps.append(f"Comparing {val} with {curr.value}")

            if val == curr.value:
                steps.append(f"Match found! Node {val} exists in the BST.")
                return True, steps, path
            elif val < curr.value:
                steps.append(f"{val} is smaller than {curr.value} — move left")
                if curr.left is None:
                    steps.append(f"Left child is empty. Value {val} not found.")
                    return False, steps, path
                curr = curr.left
            else:
                steps.append(f"{val} is greater than {curr.value} — move right")
                if curr.right is None:
                    steps.append(f"Right child is empty. Value {val} not found.")
                    return False, steps, path
                curr = curr.right

        return False, steps, path

    def delete(self, value: int) -> Tuple[bool, List[str], List[int]]:
        """
        Manually deletes an integer value from the BST using standard 3-case deletion:
        Case 1: Leaf node (simply remove).
        Case 2: One child (bypass node and attach child to parent).
        Case 3: Two children (replace with inorder successor, then delete successor).

        Returns:
            Tuple of:
                - success (bool): True if deleted, False if not found.
                - steps (List[str]): Explanation of deletion steps.
                - path_values (List[int]): Path followed to find the node.
        """
        val = int(value)
        steps: List[str] = []
        path: List[int] = []

        if self.root is None:
            steps.append("Tree is empty. Nothing to delete.")
            return False, steps, path

        parent: Optional[Node] = None
        curr: Optional[Node] = self.root

        # 1. Locate node and its parent
        while curr is not None and curr.value != val:
            path.append(curr.value)
            steps.append(f"Searching for {val}: current node {curr.value}")
            parent = curr
            if val < curr.value:
                curr = curr.left
            else:
                curr = curr.right

        if curr is None:
            steps.append(f"Value {val} was not found in the BST. Deletion aborted.")
            return False, steps, path

        path.append(curr.value)
        steps.append(f"Found node {val} to delete.")

        # Case 1: Node has no children (Leaf node)
        if curr.left is None and curr.right is None:
            steps.append(f"Node {val} is a leaf node (0 children). Removing reference.")
            if parent is None:
                self.root = None
            elif parent.left is curr:
                parent.left = None
            else:
                parent.right = None

        # Case 2: Node has only one child
        elif curr.left is None or curr.right is None:
            child = curr.left if curr.left is not None else curr.right
            steps.append(f"Node {val} has 1 child ({child.value}). Splicing child to parent.")
            if parent is None:
                self.root = child
            elif parent.left is curr:
                parent.left = child
            else:
                parent.right = child

        # Case 3: Node has two children
        else:
            steps.append(f"Node {val} has 2 children. Finding inorder successor (min in right subtree).")
            # Inorder successor: smallest node in right subtree
            succ_parent = curr
            succ = curr.right
            while succ.left is not None:
                succ_parent = succ
                succ = succ.left

            steps.append(f"Inorder successor is {succ.value}. Replacing {val} with {succ.value}.")
            curr.value = succ.value

            # Remove successor node (which has at most one right child)
            if succ_parent.left is succ:
                succ_parent.left = succ.right
            else:
                succ_parent.right = succ.right

            steps.append(f"Removed inorder successor node {succ.value}. Deletion complete.")

        return True, steps, path

    # -------------------------------------------------------------------------
    # TRAVERSALS (MANUAL RECURSION)
    # -------------------------------------------------------------------------
    def inorder(self) -> List[int]:
        """
        Inorder Traversal: Left -> Root -> Right.
        Produces sorted order in a valid BST.
        """
        result: List[int] = []

        def _traverse(node: Optional[Node]) -> None:
            if node is not None:
                _traverse(node.left)
                result.append(node.value)
                _traverse(node.right)

        _traverse(self.root)
        return result

    def preorder(self) -> List[int]:
        """
        Preorder Traversal: Root -> Left -> Right.
        Useful for copying or serializing tree structure.
        """
        result: List[int] = []

        def _traverse(node: Optional[Node]) -> None:
            if node is not None:
                result.append(node.value)
                _traverse(node.left)
                _traverse(node.right)

        _traverse(self.root)
        return result

    def postorder(self) -> List[int]:
        """
        Postorder Traversal: Left -> Right -> Root.
        Useful for bottom-up operations (e.g. freeing memory or evaluating expressions).
        """
        result: List[int] = []

        def _traverse(node: Optional[Node]) -> None:
            if node is not None:
                _traverse(node.left)
                _traverse(node.right)
                result.append(node.value)

        _traverse(self.root)
        return result

    # -------------------------------------------------------------------------
    # TREE METRICS & UTILITIES
    # -------------------------------------------------------------------------
    def clear(self) -> None:
        """Clear all nodes from the tree."""
        self.root = None

    def is_empty(self) -> bool:
        """Check if tree has no nodes."""
        return self.root is None

    def size(self) -> int:
        """Return total number of nodes in the BST."""
        def _count(node: Optional[Node]) -> int:
            if node is None:
                return 0
            return 1 + _count(node.left) + _count(node.right)

        return _count(self.root)

    def height(self) -> int:
        """
        Return the height of the tree (number of levels).
        Empty tree has height 0; root-only tree has height 1.
        """
        def _calc_height(node: Optional[Node]) -> int:
            if node is None:
                return 0
            return 1 + max(_calc_height(node.left), _calc_height(node.right))

        return _calc_height(self.root)

    def get_min(self) -> Optional[int]:
        """Return the minimum value (leftmost node) or None if empty."""
        if self.root is None:
            return None
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.value

    def get_max(self) -> Optional[int]:
        """Return the maximum value (rightmost node) or None if empty."""
        if self.root is None:
            return None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.value

    def is_balanced(self) -> bool:
        """
        Check if the tree is height-balanced (height difference between
        subtrees of any node is at most 1).
        """
        def _check(node: Optional[Node]) -> Tuple[bool, int]:
            if node is None:
                return True, 0
            left_bal, left_h = _check(node.left)
            right_bal, right_h = _check(node.right)
            balanced = left_bal and right_bal and abs(left_h - right_h) <= 1
            return balanced, 1 + max(left_h, right_h)

        bal, _ = _check(self.root)
        return bal

    def to_list(self) -> List[int]:
        """Return level-order list of values for state snapshots."""
        if self.root is None:
            return []
        res: List[int] = []
        queue: List[Node] = [self.root]
        while queue:
            curr = queue.pop(0)
            res.append(curr.value)
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        return res

    def get_all_edges(self) -> List[Tuple[Node, Node, str]]:
        """
        Returns list of all directed parent-child edges:
        [(parent_node, child_node, "L"|"R"), ...]
        """
        edges: List[Tuple[Node, Node, str]] = []
        if self.root is None:
            return edges

        def _collect(node: Node) -> None:
            if node.left is not None:
                edges.append((node, node.left, "L"))
                _collect(node.left)
            if node.right is not None:
                edges.append((node, node.right, "R"))
                _collect(node.right)

        _collect(self.root)
        return edges

    # -------------------------------------------------------------------------
    # 2D/3D VISUAL LAYOUT CALCULATION (NON-OVERLAPPING)
    # -------------------------------------------------------------------------
    def calculate_layout(
        self,
        canvas_width: int,
        canvas_height: int,
        node_width: int = 52,
        node_height: int = 34
    ) -> Dict[int, Tuple[float, float, int]]:
        """
        Calculates 2D canvas coordinates (x, y, depth) for every node in the BST
        guaranteeing non-overlapping positioning.

        Algorithm:
            1. Assign horizontal x coordinate based on inorder traversal index
               multiplied by uniform spacing. In a BST, inorder traversal produces
               strictly ascending keys, so left children are always to the left
               of parent, and right children are always to the right.
            2. Assign vertical y coordinate based on tree depth.
            3. Center the entire computed tree bounding box horizontally in canvas.

        Returns:
            Dict mapping node.value -> (x, y, depth)
        """
        positions: Dict[int, Tuple[float, float, int]] = {}
        if self.root is None:
            return positions

        tree_h = self.height()
        total_nodes = self.size()

        # Inorder ordering for strictly monotonic X
        inorder_nodes: List[Node] = []

        def _get_inorder(node: Optional[Node], depth: int) -> None:
            if node is not None:
                _get_inorder(node.left, depth + 1)
                inorder_nodes.append((node, depth))
                _get_inorder(node.right, depth + 1)

        _get_inorder(self.root, 0)

        # Dynamic spacing based on available width and count
        available_w = max(400, canvas_width - 120)
        col_spacing = max(node_width + 16, min(88, available_w / max(1, total_nodes)))

        # Vertical spacing based on height
        top_margin = 72.0
        bottom_margin = 130.0  # leave room for avatar/terrain at bottom
        available_h = max(200, canvas_height - top_margin - bottom_margin)
        level_gap = max(58.0, min(86.0, available_h / max(1, tree_h)))

        # Assign raw coordinates
        raw_coords: List[Tuple[Node, float, float, int]] = []
        for i, (node, depth) in enumerate(inorder_nodes):
            raw_x = i * col_spacing
            raw_y = top_margin + depth * level_gap
            raw_coords.append((node, raw_x, raw_y, depth))

        # Center entire layout horizontally
        if raw_coords:
            min_x = min(r[1] for r in raw_coords)
            max_x = max(r[1] for r in raw_coords)
            tree_bbox_w = max_x - min_x + node_width
            shift_x = (canvas_width - tree_bbox_w) / 2.0 - min_x

            for node, rx, ry, depth in raw_coords:
                final_x = rx + shift_x
                final_y = ry
                positions[node.value] = (final_x, final_y, depth)

        return positions
