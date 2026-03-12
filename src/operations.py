"""
operations.py

Advanced mathematical operations on Matrix objects.

Why separate from matrix.py?
- Matrix class handles the object model: construction, operators, properties
- This module handles heavier mathematical procedures: determinant, inverse,
  cofactor, adjoint — operations that involve recursion or multi-step algorithms
- Keeps matrix.py focused and readable
- These functions can be imported and used independently in future modules
  (e.g., a decomposition module, a solver module)

All functions are pure — they take Matrix objects and return new Matrix objects
or scalars. Nothing is mutated.
"""

from src.matrix import Matrix
from src.validator import MatrixValidator
from src.utils import build_minor


def determinant(matrix: Matrix) -> int | float:
    """
    Compute the determinant using cofactor expansion along the first row.
    Raises ValueError if matrix is not square.

    Time complexity: O(n!) — acceptable for small matrices.
    For large matrices, LU decomposition would be preferred (Day 2+ topic).
    """
    MatrixValidator.validate_square(matrix.shape(), "Determinant")
    n = matrix.rows

    if n == 1:
        return matrix.data[0][0]

    if n == 2:
        return (matrix.data[0][0] * matrix.data[1][1]
                - matrix.data[0][1] * matrix.data[1][0])

    det = 0
    for j in range(n):
        minor_data = build_minor(matrix.data, 0, j)
        minor_det = determinant(Matrix(minor_data))
        sign = (-1) ** j
        det += sign * matrix.data[0][j] * minor_det
    return det


def cofactor_matrix(matrix: Matrix) -> Matrix:
    """
    Compute the cofactor matrix.
    Each entry (i, j) is (-1)^(i+j) * determinant of the minor at (i, j).
    Raises ValueError if matrix is not square.
    """
    MatrixValidator.validate_square(matrix.shape(), "Cofactor")
    n = matrix.rows
    result = []
    for i in range(n):
        row = []
        for j in range(n):
            minor_data = build_minor(matrix.data, i, j)
            minor_det = determinant(Matrix(minor_data))
            sign = (-1) ** (i + j)
            row.append(sign * minor_det)
        result.append(row)
    return Matrix(result)


def adjoint(matrix: Matrix) -> Matrix:
    """
    Compute the adjoint (adjugate) — transpose of the cofactor matrix.
    Raises ValueError if matrix is not square.
    """
    return cofactor_matrix(matrix).transpose()


def inverse(matrix: Matrix) -> Matrix:
    """
    Compute the inverse using the adjoint method: A^-1 = adj(A) / det(A).
    Raises ValueError if matrix is not square or is singular (det = 0).

    Note: For numerical stability in production, LU decomposition or
    Gaussian elimination would be preferred. This implementation is
    pedagogically correct.
    """
    det = determinant(matrix)
    if det == 0:
        raise ValueError(
            "Matrix is singular (determinant = 0). "
            "Singular matrices have no inverse."
        )
    adj = adjoint(matrix)
    return adj * (1 / det)


def chain_multiply(first: Matrix, second: Matrix, *rest: Matrix) -> Matrix:
    """
    Multiply a sequence of matrices left to right: A @ B @ C @ ...
    Validates all consecutive shape pairs before computing.
    Raises ValueError on first incompatible pair, with index information.
    """
    matrices = [first, second, *rest]
    for idx in range(len(matrices) - 1):
        try:
            MatrixValidator.validate_multipliable(
                matrices[idx].shape(), matrices[idx + 1].shape()
            )
        except ValueError as e:
            raise ValueError(
                f"Chain multiplication failed at position [{idx}] @ [{idx+1}]: {e}"
            ) from e

    result = matrices[0]
    for m in matrices[1:]:
        result = result @ m
    return result