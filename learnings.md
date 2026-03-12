# Learnings

## What I Actually Learned (Honest Version)

I want to be honest in this document. Not the polished version where everything went smoothly and I had insights at every step. The real version — where I submitted broken code multiple times, fixed one bug and introduced another, and slowly understood why the process works the way it does.

---

## The Math Became Real

I've used determinants in courses. Calculated them by hand in exams. Got the right answer, moved on.

Building the recursive cofactor expansion myself was different. When you implement `determinant` recursively — pulling out a row, computing minors, alternating signs, summing — you stop seeing it as a formula and start seeing it as a *process*. The formula is a description of something. The code is the thing itself.

The moment it clicked was the singular matrix. I had always known "determinant zero means non-invertible." I knew those as two separate facts connected by a rule. When I implemented `inverse` as `adjoint / determinant` and then watched it crash on a singular matrix, the connection became physical. The determinant being zero isn't a *symptom* of non-invertibility. It's the *mechanism*. You literally cannot divide by it. The math and the code said the same thing at the same time.

That's what building from scratch gave me that using NumPy never did.

---

## Libraries Do a Lot of Invisible Work

I had assumed that NumPy's `np.linalg.inv()` was roughly what I built — compute the adjoint, divide by the determinant. It isn't.

NumPy uses LU decomposition. It's O(n³) instead of O(n!). For a 10x10 matrix, cofactor expansion requires millions of recursive calls. LU decomposition does it in roughly a thousand operations. The difference isn't marginal — it's the difference between a library being usable and not.

This is what I didn't understand before: the gap between a *correct* implementation and a *practical* one. My library is correct. It would be unusable at scale. The engineers who built NumPy solved a different problem on top of the mathematical one — they solved it at the hardware level, with LAPACK and BLAS, with cache-aware memory layouts, with parallelism.

I have a new appreciation for what `import numpy` actually means now.

---

## OOP Isn't About Organising Code — It's About Modelling Reality

I started this project wanting to write functions. My instinct was a flat utility file: `add()`, `multiply()`, `determinant()`. It felt simpler.

The redesign to a proper `Matrix` class with dunder methods felt like overhead at first. More files. More structure. More to think about.

But then I wrote `A @ B @ C` in a test and it just worked. Because `A @ B` returned a `Matrix`, and `Matrix` has `__matmul__`, the chain composed naturally. The object model wasn't overhead — it was what made the library feel like a library rather than a collection of scripts.

The lesson: OOP isn't primarily about organisation. It's about making objects behave the way the things they represent actually behave. A matrix can be multiplied by another matrix. So `Matrix` should support `@`. A matrix has a transpose. So `Matrix` should have `.transpose()`. The class structure follows from the domain, not from coding preferences.

---

## Exception Handling Is a Design Decision

I had always thought of exception handling as error handling — something you add to stop crashes. I now think about it completely differently.

The question isn't "what do I do when something goes wrong?" The question is "whose responsibility is it to handle this?" Library code detects problems and raises with clear messages. Caller code catches and decides what to do. These are different jobs.

When my early validators returned `False` on failure, I thought I was being helpful — giving the caller a flag to check. What I was actually doing was hiding information. The caller got `False` with no idea what dimension mismatched, which matrix was empty, which index was out of range. Raising with a descriptive message gives the caller everything they need.

`raise ValueError("Cannot multiply: matrix[2] has shape (3, 4) and matrix[3] has shape (2, 2). Inner dimensions must match: 4 != 2.")` is not the same thing as `return False`. One is information. One is silence.

---

## Tests Are Not Verification — They Are Design

I wrote tests after the code in my first version. Every subsequent version had more tests written earlier. The difference was not just catching bugs (though it caught many — a wrong trace formula, an inverted condition in three separate methods, a shallow copy that wasn't actually copying).

The bigger difference was that writing a test before a method forces you to think about the interface before the implementation. When I wrote `self.assertEqual(A.swap_rows(1, 2), Matrix([[3, 4], [1, 2]]))` before implementing `swap_rows`, I had already decided: it takes 1-indexed arguments, it returns a new Matrix, it doesn't mutate. Those decisions were made at the test level, not the implementation level. The code just had to satisfy them.

That inversion — test first, implement second — changes the quality of the code that comes out.

---

## What I'd Do Differently

**Implement LU decomposition.** The current determinant is mathematically correct and pedagogically useful. It's also O(n!). For Day 1 that's acceptable. For anything I actually use, it isn't.

**Add a `__str__` distinct from `__repr__`.** Right now both show the same thing. `__repr__` should be unambiguous and reconstructable. `__str__` should be human-readable, formatted like a proper matrix grid. I know how to do this — I didn't get to it.

**Type hints throughout.** The method signatures have some type hints, but not consistently. A properly typed library catches an entire class of bugs before runtime.

**Property-based testing.** I tested specific values. But mathematical laws give you test cases for free: `A @ identity == A`, `(A @ B).transpose() == B.transpose() @ A.transpose()`, `determinant(A @ B) == determinant(A) * determinant(B)`. These are true for all valid matrices. Testing them with randomly generated inputs would give much stronger coverage than any list of hand-picked cases.

---

## The Honest Summary

I started this thinking I'd spend a few hours and end up with a neat little library. I spent considerably longer, rewrote sections multiple times, shipped code with bugs in methods I was sure were correct, and had to be told — more than once — that the thing I was most confident about was wrong.

That was the point.

The habit I'm trying to build isn't "write correct code on the first try." It's "build the feedback loops that catch incorrect code before it ships." Tests. Review. Running the thing and checking the output. This project was practice for that habit as much as it was practice for linear algebra.

Day 1 done. 89 to go.