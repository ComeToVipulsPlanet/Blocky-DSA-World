"""
Learning Mode and Viva Practice Quiz Module
-------------------------------------------
Provides beginner-friendly explanations of LIFO, FIFO, Singly Linked Lists,
preset interactive scenarios with reset capabilities, and an interactive 5-question
Viva Practice Quiz with immediate feedback and explanations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, List


class LearningModeDialog(tk.Toplevel):
    """
    Learning Mode pop-up window containing comprehensive visual guides,
    step-by-step scenario demonstrations, and an interactive viva preparation quiz.
    """

    def __init__(
        self,
        parent: tk.Tk,
        load_scenario_callback: Optional[Callable[[str], None]] = None,
        reset_callback: Optional[Callable[[], None]] = None
    ):
        super().__init__(parent)
        self.title("🎓 DSA Academy & Viva Practice — Blocky World")
        self.geometry("860x650")
        self.minsize(760, 560)
        self.configure(bg="#F0F4F8")

        self.load_scenario_callback = load_scenario_callback
        self.reset_callback = reset_callback

        # Transient and focus
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self) -> None:
        # Header Banner
        header = tk.Frame(self, bg="#2C3E50", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header,
            text="🎓 BLOCKY DSA ACADEMY & VIVA GUIDE",
            font=("Segoe UI", 15, "bold"),
            fg="#F1C40F",
            bg="#2C3E50"
        )
        title_lbl.pack(anchor="w", padx=20, pady=(12, 2))

        subtitle_lbl = tk.Label(
            header,
            text="Master Stack (LIFO) & Queue (FIFO) • Linked List Magic • Viva Ready Answers",
            font=("Segoe UI", 9),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        subtitle_lbl.pack(anchor="w", padx=20)

        # Notebook tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#F0F4F8")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[14, 6])
        style.map("TNotebook.Tab", background=[("selected", "#3498DB")], foreground=[("selected", "#FFFFFF")])

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        tab_concepts = tk.Frame(notebook, bg="#FFFFFF")
        tab_scenarios = tk.Frame(notebook, bg="#FFFFFF")
        tab_quiz = tk.Frame(notebook, bg="#FFFFFF")

        notebook.add(tab_concepts, text=" 📘 Core DSA Concepts ")
        notebook.add(tab_scenarios, text=" 🕹 Interactive Demos ")
        notebook.add(tab_quiz, text=" 🏆 Viva Practice Quiz ")

        self._build_concepts_tab(tab_concepts)
        self._build_scenarios_tab(tab_scenarios)
        self._build_quiz_tab(tab_quiz)

    def _build_concepts_tab(self, parent: tk.Frame) -> None:
        canvas = tk.Canvas(parent, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        content = [
            ("📦 1. STACK — LIFO (Last In, First Out)", "#E74C3C", [
                ("Concept", "A Stack is a linear data structure where elements are added and removed from the same end, called the TOP."),
                ("LIFO Rule", "The LAST element inserted is the FIRST element to be removed (think of a stack of Roblox toy blocks, a stack of dinner plates, or browser Back button history)."),
                ("Key Operations", "• Push: Adds a new block to the top.\n• Pop: Removes and returns the top block.\n• Peek: Reads the top block without removing it."),
                ("Time Complexity", "• Push: O(1) amortized (Python list append adds to end)\n• Pop: O(1) (Python list pop() removes from end)\n• Peek: O(1) (direct index access list[-1])"),
            ]),
            ("🚀 2. QUEUE — FIFO (First In, First Out)", "#2980B9", [
                ("Concept", "A Queue is a linear data structure where elements are added at one end (REAR) and removed from the opposite end (FRONT)."),
                ("FIFO Rule", "The FIRST element inserted is the FIRST element to be removed (think of a school cafeteria line, movie ticket counter, or printer jobs)."),
                ("Key Operations", "• Enqueue: Inserts a new block at the REAR.\n• Dequeue: Removes the block from the FRONT.\n• Front: Inspects the first block without removing.\n• Rear: Inspects the last block without removing."),
                ("Time Complexity", "• Enqueue: O(1) (tail pointer directs insertion instantly)\n• Dequeue: O(1) (head pointer advances instantly)\n• Front/Rear: O(1)"),
            ]),
            ("🔗 3. WHY A SINGLY LINKED LIST FOR THE QUEUE?", "#27AE60", [
                ("The Array Problem", "If a Queue is built using a normal Python list, dequeue requires list.pop(0). This forces all remaining (N - 1) items to shift one index left, resulting in an expensive O(N) time!"),
                ("The Linked List Solution", "By creating a Node class with 'value' and 'next' pointers, we maintain two references: 'front' and 'rear'.\n1. Enqueue: We attach the new node to rear.next and update rear (O(1)).\n2. Dequeue: We move front to front.next (O(1)) — zero shifting required!"),
                ("Crucial Invariant", "When the last remaining node is dequeued, both 'front' AND 'rear' must be reset to None! Otherwise, rear would point to a disconnected zombie node."),
            ])
        ]

        for section_title, color, items in content:
            card = tk.LabelFrame(
                scrollable_frame,
                text=f"  {section_title}  ",
                font=("Segoe UI", 11, "bold"),
                fg=color,
                bg="#FFFFFF",
                bd=2,
                relief="groove"
            )
            card.pack(fill=tk.X, padx=10, pady=8, expand=True)

            for subtitle, text in items:
                row = tk.Frame(card, bg="#FFFFFF")
                row.pack(fill=tk.X, padx=12, pady=5)
                lbl_sub = tk.Label(row, text=f"{subtitle}:", font=("Segoe UI", 9, "bold"), fg="#34495E", bg="#FFFFFF", width=16, anchor="nw")
                lbl_sub.pack(side=tk.LEFT, anchor="nw")
                lbl_txt = tk.Label(row, text=text, font=("Segoe UI", 9), fg="#2C3E50", bg="#FFFFFF", justify="left", wraplength=520, anchor="w")
                lbl_txt.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _build_scenarios_tab(self, parent: tk.Frame) -> None:
        container = tk.Frame(parent, bg="#FFFFFF", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        info_lbl = tk.Label(
            container,
            text="Test real-world DSA scenarios with pre-configured block sequences.\nClick an example below to automatically stage it on the 3D visualizer!",
            font=("Segoe UI", 10),
            fg="#2C3E50",
            bg="#FFFFFF",
            justify="center"
        )
        info_lbl.pack(pady=(0, 15))

        # Demo 1: LIFO Walkthrough
        demo1_card = tk.LabelFrame(container, text="  Scenario A: LIFO Tower (Stack)  ", font=("Segoe UI", 10, "bold"), fg="#E74C3C", bg="#FDFEFE", padx=12, pady=10)
        demo1_card.pack(fill=tk.X, pady=8)

        tk.Label(
            demo1_card,
            text="Simulates stacking blocks [10, 20, 30]. When popped, notice 30 is popped first,\neven though 10 was inserted first. That is Last In, First Out!",
            font=("Segoe UI", 9),
            fg="#34495E",
            bg="#FDFEFE",
            justify="left"
        ).pack(side=tk.LEFT, padx=10)

        btn_demo1 = tk.Button(
            demo1_card,
            text="🚀 Load LIFO Demo",
            font=("Segoe UI", 9, "bold"),
            bg="#E74C3C",
            fg="#FFFFFF",
            activebackground="#C0392B",
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda: self._on_load_scenario("LIFO")
        )
        btn_demo1.pack(side=tk.RIGHT, padx=10)

        # Demo 2: FIFO Conveyor
        demo2_card = tk.LabelFrame(container, text="  Scenario B: FIFO Cafeteria Queue (Queue)  ", font=("Segoe UI", 10, "bold"), fg="#2980B9", bg="#FDFEFE", padx=12, pady=10)
        demo2_card.pack(fill=tk.X, pady=8)

        tk.Label(
            demo2_card,
            text="Simulates a line of ticket holders ['A1', 'B2', 'C3']. The first person to arrive ('A1')\nis the first person dequeued and served. First In, First Out!",
            font=("Segoe UI", 9),
            fg="#34495E",
            bg="#FDFEFE",
            justify="left"
        ).pack(side=tk.LEFT, padx=10)

        btn_demo2 = tk.Button(
            demo2_card,
            text="🚀 Load FIFO Demo",
            font=("Segoe UI", 9, "bold"),
            bg="#2980B9",
            fg="#FFFFFF",
            activebackground="#1F618D",
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda: self._on_load_scenario("FIFO")
        )
        btn_demo2.pack(side=tk.RIGHT, padx=10)

        # Demo 3: Mixed Operations
        demo3_card = tk.LabelFrame(container, text="  Scenario C: Full Lab Demo (Stack & Queue Together)  ", font=("Segoe UI", 10, "bold"), fg="#27AE60", bg="#FDFEFE", padx=12, pady=10)
        demo3_card.pack(fill=tk.X, pady=8)

        tk.Label(
            demo3_card,
            text="Fills both Stack and Queue with sample blocks so you can demonstrate\nPush/Pop and Enqueue/Dequeue side-by-side to your college examiner.",
            font=("Segoe UI", 9),
            fg="#34495E",
            bg="#FDFEFE",
            justify="left"
        ).pack(side=tk.LEFT, padx=10)

        btn_demo3 = tk.Button(
            demo3_card,
            text="🚀 Load Lab Demo",
            font=("Segoe UI", 9, "bold"),
            bg="#27AE60",
            fg="#FFFFFF",
            activebackground="#1E8449",
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda: self._on_load_scenario("BOTH")
        )
        btn_demo3.pack(side=tk.RIGHT, padx=10)

        # Reset button
        reset_frame = tk.Frame(container, bg="#FFFFFF")
        reset_frame.pack(fill=tk.X, pady=15)

        btn_reset = tk.Button(
            reset_frame,
            text="🔄 Reset Visualizer to Clean State",
            font=("Segoe UI", 10, "bold"),
            bg="#7F8C8D",
            fg="#FFFFFF",
            activebackground="#616A6B",
            cursor="hand2",
            padx=16,
            pady=8,
            command=self._on_reset_visualizer
        )
        btn_reset.pack(anchor="center")

    def _on_load_scenario(self, scenario_type: str) -> None:
        if self.load_scenario_callback:
            self.load_scenario_callback(scenario_type)
            messagebox.showinfo("Scenario Loaded", f"Successfully loaded the '{scenario_type}' demonstration scenario!\nSwitch back to the main window to watch or interact.", parent=self)

    def _on_reset_visualizer(self) -> None:
        if self.reset_callback:
            self.reset_callback()
            messagebox.showinfo("Reset Complete", "The visualizer has been cleared and reset to its initial clean state.", parent=self)

    def _build_quiz_tab(self, parent: tk.Frame) -> None:
        canvas = tk.Canvas(parent, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFFFF", padx=15, pady=10)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Questions data
        self.quiz_questions = [
            {
                "id": 1,
                "question": "1. What does the term LIFO stand for in a Stack data structure?",
                "options": [
                    "A) Linear Input Fast Output",
                    "B) Last In, First Out",
                    "C) Least Indexed Fixed Order",
                    "D) Late In Flight Operation"
                ],
                "correct": 1,
                "explanation": "LIFO stands for Last In, First Out. The most recently added element is placed at the top and will be the first one removed."
            },
            {
                "id": 2,
                "question": "2. In a Singly Linked List Queue with front and rear pointers, what is the time complexity of Enqueue and Dequeue?",
                "options": [
                    "A) O(1) for both Enqueue and Dequeue",
                    "B) O(N) for Enqueue, O(1) for Dequeue",
                    "C) O(1) for Enqueue, O(N) for Dequeue",
                    "D) O(log N) for both"
                ],
                "correct": 0,
                "explanation": "Both run in O(1) constant time! Rear pointer allows instant insertion at the tail, and front pointer allows instant removal at the head."
            },
            {
                "id": 3,
                "question": "3. When the last remaining element is dequeued from a Queue, what must the rear pointer be updated to?",
                "options": [
                    "A) It stays pointing to the deleted node",
                    "B) It points to the next available memory slot",
                    "C) It must be updated to None",
                    "D) It points back to front node"
                ],
                "correct": 2,
                "explanation": "CRITICAL POINTER RULE: When the last node is removed, front becomes None. The rear pointer MUST also be reset to None; otherwise it would remain pointing to an orphaned node."
            },
            {
                "id": 4,
                "question": "4. Why is a Linked List Queue preferred over a standard Python list queue with list.pop(0)?",
                "options": [
                    "A) Linked list uses less memory than an empty list",
                    "B) list.pop(0) requires shifting all remaining elements left, taking O(N) time",
                    "C) Python lists cannot store numbers",
                    "D) Linked lists are faster for sorting"
                ],
                "correct": 1,
                "explanation": "list.pop(0) takes O(N) linear time because all remaining elements must be shifted in memory. A linked list head pointer changes in O(1) without shifting any elements!"
            },
            {
                "id": 5,
                "question": "5. Which data structure is fundamental to implementing Function Call Stacks and Undo/Redo features?",
                "options": [
                    "A) Queue (FIFO)",
                    "B) Binary Search Tree",
                    "C) Stack (LIFO)",
                    "D) Priority Queue"
                ],
                "correct": 2,
                "explanation": "Stack (LIFO) is used for Function Call Stacks and Undo operations because the most recent function call or action must be reversed or returned first."
            }
        ]

        self.quiz_vars: List[tk.IntVar] = []
        self.feedback_labels: List[tk.Label] = []

        for q in self.quiz_questions:
            q_box = tk.LabelFrame(
                scrollable_frame,
                text=f" Question {q['id']} ",
                font=("Segoe UI", 10, "bold"),
                fg="#2C3E50",
                bg="#FFFFFF",
                bd=2,
                relief="groove"
            )
            q_box.pack(fill=tk.X, pady=8, expand=True)

            q_text = tk.Label(
                q_box,
                text=q["question"],
                font=("Segoe UI", 9, "bold"),
                fg="#1A5276",
                bg="#FFFFFF",
                wraplength=680,
                justify="left"
            )
            q_text.pack(anchor="w", padx=10, pady=(6, 4))

            var = tk.IntVar(value=-1)
            self.quiz_vars.append(var)

            for opt_idx, opt_text in enumerate(q["options"]):
                rb = tk.Radiobutton(
                    q_box,
                    text=opt_text,
                    variable=var,
                    value=opt_idx,
                    font=("Segoe UI", 9),
                    bg="#FFFFFF",
                    activebackground="#FFFFFF",
                    fg="#2C3E50",
                    selectcolor="#E8F8F5"
                )
                rb.pack(anchor="w", padx=20, pady=2)

            feedback_lbl = tk.Label(
                q_box,
                text="",
                font=("Segoe UI", 9),
                bg="#FFFFFF",
                wraplength=680,
                justify="left"
            )
            feedback_lbl.pack(anchor="w", padx=10, pady=(4, 6))
            self.feedback_labels.append(feedback_lbl)

        # Submit button & Score Banner
        submit_frame = tk.Frame(scrollable_frame, bg="#FFFFFF")
        submit_frame.pack(fill=tk.X, pady=15)

        self.btn_submit_quiz = tk.Button(
            submit_frame,
            text="📝 Submit Answers & Check Score",
            font=("Segoe UI", 10, "bold"),
            bg="#27AE60",
            fg="#FFFFFF",
            activebackground="#1E8449",
            cursor="hand2",
            padx=18,
            pady=8,
            command=self._grade_quiz
        )
        self.btn_submit_quiz.pack(side=tk.LEFT, padx=10)

        self.score_lbl = tk.Label(
            submit_frame,
            text="Select your answers and click Submit!",
            font=("Segoe UI", 10, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF"
        )
        self.score_lbl.pack(side=tk.LEFT, padx=15)

    def _grade_quiz(self) -> None:
        score = 0
        total = len(self.quiz_questions)

        for i, q in enumerate(self.quiz_questions):
            user_choice = self.quiz_vars[i].get()
            feedback = self.feedback_labels[i]

            if user_choice == -1:
                feedback.configure(
                    text="⚠️ Please select an option for this question.",
                    fg="#D35400"
                )
            elif user_choice == q["correct"]:
                score += 1
                feedback.configure(
                    text=f"✅ Correct! {q['explanation']}",
                    fg="#27AE60"
                )
            else:
                correct_letter = ["A", "B", "C", "D"][q["correct"]]
                feedback.configure(
                    text=f"❌ Incorrect. Correct answer is ({correct_letter}). {q['explanation']}",
                    fg="#C0392B"
                )

        # Update overall banner
        if score == total:
            msg = f"🎉 Perfect Score! {score}/{total} — You are 100% Viva Ready!"
            color = "#27AE60"
        elif score >= 3:
            msg = f"👍 Good Job! {score}/{total} — Review the explanations above for full mastery."
            color = "#2980B9"
        else:
            msg = f"📚 Score: {score}/{total} — Take another look at the 'Core DSA Concepts' tab!"
            color = "#E67E22"

        self.score_lbl.configure(text=msg, fg=color)
