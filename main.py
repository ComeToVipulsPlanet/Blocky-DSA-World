"""
BLOCKY DSA WORLD — 3D-Style Stack & Queue Visualizer
===================================================
A vibrant, Roblox-inspired desktop educational application that teaches
Stack (LIFO) and Queue (FIFO via Singly Linked List) data structures through
interactive operations, 3D voxel animations, live metrics, and viva exam preparation.

Author: Senior Python Developer & DSA Instructor
Tech Stack: Python 3 Standard Library + Tkinter Canvas
"""

import os
import random
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Optional

# Ensure directory containing main.py is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.stack import Stack
from src.queue_linked_list import Queue
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
        self.title("BLOCKY DSA WORLD — 3D-Style Stack & Queue Visualizer")
        self.geometry("1300x820")
        self.minsize(1080, 700)
        self.configure(bg="#E2E8F0")

        # Core Data Models
        self.stack = Stack(capacity=self.MAX_CAPACITY)
        self.queue = Queue(capacity=self.MAX_CAPACITY)
        self.history = HistoryTracker(max_history=60, max_undo=25)

        # UI Components reference
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

        # Build GUI
        self._build_header()
        self._build_main_layout()
        self._build_status_footer()

        # Connect data to Visualizer
        self.visualizer.set_data_sources(self.stack, self.queue)
        self._update_info_panel("System initialized. Ready for operations.")

    # -------------------------------------------------------------------------
    # UI CONSTRUCTION
    # -------------------------------------------------------------------------
    def _build_header(self) -> None:
        header = tk.Frame(self, bg="#0F172A", height=78)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Left Header Branding
        brand_frame = tk.Frame(header, bg="#0F172A")
        brand_frame.pack(side=tk.LEFT, padx=22, pady=10)

        title_lbl = tk.Label(
            brand_frame,
            text="🧱 BLOCKY DSA WORLD",
            font=("Segoe UI", 16, "bold"),
            fg="#FACC15",
            bg="#0F172A"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            brand_frame,
            text="Visualize • Learn • Master Data Structures | 3D-Style Interactive Lab",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A"
        )
        sub_lbl.pack(anchor="w")

        # Right Header Badges & Action Buttons
        badge_frame = tk.Frame(header, bg="#0F172A")
        badge_frame.pack(side=tk.RIGHT, padx=20, pady=14)

        # Python + DSA Badge
        badge_python = tk.Label(
            badge_frame,
            text=" 🐍 Python 3 + Tkinter ",
            font=("Segoe UI", 8, "bold"),
            fg="#0F172A",
            bg="#38BDF8",
            padx=8,
            pady=3
        )
        badge_python.pack(side=tk.LEFT, padx=6)

        badge_engine = tk.Label(
            badge_frame,
            text=" ⚡ LIFO & FIFO Engine ",
            font=("Segoe UI", 8, "bold"),
            fg="#0F172A",
            bg="#4ADE80",
            padx=8,
            pady=3
        )
        badge_engine.pack(side=tk.LEFT, padx=6)

        # Quick Viva Academy Button
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
            padx=10,
            pady=3,
            command=self.open_learning_mode
        )
        btn_academy.pack(side=tk.LEFT, padx=10)

        # Help Button
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

    def _build_main_layout(self) -> None:
        body = tk.Frame(self, bg="#CBD5E1")
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        # Left Control Panel (Fixed Width: ~280px)
        left_panel = tk.Frame(body, bg="#F8FAFC", width=290, bd=1, relief="ridge")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        left_panel.pack_propagate(False)
        self._build_control_panel(left_panel)

        # Right Information Panel (Fixed Width: ~300px)
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
        # Title of Control Panel
        tk.Label(
            parent,
            text="🎮 CONTROL DECK",
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

    def _build_info_panel(self, parent: tk.Frame) -> None:
        # Title of Info Panel
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
        """Validate and return text/number from input entry."""
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

    def _update_info_panel(self, explanation: str) -> None:
        # 1. Stack Status
        stk_size = self.stack.size()
        self.lbl_stack_size.configure(text=f"{stk_size} / {self.MAX_CAPACITY}")
        if self.stack.is_empty():
            self.lbl_stack_top.configure(text="None (Empty)", fg="#94A3B8")
        else:
            self.lbl_stack_top.configure(text=str(self.stack.peek()), fg="#E11D48")

        # 2. Queue Status
        q_size = self.queue.size()
        self.lbl_queue_size.configure(text=f"{q_size} / {self.MAX_CAPACITY}")
        if self.queue.is_empty():
            self.lbl_queue_front.configure(text="None", fg="#94A3B8")
            self.lbl_queue_rear.configure(text="None", fg="#94A3B8")
        else:
            self.lbl_queue_front.configure(text=str(self.queue.get_front()), fg="#0284C7")
            self.lbl_queue_rear.configure(text=str(self.queue.get_rear()), fg="#0284C7")

        # 3. Counters & Explanation
        self.lbl_total_ops.configure(text=str(self.history.total_successful_ops))
        self.lbl_last_op.configure(text=explanation)

        # 4. Refresh History Listbox
        self.history_listbox.delete(0, tk.END)
        for rec in self.history.get_recent(25):
            entry_line = f"#{rec.step_id:02d} [{rec.timestamp}] {rec.structure} {rec.operation}: {rec.value} -> {rec.result_message}"
            self.history_listbox.insert(tk.END, entry_line)

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

        # Snapshot for undo
        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            f"Push '{val}' onto Stack"
        )

        # Update data model
        self.stack.push(val)
        target_idx = self.stack.size() - 1

        msg = f"Pushed '{val}' to Stack Top. LIFO invariant preserved. Size={self.stack.size()}."
        self.history.record_operation("STACK", "PUSH", val, msg)
        self.visualizer.set_speech(f"Pushed block '{val}' onto the Stack! It sits at TOP (index {target_idx}).")

        # Trigger 3D Drop Animation
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

        # Snapshot for undo
        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            "Pop from Stack"
        )

        top_idx = self.stack.size() - 1
        popped_val = self.stack.pop()

        msg = f"Popped '{popped_val}' from Stack Top (LIFO rule). New size={self.stack.size()}."
        self.history.record_operation("STACK", "POP", popped_val, msg)
        self.visualizer.set_speech(f"Popped '{popped_val}' from Stack Top! Notice it was the most recently added block.")

        # Trigger 3D Rise Animation
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
                "Clear Stack"
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

        # Snapshot for undo
        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            f"Enqueue '{val}' into Queue"
        )

        target_idx = self.queue.size()
        self.queue.enqueue(val)

        msg = f"Enqueued '{val}' at Queue REAR (tail pointer advanced, O(1)). Size={self.queue.size()}."
        self.history.record_operation("QUEUE", "ENQUEUE", val, msg)
        self.visualizer.set_speech(f"Enqueued '{val}' at the REAR! In FIFO, new arrivals wait at the end of the line.")

        # Trigger Conveyor Slide Animation
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

        # Snapshot for undo
        self.history.push_undo_snapshot(
            self.stack.to_list(),
            self.queue.to_list(),
            "Dequeue from Queue"
        )

        dequeued_val = self.queue.dequeue()

        msg = f"Dequeued '{dequeued_val}' from Queue FRONT (head pointer advanced, O(1)). New size={self.queue.size()}."
        self.history.record_operation("QUEUE", "DEQUEUE", dequeued_val, msg)
        self.visualizer.set_speech(f"Dequeued '{dequeued_val}' from FRONT! Notice the first arrival was served first (FIFO).")

        # Trigger Conveyor Exit Animation
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
                "Clear Queue"
            )
            self.queue.clear()
            msg = "Queue cleared to empty state (front and rear pointers reset to None)."
            self.history.record_operation("QUEUE", "CLEAR", "-", msg)
            self.visualizer.set_speech("Queue has been cleared and pointers reset!")
            self.visualizer.redraw()
            self._update_info_panel(msg)

    # -------------------------------------------------------------------------
    # GLOBAL UTILITIES: UNDO, RESET ALL, SCENARIO LOADER
    # -------------------------------------------------------------------------
    def on_undo_operation(self) -> None:
        """Safely restores the prior Stack and Queue states."""
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

        msg = f"Undid: {snapshot.action_description}. State restored."
        self.history.record_operation("SYSTEM", "UNDO", "-", msg)
        self.visualizer.set_speech(f"Reversed '{snapshot.action_description}'! Models restored.")
        self.visualizer.redraw()
        self._update_info_panel(msg)

    def on_reset_all(self) -> None:
        """Resets both Stack, Queue, and Operation History."""
        if self.visualizer.is_animating:
            return

        if messagebox.askyesno("Reset All", "Reset both Stack, Queue, and telemetry history to zero?", parent=self):
            self.stack.clear()
            self.queue.clear()
            self.history.clear()
            msg = "All data structures and history reset to default."
            self.visualizer.set_speech("All systems reset to fresh initial state!")
            self.visualizer.redraw()
            self._update_info_panel(msg)

    def load_preset_scenario(self, scenario_type: str) -> None:
        """Loads a pre-configured scenario for classroom/viva demonstrations."""
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
            "1. Enter Value: Type any number or word in the Input Box.\n"
            "2. Push / Pop / Peek: Operates on the Stack (LIFO Tower on left).\n"
            "3. Enqueue / Dequeue: Operates on the Queue (FIFO Runway on right).\n"
            "4. Undo Button: Safely reverts your last mutation without data loss.\n"
            "5. DSA Academy: Interactive Viva Quiz & LIFO/FIFO concept lessons.\n\n"
            "Time Complexity Rules:\n"
            "• Stack Push, Pop, Peek: O(1)\n"
            "• Queue Enqueue, Dequeue, Front, Rear: O(1) via Singly Linked List pointers!\n\n"
            "Keyboard Shortcut:\n"
            "• Press [Enter] inside the value input field to quickly Push to Stack."
        )
        messagebox.showinfo("How to Use Blocky DSA World", help_text, parent=self)

    def destroy(self) -> None:
        """Clean up canvas timers before application exit."""
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
