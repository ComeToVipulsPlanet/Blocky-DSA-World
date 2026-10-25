"""
Unit Tests for Infix to Postfix Converter
=========================================
Tests:
- All required university-style benchmark expressions:
  * A+B -> A B +
  * A+B*C -> A B C * +
  * (A+B)*C -> A B + C *
  * A*B+C -> A B * C +
  * A+B*(C-D) -> A B C D - * +
  * (A+B)*(C-D) -> A B + C D - *
  * A^B^C -> A B C ^ ^
  * A+B*C-D/E -> A B C * + D E / -
  * (A+B)/(C+D)*(E-F) -> A B + C D + / E F - *
  * A+B*(C^D-E) -> A B C D ^ E - * +
- Right-associativity of Exponentiation (^)
- Left-associativity of +, -, *, /, %
- Multi-digit integers (e.g. 123+456*2)
- Multi-letter identifiers (e.g. total+price*count)
- Decimal numbers (e.g. 3.14+2.5*10)
- Whitespace handling
- Arbitrarily nested parentheses
- Expression validation & error reporting:
  * Empty input
  * Unbalanced parentheses
  * Empty parentheses ()
  * Consecutive binary operators (A + * B)
  * Missing operators between operands (A B, (A+B)(C+D))
  * Leading and trailing operators (+ A, A -)
  * Unary operators (+/- without left operand)
- ConversionStack LIFO operations and bounds
- Step trace generation completeness
- Random expression generator validity
"""

import unittest
from dsa.infix_to_postfix import (
    ConversionStack,
    InfixToPostfixConverter,
    convert_infix_to_postfix,
    generate_random_expression,
    tokenize_expression,
    validate_expression,
)


