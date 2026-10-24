"""
BLOCKY DSA WORLD — 3D Stack, Queue & BST Explorer
=================================================
A vibrant, Roblox-inspired desktop educational application that teaches:
- Stack (LIFO)
- Queue (FIFO via Singly Linked List)
- Binary Search Tree (BST Explorer with manual insertion, search, deletion,
  Inorder, Preorder, and Postorder animated traversals)

Author: Senior Python Developer & DSA Instructor
Tech Stack: Python 3 Standard Library + Tkinter Canvas (Zero external dependencies)
"""

import os
import random
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, List, Optional

# Ensure directory containing main.py is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.stack import Stack
from src.queue_linked_list import Queue
from src.bst import BinarySearchTree, Node
from src.history import HistoryTracker
from src.visualizer import VisualizerCanvas
from src.learning_mode import LearningModeDialog


class BlockyDSAWorldApp(tk.Tk):
    """
    Main Application Window for Blocky DSA World.
    """

    MAX_CAPACITY = 7

    def __init__(self):
        super().__init__()
        self.title("BLOCKY DSA WORLD — 3D Stack, Queue & BST Explorer")
        self.geometry("1300x820")
        self.minsize(1080, 700)
        self.configure(bg="#E2E8F0")

        # Core Data Models
        self.stack = Stack(capacity=self.MAX_CAPACITY)
        self.queue = Queue(capacity=self.MAX_CAPACITY)
        self.bst = BinarySearchTree()
        self.history = HistoryTracker(max_history=60, max_undo=25)
        self.current_mode: str = "STACK_QUEUE"  # "STACK_QUEUE" or "BST"

        # Traversal Animation Player State
        self.traversal_mode: Optional[str] = None
        self.traversal_sequence: List[int] = []
        self.traversal_step: int = 0
        self.traversal_timer_id: Optional[str] = None
        self.traversal_speed_ms: int = 450
        self.traversal_is_paused: bool = False

        # Stack & Queue UI References
        self.entry_val: Optional[tk.Entry] = None
        self.history_listbox: Optional[tk.Listbox] = None
        self.lbl_last_op: Optional[tk.Label] = None
        self.lbl_stack_size: Optional[tk.Label] = None
        self.lbl_stack_top: Optional[tk.Label] = None
        self.lbl_queue_size: Optional[tk.Label] = None
        self.lbl_queue_front: Optional[tk.Label] = None
        self.lbl_queue_rear: Optional[tk.Label] = None
        self.lbl_total_ops: Optional[tk.Label] = None
        self.lbl_status_msg: Optional[tk.Label] = None

        # BST UI References
        self.entry_bst_val: Optional[tk.Entry] = None
        self.entry_bst_search: Optional[tk.Entry] = None
        self.entry_bst_delete: Optional[tk.Entry] = None
        self.lbl_bst_size: Optional[tk.Label] = None
        self.lbl_bst_height: Optional[tk.Label] = None
        self.lbl_bst_root: Optional[tk.Label] = None
        self.lbl_bst_minmax: Optional[tk.Label] = None
        self.lbl_bst_balanced: Optional[tk.Label] = None
        self.lbl_traversal_type: Optional[tk.Label] = None
        self.lbl_traversal_seq: Optional[tk.Label] = None
        self.lbl_traversal_status: Optional[tk.Label] = None
        self.lbl_bst_op_name: Optional[tk.Label] = None
        self.lbl_bst_explanation: Optional[tk.Label] = None
        self.lbl_bst_complexity: Optional[tk.Label] = None
        self.history_listbox_bst: Optional[tk.Listbox] = None
        self.btn_nav_sq: Optional[tk.Button] = None
        self.btn_nav_bst: Optional[tk.Button] = None

        # Build GUI
        self._build_menu_bar()
        self._build_header()
        self._build_nav_bar()
        self._build_main_layout()
        self._build_status_footer()

        # Connect data to Visualizer
        self.visualizer.set_data_sources(self.stack, self.queue)
        self.visualizer.set_bst_source(self.bst)
        self._update_info_panel("System initialized. Ready for operations.")

    # -------------------------------------------------------------------------
    # MENU BAR & NAVIGATION
    # -------------------------------------------------------------------------
    def _build_menu_bar(self) -> None:
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # 1. Modules Menu
        mod_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modules", menu=mod_menu)
        mod_menu.add_command(label="📦 Stack & Queue Lab", command=lambda: self.switch_mode("STACK_QUEUE"))
        mod_menu.add_command(label="🌳 Binary Search Tree — BST Explorer", command=lambda: self.switch_mode("BST"))
        mod_menu.add_separator()
        mod_menu.add_command(label="Exit", command=self.destroy)

        # 2. BST Operations Menu
        bst_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="BST Operations", menu=bst_menu)
        bst_menu.add_command(label="➕ Insert Node", command=self.on_bst_insert)
        bst_menu.add_command(label="🔍 Search Value", command=self.on_bst_search)
        bst_menu.add_command(label="✂️ Delete Node", command=self.on_bst_delete)
        bst_menu.add_separator()
        bst_menu.add_command(label="🌿 Inorder Traversal [L-Root-R]", command=self.on_bst_inorder)
        bst_menu.add_command(label="🌱 Preorder Traversal [Root-L-R]", command=self.on_bst_preorder)
        bst_menu.add_command(label="🍂 Postorder Traversal [L-R-Root]", command=self.on_bst_postorder)
        bst_menu.add_separator()
        bst_menu.add_command(label="🌲 Load Sample Tree (50, 30, 70, 20, 40, 60, 80)", command=self.on_bst_load_sample)
        bst_menu.add_command(label="🗑 Clear BST", command=self.on_bst_clear)

        # 3. Stack & Queue Menu
        sq_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Stack & Queue", menu=sq_menu)
        sq_menu.add_command(label="⬆ Push Stack", command=self.on_stack_push)
        sq_menu.add_command(label="⬇ Pop Stack", command=self.on_stack_pop)
        sq_menu.add_command(label="👁 Peek Stack", command=self.on_stack_peek)
        sq_menu.add_command(label="⏩ Enqueue", command=self.on_queue_enqueue)
        sq_menu.add_command(label="⏪ Dequeue", command=self.on_queue_dequeue)

        # 4. Help & Academy Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help & Academy", menu=help_menu)
        help_menu.add_command(label="🎓 DSA Academy & Quiz", command=self.open_learning_mode)
        help_menu.add_command(label="❓ Help & Shortcuts", command=self.show_help_dialog)

    def _build_header(self) -> None:
        header = tk.Frame(self, bg="#0F172A", height=74)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Left Header Branding
        brand_frame = tk.Frame(header, bg="#0F172A")
        brand_frame.pack(side=tk.LEFT, padx=20, pady=8)

        title_lbl = tk.Label(
            brand_frame,
            text="🧱 BLOCKY DSA WORLD",
            font=("Segoe UI", 15, "bold"),
            fg="#FACC15",
            bg="#0F172A"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            brand_frame,
            text="Stack • Queue • Binary Search Tree (BST) | 3D-Style Interactive Lab",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A"
        )
        sub_lbl.pack(anchor="w")

        # Right Header Badges & Action Buttons
        badge_frame = tk.Frame(header, bg="#0F172A")
        badge_frame.pack(side=tk.RIGHT, padx=18, pady=12)

        badge_python = tk.Label(
            badge_frame,
            text=" 🐍 Python 3 + Tkinter ",
            font=("Segoe UI", 8, "bold"),
            fg="#0F172A",
            bg="#38BDF8",
            padx=7,
            pady=3
        )
        badge_python.pack(side=tk.LEFT, padx=4)

        badge_engine = tk.Label(
            badge_frame,
            text=" ⚡ LIFO & FIFO & BST ",
            font=("Segoe UI", 8, "bold"),
            fg="#0F172A",
            bg="#4ADE80",
            padx=7,
            pady=3
        )
        badge_engine.pack(side=tk.LEFT, padx=4)

        btn_academy = tk.Button(
            badge_frame,
            text="🎓 DSA Academy & Quiz",
            font=("Segoe UI", 9, "bold"),
            bg="#F59E0B",
            fg="#0F172A",
            activebackground="#D97706",
            cursor="hand2",
            relief="raised",
            bd=1,
            padx=9,
            pady=3,
            command=self.open_learning_mode
        )
        btn_academy.pack(side=tk.LEFT, padx=8)

        btn_help = tk.Button(
            badge_frame,
            text="❓ Help",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            activebackground="#475569",
            cursor="hand2",
            relief="flat",
            padx=8,
            pady=3,
            command=self.show_help_dialog
        )
        btn_help.pack(side=tk.LEFT, padx=4)

    def _build_nav_bar(self) -> None:
        """Sleek top tab selector for switching between Stack/Queue and BST Explorer."""
        nav = tk.Frame(self, bg="#1E293B", height=40)
        nav.pack(fill=tk.X, side=tk.TOP)
        nav.pack_propagate(False)

        lbl_nav = tk.Label(
            nav,
            text="MODULE DECK:",
            font=("Segoe UI", 8, "bold"),
            fg="#94A3B8",
            bg="#1E293B"
        )
        lbl_nav.pack(side=tk.LEFT, padx=(18, 10), pady=6)

        self.btn_nav_sq = tk.Button(
            nav,
            text="📦  Stack (LIFO) & 🚀 Queue (FIFO) Lab",
            font=("Segoe UI", 9, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            activebackground="#0369A1",
            cursor="hand2",
            relief="flat",
            padx=16,
            pady=4,
            command=lambda: self.switch_mode("STACK_QUEUE")
        )
        self.btn_nav_sq.pack(side=tk.LEFT, padx=4, pady=4)

        self.btn_nav_bst = tk.Button(
            nav,
            text="🌳  Binary Search Tree — BST Explorer",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#CBD5E1",
            activebackground="#475569",
            cursor="hand2",
            relief="flat",
            padx=16,
            pady=4,
            command=lambda: self.switch_mode("BST")
        )
        self.btn_nav_bst.pack(side=tk.LEFT, padx=4, pady=4)

    def switch_mode(self, mode: str) -> None:
        """Switch active DSA view between Stack/Queue and BST Explorer."""
        if self.visualizer.is_animating:
            return

        self.current_mode = mode
        self.visualizer.set_mode(mode)

        if mode == "BST":
            if self.btn_nav_bst:
                self.btn_nav_bst.configure(bg="#10B981", fg="#FFFFFF")
            if self.btn_nav_sq:
                self.btn_nav_sq.configure(bg="#334155", fg="#CBD5E1")

            self.frame_sq_ctrl.pack_forget()
            self.frame_bst_ctrl.pack(fill=tk.BOTH, expand=True)

            self.frame_sq_info.pack_forget()
            self.frame_bst_info.pack(fill=tk.BOTH, expand=True)

            if self.lbl_status_msg:
                self.lbl_status_msg.configure(
                    text="📌 BST Complexity: Search Avg O(log n) Worst O(n) | Insert Avg O(log n) Worst O(n) | Traversals O(n)"
                )
            self.visualizer.set_speech("Welcome to BST Explorer! Insert nodes, run traversals, or load the sample tree.")
            self._update_bst_info_panel("Switched to Binary Search Tree Explorer.")
        else:
            if self.btn_nav_sq:
                self.btn_nav_sq.configure(bg="#0284C7", fg="#FFFFFF")
            if self.btn_nav_bst:
                self.btn_nav_bst.configure(bg="#334155", fg="#CBD5E1")

            self.frame_bst_ctrl.pack_forget()
            self.frame_sq_ctrl.pack(fill=tk.BOTH, expand=True)

            self.frame_bst_info.pack_forget()
            self.frame_sq_info.pack(fill=tk.BOTH, expand=True)

            if self.lbl_status_msg:
                self.lbl_status_msg.configure(
                    text="📌 Complexity Reference: Stack [Push O(1), Pop O(1), Peek O(1)] || Queue Linked-List [Enqueue O(1), Dequeue O(1), Front O(1), Rear O(1)]"
                )
            self.visualizer.set_speech("Returned to Stack & Queue Lab! LIFO tower on left, FIFO runway on right.")
            self._update_info_panel("Switched to Stack & Queue Lab.")

    # -------------------------------------------------------------------------
    # MAIN APPLICATION LAYOUT
    # -------------------------------------------------------------------------
    def _build_main_layout(self) -> None:
        body = tk.Frame(self, bg="#CBD5E1")
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 4))

        # Left Control Panel (Fixed Width: ~290px)
        left_panel = tk.Frame(body, bg="#F8FAFC", width=290, bd=1, relief="ridge")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        left_panel.pack_propagate(False)
        self._build_control_panel(left_panel)

        # Right Information Panel (Fixed Width: ~310px)
        right_panel = tk.Frame(body, bg="#F8FAFC", width=310, bd=1, relief="ridge")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))
        right_panel.pack_propagate(False)
        self._build_info_panel(right_panel)

        # Center 3D Visualizer Canvas
        center_frame = tk.Frame(body, bg="#64748B", bd=2, relief="sunken")
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.visualizer = VisualizerCanvas(center_frame)
        self.visualizer.pack(fill=tk.BOTH, expand=True)

    def _build_control_panel(self, parent: tk.Frame) -> None:
        self.frame_sq_ctrl = tk.Frame(parent, bg="#F8FAFC")
        self.frame_bst_ctrl = tk.Frame(parent, bg="#F8FAFC")

        self._build_sq_controls(self.frame_sq_ctrl)
        self._build_bst_controls(self.frame_bst_ctrl)

        self.frame_sq_ctrl.pack(fill=tk.BOTH, expand=True)

    def _build_info_panel(self, parent: tk.Frame) -> None:
        self.frame_sq_info = tk.Frame(parent, bg="#F8FAFC")
        self.frame_bst_info = tk.Frame(parent, bg="#F8FAFC")

        self._build_sq_telemetry(self.frame_sq_info)
        self._build_bst_telemetry(self.frame_bst_info)

        self.frame_sq_info.pack(fill=tk.BOTH, expand=True)

    # -------------------------------------------------------------------------
    # STACK & QUEUE CONTROLS (PRESERVED)
    # -------------------------------------------------------------------------
    def _build_sq_controls(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="🎮 CONTROL DECK (LIFO & FIFO)",
            font=("Segoe UI", 11, "bold"),
            fg="#0F172A",
            bg="#F8FAFC"
        ).pack(anchor="w", padx=14, pady=(12, 6))

        # --- SECTION 1: VALUE INPUT BAR ---
        input_box = tk.LabelFrame(
            parent,
            text=" 📝 Element Value Input ",
            font=("Segoe UI", 9, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        input_box.pack(fill=tk.X, padx=12, pady=(0, 10))

        entry_row = tk.Frame(input_box, bg="#FFFFFF")
        entry_row.pack(fill=tk.X)

        self.entry_val = tk.Entry(
            entry_row,
            font=("Segoe UI", 11, "bold"),
            bg="#F1F5F9",
            fg="#0F172A",
            bd=1,
            relief="solid",
            width=11
        )
        self.entry_val.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        self.entry_val.insert(0, "42")
        self.entry_val.bind("<Return>", lambda e: self.on_stack_push())

        btn_rand = tk.Button(
            entry_row,
            text="🎲 Rand",
            font=("Segoe UI", 8, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            activebackground="#CBD5E1",
            cursor="hand2",
            relief="flat",
            padx=6,
            command=self._generate_random_val
        )
        btn_rand.pack(side=tk.RIGHT, padx=(6, 0))

        # Quick preset chips
        chip_row = tk.Frame(input_box, bg="#FFFFFF")
        chip_row.pack(fill=tk.X, pady=(6, 0))
        tk.Label(chip_row, text="Presets:", font=("Segoe UI", 7, "bold"), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        for val in [10, 25, 99, "A", "Z"]:
            btn_chip = tk.Button(
                chip_row,
                text=str(val),
                font=("Segoe UI", 7),
                bg="#F1F5F9",
                fg="#334155",
                activebackground="#E2E8F0",
                cursor="hand2",
                relief="groove",
                bd=1,
                padx=4,
                pady=1,
                command=lambda v=val: self._set_input_val(v)
            )
            btn_chip.pack(side=tk.LEFT, padx=2)

        # --- SECTION 2: STACK CONTROLS (LIFO) ---
        stack_card = tk.LabelFrame(
            parent,
            text=" 📦 STACK OPERATIONS (LIFO) ",
            font=("Segoe UI", 9, "bold"),
            fg="#E11D48",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        stack_card.pack(fill=tk.X, padx=12, pady=(0, 10))

        btn_push = tk.Button(
            stack_card,
            text="⬆  PUSH Element  [O(1)]",
            font=("Segoe UI", 9, "bold"),
            bg="#E11D48",
            fg="#FFFFFF",
            activebackground="#BE123C",
            cursor="hand2",
            relief="flat",
            pady=5,
            command=self.on_stack_push
        )
        btn_push.pack(fill=tk.X, pady=2)

        row_stack_ops = tk.Frame(stack_card, bg="#FFFFFF")
        row_stack_ops.pack(fill=tk.X, pady=2)

        btn_pop = tk.Button(
            row_stack_ops,
            text="⬇  POP [O(1)]",
            font=("Segoe UI", 8, "bold"),
            bg="#F43F5E",
            fg="#FFFFFF",
            activebackground="#E11D48",
            cursor="hand2",
            relief="flat",
            pady=4,
            command=self.on_stack_pop
        )
        btn_pop.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        btn_peek = tk.Button(
            row_stack_ops,
            text="👁  PEEK [O(1)]",
            font=("Segoe UI", 8, "bold"),
            bg="#FB7185",
            fg="#0F172A",
            activebackground="#F43F5E",
            cursor="hand2",
            relief="flat",
            pady=4,
            command=self.on_stack_peek
        )
        btn_peek.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        btn_clear_stack = tk.Button(
            stack_card,
            text="🗑  Clear Stack",
            font=("Segoe UI", 8),
            bg="#FFE4E6",
            fg="#9F1239",
            activebackground="#FECDD3",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_stack_clear
        )
        btn_clear_stack.pack(fill=tk.X, pady=(2, 0))

        # --- SECTION 3: QUEUE CONTROLS (FIFO) ---
        queue_card = tk.LabelFrame(
            parent,
            text=" 🚀 QUEUE OPERATIONS (FIFO) ",
            font=("Segoe UI", 9, "bold"),
            fg="#0284C7",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        queue_card.pack(fill=tk.X, padx=12, pady=(0, 10))

        btn_enq = tk.Button(
            queue_card,
            text="⏩  ENQUEUE (Rear)  [O(1)]",
            font=("Segoe UI", 9, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            activebackground="#0369A1",
            cursor="hand2",
            relief="flat",
            pady=5,
            command=self.on_queue_enqueue
        )
        btn_enq.pack(fill=tk.X, pady=2)

        row_q_ops = tk.Frame(queue_card, bg="#FFFFFF")
        row_q_ops.pack(fill=tk.X, pady=2)

        btn_deq = tk.Button(
            row_q_ops,
            text="⏪  DEQUEUE [O(1)]",
            font=("Segoe UI", 8, "bold"),
            bg="#0EA5E9",
            fg="#FFFFFF",
            activebackground="#0284C7",
            cursor="hand2",
            relief="flat",
            pady=4,
            command=self.on_queue_dequeue
        )
        btn_deq.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        btn_front = tk.Button(
            row_q_ops,
            text="🔍  FRONT",
            font=("Segoe UI", 8, "bold"),
            bg="#38BDF8",
            fg="#0F172A",
            activebackground="#0EA5E9",
            cursor="hand2",
            relief="flat",
            pady=4,
            command=self.on_queue_front
        )
        btn_front.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        row_q_extra = tk.Frame(queue_card, bg="#FFFFFF")
        row_q_extra.pack(fill=tk.X, pady=2)

        btn_rear = tk.Button(
            row_q_extra,
            text="🎯  REAR [O(1)]",
            font=("Segoe UI", 8),
            bg="#BAE6FD",
            fg="#0369A1",
            activebackground="#7DD3FC",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_queue_rear
        )
        btn_rear.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        btn_clear_queue = tk.Button(
            row_q_extra,
            text="🗑  Clear Queue",
            font=("Segoe UI", 8),
            bg="#E0F2FE",
            fg="#0369A1",
            activebackground="#BAE6FD",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_queue_clear
        )
        btn_clear_queue.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        # --- SECTION 4: GLOBAL CONTROLS & UNDO ---
        global_card = tk.LabelFrame(
            parent,
            text=" ⚙️ GLOBAL & LAB UTILITIES ",
            font=("Segoe UI", 9, "bold"),
            fg="#475569",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        global_card.pack(fill=tk.X, padx=12, pady=(0, 10))

        btn_undo = tk.Button(
            global_card,
            text="↩  UNDO Last Action",
            font=("Segoe UI", 9, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            activebackground="#059669",
            cursor="hand2",
            relief="flat",
            pady=4,
            command=self.on_undo_operation
        )
        btn_undo.pack(fill=tk.X, pady=2)

        btn_reset_all = tk.Button(
            global_card,
            text="🔄  RESET ALL LABS",
            font=("Segoe UI", 8, "bold"),
            bg="#64748B",
            fg="#FFFFFF",
            activebackground="#475569",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_reset_all
        )
        btn_reset_all.pack(fill=tk.X, pady=2)

    # -------------------------------------------------------------------------
    # BST CONTROLS (NEW MODULE)
    # -------------------------------------------------------------------------
    def _build_bst_controls(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="🎮 BST EXPLORER DECK",
            font=("Segoe UI", 11, "bold"),
            fg="#0F172A",
            bg="#F8FAFC"
        ).pack(anchor="w", padx=14, pady=(10, 4))

        # Card 1: Node Value Input & Insertion
        card_input = tk.LabelFrame(
            parent,
            text=" 📝 BST Node Input ",
            font=("Segoe UI", 9, "bold"),
            fg="#059669",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=8,
            pady=6
        )
        card_input.pack(fill=tk.X, padx=10, pady=(0, 6))

        entry_row = tk.Frame(card_input, bg="#FFFFFF")
        entry_row.pack(fill=tk.X)

        self.entry_bst_val = tk.Entry(
            entry_row,
            font=("Segoe UI", 11, "bold"),
            bg="#F1F5F9",
            fg="#0F172A",
            bd=1,
            relief="solid",
            width=9
        )
        self.entry_bst_val.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        self.entry_bst_val.insert(0, "50")
        self.entry_bst_val.bind("<Return>", lambda e: self.on_bst_insert())

        btn_rand_bst = tk.Button(
            entry_row,
            text="🎲 Rand",
            font=("Segoe UI", 8, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            activebackground="#CBD5E1",
            cursor="hand2",
            relief="flat",
            padx=6,
            command=self._generate_random_bst_val
        )
        btn_rand_bst.pack(side=tk.RIGHT, padx=(4, 0))

        # Quick preset chips
        chip_row = tk.Frame(card_input, bg="#FFFFFF")
        chip_row.pack(fill=tk.X, pady=(4, 4))
        tk.Label(chip_row, text="Presets:", font=("Segoe UI", 7, "bold"), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        for p_val in [20, 30, 40, 50, 60, 70, 80]:
            tk.Button(
                chip_row,
                text=str(p_val),
                font=("Segoe UI", 7),
                bg="#F1F5F9",
                fg="#334155",
                relief="groove",
                bd=1,
                padx=2,
                pady=1,
                command=lambda v=p_val: self._set_bst_input_val(v)
            ).pack(side=tk.LEFT, padx=1)

        btn_insert = tk.Button(
            card_input,
            text="➕  INSERT Node  [O(log n)]",
            font=("Segoe UI", 9, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            activebackground="#059669",
            cursor="hand2",
            relief="flat",
            pady=4,
            command=self.on_bst_insert
        )
        btn_insert.pack(fill=tk.X, pady=(2, 2))

        btn_sample = tk.Button(
            card_input,
            text="🌲  Load Sample Tree [50, 30, 70...]",
            font=("Segoe UI", 8, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            activebackground="#0369A1",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_bst_load_sample
        )
        btn_sample.pack(fill=tk.X, pady=(2, 0))

        # Card 2: Search & Deletion
        card_search = tk.LabelFrame(
            parent,
            text=" 🔍 Search & Delete ",
            font=("Segoe UI", 9, "bold"),
            fg="#0284C7",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=8,
            pady=6
        )
        card_search.pack(fill=tk.X, padx=10, pady=(0, 6))

        s_row = tk.Frame(card_search, bg="#FFFFFF")
        s_row.pack(fill=tk.X, pady=2)
        self.entry_bst_search = tk.Entry(s_row, font=("Segoe UI", 9, "bold"), bg="#F1F5F9", fg="#0F172A", bd=1, relief="solid", width=7)
        self.entry_bst_search.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=1)
        self.entry_bst_search.insert(0, "40")
        self.entry_bst_search.bind("<Return>", lambda e: self.on_bst_search())

        btn_search = tk.Button(
            s_row,
            text="🔍 Search [O(log n)]",
            font=("Segoe UI", 8, "bold"),
            bg="#38BDF8",
            fg="#0F172A",
            activebackground="#0284C7",
            cursor="hand2",
            relief="flat",
            padx=6,
            pady=2,
            command=self.on_bst_search
        )
        btn_search.pack(side=tk.RIGHT, padx=(4, 0))

        d_row = tk.Frame(card_search, bg="#FFFFFF")
        d_row.pack(fill=tk.X, pady=2)
        self.entry_bst_delete = tk.Entry(d_row, font=("Segoe UI", 9, "bold"), bg="#F1F5F9", fg="#0F172A", bd=1, relief="solid", width=7)
        self.entry_bst_delete.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=1)
        self.entry_bst_delete.insert(0, "30")
        self.entry_bst_delete.bind("<Return>", lambda e: self.on_bst_delete())

        btn_del = tk.Button(
            d_row,
            text="✂️ Delete Node",
            font=("Segoe UI", 8, "bold"),
            bg="#F43F5E",
            fg="#FFFFFF",
            activebackground="#E11D48",
            cursor="hand2",
            relief="flat",
            padx=6,
            pady=2,
            command=self.on_bst_delete
        )
        btn_del.pack(side=tk.RIGHT, padx=(4, 0))

        # Card 3: 3D Tree Traversals & Player
        card_trav = tk.LabelFrame(
            parent,
            text=" 🚶 3D Tree Traversals ",
            font=("Segoe UI", 9, "bold"),
            fg="#7C3AED",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=8,
            pady=6
        )
        card_trav.pack(fill=tk.X, padx=10, pady=(0, 6))

        btn_inorder = tk.Button(
            card_trav,
            text="🌿  INORDER (L ➔ Root ➔ R)",
            font=("Segoe UI", 8, "bold"),
            bg="#059669",
            fg="#FFFFFF",
            activebackground="#047857",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_bst_inorder
        )
        btn_inorder.pack(fill=tk.X, pady=1)

        btn_preorder = tk.Button(
            card_trav,
            text="🌱  PREORDER (Root ➔ L ➔ R)",
            font=("Segoe UI", 8, "bold"),
            bg="#0D9488",
            fg="#FFFFFF",
            activebackground="#0f766e",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_bst_preorder
        )
        btn_preorder.pack(fill=tk.X, pady=1)

        btn_postorder = tk.Button(
            card_trav,
            text="🍂  POSTORDER (L ➔ R ➔ Root)",
            font=("Segoe UI", 8, "bold"),
            bg="#7C3AED",
            fg="#FFFFFF",
            activebackground="#6D28D9",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_bst_postorder
        )
        btn_postorder.pack(fill=tk.X, pady=1)

        # Animation Player Controls
        tk.Label(
            card_trav,
            text="Animation Player Controls:",
            font=("Segoe UI", 7, "bold"),
            fg="#64748B",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(4, 2))

        ctrl_row = tk.Frame(card_trav, bg="#FFFFFF")
        ctrl_row.pack(fill=tk.X, pady=2)

        tk.Button(ctrl_row, text="▶ Play", font=("Segoe UI", 7, "bold"), bg="#10B981", fg="#FFFFFF", cursor="hand2", relief="flat", padx=3, pady=2, command=self.on_traversal_play).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(ctrl_row, text="⏸ Pause", font=("Segoe UI", 7, "bold"), bg="#F59E0B", fg="#0F172A", cursor="hand2", relief="flat", padx=3, pady=2, command=self.on_traversal_pause).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(ctrl_row, text="⏯ Resume", font=("Segoe UI", 7, "bold"), bg="#38BDF8", fg="#0F172A", cursor="hand2", relief="flat", padx=3, pady=2, command=self.on_traversal_resume).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(ctrl_row, text="🔄 Restart", font=("Segoe UI", 7, "bold"), bg="#64748B", fg="#FFFFFF", cursor="hand2", relief="flat", padx=3, pady=2, command=self.on_traversal_restart).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(ctrl_row, text="⏹ Reset", font=("Segoe UI", 7, "bold"), bg="#EF4444", fg="#FFFFFF", cursor="hand2", relief="flat", padx=3, pady=2, command=self.on_traversal_reset).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        # Speed buttons
        speed_row = tk.Frame(card_trav, bg="#FFFFFF")
        speed_row.pack(fill=tk.X, pady=(4, 1))
        tk.Label(speed_row, text="Speed:", font=("Segoe UI", 7, "bold"), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)

        btn_slow = tk.Button(speed_row, text="Slow", font=("Segoe UI", 7), bg="#E2E8F0", fg="#1E293B", cursor="hand2", relief="groove", bd=1, padx=4, pady=1)
        btn_norm = tk.Button(speed_row, text="Normal", font=("Segoe UI", 7, "bold"), bg="#0284C7", fg="#FFFFFF", cursor="hand2", relief="groove", bd=1, padx=4, pady=1)
        btn_fast = tk.Button(speed_row, text="Fast", font=("Segoe UI", 7), bg="#E2E8F0", fg="#1E293B", cursor="hand2", relief="groove", bd=1, padx=4, pady=1)

        all_spd = [btn_slow, btn_norm, btn_fast]
        btn_slow.configure(command=lambda: self.set_traversal_speed(950, btn_slow, all_spd))
        btn_norm.configure(command=lambda: self.set_traversal_speed(450, btn_norm, all_spd))
        btn_fast.configure(command=lambda: self.set_traversal_speed(180, btn_fast, all_spd))

        btn_slow.pack(side=tk.LEFT, padx=2)
        btn_norm.pack(side=tk.LEFT, padx=2)
        btn_fast.pack(side=tk.LEFT, padx=2)

        # Card 4: Utilities
        card_utils = tk.LabelFrame(
            parent,
            text=" ⚙️ BST Utilities ",
            font=("Segoe UI", 9, "bold"),
            fg="#475569",
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            padx=8,
            pady=5
        )
        card_utils.pack(fill=tk.X, padx=10, pady=(0, 6))

        btn_clear_bst = tk.Button(
            card_utils,
            text="🗑  Clear Tree",
            font=("Segoe UI", 8),
            bg="#FFE4E6",
            fg="#9F1239",
            activebackground="#FECDD3",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_bst_clear
        )
        btn_clear_bst.pack(fill=tk.X, pady=1)

        btn_undo_bst = tk.Button(
            card_utils,
            text="↩  UNDO Last Action",
            font=("Segoe UI", 8, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            activebackground="#059669",
            cursor="hand2",
            relief="flat",
            pady=3,
            command=self.on_undo_operation
        )
        btn_undo_bst.pack(fill=tk.X, pady=1)

    # -------------------------------------------------------------------------
    # STACK & QUEUE TELEMETRY (PRESERVED)
    # -------------------------------------------------------------------------
    def _build_sq_telemetry(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="📊 TELEMETRY & STATS",
            font=("Segoe UI", 11, "bold"),
            fg="#0F172A",
            bg="#F8FAFC"
        ).pack(anchor="w", padx=14, pady=(12, 6))

        # 1. Stack Status Card
        card_stack = tk.LabelFrame(
            parent,
            text=" 📦 Stack Status (LIFO) ",
            font=("Segoe UI", 8, "bold"),
            fg="#E11D48",
            bg="#FFFFFF",
            padx=10,
            pady=6
        )
        card_stack.pack(fill=tk.X, padx=12, pady=(0, 6))

        r1 = tk.Frame(card_stack, bg="#FFFFFF")
        r1.pack(fill=tk.X)
        tk.Label(r1, text="Current Size:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_stack_size = tk.Label(r1, text="0 / 7", font=("Segoe UI", 9, "bold"), fg="#0F172A", bg="#FFFFFF")
        self.lbl_stack_size.pack(side=tk.RIGHT)

        r2 = tk.Frame(card_stack, bg="#FFFFFF")
        r2.pack(fill=tk.X)
        tk.Label(r2, text="Top Element:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_stack_top = tk.Label(r2, text="None (Empty)", font=("Segoe UI", 9, "bold"), fg="#E11D48", bg="#FFFFFF")
        self.lbl_stack_top.pack(side=tk.RIGHT)

        tk.Label(card_stack, text="Complexity: Push O(1) | Pop O(1)", font=("Segoe UI", 7, "italic"), fg="#94A3B8", bg="#FFFFFF").pack(anchor="w", pady=(2, 0))

        # 2. Queue Status Card
        card_queue = tk.LabelFrame(
            parent,
            text=" 🚀 Queue Status (Singly Linked List) ",
            font=("Segoe UI", 8, "bold"),
            fg="#0284C7",
            bg="#FFFFFF",
            padx=10,
            pady=6
        )
        card_queue.pack(fill=tk.X, padx=12, pady=(0, 6))

        q1 = tk.Frame(card_queue, bg="#FFFFFF")
        q1.pack(fill=tk.X)
        tk.Label(q1, text="Current Size:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_queue_size = tk.Label(q1, text="0 / 7", font=("Segoe UI", 9, "bold"), fg="#0F172A", bg="#FFFFFF")
        self.lbl_queue_size.pack(side=tk.RIGHT)

        q2 = tk.Frame(card_queue, bg="#FFFFFF")
        q2.pack(fill=tk.X)
        tk.Label(q2, text="Front (Head):", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_queue_front = tk.Label(q2, text="None", font=("Segoe UI", 9, "bold"), fg="#0284C7", bg="#FFFFFF")
        self.lbl_queue_front.pack(side=tk.RIGHT)

        q3 = tk.Frame(card_queue, bg="#FFFFFF")
        q3.pack(fill=tk.X)
        tk.Label(q3, text="Rear (Tail):", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_queue_rear = tk.Label(q3, text="None", font=("Segoe UI", 9, "bold"), fg="#0284C7", bg="#FFFFFF")
        self.lbl_queue_rear.pack(side=tk.RIGHT)

        tk.Label(card_queue, text="Complexity: Enqueue O(1) | Dequeue O(1)", font=("Segoe UI", 7, "italic"), fg="#94A3B8", bg="#FFFFFF").pack(anchor="w", pady=(2, 0))

        # 3. Overall Counters & Last Action Message
        ops_card = tk.LabelFrame(
            parent,
            text=" 💡 Last Operation Explanation ",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#FFFFFF",
            padx=10,
            pady=6
        )
        ops_card.pack(fill=tk.X, padx=12, pady=(0, 6))

        c1 = tk.Frame(ops_card, bg="#FFFFFF")
        c1.pack(fill=tk.X)
        tk.Label(c1, text="Successful Ops:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_total_ops = tk.Label(c1, text="0", font=("Segoe UI", 9, "bold"), fg="#16A34A", bg="#FFFFFF")
        self.lbl_total_ops.pack(side=tk.RIGHT)

        self.lbl_last_op = tk.Label(
            ops_card,
            text="Application started. Ready.",
            font=("Segoe UI", 8),
            fg="#1E293B",
            bg="#F1F5F9",
            justify="left",
            wraplength=260,
            padx=6,
            pady=5,
            bd=1,
            relief="groove"
        )
        self.lbl_last_op.pack(fill=tk.X, pady=(4, 0))

        # 4. Operation History Listbox
        hist_card = tk.LabelFrame(
            parent,
            text=" 📜 Recent Operations Log ",
            font=("Segoe UI", 8, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            padx=6,
            pady=4
        )
        hist_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))

        hist_frame = tk.Frame(hist_card, bg="#FFFFFF")
        hist_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical")
        self.history_listbox = tk.Listbox(
            hist_frame,
            font=("Consolas", 8),
            bg="#F8FAFC",
            fg="#1E293B",
            selectbackground="#E2E8F0",
            selectforeground="#0F172A",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.history_listbox.yview)

        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # -------------------------------------------------------------------------
    # BST TELEMETRY & STATS (NEW MODULE)
    # -------------------------------------------------------------------------
    def _build_bst_telemetry(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="📊 BST TELEMETRY & STATS",
            font=("Segoe UI", 11, "bold"),
            fg="#0F172A",
            bg="#F8FAFC"
        ).pack(anchor="w", padx=14, pady=(10, 4))

        # Card 1: Tree Metrics
        card_prop = tk.LabelFrame(
            parent,
            text=" 🌳 BST Metrics & Invariants ",
            font=("Segoe UI", 8, "bold"),
            fg="#059669",
            bg="#FFFFFF",
            padx=8,
            pady=4
        )
        card_prop.pack(fill=tk.X, padx=10, pady=(0, 4))

        r_size = tk.Frame(card_prop, bg="#FFFFFF")
        r_size.pack(fill=tk.X)
        tk.Label(r_size, text="Nodes Count:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_bst_size = tk.Label(r_size, text="0 nodes", font=("Segoe UI", 9, "bold"), fg="#0F172A", bg="#FFFFFF")
        self.lbl_bst_size.pack(side=tk.RIGHT)

        r_h = tk.Frame(card_prop, bg="#FFFFFF")
        r_h.pack(fill=tk.X)
        tk.Label(r_h, text="Tree Height:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_bst_height = tk.Label(r_h, text="0 levels", font=("Segoe UI", 9, "bold"), fg="#0284C7", bg="#FFFFFF")
        self.lbl_bst_height.pack(side=tk.RIGHT)

        r_root = tk.Frame(card_prop, bg="#FFFFFF")
        r_root.pack(fill=tk.X)
        tk.Label(r_root, text="Root Node:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_bst_root = tk.Label(r_root, text="None (Empty)", font=("Segoe UI", 9, "bold"), fg="#D97706", bg="#FFFFFF")
        self.lbl_bst_root.pack(side=tk.RIGHT)

        r_mm = tk.Frame(card_prop, bg="#FFFFFF")
        r_mm.pack(fill=tk.X)
        tk.Label(r_mm, text="Min / Max Keys:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_bst_minmax = tk.Label(r_mm, text="None / None", font=("Segoe UI", 8, "bold"), fg="#475569", bg="#FFFFFF")
        self.lbl_bst_minmax.pack(side=tk.RIGHT)

        r_bal = tk.Frame(card_prop, bg="#FFFFFF")
        r_bal.pack(fill=tk.X)
        tk.Label(r_bal, text="Height-Balanced:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_bst_balanced = tk.Label(r_bal, text="Yes (Balanced)", font=("Segoe UI", 8, "bold"), fg="#16A34A", bg="#FFFFFF")
        self.lbl_bst_balanced.pack(side=tk.RIGHT)

        # Card 2: Traversal Sequence Output Area
        card_trav_out = tk.LabelFrame(
            parent,
            text=" 🚶 Traversal Output Sequence ",
            font=("Segoe UI", 8, "bold"),
            fg="#7C3AED",
            bg="#FFFFFF",
            padx=8,
            pady=4
        )
        card_trav_out.pack(fill=tk.X, padx=10, pady=(0, 4))

        t_row = tk.Frame(card_trav_out, bg="#FFFFFF")
        t_row.pack(fill=tk.X)
        tk.Label(t_row, text="Order:", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_traversal_type = tk.Label(t_row, text="None Selected", font=("Segoe UI", 8, "bold"), fg="#7C3AED", bg="#FFFFFF")
        self.lbl_traversal_type.pack(side=tk.RIGHT)

        self.lbl_traversal_status = tk.Label(
            card_trav_out,
            text="Idle — Select Inorder, Preorder, or Postorder",
            font=("Segoe UI", 7, "italic"),
            fg="#64748B",
            bg="#FFFFFF",
            anchor="w"
        )
        self.lbl_traversal_status.pack(fill=tk.X, pady=(2, 2))

        # Visible traversal output sequence area
        self.lbl_traversal_seq = tk.Label(
            card_trav_out,
            text="None (Run Inorder, Preorder, or Postorder to view)",
            font=("Consolas", 8, "bold"),
            fg="#1E293B",
            bg="#F1F5F9",
            justify="left",
            wraplength=260,
            padx=6,
            pady=5,
            bd=1,
            relief="sunken"
        )
        self.lbl_traversal_seq.pack(fill=tk.X, pady=(2, 0))

        # Card 3: Operation Explanation
        card_exp = tk.LabelFrame(
            parent,
            text=" 💡 Last BST Operation ",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#FFFFFF",
            padx=8,
            pady=4
        )
        card_exp.pack(fill=tk.X, padx=10, pady=(0, 4))

        self.lbl_bst_op_name = tk.Label(
            card_exp,
            text="System Initialized",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#FFFFFF",
            anchor="w"
        )
        self.lbl_bst_op_name.pack(fill=tk.X)

        self.lbl_bst_explanation = tk.Label(
            card_exp,
            text="Ready to perform BST operations. Insert a node or load the sample tree.",
            font=("Segoe UI", 8),
            fg="#1E293B",
            bg="#F8FAFC",
            justify="left",
            wraplength=260,
            padx=6,
            pady=4,
            bd=1,
            relief="groove"
        )
        self.lbl_bst_explanation.pack(fill=tk.X, pady=(2, 2))

        self.lbl_bst_complexity = tk.Label(
            card_exp,
            text="Time Complexity: Search/Insert Avg O(log n), Traversals O(n)",
            font=("Segoe UI", 7, "italic"),
            fg="#64748B",
            bg="#FFFFFF",
            anchor="w"
        )
        self.lbl_bst_complexity.pack(fill=tk.X)

        # Card 4: Standard Time Complexity Reference Table
        card_tbl = tk.LabelFrame(
            parent,
            text=" ⏱ Time Complexity Reference Table ",
            font=("Segoe UI", 8, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            padx=6,
            pady=3
        )
        card_tbl.pack(fill=tk.X, padx=10, pady=(0, 4))

        # Table header
        hdr_row = tk.Frame(card_tbl, bg="#F1F5F9")
        hdr_row.pack(fill=tk.X, pady=(1, 2))
        tk.Label(hdr_row, text="Operation", font=("Segoe UI", 7, "bold"), fg="#1E293B", bg="#F1F5F9", width=14, anchor="w").pack(side=tk.LEFT, padx=2)
        tk.Label(hdr_row, text="Avg Case", font=("Segoe UI", 7, "bold"), fg="#059669", bg="#F1F5F9", width=10, anchor="center").pack(side=tk.LEFT)
        tk.Label(hdr_row, text="Worst Case", font=("Segoe UI", 7, "bold"), fg="#DC2626", bg="#F1F5F9", width=10, anchor="center").pack(side=tk.LEFT)

        complexity_rows = [
            ("Search", "O(log n)", "O(n)"),
            ("Insert", "O(log n)", "O(n)"),
            ("Inorder Traversal", "O(n)", "O(n)"),
            ("Preorder Traversal", "O(n)", "O(n)"),
            ("Postorder Traversal", "O(n)", "O(n)"),
        ]
        for op, avg_c, wst_c in complexity_rows:
            r = tk.Frame(card_tbl, bg="#FFFFFF")
            r.pack(fill=tk.X, pady=1)
            tk.Label(r, text=op, font=("Segoe UI", 7), fg="#334155", bg="#FFFFFF", width=14, anchor="w").pack(side=tk.LEFT, padx=2)
            tk.Label(r, text=avg_c, font=("Consolas", 7, "bold"), fg="#059669", bg="#FFFFFF", width=10, anchor="center").pack(side=tk.LEFT)
            tk.Label(r, text=wst_c, font=("Consolas", 7, "bold"), fg="#DC2626", bg="#FFFFFF", width=10, anchor="center").pack(side=tk.LEFT)

        tk.Label(
            card_tbl,
            text="* Note: Unbalanced (skewed) BST degrades to O(n) search/insert time.",
            font=("Segoe UI", 6, "italic"),
            fg="#94A3B8",
            bg="#FFFFFF",
            anchor="w"
        ).pack(fill=tk.X, pady=(2, 0))

        # Card 5: BST Operations Log
        hist_card = tk.LabelFrame(
            parent,
            text=" 📜 Operations Log ",
            font=("Segoe UI", 8, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            padx=6,
            pady=3
        )
        hist_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 6))

        hist_frame = tk.Frame(hist_card, bg="#FFFFFF")
        hist_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical")
        self.history_listbox_bst = tk.Listbox(
            hist_frame,
            font=("Consolas", 8),
            bg="#F8FAFC",
            fg="#1E293B",
            selectbackground="#E2E8F0",
            selectforeground="#0F172A",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.history_listbox_bst.yview)

        self.history_listbox_bst.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_status_footer(self) -> None:
        footer = tk.Frame(self, bg="#0F172A", height=32)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        self.lbl_status_msg = tk.Label(
            footer,
            text="📌 Complexity Reference: Stack [Push O(1), Pop O(1), Peek O(1)] || Queue Linked-List [Enqueue O(1), Dequeue O(1), Front O(1), Rear O(1)]",
            font=("Segoe UI", 8),
            fg="#94A3B8",
            bg="#0F172A"
        )
        self.lbl_status_msg.pack(side=tk.LEFT, padx=16, pady=6)

        lbl_author = tk.Label(
            footer,
            text="Blocky DSA World • Pure Python & Tkinter Canvas",
            font=("Segoe UI", 8, "bold"),
            fg="#FACC15",
            bg="#0F172A"
        )
        lbl_author.pack(side=tk.RIGHT, padx=16, pady=6)

    # -------------------------------------------------------------------------
    # VALIDATION & HELPER METHODS
    # -------------------------------------------------------------------------
    def _get_input_value(self) -> Optional[str]:
        if not self.entry_val:
            return None
        raw = self.entry_val.get().strip()
        if not raw:
            messagebox.showwarning(
                "Input Required",
                "Please enter a value into the Input Box (e.g. 42, 100, or 'A') before performing this operation.",
                parent=self
            )
            self.entry_val.focus_set()
            return None
        return raw

    def _set_input_val(self, val: Any) -> None:
        if self.entry_val:
            self.entry_val.delete(0, tk.END)
            self.entry_val.insert(0, str(val))

    def _generate_random_val(self) -> None:
        rand_num = random.randint(10, 99)
        self._set_input_val(rand_num)

    def _set_bst_input_val(self, val: int) -> None:
        if self.entry_bst_val:
            self.entry_bst_val.delete(0, tk.END)
            self.entry_bst_val.insert(0, str(val))

    def _generate_random_bst_val(self) -> None:
        rand_int = random.randint(10, 99)
        self._set_bst_input_val(rand_int)

    def _update_info_panel(self, explanation: str) -> None:
        """Update telemetry cards for Stack and Queue mode."""
        stk_size = self.stack.size()
        if self.lbl_stack_size:
            self.lbl_stack_size.configure(text=f"{stk_size} / {self.MAX_CAPACITY}")
        if self.lbl_stack_top:
            if self.stack.is_empty():
                self.lbl_stack_top.configure(text="None (Empty)", fg="#94A3B8")
            else:
                self.lbl_stack_top.configure(text=str(self.stack.peek()), fg="#E11D48")

        q_size = self.queue.size()
        if self.lbl_queue_size:
            self.lbl_queue_size.configure(text=f"{q_size} / {self.MAX_CAPACITY}")
        if self.lbl_queue_front and self.lbl_queue_rear:
            if self.queue.is_empty():
                self.lbl_queue_front.configure(text="None", fg="#94A3B8")
                self.lbl_queue_rear.configure(text="None", fg="#94A3B8")
            else:
                self.lbl_queue_front.configure(text=str(self.queue.get_front()), fg="#0284C7")
                self.lbl_queue_rear.configure(text=str(self.queue.get_rear()), fg="#0284C7")

        if self.lbl_total_ops:
            self.lbl_total_ops.configure(text=str(self.history.total_successful_ops))
        if self.lbl_last_op:
            self.lbl_last_op.configure(text=explanation)

        self._refresh_history_lists()

    def _update_bst_info_panel(self, explanation: str) -> None:
        """Update telemetry cards for BST mode."""
        if self.lbl_bst_size:
            self.lbl_bst_size.configure(text=f"{self.bst.size()} nodes")
        if self.lbl_bst_height:
            self.lbl_bst_height.configure(text=f"{self.bst.height()} levels")
        if self.lbl_bst_root:
            if self.bst.root:
                self.lbl_bst_root.configure(text=f"{self.bst.root.value}", fg="#D97706")
            else:
                self.lbl_bst_root.configure(text="None (Empty)", fg="#94A3B8")
        if self.lbl_bst_minmax:
            if self.bst.is_empty():
                self.lbl_bst_minmax.configure(text="None / None")
            else:
                self.lbl_bst_minmax.configure(text=f"{self.bst.get_min()} / {self.bst.get_max()}")
        if self.lbl_bst_balanced:
            if self.bst.is_balanced():
                self.lbl_bst_balanced.configure(text="Yes (Balanced)", fg="#16A34A")
            else:
                self.lbl_bst_balanced.configure(text="No (Unbalanced)", fg="#DC2626")

        if self.lbl_bst_explanation:
            self.lbl_bst_explanation.configure(text=explanation)

        self._refresh_history_lists()

    def _refresh_history_lists(self) -> None:
        """Populate operation log listboxes in both panels."""
        records = self.history.get_recent(25)
        for lb in [self.history_listbox, self.history_listbox_bst]:
            if lb:
                lb.delete(0, tk.END)
                for rec in records:
                    entry_line = f"#{rec.step_id:02d} [{rec.timestamp}] {rec.structure} {rec.operation}: {rec.value} -> {rec.result_message}"
                    lb.insert(tk.END, entry_line)

    # -------------------------------------------------------------------------
    # STACK OPERATIONS (LIFO)
    # -------------------------------------------------------------------------
    def on_stack_push(self, animate: bool = True) -> None:
        if self.visualizer.is_animating:
            return

        val = self._get_input_value()
        if val is None:
            return

        if self.stack.is_full():
            messagebox.showerror(
                "Stack Overflow!",
                f"Cannot push element '{val}'. The Stack has reached its maximum capacity limit of {self.MAX_CAPACITY} blocks.",
                parent=self
            )
            return

        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            f"Push '{val}' onto Stack",
            bst_items=self.bst.to_list()
        )

        self.stack.push(val)
        target_idx = self.stack.size() - 1

        msg = f"Pushed '{val}' to Stack Top. LIFO invariant preserved. Size={self.stack.size()}."
        self.history.record_operation("STACK", "PUSH", val, msg)
        self.visualizer.set_speech(f"Pushed block '{val}' onto the Stack! It sits at TOP (index {target_idx}).")

        self.visualizer.animate_stack_push(
            val,
            target_idx,
            on_complete=lambda: self._update_info_panel(msg),
            animate=animate
        )

    def on_stack_pop(self, animate: bool = True) -> None:
        if self.visualizer.is_animating:
            return

        if self.stack.is_empty():
            messagebox.showerror(
                "Stack Underflow!",
                "Cannot pop from an empty Stack! In LIFO, there must be at least one block present.",
                parent=self
            )
            return

        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            "Pop from Stack",
            bst_items=self.bst.to_list()
        )

        top_idx = self.stack.size() - 1
        popped_val = self.stack.pop()

        msg = f"Popped '{popped_val}' from Stack Top (LIFO rule). New size={self.stack.size()}."
        self.history.record_operation("STACK", "POP", popped_val, msg)
        self.visualizer.set_speech(f"Popped '{popped_val}' from Stack Top! Notice it was the most recently added block.")

        self.visualizer.animate_stack_pop(
            popped_val,
            top_idx,
            on_complete=lambda: self._update_info_panel(msg),
            animate=animate
        )

    def on_stack_peek(self) -> None:
        if self.visualizer.is_animating:
            return

        if self.stack.is_empty():
            messagebox.showinfo("Stack Empty", "The Stack is empty. Nothing to peek!", parent=self)
            return

        top_val = self.stack.peek()
        top_idx = self.stack.size() - 1

        msg = f"Peeked at Stack Top: '{top_val}' (no element was removed, O(1))."
        self.history.record_operation("STACK", "PEEK", top_val, msg)
        self.visualizer.set_speech(f"Peeking at TOP block '{top_val}'. Size remains {self.stack.size()}.")
        self.visualizer.highlight_stack_element(top_idx)
        self._update_info_panel(msg)

    def on_stack_clear(self) -> None:
        if self.visualizer.is_animating:
            return

        if self.stack.is_empty():
            messagebox.showinfo("Already Empty", "The Stack is already empty.", parent=self)
            return

        if messagebox.askyesno("Clear Stack", "Are you sure you want to clear all blocks from the Stack?", parent=self):
            self.history.push_undo_snapshot(
                self.stack.to_list(),
                self.queue.to_list(),
                "Clear Stack",
                bst_items=self.bst.to_list()
            )
            self.stack.clear()
            msg = "Stack cleared to empty state."
            self.history.record_operation("STACK", "CLEAR", "-", msg)
            self.visualizer.set_speech("Stack has been cleared!")
            self.visualizer.redraw()
            self._update_info_panel(msg)

    # -------------------------------------------------------------------------
    # QUEUE OPERATIONS (FIFO)
    # -------------------------------------------------------------------------
    def on_queue_enqueue(self, animate: bool = True) -> None:
        if self.visualizer.is_animating:
            return

        val = self._get_input_value()
        if val is None:
            return

        if self.queue.is_full():
            messagebox.showerror(
                "Queue Overflow!",
                f"Cannot enqueue element '{val}'. The Queue conveyor has reached its capacity limit of {self.MAX_CAPACITY} blocks.",
                parent=self
            )
            return

        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            f"Enqueue '{val}' into Queue",
            bst_items=self.bst.to_list()
        )

        target_idx = self.queue.size()
        self.queue.enqueue(val)

        msg = f"Enqueued '{val}' at Queue REAR (tail pointer advanced, O(1)). Size={self.queue.size()}."
        self.history.record_operation("QUEUE", "ENQUEUE", val, msg)
        self.visualizer.set_speech(f"Enqueued '{val}' at the REAR! In FIFO, new arrivals wait at the end of the line.")

        self.visualizer.animate_queue_enqueue(
            val,
            target_idx,
            on_complete=lambda: self._update_info_panel(msg),
            animate=animate
        )

    def on_queue_dequeue(self, animate: bool = True) -> None:
        if self.visualizer.is_animating:
            return

        if self.queue.is_empty():
            messagebox.showerror(
                "Queue Underflow!",
                "Cannot dequeue from an empty Queue! No elements are waiting in line.",
                parent=self
            )
            return

        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            "Dequeue from Queue",
            bst_items=self.bst.to_list()
        )

        dequeued_val = self.queue.dequeue()

        msg = f"Dequeued '{dequeued_val}' from Queue FRONT (head pointer advanced, O(1)). New size={self.queue.size()}."
        self.history.record_operation("QUEUE", "DEQUEUE", dequeued_val, msg)
        self.visualizer.set_speech(f"Dequeued '{dequeued_val}' from FRONT! Notice the first arrival was served first (FIFO).")

        self.visualizer.animate_queue_dequeue(
            dequeued_val,
            on_complete=lambda: self._update_info_panel(msg),
            animate=animate
        )

    def on_queue_front(self) -> None:
        if self.visualizer.is_animating:
            return

        if self.queue.is_empty():
            messagebox.showinfo("Queue Empty", "The Queue is empty. No FRONT element exists!", parent=self)
            return

        front_val = self.queue.get_front()
        msg = f"Inspected Queue FRONT: '{front_val}' without removing (O(1))."
        self.history.record_operation("QUEUE", "FRONT", front_val, msg)
        self.visualizer.set_speech(f"Queue FRONT element is '{front_val}'. It is next in line to dequeue!")
        self.visualizer.highlight_queue_element(0)
        self._update_info_panel(msg)

    def on_queue_rear(self) -> None:
        if self.visualizer.is_animating:
            return

        if self.queue.is_empty():
            messagebox.showinfo("Queue Empty", "The Queue is empty. No REAR element exists!", parent=self)
            return

        rear_val = self.queue.get_rear()
        rear_idx = self.queue.size() - 1
        msg = f"Inspected Queue REAR: '{rear_val}' without removing (O(1))."
        self.history.record_operation("QUEUE", "REAR", rear_val, msg)
        self.visualizer.set_speech(f"Queue REAR element is '{rear_val}'. It was the most recent enqueue.")
        self.visualizer.highlight_queue_element(rear_idx)
        self._update_info_panel(msg)

    def on_queue_clear(self) -> None:
        if self.visualizer.is_animating:
            return

        if self.queue.is_empty():
            messagebox.showinfo("Already Empty", "The Queue is already empty.", parent=self)
            return

        if messagebox.askyesno("Clear Queue", "Are you sure you want to clear all blocks from the Queue?", parent=self):
            self.history.push_undo_snapshot(
                self.stack.to_list(),
                self.queue.to_list(),
                "Clear Queue",
                bst_items=self.bst.to_list()
            )
            self.queue.clear()
            msg = "Queue cleared to empty state (front and rear pointers reset to None)."
            self.history.record_operation("QUEUE", "CLEAR", "-", msg)
            self.visualizer.set_speech("Queue has been cleared and pointers reset!")
            self.visualizer.redraw()
            self._update_info_panel(msg)

    # -------------------------------------------------------------------------
    # BST OPERATIONS (MANUAL ALGORITHMS & ANIMATIONS)
    # -------------------------------------------------------------------------
    def on_bst_insert(self, animate: bool = True) -> None:
        if self.visualizer.is_animating:
            return

        if not self.entry_bst_val:
            return
        raw = self.entry_bst_val.get().strip()
        if not raw:
            messagebox.showwarning("Input Required", "Please enter an integer value for the BST node (e.g. 50, 30).", parent=self)
            self.entry_bst_val.focus_set()
            return

        try:
            val = int(raw)
        except ValueError:
            messagebox.showerror("Invalid Input", f"'{raw}' is not a valid integer. BST node values must be integers.", parent=self)
            self.entry_bst_val.focus_set()
            return

        # Snapshot for undo
        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            f"Insert node {val} into BST",
            bst_items=self.bst.to_list()
        )

        success, steps, path = self.bst.insert(val)

        if not success:
            # Duplicate rejected!
            self.history.pop_undo_snapshot()  # No mutation occurred
            dup_msg = f"Duplicate value {val} rejected! BST keys must be unique."
            self.history.record_operation("BST", "INSERT_REJECT", val, dup_msg)

            if self.lbl_bst_op_name:
                self.lbl_bst_op_name.configure(text=f"INSERT {val} (DUPLICATE REJECTED)")
            if self.lbl_bst_explanation:
                self.lbl_bst_explanation.configure(text=dup_msg)
            if self.lbl_bst_complexity:
                self.lbl_bst_complexity.configure(text="Duplicate check: Traversed comparison path to match")

            messagebox.showwarning("Duplicate Value", f"Value {val} already exists in the BST! Duplicates are rejected.", parent=self)
            self.visualizer.animate_bst_duplicate(
                val,
                path,
                on_complete=lambda: self._update_bst_info_panel(dup_msg),
                animate=animate
            )
            return

        # Successful insertion
        msg = f"Inserted node {val} into BST. Total nodes={self.bst.size()}, Height={self.bst.height()}."
        self.history.record_operation("BST", "INSERT", val, msg)

        if self.lbl_bst_op_name:
            self.lbl_bst_op_name.configure(text=f"INSERT NODE {val} [O(log n)]")
        if self.lbl_bst_explanation:
            step_summary = "\n".join(steps[-3:])
            self.lbl_bst_explanation.configure(text=step_summary)
        if self.lbl_bst_complexity:
            self.lbl_bst_complexity.configure(text="Time Complexity: Avg O(log n) | Worst O(n)")

        self.visualizer.animate_bst_insert(
            val,
            path,
            steps,
            on_complete=lambda: self._update_bst_info_panel(msg),
            animate=animate
        )

    def on_bst_search(self, animate: bool = True) -> None:
        if self.visualizer.is_animating:
            return

        if not self.entry_bst_search:
            return
        raw = self.entry_bst_search.get().strip()
        if not raw:
            messagebox.showwarning("Search Input", "Please enter an integer value to search for in the BST.", parent=self)
            return

        try:
            val = int(raw)
        except ValueError:
            messagebox.showerror("Invalid Search Key", f"'{raw}' is not a valid integer.", parent=self)
            return

        if self.bst.is_empty():
            messagebox.showinfo("Tree Empty", "The Binary Search Tree is currently empty. Nothing to search!", parent=self)
            return

        found, steps, path = self.bst.search(val)
        res_str = "FOUND" if found else "NOT FOUND"
        msg = f"Search for {val}: {res_str}. Traversed path: {' ➔ '.join(str(x) for x in path)}."
        self.history.record_operation("BST", "SEARCH", val, msg)

        if self.lbl_bst_op_name:
            self.lbl_bst_op_name.configure(text=f"SEARCH {val} [{res_str}]")
        if self.lbl_bst_explanation:
            self.lbl_bst_explanation.configure(text="\n".join(steps[-3:]))
        if self.lbl_bst_complexity:
            self.lbl_bst_complexity.configure(text="Time Complexity: Avg O(log n) | Worst O(n)")

        self.visualizer.animate_bst_search(
            val,
            path,
            found,
            steps,
            on_complete=lambda: self._update_bst_info_panel(msg),
            animate=animate
        )

    def on_bst_delete(self) -> None:
        if self.visualizer.is_animating:
            return

        if not self.entry_bst_delete:
            return
        raw = self.entry_bst_delete.get().strip()
        if not raw:
            messagebox.showwarning("Delete Input", "Please enter an integer node value to delete.", parent=self)
            return

        try:
            val = int(raw)
        except ValueError:
            messagebox.showerror("Invalid Key", f"'{raw}' is not a valid integer.", parent=self)
            return

        if self.bst.is_empty():
            messagebox.showinfo("Tree Empty", "The Binary Search Tree is currently empty. Nothing to delete!", parent=self)
            return

        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            f"Delete node {val} from BST",
            bst_items=self.bst.to_list()
        )

        success, steps, path = self.bst.delete(val)
        if not success:
            self.history.pop_undo_snapshot()
            messagebox.showinfo("Not Found", f"Node {val} was not found in the BST. Cannot delete.", parent=self)
            return

        msg = f"Deleted node {val} from BST. Case: {steps[-1]}. Remaining size={self.bst.size()}."
        self.history.record_operation("BST", "DELETE", val, msg)

        if self.lbl_bst_op_name:
            self.lbl_bst_op_name.configure(text=f"DELETE NODE {val}")
        if self.lbl_bst_explanation:
            self.lbl_bst_explanation.configure(text="\n".join(steps[-2:]))
        if self.lbl_bst_complexity:
            self.lbl_bst_complexity.configure(text="Time Complexity: Avg O(log n) | Worst O(n)")

        self.visualizer.clear_bst_highlights()
        self.visualizer.set_speech(f"Deleted node {val}! {steps[-1]}")
        self.visualizer.redraw()
        self._update_bst_info_panel(msg)

    def on_bst_clear(self) -> None:
        if self.visualizer.is_animating:
            return

        if self.bst.is_empty():
            messagebox.showinfo("Already Empty", "The Binary Search Tree is already empty.", parent=self)
            return

        if messagebox.askyesno("Clear BST", "Are you sure you want to clear all nodes from the Binary Search Tree?", parent=self):
            self.history.push_undo_snapshot(
                self.stack.to_list(),
                self.queue.to_list(),
                "Clear BST",
                bst_items=self.bst.to_list()
            )
            self.bst.clear()
            self.on_traversal_reset()
            msg = "BST cleared to empty root."
            self.history.record_operation("BST", "CLEAR", "-", msg)
            self.visualizer.set_speech("Binary Search Tree has been cleared!")
            self.visualizer.redraw()
            self._update_bst_info_panel(msg)

    def on_bst_load_sample(self) -> None:
        """
        Loads the sample BST specified in the requirements:
        Values: 50, 30, 70, 20, 40, 60, 80
        Structure:
                      50
                    /    \\
                  30      70
                 /  \\    /  \\
                20  40  60  80
        """
        if self.visualizer.is_animating:
            return

        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            "Load Sample Tree [50, 30, 70, 20, 40, 60, 80]",
            bst_items=self.bst.to_list()
        )

        self.bst.clear()
        sample_vals = [50, 30, 70, 20, 40, 60, 80]
        for val in sample_vals:
            self.bst.insert(val)

        self.on_traversal_reset()
        msg = "Loaded sample BST: [50, 30, 70, 20, 40, 60, 80]. Perfect balanced tree for traversal demos."
        self.history.record_operation("BST", "SAMPLE_TREE", "-", msg)

        if self.lbl_bst_op_name:
            self.lbl_bst_op_name.configure(text="LOAD SAMPLE TREE")
        if self.lbl_bst_explanation:
            self.lbl_bst_explanation.configure(
                text="Constructed 7-node balanced tree:\nRoot: 50 | Left: 30 (20, 40) | Right: 70 (60, 80)"
            )

        self.visualizer.set_speech("Sample tree loaded [50, 30, 70, 20, 40, 60, 80]! Ready for Inorder, Preorder, and Postorder traversals.")
        self.visualizer.redraw()
        self._update_bst_info_panel(msg)

    # -------------------------------------------------------------------------
    # 3D TRAVERSAL ENGINE & ANIMATION PLAYER
    # -------------------------------------------------------------------------
    def on_bst_inorder(self) -> None:
        self.start_traversal("INORDER")

    def on_bst_preorder(self) -> None:
        self.start_traversal("PREORDER")

    def on_bst_postorder(self) -> None:
        self.start_traversal("POSTORDER")

    def start_traversal(self, traversal_type: str) -> None:
        if self.visualizer.is_animating:
            return

        if self.bst.is_empty():
            messagebox.showwarning(
                "Tree Empty",
                "The Binary Search Tree is currently empty! Insert nodes or load the sample tree before traversing.",
                parent=self
            )
            return

        # Cancel any active running traversal
        if self.traversal_timer_id:
            try:
                self.after_cancel(self.traversal_timer_id)
            except Exception:
                pass
            self.traversal_timer_id = None

        self.traversal_mode = traversal_type
        if traversal_type == "INORDER":
            self.traversal_sequence = self.bst.inorder()
            order_name = "INORDER (Left ➔ Root ➔ Right)"
            explanation = "Order: Left Subtree ➔ Root ➔ Right Subtree.\nIn a BST, Inorder visits keys in strictly ascending sorted order!"
        elif traversal_type == "PREORDER":
            self.traversal_sequence = self.bst.preorder()
            order_name = "PREORDER (Root ➔ Left ➔ Right)"
            explanation = "Order: Root ➔ Left Subtree ➔ Right Subtree.\nCommonly used to create a replica of the tree or serialize structure."
        else:
            self.traversal_sequence = self.bst.postorder()
            order_name = "POSTORDER (Left ➔ Right ➔ Root)"
            explanation = "Order: Left Subtree ➔ Right Subtree ➔ Root.\nUseful for bottom-up cleanup, deleting trees, or postfix expression evaluation."

        self.traversal_step = 0
        self.traversal_is_paused = False

        if self.lbl_traversal_type:
            self.lbl_traversal_type.configure(text=order_name)
        if self.lbl_bst_op_name:
            self.lbl_bst_op_name.configure(text=f"{traversal_type} TRAVERSAL")
        if self.lbl_bst_explanation:
            self.lbl_bst_explanation.configure(text=explanation)
        if self.lbl_bst_complexity:
            self.lbl_bst_complexity.configure(text="Time Complexity: O(n) [Visits all n nodes exactly once]")

        # Launch animated playback starting at step 0
        self._run_traversal_step()

    def _run_traversal_step(self) -> None:
        if self.traversal_is_paused:
            return
        if not self.traversal_sequence:
            return

        total = len(self.traversal_sequence)
        if self.traversal_step < total:
            cur_val = self.traversal_sequence[self.traversal_step]
            visited = self.traversal_sequence[: self.traversal_step + 1]

            if self.lbl_traversal_status:
                self.lbl_traversal_status.configure(
                    text=f"Step {self.traversal_step + 1} of {total}: Visiting Node {cur_val}"
                )
            if self.lbl_traversal_seq:
                seq_str = " ➔ ".join(str(x) for x in visited)
                self.lbl_traversal_seq.configure(text=seq_str)

            self.visualizer.highlight_bst_node(cur_val, visited)
            self.visualizer.set_speech(f"{self.traversal_mode.title()} Traversal: Visiting Node {cur_val} (Step {self.traversal_step + 1}/{total})")

            self.traversal_step += 1
            if self.traversal_step < total:
                self.traversal_timer_id = self.after(self.traversal_speed_ms, self._run_traversal_step)
            else:
                # Finished complete traversal sequence
                full_seq = " ➔ ".join(str(x) for x in self.traversal_sequence)
                if self.lbl_traversal_status:
                    self.lbl_traversal_status.configure(
                        text=f"✅ {self.traversal_mode.title()} Complete! ({total} nodes visited)"
                    )
                self.visualizer.highlight_bst_node(self.traversal_sequence[-1], self.traversal_sequence)
                self.visualizer.set_speech(f"{self.traversal_mode.title()} Complete! Result: {full_seq}")
                msg = f"{self.traversal_mode.title()} traversal complete: {full_seq}"
                self.history.record_operation("BST", self.traversal_mode, "-", msg)
                self._update_bst_info_panel(msg)

    def on_traversal_play(self) -> None:
        if self.traversal_is_paused:
            self.on_traversal_resume()
        elif self.traversal_mode:
            self.start_traversal(self.traversal_mode)
        else:
            self.start_traversal("INORDER")

    def on_traversal_pause(self) -> None:
        if self.traversal_timer_id:
            try:
                self.after_cancel(self.traversal_timer_id)
            except Exception:
                pass
            self.traversal_timer_id = None

        self.traversal_is_paused = True
        if self.lbl_traversal_status:
            step_disp = self.traversal_step if self.traversal_step > 0 else 1
            node_disp = self.traversal_sequence[step_disp - 1] if self.traversal_sequence else "-"
            self.lbl_traversal_status.configure(text=f"⏸ Paused at step {step_disp} (Node {node_disp})")
        self.visualizer.set_speech("Traversal paused! Click [Resume] to continue or [Restart] to replay.")

    def on_traversal_resume(self) -> None:
        if not self.traversal_is_paused or not self.traversal_sequence:
            return
        self.traversal_is_paused = False
        if self.traversal_step < len(self.traversal_sequence):
            self.visualizer.set_speech("Resuming traversal...")
            self._run_traversal_step()

    def on_traversal_restart(self) -> None:
        if self.traversal_mode:
            self.start_traversal(self.traversal_mode)
        else:
            self.start_traversal("INORDER")

    def on_traversal_reset(self) -> None:
        if self.traversal_timer_id:
            try:
                self.after_cancel(self.traversal_timer_id)
            except Exception:
                pass
            self.traversal_timer_id = None

        self.traversal_is_paused = False
        self.traversal_step = 0
        if self.lbl_traversal_type:
            self.lbl_traversal_type.configure(text="None Selected")
        if self.lbl_traversal_status:
            self.lbl_traversal_status.configure(text="Idle — Select Inorder, Preorder, or Postorder")
        if self.lbl_traversal_seq:
            self.lbl_traversal_seq.configure(text="None (Run Inorder, Preorder, or Postorder to view)")

        self.visualizer.clear_bst_highlights()
        self.visualizer.set_speech("Traversal reset. Ready for next exploration.")

    def set_traversal_speed(self, speed_ms: int, btn_selected: tk.Button, all_btns: List[tk.Button]) -> None:
        self.traversal_speed_ms = speed_ms
        for b in all_btns:
            b.configure(bg="#E2E8F0", fg="#1E293B", font=("Segoe UI", 7))
        btn_selected.configure(bg="#0284C7", fg="#FFFFFF", font=("Segoe UI", 7, "bold"))

    # -------------------------------------------------------------------------
    # GLOBAL UTILITIES: UNDO, RESET ALL, SCENARIO LOADER
    # -------------------------------------------------------------------------
    def on_undo_operation(self) -> None:
        """Safely restores the prior Stack, Queue, and BST states."""
        if self.visualizer.is_animating:
            return

        if not self.history.can_undo():
            messagebox.showinfo("Nothing to Undo", "No previous actions available to undo.", parent=self)
            return

        snapshot = self.history.pop_undo_snapshot()
        if snapshot is None:
            return

        # Restore Stack
        self.stack.clear()
        for item in snapshot.stack_items:
            self.stack.push(item)

        # Restore Queue
        self.queue.clear()
        for item in snapshot.queue_items:
            self.queue.enqueue(item)

        # Restore BST if captured in snapshot
        if snapshot.bst_items is not None:
            self.bst.clear()
            for item in snapshot.bst_items:
                self.bst.insert(item)

        msg = f"Undid: {snapshot.action_description}. State restored."
        self.history.record_operation("SYSTEM", "UNDO", "-", msg)
        self.visualizer.set_speech(f"Reversed '{snapshot.action_description}'! Models restored.")
        self.visualizer.clear_bst_highlights()
        self.visualizer.redraw()

        if self.current_mode == "BST":
            self._update_bst_info_panel(msg)
        else:
            self._update_info_panel(msg)

    def on_reset_all(self) -> None:
        """Resets Stack, Queue, BST, and Operation History."""
        if self.visualizer.is_animating:
            return

        if messagebox.askyesno("Reset All", "Reset Stack, Queue, BST, and telemetry history to zero?", parent=self):
            self.stack.clear()
            self.queue.clear()
            self.bst.clear()
            self.history.clear()

            if self.traversal_timer_id:
                try:
                    self.after_cancel(self.traversal_timer_id)
                except Exception:
                    pass
                self.traversal_timer_id = None

            self.traversal_is_paused = False
            self.traversal_step = 0

            msg = "All data structures and history reset to default."
            self.visualizer.set_speech("All systems reset to fresh initial state!")
            self.visualizer.clear_bst_highlights()
            self.visualizer.redraw()

            if self.current_mode == "BST":
                self._update_bst_info_panel(msg)
            else:
                self._update_info_panel(msg)

    def load_preset_scenario(self, scenario_type: str) -> None:
        """Loads a pre-configured scenario for classroom/viva demonstrations."""
        if scenario_type == "BST":
            self.switch_mode("BST")
            self.on_bst_load_sample()
            return

        self.stack.clear()
        self.queue.clear()

        if scenario_type == "LIFO":
            for val in [10, 20, 30]:
                self.stack.push(val)
            self.visualizer.set_speech("Loaded LIFO Scenario: Blocks [10, 20, 30] pushed. Try popping 30!")
            msg = "Loaded LIFO Tower scenario (3 blocks in Stack)."

        elif scenario_type == "FIFO":
            for val in ["T1", "T2", "T3"]:
                self.queue.enqueue(val)
            self.visualizer.set_speech("Loaded FIFO Scenario: Ticket queue ['T1', 'T2', 'T3']. Dequeue serves 'T1' first!")
            msg = "Loaded FIFO Conveyor scenario (3 tickets in Queue)."

        else:  # BOTH / LAB
            for val in [10, 20, 30]:
                self.stack.push(val)
            for val in ["A1", "B2", "C3"]:
                self.queue.enqueue(val)
            self.visualizer.set_speech("Loaded Dual Lab Scenario! Ready for college viva demonstration.")
            msg = "Loaded full dual lab scenario (Stack + Queue)."

        self.history.record_operation("SYSTEM", "LOAD_SCENARIO", scenario_type, msg)
        self.visualizer.redraw()
        self._update_info_panel(msg)

    def open_learning_mode(self) -> None:
        """Opens the DSA Academy, concept guides, and Viva Practice Quiz dialog."""
        LearningModeDialog(
            self,
            load_scenario_callback=self.load_preset_scenario,
            reset_callback=self.on_reset_all
        )

    def show_help_dialog(self) -> None:
        """Displays user guide and keyboard shortcuts."""
        help_text = (
            "BLOCKY DSA WORLD — QUICK REFERENCE GUIDE\n\n"
            "MODULES:\n"
            "• Stack & Queue Lab: LIFO tower and FIFO singly linked-list conveyor.\n"
            "• BST Explorer: 3D Binary Search Tree with automated layout & animations.\n\n"
            "BST OPERATIONS:\n"
            "• Insert: Places node according to BST rule (smaller left, greater right).\n"
            "• Search: Traverses comparison path to locate key [Avg O(log n)].\n"
            "• Delete: Handles leaf, 1-child, and 2-child cases (inorder successor).\n"
            "• Traversals: Inorder (sorted), Preorder (structure), Postorder (bottom-up).\n"
            "• Animation Player: Play, Pause, Resume, Restart, and Speed controls.\n\n"
            "COMPLEXITIES:\n"
            "• Stack Push/Pop/Peek: O(1)\n"
            "• Queue Enqueue/Dequeue/Front/Rear: O(1)\n"
            "• BST Search/Insert: Average O(log n), Worst O(n) (unbalanced/skewed tree)\n"
            "• BST Traversals: O(n)\n\n"
            "SAMPLE TREE TESTING:\n"
            "• Values: 50, 30, 70, 20, 40, 60, 80\n"
            "• Click 'Load Sample Tree' to stage instantly!"
        )
        messagebox.showinfo("How to Use Blocky DSA World", help_text, parent=self)

    def destroy(self) -> None:
        """Clean up canvas and traversal timers before application exit."""
        if hasattr(self, "traversal_timer_id") and self.traversal_timer_id:
            try:
                self.after_cancel(self.traversal_timer_id)
            except Exception:
                pass
            self.traversal_timer_id = None

        try:
            if hasattr(self, "visualizer") and self.visualizer:
                self.visualizer.destroy()
        except Exception:
            pass
        super().destroy()


def main():
    """Application entry point."""
    app = BlockyDSAWorldApp()
    app.mainloop()


if __name__ == "__main__":
    main()
