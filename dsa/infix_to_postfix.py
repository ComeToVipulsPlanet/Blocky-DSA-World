"""
Infix to Postfix Conversion Engine — Blocky DSA World
======================================================
Implements a complete, robust, educational Infix to Postfix (Reverse Polish
Notation) conversion algorithm utilizing a custom Stack data structure.

Features:
- Pure Python implementation (Zero external dependencies).
- Strict LIFO Stack implementation with custom capacity and inspection.
- Full operator precedence and associativity support:
    * Exponentiation: ^ (Precedence 3, Right-Associative)
    * Multiplication, Division, Modulus: *, /, % (Precedence 2, Left-Associative)
    * Addition, Subtraction: +, - (Precedence 1, Left-Associative)
    * Parentheses: ( ) (Grouping controls)
- Multi-character support:
    * Single-letter operands (A, B, x, y)
    * Multi-letter identifiers (total, price, count)
    * Multi-digit integer literals (123, 456)
    * Floating-point / decimal literals (3.14, 0.5)
- Comprehensive expression validation and detailed error reporting.
- Fine-grained step-by-step conversion recording for 3D animation simulation.
- Random practice expression generator for Challenge Mode.
- Clear time & space complexity telemetry: Time O(n), Space O(n).
"""

from dataclasses import dataclass
from enum import Enum, auto
import random
import re
from typing import Any, Dict, List, NamedTuple, Optional, Tuple


# -----------------------------------------------------------------------------
# 1. TOKENS & OPERATOR SPECIFICATIONS
# -----------------------------------------------------------------------------

class TokenType(Enum):
    OPERAND = auto()
    OPERATOR = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()


@dataclass(frozen=True)
class Token:
    """Represents a discrete lexical token in an expression."""
    type: TokenType
    value: str
    position: int  # 0-indexed character start position in the source string

    def __str__(self) -> str:
        return self.value


class OperatorInfo(NamedTuple):
    precedence: int
    associativity: str  # 'L' for left-associative, 'R' for right-associative
    symbol: str
    name: str


OPERATOR_TABLE: Dict[str, OperatorInfo] = {
    "^": OperatorInfo(precedence=3, associativity="R", symbol="^", name="Exponentiation"),
    "*": OperatorInfo(precedence=2, associativity="L", symbol="*", name="Multiplication"),
    "/": OperatorInfo(precedence=2, associativity="L", symbol="/", name="Division"),
    "%": OperatorInfo(precedence=2, associativity="L", symbol="%", name="Modulus"),
    "+": OperatorInfo(precedence=1, associativity="L", symbol="+", name="Addition"),
    "-": OperatorInfo(precedence=1, associativity="L", symbol="-", name="Subtraction"),
}


# -----------------------------------------------------------------------------
# 2. CUSTOM STACK DATA STRUCTURE
# -----------------------------------------------------------------------------