class TestInfixToPostfixUniversityExamples(unittest.TestCase):
    """Verifies all mandatory university-style benchmark examples."""

    def test_simple_addition(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A+B")
        self.assertTrue(ok)
        self.assertIsNone(err)
        self.assertEqual(postfix, "A B +")

    def test_precedence_multiplication_over_addition(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A+B*C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C * +")

    def test_parentheses_override_precedence(self):
        ok, err, postfix, _ = convert_infix_to_postfix("(A+B)*C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B + C *")

    def test_multiplication_then_addition(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A*B+C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B * C +")

    def test_mixed_parentheses_and_multiplication(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A+B*(C-D)")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C D - * +")

    def test_two_parenthesized_factors(self):
        ok, err, postfix, _ = convert_infix_to_postfix("(A+B)*(C-D)")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B + C D - *")

    def test_right_associativity_exponentiation(self):
        """A^B^C must convert to A B C ^ ^ (not A B ^ C ^)."""
        ok, err, postfix, _ = convert_infix_to_postfix("A^B^C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C ^ ^")

    def test_four_operator_chain(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A+B*C-D/E")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C * + D E / -")

    def test_complex_parenthesized_expression(self):
        ok, err, postfix, _ = convert_infix_to_postfix("(A+B)/(C+D)*(E-F)")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B + C D + / E F - *")

    def test_nested_exponentiation_with_parentheses(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A+B*(C^D-E)")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C D ^ E - * +")


class TestOperatorPrecedenceAndAssociativity(unittest.TestCase):
    """Detailed tests for precedence and associativity semantics."""

    def test_modulus_operator(self):
        ok, err, postfix, _ = convert_infix_to_postfix("A%B+C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B % C +")

    def test_division_and_multiplication_left_associativity(self):
        # A / B * C should be (A / B) * C -> A B / C *
        ok, err, postfix, _ = convert_infix_to_postfix("A/B*C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B / C *")

    def test_subtraction_left_associativity(self):
        # A - B - C should be (A - B) - C -> A B - C -
        ok, err, postfix, _ = convert_infix_to_postfix("A-B-C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B - C -")

    def test_exponentiation_triple_chain(self):
        # A^B^C^D should evaluate as A^(B^(C^D)) -> A B C D ^ ^ ^
        ok, err, postfix, _ = convert_infix_to_postfix("A^B^C^D")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C D ^ ^ ^")

    def test_parentheses_overriding_right_associativity(self):
        # (A^B)^C should evaluate (A^B) first -> A B ^ C ^
        ok, err, postfix, _ = convert_infix_to_postfix("(A^B)^C")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B ^ C ^")


class TestOperandsAndSpacing(unittest.TestCase):
    """Tests tokenization with multi-digit integers, variables, decimals, and whitespace."""

    def test_multi_digit_integers(self):
        ok, err, postfix, _ = convert_infix_to_postfix("123+456*2")
        self.assertTrue(ok)
        self.assertEqual(postfix, "123 456 2 * +")

    def test_multi_letter_variables(self):
        ok, err, postfix, _ = convert_infix_to_postfix("total+price*count")
        self.assertTrue(ok)
        self.assertEqual(postfix, "total price count * +")

    def test_decimal_numeric_operands(self):
        ok, err, postfix, _ = convert_infix_to_postfix("3.14+2.5*10")
        self.assertTrue(ok)
        self.assertEqual(postfix, "3.14 2.5 10 * +")

    def test_expressions_with_irregular_whitespace(self):
        ok, err, postfix, _ = convert_infix_to_postfix("  A   +  B  * ( C - D )   ")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B C D - * +")

    def test_arbitrarily_nested_parentheses(self):
        ok, err, postfix, _ = convert_infix_to_postfix("(((A+B)))")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B +")

        ok, err, postfix, _ = convert_infix_to_postfix("((A+B)*(C-(D/E)))")
        self.assertTrue(ok)
        self.assertEqual(postfix, "A B + C D E / - *")


class TestExpressionValidationAndErrors(unittest.TestCase):
    """Ensures improper expressions fail gracefully with informative error messages."""

    def test_empty_string(self):
        ok, err, _, _ = convert_infix_to_postfix("")
        self.assertFalse(ok)
        self.assertIn("empty", err.lower())

    def test_whitespace_only(self):
        ok, err, _, _ = convert_infix_to_postfix("   \t  \n ")
        self.assertFalse(ok)
        self.assertIn("empty", err.lower())

    def test_invalid_character(self):
        ok, err, _, _ = convert_infix_to_postfix("A + B @ C")
        self.assertFalse(ok)
        self.assertIn("@", err)

    def test_unbalanced_open_parenthesis(self):
        ok, err, _, _ = convert_infix_to_postfix("(A+B")
        self.assertFalse(ok)
        self.assertIn("unbalanced", err.lower())

    def test_unbalanced_close_parenthesis(self):
        ok, err, _, _ = convert_infix_to_postfix("A+B)")
        self.assertFalse(ok)
        self.assertIn("unbalanced", err.lower())

    def test_empty_parentheses(self):
        ok, err, _, _ = convert_infix_to_postfix("A+()+B")
        self.assertFalse(ok)
        self.assertIn("empty parentheses", err.lower())

    def test_consecutive_binary_operators(self):
        ok, err, _, _ = convert_infix_to_postfix("A + * B")
        self.assertFalse(ok)
        self.assertIn("consecutive", err.lower())

    def test_missing_operator_between_operands(self):
        ok, err, _, _ = convert_infix_to_postfix("A B + C")
        self.assertFalse(ok)
        self.assertIn("missing operator", err.lower())

    def test_missing_operator_between_parentheses(self):
        ok, err, _, _ = convert_infix_to_postfix("(A+B)(C+D)")
        self.assertFalse(ok)
        self.assertIn("missing operator", err.lower())

    def test_leading_operator(self):
        ok, err, _, _ = convert_infix_to_postfix("* A + B")
        self.assertFalse(ok)
        self.assertIn("cannot start with operator", err.lower())

    def test_trailing_operator(self):
        ok, err, _, _ = convert_infix_to_postfix("A + B -")
        self.assertFalse(ok)
        self.assertIn("cannot end with operator", err.lower())

    def test_unary_operator_unsupported_notice(self):
        """Unary minus/plus must be explicitly flagged with instructions."""
        ok, err, _, _ = convert_infix_to_postfix("-A + B")
        self.assertFalse(ok)
        self.assertIn("unary", err.lower())

        ok, err, _, _ = convert_infix_to_postfix("A * -B")
        self.assertFalse(ok)
        self.assertIn("unary", err.lower())

    def test_invalid_decimal_format(self):
        ok, err, _, _ = convert_infix_to_postfix("3.14.15 + 2")
        self.assertFalse(ok)
        self.assertIn("multiple decimal points", err.lower())


class TestConversionStack(unittest.TestCase):
    """Unit tests for ConversionStack class."""

    def test_stack_operations(self):
        stk = ConversionStack(capacity=3)
        self.assertTrue(stk.is_empty())
        stk.push("+")
        stk.push("*")
        self.assertEqual(stk.size(), 2)
        self.assertEqual(stk.peek(), "*")
        self.assertEqual(stk.pop(), "*")
        self.assertEqual(stk.pop(), "+")
        self.assertTrue(stk.is_empty())

    def test_stack_overflow(self):
        stk = ConversionStack(capacity=2)
        stk.push("A")
        stk.push("B")
        with self.assertRaises(OverflowError):
            stk.push("C")

    def test_stack_underflow(self):
        stk = ConversionStack()
        with self.assertRaises(IndexError):
            stk.pop()
        with self.assertRaises(IndexError):
            stk.peek()


class TestStepsAndRandomGenerator(unittest.TestCase):
    """Tests conversion trace steps and challenge mode generator."""

    def test_conversion_steps_generated(self):
        converter = InfixToPostfixConverter()
        ok, err, tokens, steps = converter.convert("A+B*C")
        self.assertTrue(ok)
        self.assertEqual(tokens, ["A", "B", "C", "*", "+"])
        self.assertGreater(len(steps), 4)
        for s in steps:
            self.assertIsNotNone(s.explanation)
            self.assertIsNotNone(s.reason)

    def test_random_expression_generator(self):
        for diff in ["easy", "medium", "hard"]:
            expr, postfix = generate_random_expression(difficulty=diff)
            self.assertIsInstance(expr, str)
            self.assertIsInstance(postfix, str)
            ok, err, verified, _ = convert_infix_to_postfix(expr)
            self.assertTrue(ok, f"Generated expression failed validation: {expr} with err: {err}")
            self.assertEqual(postfix, verified)


if __name__ == "__main__":
    unittest.main()
