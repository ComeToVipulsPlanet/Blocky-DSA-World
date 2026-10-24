# 🧱 BLOCKY DSA WORLD — 3D-Style Stack, Queue & Binary Search Tree (BST) Visualizer

> **Visualize • Learn • Master Data Structures**  
> An attractive, colorful, Roblox-inspired blocky desktop application that teaches Stack, Queue, and Binary Search Tree (BST) data structures through interactive 3D operations, path comparison animations, tree traversals, live telemetry metrics, and a built-in Viva Academy.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Objectives](#-objectives)
4. [Key Features](#-key-features)
5. [Technologies Used](#-technologies-used)
6. [Core DSA Concepts Implemented](#-core-dsa-concepts-implemented)
7. [Time Complexity Reference Table](#-time-complexity-reference-table)
8. [Project Folder Structure](#-project-folder-structure)
9. [Installation & Setup (Windows)](#-installation--setup-windows)
10. [How to Run the Application](#-how-to-run-the-application)
11. [How to Run the Unit Tests](#-how-to-run-the-unit-tests)
12. [Step-by-Step Operation Examples](#-step-by-step-operation-examples)
13. [Screenshots & Visuals](#-screenshots--visuals)
14. [Limitations & Future Enhancements](#-limitations--future-enhancements)
15. [GitHub Upload Instructions](#-github-upload-instructions)
16. [Author & License](#-author--license)

---

## 🌟 Project Overview

**BLOCKY DSA WORLD** is an interactive desktop visualization tool created in pure Python using `tkinter`. It transforms abstract Data Structures and Algorithms (DSA) into intuitive, tangible 3D toy blocks inspired by the playful, voxel aesthetic of block-building games like Roblox.

Instead of staring at terminal text or dry whiteboard diagrams, students can explore:
- A vertical **Stack Tower (LIFO)** where blocks drop and pop from the top.
- A horizontal **Queue Conveyor Belt (FIFO)** where blocks slide from rear to front.
- A dedicated **3D Binary Search Tree (BST) World** where tree nodes stand as 3D blocks with toy studs connected by 3D cylindrical beams, complete with path-comparison animations for insertion/search/deletion, animated Inorder, Preorder, and Postorder traversals, and dynamic camera pan/zoom controls.

Every operation—Push, Pop, Peek, Enqueue, Dequeue, Front, Rear, BST Insert, Search, Delete, and Traversals—is animated in real time, directly reflecting the state of pure Python algorithms without external dependencies.

---

## 🎯 Problem Statement

Beginners in computer science often struggle to understand:
- The fundamental difference between **LIFO (Last In, First Out)** and **FIFO (First In, First Out)**.
- Why removing an element from the front of a standard Python list (`list.pop(0)`) is computationally slow ($O(N)$), while a **Singly Linked List** allows $O(1)$ constant time removal.
- How internal pointers (`front`, `rear`, `next`, `left`, `right`) actually shift and update during data insertion and deletion.
- How a **Binary Search Tree** compares keys at each node, branching left or right, and how tree traversals (Inorder, Preorder, Postorder) systematically visit every node.
- How to answer critical technical questions during college viva and lab examinations.

Standard visualizers are often either complex web apps with heavy npm dependencies, or static mockups that do not run locally on simple student PCs. **Blocky DSA World** solves this by providing a self-contained, offline-first Python desktop application with 100% standard library compliance.

---

## 🚀 Objectives

1. **Interactive Pedagogy**: Provide an intuitive visual mental model for Stack, Queue, and BST operations.
2. **Algorithmic Rigor**: Implement genuine, manual data structures (List-backed Stack, Singly Linked List Queue, and Node-based Binary Search Tree) with strict pointer invariants.
3. **Smooth Canvas Animations**: Deliver delightful frame-by-frame 3D block movements using `tkinter.Canvas.after()` without freezing the GUI thread.
4. **Resilience & Safe State**: Include input validation, duplicate rejection, overflow/underflow warnings, and a snapshot-based **Undo** feature.
5. **Viva Exam Readiness**: Integrate an in-app "DSA Academy" complete with concept summaries, demo scenarios, and an interactive 7-question viva quiz.

---

## ✨ Key Features

- **Roblox-Inspired 3D Voxel Aesthetic**:
  - Sky blue environment with procedural drifting voxel clouds and a glowing voxel sun.
  - Voxel terrain with checkerboard grass layers and decorative pine trees.
  - Friendly mascot avatar (**"Coder Alex" / "Blocky Bob"**) with animated idle breathing and an interactive speech bubble explaining every action.
  - Multi-face shaded 3D blocks with top studs (cylindrical buttons) for an authentic blocky toy aesthetic.
- **Dedicated Stack Tower (LIFO)**:
  - Vertical slot guides with index indicators `[0]` to `[6]`.
  - Floating golden crown pointer: `👑 TOP [LIFO]`.
  - Animated 3D drop on **Push** and skyward lift-off on **Pop**.
  - Non-destructive **Peek** with golden aura highlight.
- **Dedicated Queue Conveyor Belt (FIFO)**:
  - Voxel runway with directional neon chevrons `⏩ ⏩ ⏩`.
  - Clear intake chute on the right (`📥 REAR`) and exit chute on the left (`🚀 FRONT`).
  - Animated slide onto the belt on **Enqueue** and exit roll-off on **Dequeue**.
  - Separate pointers: Cyan `⬅ FRONT` (Head) and Magenta `REAR ➡` (Tail).
- **Dedicated Binary Search Tree (BST) Explorer**:
  - Manual, pointer-based `Node(value, left, right)` and `BinarySearchTree` classes without third-party packages.
  - Non-overlapping 3D isometric layout rendering with 3D connecting beams, directional branch labels (`L` / `R`), and golden `👑 ROOT` badge.
  - **Animated Insert**: Drops new block from sky, highlights comparison path (Green = Less/Left, Magenta = Greater/Right), and anchors at correct leaf slot.
  - **Duplicate Rejection**: Gracefully detects and flashes warning when attempting to insert existing keys.
  - **Animated Search**: Highlights traversal path from root downward to target node.
  - **Animated Delete**: Supports all 3 BST deletion cases (leaf node, node with 1 child, and node with 2 children using inorder successor replacement).
  - **Animated Traversals**: Inorder (Left → Root → Right, guaranteed sorted order), Preorder (Root → Left → Right), and Postorder (Left → Right → Root) with step-by-step node highlights and live output list updates.
  - **Animation Player Deck**: Play, Pause, Resume, Restart, and Speed buttons (0.5x, 1x, 2x).
  - **Interactive 3D Camera**: Drag left mouse button to pan, use mouse wheel (or buttons) to zoom in/out, and reset camera view.
  - **Sample Tree Loader**: Instant one-click population of canonical sample tree `[50, 30, 70, 20, 40, 60, 80]`.
- **Safe Undo System**:
  - Automatically captures state snapshots before every mutating operation across Stack, Queue, and BST.
  - Reverts state safely without data corruption or memory leaks.
- **Control Deck & Input Validation**:
  - Text/numeric input field with `[Enter]` shortcut.
  - `🎲 Rand` generator and quick preset chips (`50`, `30`, `70`, `20`, `40`, `60`, `80`).
- **Telemetry & Stats Panel**:
  - Real-time size, height, min, max, and balance status indicators.
  - Scrollable chronological operation history with timestamped logs.
  - Human-readable narrative explaining the last operation in plain English.
- **In-App DSA Academy & Viva Quiz**:
  - Core DSA concept breakdowns (Stack, Queue, Singly Linked List, and BST).
  - Pre-staged scenarios (Load LIFO Demo, Load FIFO Demo, Dual Lab Demo, BST Explorer Demo).
  - 7-question multiple-choice practice quiz with instant grading and detailed explanations.

---

## 🛠 Technologies Used

- **Language**: Python 3.8+ (tested on Python 3.14 on Windows)
- **GUI Toolkit**: `tkinter` & `ttk` (Standard Python Library)
- **Graphics & Animation Engine**: `tkinter.Canvas` with isometric projection math, 3D shading, and non-blocking `after()` event scheduling.
- **Testing Framework**: `unittest` (Standard Python Library)
- **Dependencies**: **Zero** external libraries required! (No Pygame, OpenGL, Node.js, or pip packages needed).

---

## 🧠 Core DSA Concepts Implemented

### 1. Stack — LIFO (Last In, First Out)
- **Mechanism**: Elements are inserted and removed from the same end, known as the **TOP**.
- **Analogy**: A stack of Minecraft/Roblox blocks or cafeteria trays.
- **Implementation**: Encapsulated in `src/stack.py` using an internal Python list `self._items`.
  - `push(item)`: Appends element to the end of the list ($O(1)$ amortized).
  - `pop()`: Removes and returns the last element ($O(1)$).
  - `peek()`: Returns `self._items[-1]` without removing ($O(1)$).
  - `is_empty()`, `is_full()`, `size()`, `clear()`.

### 2. Queue — FIFO (First In, First Out) via Singly Linked List
- **Mechanism**: Elements are inserted at the **REAR** (tail) and removed from the **FRONT** (head).
- **Analogy**: A line of students waiting at the school cafeteria lunch counter.
- **Why a Singly Linked List?**  
  In a standard Python list, `list.pop(0)` takes $O(N)$ time because all remaining elements must shift left in memory. By implementing a manual **Singly Linked List** with `Node(value, next)`:
  - `enqueue(item)`: Attaches a new node to `self.rear.next` and updates `rear` in **$O(1)$ constant time**.
  - `dequeue()`: Moves `self.front` to `self.front.next` in **$O(1)$ constant time** with zero memory shifting.
  - **Pointer Invariant**: When the final node is dequeued, `self.rear` is explicitly reset to `None` so it does not point to an orphaned node.

### 3. Binary Search Tree (BST) — Hierarchical Search Structure
- **Mechanism**: Non-linear tree structure where each node has at most two children (`left` and `right`).
- **BST Invariant**: For every node $N$, all keys in the left subtree are strictly $< N.val$, and all keys in the right subtree are strictly $> N.val$.
- **Implementation**: Encapsulated in `src/bst.py` with manual `Node` references.
  - `insert(val)`: Recursively or iteratively navigates down comparing values to insert at the correct leaf position. Rejects duplicate values.
  - `search(val)`: Halves search space at each level, returning boolean and visited comparison path.
  - `delete(val)`: Handles all three cases:
    - **Leaf Node**: Simply detaches node from parent.
    - **Single Child**: Replaces node with its sole child.
    - **Two Children**: Locates inorder successor (smallest in right subtree), replaces value, and deletes successor recursively.
  - **Traversals**:
    - **Inorder** ($L \to \text{Root} \to R$): Guaranteed strictly ascending order for valid BSTs.
    - **Preorder** ($\text{Root} \to L \to R$): Used for tree duplication and serialization.
    - **Postorder** ($L \to R \to \text{Root}$): Used for bottom-up tree deletion and dependency evaluation.

---

## ⏱ Time Complexity Reference Table

| Data Structure | Operation | Method | Average Time | Worst-case Time | Space Complexity | Explanation |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Stack** | Push | `push(x)` | **$O(1)$** | **$O(1)$** amortized | $O(1)$ | Appends to the top of internal list |
| **Stack** | Pop | `pop()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Removes top element without shifting |
| **Stack** | Peek | `peek()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Direct index access to top element |
| **Stack** | Is Empty | `is_empty()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Checks if size is zero |
| **Queue** | Enqueue | `enqueue(x)` | **$O(1)$** | **$O(1)$** | $O(1)$ | Direct insertion at `rear` pointer |
| **Queue** | Dequeue | `dequeue()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Direct removal at `front` pointer |
| **Queue** | Front | `get_front()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Reads head node value |
| **Queue** | Rear | `get_rear()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Reads tail node value |
| **Queue** | Is Empty | `is_empty()` | **$O(1)$** | **$O(1)$** | $O(1)$ | Checks if `front` is `None` |
| **BST** | Search | `search(k)` | **$O(\log n)$** | **$O(n)$** | $O(h)$ | Skewed tree degrades to linear search |
| **BST** | Insert | `insert(k)` | **$O(\log n)$** | **$O(n)$** | $O(h)$ | Navigates down tree height $h$ |
| **BST** | Delete | `delete(k)` | **$O(\log n)$** | **$O(n)$** | $O(h)$ | Replaces with inorder successor if 2 children |
| **BST** | Inorder | `inorder()` | **$O(n)$** | **$O(n)$** | $O(n)$ | Visits every node in sorted order |
| **BST** | Preorder | `preorder()` | **$O(n)$** | **$O(n)$** | $O(n)$ | Visits root before subtrees |
| **BST** | Postorder | `postorder()` | **$O(n)$** | **$O(n)$** | $O(n)$ | Visits subtrees before root |

---

## 📁 Project Folder Structure

```text
blocky-dsa-world/
│
├── main.py                     # Main application entry point, dual lab & BST GUI
├── requirements.txt            # Dependency notice (Python standard library only)
├── README.md                   # Comprehensive project documentation & viva guide
├── .gitignore                  # Python-specific git exclusion rules
│
├── src/                        # Modular source code
│   ├── __init__.py             # Exposes public package symbols (Stack, Queue, BST)
│   ├── stack.py                # Stack class (LIFO, Python list-backed)
│   ├── queue_linked_list.py    # Node & Queue classes (FIFO, Singly Linked List)
│   ├── bst.py                  # Node & BinarySearchTree classes (Search, Insert, Delete, Traversals)
│   ├── visualizer.py           # 3D Canvas visualizer, voxel scenery, animations, 3D BST World
│   ├── learning_mode.py        # Educational tabs, scenario presets, viva quiz
│   └── history.py              # Operation telemetry & safe undo snapshots (Stack, Queue, BST)
│
├── tests/                      # Automated test suite (37 tests)
│   ├── __init__.py             # Test package marker
│   ├── test_stack.py           # Unit tests for Stack operations & invariants
│   ├── test_queue.py           # Unit tests for Singly Linked List Queue & pointers
│   ├── test_bst.py             # Unit tests for BST operations, sample tree, & edge cases
│   └── test_gui_integration.py # Headless end-to-end GUI integration tests
│
└── assets/                     # Media & screenshot documentation
    └── README.md               # Screenshot placement guidelines
```

---

## 💻 Installation & Setup (Windows)

### Prerequisites
- Windows 10 or 11
- Python 3.8 or newer (comes with `tkinter` pre-installed on Windows)

### Steps
1. Open PowerShell or Command Prompt.
2. Verify your Python installation:
   ```powershell
   python --version
   ```
3. Navigate to the project directory:
   ```powershell
   cd "C:\path\to\blocky-dsa-world"
   ```
4. Verify Tkinter is available:
   ```powershell
   python -c "import tkinter; print('Tkinter is ready!')"
   ```

---

## 🎮 How to Run the Application

Launch the desktop visualizer with a single command:

```powershell
python main.py
```

### Quick Walkthrough
1. **Switch Modules**: Use the top navigation tabs:
   - **📦 Stack & Queue Lab**: Push/Pop on the Stack Tower or Enqueue/Dequeue on the Conveyor Belt.
   - **🌳 BST Explorer**: Full 3D Binary Search Tree world with camera controls and traversal player.
2. **Load Sample BST**: In BST Explorer, click `⭐ Load Sample Tree (50, 30, 70, 20, 40, 60, 80)`.
3. **Run Traversals**:
   - Click `🔄 Inorder (L-Root-R)` -> Watch blocks highlight one-by-one in ascending sorted order: `[20, 30, 40, 50, 60, 70, 80]`.
   - Click `🌱 Preorder (Root-L-R)` -> Visited root first: `[50, 30, 20, 40, 70, 60, 80]`.
   - Click `🍂 Postorder (L-R-Root)` -> Visited subtrees first: `[20, 40, 30, 60, 80, 70, 50]`.
4. **Animation Player**: Use `⏸ Pause`, `▶ Resume`, `🔄 Restart`, and speed controls (`0.5x`, `1x`, `2x`) during any active traversal.
5. **Interactive Camera**: Drag canvas with left mouse button to pan 3D scene; scroll wheel or `+` / `-` buttons to zoom in and out.
6. **Undo an Action**: Click `↩ UNDO Last Action` anytime to safely step backward.
7. **Launch Academy**: Click `🎓 DSA Academy & Quiz` in the header for lessons and quizzes.

---

## 🧪 How to Run the Unit Tests

The test suite covers:
- Boundary conditions (empty structures, full capacity overflow, duplicate BST insertions).
- Pointer invariant checks (e.g., verifying `rear` becomes `None` when the last queue element is dequeued).
- LIFO, FIFO, and BST ordering verification.
- Complete canonical sample tree traversal verification against expected outputs.
- Non-blocking headless GUI integration tests.

Run all tests via Python's standard `unittest` test runner:

```powershell
python -m unittest discover tests -v
```

Expected output:
```text
test_copy (test_stack.TestStack) ... ok
test_lifo_order (test_stack.TestStack) ... ok
test_peek_behavior (test_stack.TestStack) ... ok
test_single_element_removal_resets_rear (test_queue.TestQueue) ... ok
test_fifo_order (test_queue.TestQueue) ... ok
test_stack_gui_lifecycle (test_gui_integration.TestGUIIntegration) ... ok
...
Ran 27 tests in 1.111s

OK
```

---

## 📖 Step-by-Step Operation Examples

### Example 1: Demonstrating LIFO (Stack)
1. Push `10` -> Stack has `[10]`. Top is `10`.
2. Push `20` -> Stack has `[10, 20]`. Top is `20`.
3. Push `30` -> Stack has `[10, 20, 30]`. Top is `30`.
4. Click `⬇ POP`: Block `30` is popped first, even though `10` was entered first.
   - **Conclusion**: *Last In, First Out (LIFO)*.

### Example 2: Demonstrating FIFO (Queue)
1. Enqueue `"A1"` -> Queue has `["A1"]`. Front is `"A1"`, Rear is `"A1"`.
2. Enqueue `"B2"` -> Queue has `["A1", "B2"]`. Front is `"A1"`, Rear is `"B2"`.
3. Enqueue `"C3"` -> Queue has `["A1", "B2", "C3"]`.
4. Click `⏪ DEQUEUE`: Block `"A1"` is removed first because it entered first.
   - **Conclusion**: *First In, First Out (FIFO)*.

---

## 📸 Screenshots & Visuals

Genuine screenshots can be captured directly from your screen when running `python main.py` and placed in the `assets/` directory:

| Screenshot | Description |
| :--- | :--- |
| `assets/screenshot_overview.png` | Complete UI showing 3D blocks on Stack Tower and Queue Conveyor. |
| `assets/screenshot_learning_mode.png` | The DSA Academy dialog showing viva concepts and practice quiz. |
| `assets/screenshot_telemetry.png` | Real-time metrics card showing size, pointers, and history logs. |

---

## ⚠️ Limitations & Future Enhancements

### Current Limitations
- **Capacity Ceiling**: Stack and Queue are capped at 7 items each to ensure clear, high-resolution rendering without canvas scrolling.
- **Single-Threaded Tkinter Event Loop**: Animation frames run via `root.after()`. While completely non-blocking, resizing the window during a mid-frame transition redraws the target block at the resting slot.

### Future Enhancements
- **Circular Queue Visualizer**: A 3D circular carousel showing how array indices wrap around using modulo arithmetic (`(rear + 1) % MAX`).
- **Sound Effects**: Audio chimes using standard Windows `winsound` for block placements and pop sounds.
- **Double-Ended Queue (Deque)**: Support for pushing and popping at both ends.

---

## 📤 GitHub Upload Instructions

To upload this project to your GitHub account:

1. Open PowerShell in the project directory:
   ```powershell
   cd "C:\Users\Vipul\OneDrive\Documents\Desktop\project 4"
   ```
2. Initialize a local git repository:
   ```powershell
   git init
   ```
3. Stage all project files:
   ```powershell
   git add .
   ```
4. Commit the files:
   ```powershell
   git commit -m "Initial commit: Blocky DSA World 3D-Style Stack & Queue Visualizer"
   ```
5. Rename the branch to `main`:
   ```powershell
   git branch -M main
   ```
6. Add your GitHub remote repository (replace with your repository URL):
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/blocky-dsa-world.git
   ```
7. Push to GitHub:
   ```powershell
   git push -u origin main
   ```

---
