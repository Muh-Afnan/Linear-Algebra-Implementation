# Day 01 — Matrix Operations Library from Scratch

> Part of my 90-day Python challenge — building toward machine learning, deep learning, and AI engineering from the ground up.

---

## What Is This

A matrix operations library built entirely from scratch in Python. No NumPy. No SciPy. No math libraries of any kind.

Every operation — from basic addition to determinant and inverse — is implemented from first principles, with the mathematics understood before the code was written.

This is Day 1 of 90. The matrix library is the foundation. Almost everything that follows — gradient descent, PCA, neural networks, transformers — lives on top of linear algebra. I wanted to meet that foundation on its own terms before ever treating it as a black box.

---

## Why Build This When NumPy Exists

Because calling `np.linalg.det()` and moving on meant I didn't actually know what was happening. I knew *what* it did — not *how* or *why*.

Building this library answered questions I'd been carrying around:
- What does matrix multiplication actually compute geometrically?
- How does a library find the determinant of a large matrix?
- What does it mean for a matrix to be singular — really?
- Why do libraries raise the errors they raise?

After building this, `import numpy` means something different to me than it did before.

---

## Project Structure

```
day-01-matrix-library/
│
├── matrix_library/
│   ├── __init__.py         ← public API
│   ├── validator.py        ← pure validation logic
│   ├── utils.py            ← stateless factory functions
│   ├── matrix.py           ← Matrix class, object model, dunders
│   └── operations.py       ← determinant, inverse, cofactor, chain multiply
│
├── tests/
│   ├── test_matrix.py      ← 57 tests for the Matrix class
│   └── test_operations.py  ← 19 tests for advanced operations
│
├── problem_statement.md    ← why this project exists
├── approach.md             ← design decisions and tradeoffs
├── learnings.md            ← honest reflections
├── comparison.md           ← how this compares to NumPy/SciPy/SymPy
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/muhammad/day-01-matrix-library
cd day-01-matrix-library
python -m unittest discover tests/ -v
```

No dependencies. Pure Python 3.10+.

---

## Usage

```python
from matrix_library import Matrix, determinant, inverse, chain_multiply

# Construction
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

# Arithmetic — all return Matrix instances, chaining works naturally
C = A + B           # Matrix([[6, 8], [10, 12]])
D = A @ B           # Matrix([[19, 22], [43, 50]])
E = A * 3           # scalar multiplication
F = 3 * A           # also works
G = A * B           # element-wise (Hadamard) multiplication

# Chaining
result = (A + B) @ B    # works because every operation returns a Matrix

# Transpose
A.transpose()

# Trace
A.trace()           # 5

# Row operations — all non-mutating, return new Matrix
A.swap_rows(1, 2)
A.add_rows(1, 2)    # row1 = row1 + row2
A.scale_row(1, 3)   # row1 = row1 * 3

# Property checks
A.is_square()
A.is_symmetric()
A.is_skew_symmetric()
A.is_diagonal()
A.is_identity()
A.is_zero()

# Advanced operations
det = determinant(A)            # -2
inv = inverse(A)                # Matrix([[-2.0, 1.0], [1.5, -0.5]])
adj = adjoint(A)
cof = cofactor_matrix(A)

# Chain multiply — validates all shapes before computing
result = chain_multiply(A, B, C)

# Factories
Matrix.zeros(3, 3)
Matrix.ones(2, 4)
Matrix.identity(5)
```

---

## Operations Implemented

### Core Object
| Feature | Description |
|---|---|
| `__init__` | Validates input, deep copies data, stores shape |
| `__repr__` | Clean formatted output |
| `__eq__` | Equality with floating point tolerance (1e-9) |
| `shape()` | Returns (rows, cols) tuple |

### Arithmetic Operators
| Operator | Operation |
|---|---|
| `A + B` | Matrix addition |
| `A - B` | Matrix subtraction |
| `A * scalar` | Scalar multiplication |
| `scalar * A` | Scalar multiplication (reversed) |
| `A * B` | Element-wise (Hadamard) multiplication |
| `A @ B` | Matrix (dot) product |

