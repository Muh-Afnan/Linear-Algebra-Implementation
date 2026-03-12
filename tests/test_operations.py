"""
test_operations.py

Tests for advanced matrix operations: determinant, inverse, cofactor,
adjoint, and chain multiplication.
"""

import unittest
from src import Matrix, determinant, inverse, cofactor_matrix, adjoint, chain_multiply


class TestDeterminant(unittest.TestCase):

    def test_1x1(self):
        self.assertEqual(determinant(Matrix([[7]])), 7)

    def test_2x2(self):
        self.assertEqual(determinant(Matrix([[1, 2], [3, 4]])), -2)

    def test_2x2_positive(self):
        self.assertEqual(determinant(Matrix([[3, 1], [2, 4]])), 10)

    def test_3x3(self):
        A = Matrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
        self.assertEqual(determinant(A), -306)

    def test_identity_det_is_1(self):
        self.assertEqual(determinant(Matrix.identity(5)), 1)

    def test_singular_det_is_0(self):
        A = Matrix([[1, 2], [2, 4]])
        self.assertEqual(determinant(A), 0)

    def test_non_square_raises(self):
        with self.assertRaises(ValueError):
            determinant(Matrix([[1, 2, 3], [4, 5, 6]]))


class TestInverse(unittest.TestCase):

    def test_inverse_2x2(self):
        A = Matrix([[4, 7], [2, 6]])
        result = inverse(A)
        expected = Matrix([[0.6, -0.7], [-0.2, 0.4]])
        self.assertEqual(result, expected)

    def test_inverse_identity(self):
        I = Matrix.identity(3)
        self.assertEqual(inverse(I), I)

    def test_inverse_singular_raises(self):
        with self.assertRaises(ValueError):
            inverse(Matrix([[1, 2], [2, 4]]))

    def test_a_times_inverse_is_identity(self):
        """A @ A^-1 should equal the identity matrix."""
        A = Matrix([[4, 7], [2, 6]])
        I = A @ inverse(A)
        self.assertEqual(I, Matrix.identity(2))

    def test_non_square_raises(self):
        with self.assertRaises(ValueError):
            inverse(Matrix([[1, 2, 3], [4, 5, 6]]))


class TestCofactorAndAdjoint(unittest.TestCase):

    def test_cofactor_2x2(self):
        A = Matrix([[1, 2], [3, 4]])
        C = cofactor_matrix(A)
        self.assertEqual(C, Matrix([[4, -3], [-2, 1]]))

    def test_adjoint_is_transpose_of_cofactor(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(adjoint(A), cofactor_matrix(A).transpose())

    def test_non_square_cofactor_raises(self):
        with self.assertRaises(ValueError):
            cofactor_matrix(Matrix([[1, 2, 3], [4, 5, 6]]))


class TestChainMultiply(unittest.TestCase):

    def test_two_matrices(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        self.assertEqual(chain_multiply(A, B), A @ B)

    def test_three_matrices(self):
        F = Matrix([[1, 2, 3], [4, 5, 6]])
        G = Matrix([[7, 8], [9, 10], [11, 12]])
        C = Matrix([[1, 2], [3, 4]])
        result = chain_multiply(F, G, C)
        self.assertEqual(result, Matrix([[250, 372], [601, 894]]))

    def test_incompatible_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            chain_multiply(A, B)

    def test_error_message_contains_position(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        try:
            chain_multiply(A, B)
        except ValueError as e:
            self.assertIn("[0]", str(e))


if __name__ == "__main__":
    unittest.main()