class ConversionStack:
    """
    A robust, educational Stack data structure adhering to the Last In, First Out (LIFO)
    principle, tailored for expression conversion with step logging and inspection.
    """

    def __init__(self, capacity: Optional[int] = None):
        """
        Initialize the stack.

        Args:
            capacity: Optional maximum size limit. If None, the stack is unbounded.
        """
        if capacity is not None and capacity <= 0:
            raise ValueError("Capacity must be a positive integer if specified.")
        self.capacity: Optional[int] = capacity
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        """
        Pushes an item onto the top of the stack.
        Time Complexity: O(1) amortized.
        """
        if self.is_full():
            raise OverflowError(f"Stack Overflow! Capacity of {self.capacity} exceeded.")
        self._items.append(item)

    def pop(self) -> Any:
        """
        Removes and returns the item at the top of the stack.
        Time Complexity: O(1).
        """
        if self.is_empty():
            raise IndexError("Stack Underflow! Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> Any:
        """
        Returns the top item without removing it.
        Time Complexity: O(1).
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Returns True if the stack has zero elements."""
        return len(self._items) == 0

    def is_full(self) -> bool:
        """Returns True if a finite capacity is set and reached."""
        if self.capacity is None:
            return False
        return len(self._items) >= self.capacity

    def size(self) -> int:
        """Returns the number of elements currently on the stack."""
        return len(self._items)

    def to_list(self) -> List[Any]:
        """Returns a shallow copy of items from bottom [0] to top [-1]."""
        return list(self._items)

    def clear(self) -> None:
        """Empties the stack."""
        self._items.clear()

    def __repr__(self) -> str:
        return f"ConversionStack(bottom_to_top={self._items})"


# -----------------------------------------------------------------------------
# 3. STEP RECORDING FOR 3D ANIMATION & TELEMETRY
# -----------------------------------------------------------------------------

@dataclass
class ConversionStep:
    """
    Snapshot of a single pedagogical transition during the conversion algorithm.
    """
    step_number: int
    token: str
    action_type: str  # "OUTPUT_OPERAND", "PUSH_OPERATOR", "PUSH_PAREN", "POP_TO_OUTPUT", "DISCARD_PAREN", "DRAIN_STACK", "FINISH"
    action_summary: str
    stack_snapshot: List[str]  # Bottom to top
    postfix_snapshot: List[str]  # Current list of postfix tokens
    explanation: str
    reason: str
    animated_item: Optional[str] = None
    target_destination: Optional[str] = None  # "STACK", "OUTPUT", "DISCARD"


# -----------------------------------------------------------------------------
# 4. TOKENIZATION & LEXICAL ANALYSIS
# -----------------------------------------------------------------------------

def tokenize_expression(expr: str) -> Tuple[List[Token], Optional[str]]:
    """
    Scans an infix expression string into a sequence of strongly-typed Tokens.

    Supports:
    - Operators: +, -, *, /, %, ^
    - Parentheses: (, )
    - Single & Multi-letter identifiers: A, B, x, total, price, count
    - Multi-digit integers: 0, 12, 123456
    - Decimal numbers: 3.14, 0.5, 42.0

    Returns:
        (tokens, None) on success, or ([], error_message) on lexical failure.
    """
    if not expr:
        return [], "Expression is empty."

    tokens: List[Token] = []
    i = 0
    n = len(expr)

    while i < n:
        char = expr[i]

        # 1. Skip whitespace
        if char.isspace():
            i += 1
            continue

        pos = i

        # 2. Parentheses
        if char == "(":
            tokens.append(Token(TokenType.LEFT_PAREN, "(", pos))
            i += 1
            continue
        if char == ")":
            tokens.append(Token(TokenType.RIGHT_PAREN, ")", pos))
            i += 1
            continue

        # 3. Operators
        if char in OPERATOR_TABLE:
            tokens.append(Token(TokenType.OPERATOR, char, pos))
            i += 1
            continue

        # 4. Numeric Literals (Integers & Decimals)
        if char.isdigit() or (char == "." and i + 1 < n and expr[i + 1].isdigit()):
            num_chars = []
            dot_count = 0
            while i < n and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        return [], f"Invalid numeric format with multiple decimal points at position {i}: '{expr[pos:i+1]}'"
                num_chars.append(expr[i])
                i += 1
            num_val = "".join(num_chars)
            tokens.append(Token(TokenType.OPERAND, num_val, pos))
            continue

        # 5. Identifier / Variable Operands (e.g. A, var1, total_cost)
        if char.isalpha() or char == "_":
            var_chars = []
            while i < n and (expr[i].isalnum() or expr[i] == "_"):
                var_chars.append(expr[i])
                i += 1
            var_val = "".join(var_chars)
            tokens.append(Token(TokenType.OPERAND, var_val, pos))
            continue

        # 6. Unrecognized symbol
        return [], f"Unrecognized character '{char}' at position {pos}."

    if not tokens:
        return [], "Expression contains no valid tokens."

    return tokens, None


# -----------------------------------------------------------------------------
# 5. SYNTAX VALIDATION & ERROR REPORTING
# -----------------------------------------------------------------------------

def validate_expression(expr: str) -> Tuple[bool, Optional[str], List[Token]]:
    """
    Validates an expression according to strict binary infix grammar.

    Enforces:
    - Non-empty expression
    - Valid characters and numbers
    - Balanced parentheses
    - Non-empty parentheses: '()' is invalid
    - No consecutive operators: 'A + * B' is invalid
    - No consecutive operands: 'A B' or '12 34' is invalid (missing operator)
    - Valid start and end tokens (cannot begin or end with a binary operator)
    - Operator placement around parentheses (cannot have '( * A' or 'A + )')
    - Explicit detection and rejection of unary operators (e.g. '-A', '+A', 'A * -B')
      with friendly instructions to use '(0 - A)' instead.

    Returns:
        (is_valid, error_message, tokens)
    """
    trimmed = expr.strip()
    if not trimmed:
        return False, "Expression is empty. Please enter an infix expression.", []

    tokens, err = tokenize_expression(trimmed)
    if err:
        return False, err, []

    # Check for empty parentheses ()
    for i in range(len(tokens) - 1):
        if tokens[i].type == TokenType.LEFT_PAREN and tokens[i + 1].type == TokenType.RIGHT_PAREN:
            return False, f"Empty parentheses '()' detected at position {tokens[i].position}. An expression is expected inside parentheses.", tokens

    # Check parentheses balancing
    paren_depth = 0
    for tok in tokens:
        if tok.type == TokenType.LEFT_PAREN:
            paren_depth += 1
        elif tok.type == TokenType.RIGHT_PAREN:
            paren_depth -= 1
            if paren_depth < 0:
                return False, f"Unbalanced parentheses: unexpected closing ')' at position {tok.position} with no matching opening '('.", tokens

    if paren_depth > 0:
        return False, f"Unbalanced parentheses: {paren_depth} opening '(' left unclosed.", tokens

    # Check leading token
    first_tok = tokens[0]
    if first_tok.type == TokenType.OPERATOR:
        if first_tok.value in ("+", "-"):
            return (
                False,
                f"Unary operator '{first_tok.value}' at position {first_tok.position} is not supported. "
                f"Please write as a binary expression (e.g., '(0 {first_tok.value} ...)') instead.",
                tokens,
            )
        return False, f"Expression cannot start with operator '{first_tok.value}' at position {first_tok.position}.", tokens

    if first_tok.type == TokenType.RIGHT_PAREN:
        return False, f"Expression cannot begin with a closing parenthesis at position {first_tok.position}.", tokens

    # Check trailing token
    last_tok = tokens[-1]
    if last_tok.type == TokenType.OPERATOR:
        return False, f"Expression cannot end with operator '{last_tok.value}' at position {last_tok.position}. An operand is missing.", tokens
    if last_tok.type == TokenType.LEFT_PAREN:
        return False, f"Expression cannot end with an opening parenthesis at position {last_tok.position}.", tokens

    # Pairwise sequence validation
    for i in range(len(tokens) - 1):
        curr = tokens[i]
        nxt = tokens[i + 1]

        # Case 1: Consecutive operators (e.g. A + * B or A * -B)
        if curr.type == TokenType.OPERATOR and nxt.type == TokenType.OPERATOR:
            if nxt.value in ("+", "-"):
                return (
                    False,
                    f"Unary operator '{nxt.value}' after '{curr.value}' at position {nxt.position} is not supported. "
                    f"Please rewrite using binary notation (e.g., '(0 - ...)') instead.",
                    tokens,
                )
            return (
                False,
                f"Consecutive operators '{curr.value}' and '{nxt.value}' detected at position {nxt.position}. Missing an operand between them.",
                tokens,
            )

        # Case 2: Consecutive operands (e.g. A B or 12 34) -> Missing operator
        if curr.type == TokenType.OPERAND and nxt.type == TokenType.OPERAND:
            return (
                False,
                f"Missing operator between operand '{curr.value}' and '{nxt.value}' at position {nxt.position}.",
                tokens,
            )

        # Case 3: Operand followed immediately by Left Paren (e.g. A(B+C) or 2(3))
        if curr.type == TokenType.OPERAND and nxt.type == TokenType.LEFT_PAREN:
            return (
                False,
                f"Missing operator between operand '{curr.value}' and '(' at position {nxt.position}. Implicit multiplication is not allowed.",
                tokens,
            )

        # Case 4: Right Paren followed immediately by Operand (e.g. (A+B)C)
        if curr.type == TokenType.RIGHT_PAREN and nxt.type == TokenType.OPERAND:
            return (
                False,
                f"Missing operator between ')' and operand '{nxt.value}' at position {nxt.position}.",
                tokens,
            )

        # Case 5: Adjacent parentheses (A+B)(C+D)
        if curr.type == TokenType.RIGHT_PAREN and nxt.type == TokenType.LEFT_PAREN:
            return (
                False,
                f"Missing operator between ')' and '(' at position {nxt.position}.",
                tokens,
            )

        # Case 6: Operator immediately after '(' (e.g. ( + A ))
        if curr.type == TokenType.LEFT_PAREN and nxt.type == TokenType.OPERATOR:
            if nxt.value in ("+", "-"):
                return (
                    False,
                    f"Unary operator '{nxt.value}' immediately after '(' at position {nxt.position} is not supported. Use '(0 {nxt.value} ...)' instead.",
                    tokens,
                )
            return (
                False,
                f"Unexpected operator '{nxt.value}' immediately after '(' at position {nxt.position}.",
                tokens,
            )

        # Case 7: Operator immediately before ')' (e.g. ( A + ))
        if curr.type == TokenType.OPERATOR and nxt.type == TokenType.RIGHT_PAREN:
            return (
                False,
                f"Unexpected operator '{curr.value}' immediately before ')' at position {curr.position}. An operand is missing.",
                tokens,
            )

    return True, None, tokens


# -----------------------------------------------------------------------------
# 6. INFIX TO POSTFIX CONVERSION ALGORITHM & STEP RECORDER
# -----------------------------------------------------------------------------

class InfixToPostfixConverter:
    """
    Stateful and reusable Infix to Postfix converter.
    Generates step-by-step traces suitable for frame-by-frame 3D animations.
    """

    def __init__(self):
        self.stack = ConversionStack()
        self.steps: List[ConversionStep] = []
        self.postfix_tokens: List[str] = []
        self.step_counter: int = 0

    def _record_step(
        self,
        token_val: str,
        action_type: str,
        action_summary: str,
        explanation: str,
        reason: str,
        animated_item: Optional[str] = None,
        target_destination: Optional[str] = None,
    ) -> None:
        self.step_counter += 1
        self.steps.append(
            ConversionStep(
                step_number=self.step_counter,
                token=token_val,
                action_type=action_type,
                action_summary=action_summary,
                stack_snapshot=self.stack.to_list(),
                postfix_snapshot=list(self.postfix_tokens),
                explanation=explanation,
                reason=reason,
                animated_item=animated_item or token_val,
                target_destination=target_destination,
            )
        )

    def convert(self, expr: str) -> Tuple[bool, Optional[str], List[str], List[ConversionStep]]:
        """
        Executes the conversion algorithm and produces an animation trace.

        Returns:
            (is_success, error_message, postfix_tokens, conversion_steps)
        """
        self.stack.clear()
        self.steps.clear()
        self.postfix_tokens.clear()
        self.step_counter = 0

        is_valid, err_msg, tokens = validate_expression(expr)
        if not is_valid:
            return False, err_msg, [], []

        # Step 0: Initial state
        self._record_step(
            token_val="START",
            action_type="INITIALIZE",
            action_summary="Initialize conversion arena",
            explanation=f"Expression successfully validated: {len(tokens)} tokens identified. Stack is empty.",
            reason="Conversion algorithm begins with an empty operator stack and empty postfix output lane.",
            target_destination=None,
        )

        for tok in tokens:
            val = tok.value

            # --- CASE A: OPERAND ---
            if tok.type == TokenType.OPERAND:
                self.postfix_tokens.append(val)
                self._record_step(
                    token_val=val,
                    action_type="OUTPUT_OPERAND",
                    action_summary=f"Send operand '{val}' to postfix output",
                    explanation=f"Token '{val}' is an operand. It is routed directly to the postfix output platform.",
                    reason="Operands maintain their exact relative order from infix to postfix notation.",
                    animated_item=val,
                    target_destination="OUTPUT",
                )

            # --- CASE B: OPENING PARENTHESIS ---
            elif tok.type == TokenType.LEFT_PAREN:
                self.stack.push("(")
                self._record_step(
                    token_val="(",
                    action_type="PUSH_PAREN",
                    action_summary="Push '(' onto stack tower",
                    explanation="Token '(' opens a sub-expression. Push it onto the stack as a scope boundary.",
                    reason="Opening parenthesis acts as a floor barrier for subsequent operator precedence checks.",
                    animated_item="(",
                    target_destination="STACK",
                )

            # --- CASE C: CLOSING PARENTHESIS ---
            elif tok.type == TokenType.RIGHT_PAREN:
                self._record_step(
                    token_val=")",
                    action_type="PROCESS_PAREN",
                    action_summary="Encountered ')' — pop enclosed operators",
                    explanation="Token ')' closes a sub-expression. Pop all operators until the matching '(' is reached.",
                    reason="Operations inside parentheses have finished and must now appear in the postfix output.",
                    animated_item=")",
                    target_destination=None,
                )

                while not self.stack.is_empty() and self.stack.peek() != "(":
                    top_op = self.stack.pop()
                    self.postfix_tokens.append(top_op)
                    self._record_step(
                        token_val=")",
                        action_type="POP_TO_OUTPUT",
                        action_summary=f"Pop '{top_op}' to postfix output",
                        explanation=f"Popped operator '{top_op}' from stack into postfix output.",
                        reason="Operators inside parentheses must be output before discarding the group boundary.",
                        animated_item=top_op,
                        target_destination="OUTPUT",
                    )

                if not self.stack.is_empty() and self.stack.peek() == "(":
                    self.stack.pop()  # Discard '('
                    self._record_step(
                        token_val=")",
                        action_type="DISCARD_PAREN",
                        action_summary="Discard matching '(' from stack",
                        explanation="Matching opening parenthesis '(' has been popped and discarded.",
                        reason="Parentheses are redundant in postfix notation because operation order is implicit.",
                        animated_item="(",
                        target_destination="DISCARD",
                    )

            # --- CASE D: OPERATORS (+, -, *, /, %, ^) ---
            elif tok.type == TokenType.OPERATOR:
                curr_info = OPERATOR_TABLE[val]

                # Pop operators from the stack while they have higher precedence,
                # or equal precedence with LEFT-associativity.
                while not self.stack.is_empty() and self.stack.peek() != "(":
                    top_op = self.stack.peek()
                    top_info = OPERATOR_TABLE[top_op]

                    should_pop = False
                    if top_info.precedence > curr_info.precedence:
                        should_pop = True
                    elif top_info.precedence == curr_info.precedence:
                        if curr_info.associativity == "L":
                            should_pop = True
                        else:
                            # Right-associative operator (e.g. ^): DO NOT POP!
                            should_pop = False

                    if should_pop:
                        popped_op = self.stack.pop()
                        self.postfix_tokens.append(popped_op)

                        if top_info.precedence > curr_info.precedence:
                            reason_msg = (
                                f"Stack top '{popped_op}' (Precedence {top_info.precedence}) has higher precedence "
                                f"than '{val}' (Precedence {curr_info.precedence}). Higher precedence binds first."
                            )
                        else:
                            reason_msg = (
                                f"Stack top '{popped_op}' and '{val}' both have Precedence {curr_info.precedence}. "
                                f"Because '{val}' is left-associative, the earlier operator evaluates first."
                            )

                        self._record_step(
                            token_val=val,
                            action_type="POP_TO_OUTPUT",
                            action_summary=f"Pop '{popped_op}' to postfix output",
                            explanation=f"Top operator '{popped_op}' must be evaluated before '{val}'. Move to output.",
                            reason=reason_msg,
                            animated_item=popped_op,
                            target_destination="OUTPUT",
                        )
                    else:
                        break

                # Now push the current operator onto the stack
                self.stack.push(val)
                assoc_desc = "Right-Associative" if curr_info.associativity == "R" else "Left-Associative"
                self._record_step(
                    token_val=val,
                    action_type="PUSH_OPERATOR",
                    action_summary=f"Push '{val}' onto stack tower",
                    explanation=f"Push operator '{val}' (Prec: {curr_info.precedence}, {assoc_desc}) onto stack.",
                    reason=f"Operator '{val}' waits on the stack until its operands and any higher-precedence operations are resolved.",
                    animated_item=val,
                    target_destination="STACK",
                )

        # --- FINAL STAGE: DRAIN REMAINING STACK ---
        if not self.stack.is_empty():
            self._record_step(
                token_val="END",
                action_type="DRAIN_START",
                action_summary="End of expression: empty the stack",
                explanation="All tokens in the input expression have been scanned. Popping remaining operators.",
                reason="Any operators remaining on the stack must now be moved to the postfix output in LIFO order.",
                target_destination=None,
            )

            while not self.stack.is_empty():
                top_op = self.stack.pop()
                self.postfix_tokens.append(top_op)
                self._record_step(
                    token_val="END",
                    action_type="DRAIN_STACK",
                    action_summary=f"Pop remaining '{top_op}' to postfix output",
                    explanation=f"Remaining operator '{top_op}' popped and appended to postfix output platform.",
                    reason="LIFO order ensures the most recent pending operation is emitted first.",
                    animated_item=top_op,
                    target_destination="OUTPUT",
                )

        # Final completion step
        result_str = " ".join(self.postfix_tokens)
        self._record_step(
            token_val="DONE",
            action_type="FINISH",
            action_summary="Conversion Completed!",
            explanation=f"Resulting Postfix Expression: {result_str}",
            reason="All tokens processed and stack fully cleared. Result is ready for evaluation or copying.",
            target_destination=None,
        )

        return True, None, list(self.postfix_tokens), list(self.steps)


def convert_infix_to_postfix(expr: str) -> Tuple[bool, Optional[str], str, List[ConversionStep]]:
    """
    Convenience functional wrapper.

    Returns:
        (is_valid, error_message, postfix_string, steps)
    """
    converter = InfixToPostfixConverter()
    ok, err, tokens, steps = converter.convert(expr)
    if not ok:
        return False, err, "", []
    return True, None, " ".join(tokens), steps


# -----------------------------------------------------------------------------
# 7. RANDOM PRACTICE EXPRESSION GENERATOR (CHALLENGE MODE)
# -----------------------------------------------------------------------------

def generate_random_expression(difficulty: str = "medium") -> Tuple[str, str]:
    """
    Generates a valid, pedagogical infix expression alongside its correct postfix answer.

    Difficulty levels:
    - 'easy': Simple binary operators (+, -, *), 3-4 operands, single letters.
    - 'medium': Mixed precedence (+, -, *, /, ^), parentheses, 4-6 operands.
    - 'hard': Nested parentheses, multi-character variables, exponentiation chains, modulus.

    Returns:
        (infix_expression, postfix_expression)
    """
    operands_pool = ["A", "B", "C", "D", "E", "F"]

    def build_tree(depth: int, max_depth: int, available_ops: List[str], vars_iter) -> str:
        if depth >= max_depth or random.random() < 0.25:
            try:
                return next(vars_iter)
            except StopIteration:
                return random.choice(operands_pool)

        op = random.choice(available_ops)
        left = build_tree(depth + 1, max_depth, available_ops, vars_iter)
        right = build_tree(depth + 1, max_depth, available_ops, vars_iter)

        use_parens = random.random() < 0.5 or depth == 0
        if use_parens and depth > 0:
            return f"({left}{op}{right})"
        return f"{left}{op}{right}"

    # Try up to 20 times to generate a strictly valid expression
    for _ in range(25):
        shuffled_vars = iter(random.sample(operands_pool, len(operands_pool)))
        if difficulty == "easy":
            ops = ["+", "-", "*"]
            expr = build_tree(0, 2, ops, shuffled_vars)
        elif difficulty == "hard":
            ops = ["+", "-", "*", "/", "%", "^"]
            expr = build_tree(0, 3, ops, shuffled_vars)
        else:  # medium
            ops = ["+", "-", "*", "/", "^"]
            expr = build_tree(0, 2, ops, shuffled_vars)

        ok, err, postfix, _ = convert_infix_to_postfix(expr)
        if ok and postfix:
            return expr, postfix

    # Fallback to guaranteed valid expressions
    fallbacks = [
        ("A+B*C", "A B C * +"),
        ("(A+B)*C", "A B + C *"),
        ("A+B*(C-D)", "A B C D - * +"),
        ("A^B^C", "A B C ^ ^"),
        ("(A+B)*(C-D)", "A B + C D - *"),
        ("A+B*C-D/E", "A B C * + D E / -"),
        ("(A+B)/(C+D)*(E-F)", "A B + C D + / E F - *"),
    ]
    return random.choice(fallbacks)
