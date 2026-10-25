# 🧱 BLOCKY DSA WORLD — 3D Stack, Queue, BST & Infix to Postfix Kingdom

> **Visualize • Learn • Master Data Structures & Algorithms**  
> An attractive, colorful, Roblox-inspired blocky 3D desktop application built in pure Python that teaches:
> - **Stack (LIFO)** via a vertical block tower
> - **Queue (FIFO)** via a Singly Linked List conveyor runway
> - **Binary Search Tree (BST Explorer)** with 3D nodes, animated search/insert/delete, and traversals
> - **Infix to Postfix Kingdom**: an interactive 3D conversion arena demonstrating Dijkstra's Shunting-Yard algorithm with a custom LIFO Stack, step-by-step 3D animations, Challenge Mode, and Infix Masterclass.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Objectives](#-objectives)
4. [Key Features](#-key-features)
   - [👑 Infix to Postfix Kingdom](#-infix-to-postfix-kingdom)
   - [📦 Stack & Queue Lab](#-stack--queue-lab)
   - [🌳 BST Explorer](#-bst-explorer)
5. [Technologies Used](#-technologies-used)
6. [Core DSA Concepts Implemented](#-core-dsa-concepts-implemented)
7. [Operator Precedence & Associativity Specification](#-operator-precedence--associativity-specification)
8. [University Benchmark Expressions](#-university-benchmark-expressions)
9. [Time & Space Complexity Reference Table](#-time--space-complexity-reference-table)
10. [Project Folder Structure](#-project-folder-structure)
11. [Installation & Setup (Windows)](#-installation--setup-windows)
12. [How to Run the Application](#-how-to-run-the-application)
13. [How to Run the Unit Tests (81 Tests)](#-how-to-run-the-unit-tests-81-tests)
14. [Step-by-Step Operation Examples](#-step-by-step-operation-examples)
15. [Limitations & Future Enhancements](#-limitations--future-enhancements)
16. [Author & License](#-author--license)

---

## 🌟 Project Overview

**BLOCKY DSA WORLD** is an interactive desktop visualization environment created in pure Python using `tkinter`. It transforms abstract Data Structures and Algorithms (DSA) into intuitive, tangible 3D toy blocks inspired by the playful, voxel aesthetic of block-building games like Roblox.

Instead of staring at terminal text or dry whiteboard diagrams, students can explore three interconnected educational locations:
1. **📦 Stack & Queue Lab**: A vertical **Stack Tower (LIFO)** where blocks drop and pop from the top, and a horizontal **Queue Conveyor Runway (FIFO)** where blocks slide from rear to front.
2. **🌳 BST Explorer**: A dedicated 3D Binary Search Tree world where nodes stand as 3D blocks with toy studs connected by 3D cylindrical beams, complete with path-comparison animations for insertion/search/deletion, animated Inorder, Preorder, and Postorder traversals, and dynamic camera pan/zoom controls.
3. **👑 Infix to Postfix Kingdom**: A vibrant 3D floating island dedicated to expression parsing and Reverse Polish Notation (RPN) conversion. Watch tokens glide along the processing lane, operators push onto and pop off the vertical stack tower based on precedence and right-associativity, and operands march directly into the postfix output runway.

Every operation is computed live in Python with custom data structures and animated in real-time with zero external third-party packages or web dependencies.

---

## 🎯 Problem Statement

Students and programmers frequently encounter difficulty mastering:
- **Expression Parsing & Evaluation**: Why human-readable infix expressions ($A + B \times C$) cannot be evaluated directly by compilers from left to right without operator precedence ambiguities.
- **The Shunting-Yard Algorithm**: How a simple LIFO stack manages operator precedence, left/right associativity, and nested parentheses in linear $O(n)$ time.
- **Associativity Invariants**: Why exponentiation ($A \wedge B \wedge C$) is right-associative ($A \wedge (B \wedge C)$) and must **not** pop an existing `^` operator off the stack, while $+$, $-$, $\times$, $/$, $\%$ are left-associative.
- **Why Parentheses Disappear**: How parentheses enforce subexpression evaluation order during conversion and are systematically discarded from the final postfix output.
- **LIFO vs FIFO**: The physical mechanics of Last-In First-Out vs First-In First-Out.
- **Tree Traversals**: How recursive comparison paths operate in a Binary Search Tree.

**Blocky DSA World** solves this by providing a self-contained, offline-first Python desktop application with 100% standard library compliance.

---

## 🚀 Objectives

1. **Interactive Pedagogy**: Provide an intuitive visual mental model for Stack, Queue, BST, and Expression Conversion.
2. **Algorithmic Rigor**: Implement genuine, manual data structures (custom `ConversionStack`, Singly Linked List `Queue`, and Node-based `BinarySearchTree`) with strict pointer invariants.
3. **Smooth Canvas Animations**: Deliver delightful frame-by-frame 3D block movements (parabolic arc block flights, token scanning cursors, glowing pointers) using `tkinter.Canvas.after()` without freezing the GUI thread.
4. **Resilience & Safe State**: Include input validation, duplicate rejection, overflow/underflow warnings, and a snapshot-based **Undo** feature.
5. **Exam Readiness**: Integrate an in-app "Infix Masterclass", "DSA Academy", preset scenarios, and a randomized **Challenge Mode** with score tracking.

---

## ✨ Key Features

### 👑 Infix to Postfix Kingdom
- **Blocky 3D Conversion Arena**:
  - Floating 3D island terrain with grass top, gold stud trim, and glowing purple, cyan, yellow, and pink crystal ore deposits in the cliff face.
  - Spanning grand entrance banner reading `👑 INFIX TO POSTFIX KINGDOM 👑` framed by twin 3D pillars with flame lanterns.
  - **Interactive 3D Portals**:
    - `🚪 RETURN [DSA World]`: Clickable 3D portal with deep indigo frame and glowing purple vortex that seamlessly transports the player back to the Stack & Queue Lab.
    - `🌀 RESET [Clear All]`: Clickable 3D portal with cyan vortex that resets the expression converter and arena.
  - **Infix Token Processing Lane**: Raised 3D conveyor track displaying the discrete tokens of the current expression, complete with a neon blue animated scanner cursor.
  - **Operator Stack Tower (LIFO)**: Vertical platform with side rails and a golden `👑 TOP` crown displaying stack items from bottom to top.
  - **Postfix Output Runway**: Horizontal platform with directional neon chevrons displaying output blocks in exact evaluation order.
  - **3D Tech Explanation Board**: Floating terminal console showing current step number, active token, action taken, and theoretical reasoning.
  - **Coder Mascot Avatar ("Blocky Bob")**: Interactive 3D mascot with live speech bubble commenting on every step.
- **Full Expression Parsing & Tokenization**:
  - Supports single-letter variables (`A`, `B`), multi-letter variables (`total`, `price`, `count`), multi-digit integers (`123`, `456`), decimal numbers (`3.14`, `0.5`), and whitespace-tolerant input.
  - Supported operators: `+`, `-`, `*`, `/`, `%`, `^`, and arbitrarily nested parentheses `( )`.
  - Comprehensive syntax validation: detects empty input, consecutive operators, missing operands, unbalanced parentheses, empty parentheses, and explicitly flags unary operators.
- **Benchmark Presets**: One-click quick load buttons for 6 canonical university test expressions:
  - `A+B*C` $\to$ `A B C * +`
  - `(A+B)*C` $\to$ `A B + C *`
  - `A+B*(C-D)` $\to$ `A B C D - * +`
  - `A^B^C` $\to$ `A B C ^ ^`
  - `(A+B)*(C-D)` $\to$ `A B + C D - *`
  - `A+B*C-D/E` $\to$ `A B C * + D E / -`
- **Playback & Navigation Controls**:
  - `▶ Play` / `⏸ Pause`: Automated continuous step playback.
  - `⏮ Prev` / `⏭ Next`: Step-by-step pedagogical progression.
  - `⏭ Skip to Result`: Instantly jumps to final converted postfix expression.
  - `🔄 Reset Arena`: Restores arena to step 0.
  - **Speed Slider**: Continuously adjustable animation delay from 0ms (Instant) to 900ms.
- **Postfix Output Deck**:
  - `📋 Copy Result`: Copies postfix string directly to the OS clipboard with GUI feedback.
  - `🔁 Replay`: Re-triggers full animated playback from step 0.
- **Challenge Mode (Practice Viva / Exam)**:
  - Generates randomized valid infix expressions with varied precedence and parentheses across Easy, Medium, and Hard difficulties.
  - Prompts the user to predict the postfix result.
  - Validates answer order (ignoring harmless whitespace), provides instant feedback, updates session score/accuracy (`X / Y (Z%)`), and offers a `👁 Watch Solution` button to step through in 3D.
- **Interactive Trace Table**: Scrollable Treeview listing every step `#`, `Token`, and `Action Summary`. Clicking any row instantly jumps the 3D arena to that exact state.

---

### 📦 Stack & Queue Lab
- **Stack Tower (LIFO)**:
  - Vertical slot guides with index indicators `[0]` to `[6]`.
  - Floating golden crown pointer: `👑 TOP [LIFO]`.
  - Animated 3D drop on **Push** and skyward lift-off on **Pop**.
  - Non-destructive **Peek** with golden aura highlight.
- **Queue Conveyor Belt (FIFO)**:
  - Voxel runway with directional neon chevrons `⏩ ⏩ ⏩`.
  - Intake chute on right (`📥 REAR`) and exit chute on left (`🚀 FRONT`).
  - Animated slide onto the belt on **Enqueue** and exit roll-off on **Dequeue**.
  - Dual pointers: Cyan `⬅ FRONT` (Head) and Magenta `REAR ➡` (Tail).

---

### 🌳 BST Explorer
- Manual, pointer-based `Node(value, left, right)` and `BinarySearchTree` classes without third-party packages.
- Non-overlapping 3D isometric layout rendering with 3D connecting beams, directional branch labels (`L` / `R`), and golden `👑 ROOT` badge.
- **Animated Operations**:
  - **Insert**: Drops block from sky, highlights comparison path (Green = Less/Left, Magenta = Greater/Right), and anchors at leaf.
  - **Duplicate Rejection**: Gracefully detects and flags existing keys.
  - **Search**: Highlights traversal path from root downward.
  - **Delete**: Handles leaf, 1-child, and 2-child cases (inorder successor replacement).
- **Traversals**: Inorder (sorted), Preorder (structure), and Postorder (bottom-up) with step highlights and live output list updates.
- **Interactive 3D Camera**: Drag left mouse button to pan, use mouse wheel to zoom in/out, and reset camera view.

---

## 🛠 Technologies Used

- **Language**: Python 3.8+ (tested on Python 3.14 on Windows)
- **GUI Toolkit**: `tkinter` & `ttk` (Standard Python Library)
- **Graphics & Animation Engine**: `tkinter.Canvas` with isometric 3D projection, depth shading, top studs, and non-blocking `after()` event loops.
- **Testing Framework**: `unittest` (Standard Python Library)
- **Dependencies**: **Zero** external libraries required! (No Pygame, Ursina, OpenGL, Node.js, or pip packages needed).

---

## 🧠 Core DSA Concepts Implemented

### 1. Infix to Postfix Conversion (Dijkstra's Shunting-Yard Algorithm)
- **Infix Notation**: Operators are placed between operands (e.g. $A + B$). Requires parentheses and operator precedence conventions to remove ambiguity.
- **Postfix Notation (Reverse Polish Notation — RPN)**: Operators appear after their operands (e.g. $A B +$). Evaluated strictly left-to-right by stack machines with **zero** parentheses required.
- **Algorithm Rules**:
  1. **Operands**: Added directly to the Postfix output runway.
  2. **Left Parenthesis `(`**: Pushed onto the Stack to define a subexpression scope.
  3. **Right Parenthesis `)`**: Pop operators from the Stack to the output runway until the matching `(` is popped. The parentheses are discarded.
  4. **Operators (`+`, `-`, `*`, `/`, `%`, `^`)**:
     - While the top of the stack has an operator with **greater precedence**, or **equal precedence with left-associativity**, pop it to the output runway.
     - Push the incoming operator onto the Stack.
  5. **End of Expression**: Pop all remaining operators from the Stack to the output runway.

---

## 📐 Operator Precedence & Associativity Specification

| Symbol | Name | Precedence | Associativity | Stack Pop Condition on Top Operator $T$ with Incoming $O$ |
| :---: | :---: | :---: | :---: | :--- |
| **`(`** | Left Parenthesis | Scope Boundary | None | Never popped by an incoming operator; acts as boundary until `)` |
| **`^`** | Exponentiation | **3 (Highest)** | **Right (R)** | Pop $T$ only if $\text{prec}(T) > \text{prec}(O)$. Equal precedence does **not** pop! |
| **`*`, `/`, `%`** | Multiply, Divide, Mod | **2 (Medium)** | **Left (L)** | Pop $T$ if $\text{prec}(T) \ge \text{prec}(O)$ |
| **`+`, `-`** | Addition, Subtraction | **1 (Lowest)** | **Left (L)** | Pop $T$ if $\text{prec}(T) \ge \text{prec}(O)$ |

> **Critical Associativity Note**:  
> Because exponentiation (`^`) is **right-associative**, $A \wedge B \wedge C = A \wedge (B \wedge C)$. When scanning the second `^`, the first `^` on top of the stack has equal precedence (3 == 3), but must **remain on the stack**. The final postfix expression is `A B C ^ ^`.

---

## 🎓 University Benchmark Expressions

The conversion algorithm has been verified against standard university computer science examination test cases:

| # | Infix Expression | Correct Postfix (RPN) | Pedagogical Focus |
| :---: | :--- | :--- | :--- |
| 1 | `A+B` | `A B +` | Fundamental binary operator |
| 2 | `A+B*C` | `A B C * +` | Operator precedence ($* > +$) |
| 3 | `(A+B)*C` | `A B + C *` | Parentheses overriding precedence |
| 4 | `A*B+C` | `A B * C +` | Left-to-right evaluation |
| 5 | `A+B*(C-D)` | `A B C D - * +` | Precedence + nested grouping |
| 6 | `(A+B)*(C-D)` | `A B + C D - *` | Symmetric dual grouping |
| 7 | `A^B^C` | `A B C ^ ^` | **Right-associativity** of exponentiation |
| 8 | `A+B*C-D/E` | `A B C * + D E / -` | Mixed precedence with subtraction & division |
| 9 | `(A+B)/(C+D)*(E-F)` | `A B + C D + / E F - *` | Complex multi-parenthesis pipeline |
| 10 | `A+B*(C^D-E)` | `A B C D ^ E - * +` | Exponentiation inside parentheses |
| 11 | `123+456*2` | `123 456 2 * +` | Multi-digit integer literals |
| 12 | `total+price*count` | `total price count * +` | Multi-character variable identifiers |
| 13 | `3.14*r^2` | `3.14 r 2 ^ *` | Decimal float literals & identifiers |

---

## ⏱ Time & Space Complexity Reference Table

| Data Structure / Algorithm | Operation | Average Time | Worst-case Time | Space Complexity | Description |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Infix to Postfix** | Conversion | **$O(n)$** | **$O(n)$** | **$O(n)$** | $n$ tokens. Each token pushed and popped at most once |
| **Infix to Postfix** | Tokenization | **$O(n)$** | **$O(n)$** | **$O(n)$** | Single-pass linear lexical scanner |
| **Stack** | Push / Pop / Peek | **$O(1)$** | **$O(1)$** | **$O(1)$** | Constant-time LIFO top operations |
| **Queue (Linked List)** | Enqueue / Dequeue | **$O(1)$** | **$O(1)$** | **$O(1)$** | Constant-time pointer updates at `front` and `rear` |
| **BST** | Search / Insert / Delete | **$O(\log n)$** | **$O(n)$** | **$O(h)$** | Tree height $h$; skewed tree degrades to linear |
| **BST** | Inorder / Pre / Post | **$O(n)$** | **$O(n)$** | **$O(n)$** | Systematically visits every tree node once |

---

## 📁 Project Folder Structure

```text
blocky-dsa-world/
│
├── main.py                     # Main application entry point, module switcher & GUI
├── requirements.txt            # Dependency notice (Python standard library only)
├── README.md                   # Comprehensive project documentation & viva guide
├── .gitignore                  # Python-specific git exclusion rules
│
├── dsa/                        # Pure algorithm & data structure engine
│   ├── __init__.py             # Exports InfixToPostfixConverter, ConversionStack, etc.
│   └── infix_to_postfix.py     # Tokenizer, Validator, Shunting-Yard engine, Step Trace & Generator
│
├── src/                        # GUI & Visualization components
│   ├── __init__.py             # Public package symbols
│   ├── stack.py                # Stack class (LIFO, Python list-backed)
│   ├── queue_linked_list.py    # Node & Queue classes (FIFO, Singly Linked List)
│   ├── bst.py                  # Node & BinarySearchTree classes (Search, Insert, Delete, Traversals)
│   ├── visualizer.py           # 3D Canvas visualizer, Infix Kingdom arena, BST World, portals
│   ├── learning_mode.py        # Educational tabs, Infix Masterclass modal, Viva quiz
│   ├── history.py              # Operation telemetry & safe undo snapshots
│   └── infix_to_postfix.py     # Re-export bridge to dsa.infix_to_postfix
│
└── tests/                      # Automated test suite (81 tests)
    ├── __init__.py             # Test package marker
    ├── test_infix_to_postfix.py# 38 unit tests for conversion, precedence, associativity, errors
    ├── test_stack.py           # 8 unit tests for Stack operations & invariants
    ├── test_queue.py           # 11 unit tests for Singly Linked List Queue & pointers
    ├── test_bst.py             # 12 unit tests for BST operations, sample tree, edge cases
    └── test_gui_integration.py # 12 headless end-to-end GUI integration tests
```

---

## 💻 Installation & Setup (Windows)

### Prerequisites
- Windows 10 or 11
- Python 3.8 or newer (with `tkinter` included by default)

### Steps
1. Open PowerShell or Command Prompt.
2. Verify Python installation:
   ```powershell
   python --version
   ```
3. Navigate to the project directory:
   ```powershell
   cd "C:\Users\Vipul\OneDrive\Documents\Desktop\project 4"
   ```
4. Verify Tkinter is ready:
   ```powershell
   python -c "import tkinter; print('Tkinter is ready!')"
   ```

---

## 🎮 How to Run the Application

Launch the desktop visualizer with a single command:

```powershell
python main.py
```

### Module Navigation
Use the top **MODULE DECK** tab buttons:
- **📦 Stack & Queue Lab**: Push/Pop on the Stack Tower or Enqueue/Dequeue on the Conveyor Belt.
- **🌳 BST Explorer**: 3D Binary Search Tree world with camera controls and traversal player.
- **👑 Infix to Postfix Kingdom**: 3D conversion arena with token lane, stack tower, postfix runway, and challenge mode.

### Infix Kingdom Walkthrough
1. **Choose or Enter an Expression**:
   - Type any custom expression into the input field (e.g. `(A+B)*C` or `123+456*2`).
   - Or click one of the 6 quick sample buttons (`A+B*C`, `(A+B)*C`, `A+B*(C-D)`, `A^B^C`, `(A+B)*(C-D)`, `A+B*C-D/E`).
2. **Step Through the Conversion**:
   - Click `▶ Play` for smooth continuous 3D block flight animations.
   - Click `⏭ Next` or `⏮ Prev` to step forward and backward.
   - Click `⏭ Skip to Result` for instant conversion.
   - Click any row in the **Full Step Trace** table to jump directly to that step.
3. **Copy the Result**:
   - Click `📋 Copy Result` to copy the generated postfix string to your clipboard.
4. **Practice in Challenge Mode**:
   - Select difficulty (Easy, Medium, Hard) and click `🎲 New Challenge`.
   - Predict the postfix result and click `✅ Submit Prediction`.
   - Click `👁 Watch Solution` to view the conversion in the 3D arena.
5. **Portals**:
   - Click the purple **🚪 RETURN** portal on the left to return to the Stack & Queue Lab.
   - Click the cyan **🌀 RESET** portal on the right to reset the conversion arena.

---

## 🧪 How to Run the Unit Tests (81 Tests)

The test suite covers:
- Complete Infix to Postfix tokenization, operator precedence, right-associativity, and parentheses.
- Multi-digit numbers, multi-letter variables, decimal numbers, and invalid syntax rejection.
- Random challenge generation validity.
- Boundary conditions (empty structures, full capacity overflow, duplicate BST insertions).
- Pointer invariant checks (e.g. verifying `rear` becomes `None` on empty queue).
- Headless GUI integration tests for all modules.

Run the entire test suite using Python's standard `unittest` test runner:

```powershell
python -m unittest discover tests -v
```

Expected output:
```text
test_all_samples_match (tests.test_infix_to_postfix.TestInfixToPostfix) ... ok
test_exponentiation_right_associativity (tests.test_infix_to_postfix.TestInfixToPostfix) ... ok
test_multi_digit_numbers (tests.test_infix_to_postfix.TestInfixToPostfix) ... ok
test_syntax_errors_caught (tests.test_infix_to_postfix.TestInfixToPostfix) ... ok
test_infix_mode_switch (tests.test_gui_integration.TestGUIIntegration) ... ok
test_infix_step_navigation (tests.test_gui_integration.TestGUIIntegration) ... ok
test_infix_challenge_mode (tests.test_gui_integration.TestGUIIntegration) ... ok
...
Ran 81 tests in 4.466s

OK
```

---

## 📖 Step-by-Step Operation Examples

### Example: Converting `A+B*C` to Postfix
1. **Token `A` (Operand)**: Sent directly to output $\to$ Output: `[A]`, Stack: `[]`.
2. **Token `+` (Operator)**: Stack is empty $\to$ Push `+` $\to$ Output: `[A]`, Stack: `[+]`.
3. **Token `B` (Operand)**: Sent directly to output $\to$ Output: `[A, B]`, Stack: `[+]`.
4. **Token `*` (Operator)**: Precedence of `*` (2) > `+` (1) $\to$ Push `*` $\to$ Output: `[A, B]`, Stack: `[+, *]`.
5. **Token `C` (Operand)**: Sent directly to output $\to$ Output: `[A, B, C]`, Stack: `[+, *]`.
6. **End of Expression (Drain Stack)**:
   - Pop `*` $\to$ Output: `[A, B, C, *]`.
   - Pop `+` $\to$ Output: `[A, B, C, *, +]`.
7. **Final Postfix Result**: `A B C * +`

### Example: Converting `A^B^C` (Right-Associative Exponentiation)
1. **Token `A`**: Output: `[A]`.
2. **Token `^`**: Stack: `[^]`.
3. **Token `B`**: Output: `[A, B]`.
4. **Token `^`**: Incoming `^` has precedence 3. Top of stack `^` has precedence 3. Because `^` is **right-associative**, top is **not** popped! Push incoming `^` $\to$ Stack: `[^, ^]`.
5. **Token `C`**: Output: `[A, B, C]`.
6. **Drain Stack**: Pop top `^`, then second `^` $\to$ Output: `A B C ^ ^`.

---

## ⚠️ Limitations & Future Enhancements

### Current Limitations
- **Capacity Ceiling in Lab Mode**: Stack Tower and Queue Runway in the classic Lab are capped at 7 items for fixed-canvas clarity. Infix Kingdom supports expressions of arbitrary practical length.
- **Single-Threaded Tkinter Event Loop**: Animation frames run via `root.after()`. Resizing during mid-flight block motion gracefully settles the active block at its destination.

### Future Enhancements
- **Postfix Expression Evaluator**: Enter numeric values for variables (e.g. $A=2, B=3, C=4$) and watch a 3D postfix evaluation stack compute the final numeric result.
- **Sound Effects**: Audio chimes using standard Windows `winsound` for block placements and portal warps.
- **Prefix (Polish Notation) Kingdom**: Bidirectional converter from Infix to Prefix notation.

---

## 👤 Author & License

- **Author**: Senior Python Developer, DSA Professor & 3D Game Developer
- **Tech Stack**: Python 3 Standard Library + Tkinter Canvas
- **License**: MIT License — free for educational, classroom, and personal use.
