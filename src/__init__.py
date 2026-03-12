"""
matrix_library

A matrix operations library built from scratch without NumPy.

Public API:
    Matrix          — the core matrix object
    determinant     — compute det(A)
    inverse         — compute A^-1
    cofactor_matrix — compute cofactor matrix
    adjoint         — compute adjoint (adjugate)
    chain_multiply  — multiply a sequence of matrices

Usage:
    from matrix_library import Matrix, determinant, inverse

    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])

    C = A + B
    D = A @ B
    det = determinant(A)
    inv = inverse(A)
"""

from src.matrix import Matrix
from src.operations import (
    determinant,
    inverse,
    cofactor_matrix,
    adjoint,
    chain_multiply,
)

__all__ = [
    "Matrix",
    "determinant",
    "inverse",
    "cofactor_matrix",
    "adjoint",
    "chain_multiply",
]