### Matrix Operations
| Method | Description |
|---|---|
| `transpose()` | Returns transposed matrix |
| `trace()` | Sum of diagonal elements |
| `swap_rows(r1, r2)` | Swap two rows (1-indexed) |
| `add_rows(target, source)` | target row = target + source |
| `scale_row(row, factor)` | Multiply a row by scalar |

### Property Checks
| Method | Returns |
|---|---|
| `is_square()` | True if rows == cols |
| `is_symmetric()` | True if A == Aᵀ |
| `is_skew_symmetric()` | True if A == -Aᵀ |
| `is_diagonal()` | True if all off-diagonal elements are zero |
| `is_identity()` | True if diagonal is 1, rest is 0 |
| `is_zero()` | True if all elements are zero |

### Advanced Operations (operations.py)
| Function | Description |
|---|---|
| `determinant(A)` | Cofactor expansion, recursive, exact |
| `cofactor_matrix(A)` | Full cofactor matrix |
| `adjoint(A)` | Transpose of cofactor matrix |
| `inverse(A)` | A⁻¹ via adjoint method |
| `chain_multiply(A, B, ...)` | Multiply sequence of matrices |

### Factories
| Method | Description |
|---|---|
| `Matrix.zeros(r, c)` | r × c matrix of zeros |
| `Matrix.ones(r, c)` | r × c matrix of ones |
| `Matrix.identity(n)` | n × n identity matrix |

---

## Tests

```
76 tests — all passing

test_matrix.py       57 tests
  TestMatrixConstruction      5 tests
  TestMatrixRepr              2 tests
  TestMatrixEquality          4 tests
  TestMatrixAddition          4 tests
  TestMatrixSubtraction       2 tests
  TestScalarMultiplication    3 tests
  TestElementWiseMultiply     2 tests
  TestMatmul                  5 tests
  TestTranspose               3 tests
  TestTrace                   3 tests
  TestRowOperations           8 tests
  TestMatrixProperties       11 tests
  TestFactories               3 tests

test_operations.py   19 tests
  TestDeterminant             7 tests
  TestInverse                 5 tests
  TestCofactorAndAdjoint      3 tests
  TestChainMultiply           4 tests
```

Run them:
```bash
python -m unittest discover tests/ -v
```

---

## Known Limitations

**Determinant is O(n!)** — cofactor expansion is correct but impractical beyond ~8×8 matrices. A production library would use LU decomposition (O(n³)). This is intentional for Day 1 — understanding the recursive structure matters more than performance at this stage.

**No complex number support** — type hints and logic assume `int | float` throughout.

**Float tolerance in property checks** — `is_symmetric()` and similar use the same `1e-9` absolute tolerance as `__eq__`. For matrices produced by heavy floating point computation, a relative tolerance (like `np.allclose`) would be more robust.

---

## How This Compares to NumPy

See [`comparison.md`](./comparison.md) for a full operation-by-operation breakdown.

The short version: the algorithms are correct and in most cases identical to what NumPy does. The gaps are in memory layout (nested lists vs contiguous C arrays), lazy evaluation (copies vs views), and algorithm choice (cofactor expansion vs LU decomposition for determinant).

The most important insight from building this: NumPy is not a faster version of this library. It is a fundamentally different thing operating under the same mathematical abstraction.

---

## Further Reading

- *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong (free PDF) — Chapter 2 covers everything this library implements
- *Linear Algebra Done Right* — Axler — for the theory behind eigenvectors and beyond
- [3Blue1Brown — Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — the geometric intuition behind every operation in this library

---

## Part of a Larger Journey

This is Day 1 of a 90-day challenge building toward ML engineering from scratch.

| Pillar | Days | Focus |
|---|---|---|
| Mathematical Foundations | 1–15 | Linear algebra, probability, calculus, optimization |
| Classical ML from Scratch | 16–30 | Every major algorithm, no sklearn |
| Deep Learning | 31–45 | NumPy neural net → PyTorch → Transformers |
| AI Engineering | 46–90 | Pipelines, serving, RAG, agents, capstones |

→ [See the full 90-day roadmap](#)
→ [GitHub Profile](#)