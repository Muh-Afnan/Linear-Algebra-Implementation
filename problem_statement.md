Problem Statement
Why I Built This
I use NumPy almost every day. I call np.linalg.det(), np.transpose(), np.linalg.inv() and move on. It works, and I never think twice about it.
But that started bothering me.
I didn't actually know what was happening inside those calls. I knew what they did — not how they did it. And for someone who wants to work seriously in machine learning and AI engineering, that gap felt wrong. How can I debug a model that's misbehaving if I don't understand the math underneath it? How can I reason about numerical stability, or explain why a matrix is singular, or catch a shape mismatch before it crashes my training loop — if I've always just trusted the library to handle it?
So I decided to find out for myself.
The Goal
Build a matrix operations library from scratch. No NumPy. No SciPy. No math libraries of any kind. Just Python and the underlying mathematics.
The rules I set for myself were simple:

If I couldn't explain why the code works mathematically, I couldn't write it
Every operation had to be tested — not just "does it run" but "does it produce the right answer"
The library had to be something another person could actually use, not just a script I ran once

What I Wanted to Understand
Specifically, I wanted to answer a few questions I'd been carrying around:
What does matrix multiplication actually compute? Not the rule — why does multiplying rows by columns produce something meaningful? What geometric transformation is happening?
How does a library find the determinant of a large matrix? I knew the 2x2 formula. But a 5x5? A 10x10? There had to be a recursive structure there.
What does it mean for a matrix to be singular? I'd heard "non-invertible" and "determinant is zero" as if they were separate facts. Building the inverse from scratch made clear they're the same fact.
Why do libraries raise errors the way they do? When NumPy throws a LinAlgError, what did it actually check? Writing my own validation logic taught me that proper error messages are a design decision, not an afterthought.
The Broader Context
This is Day 1 of a 90-day challenge I've set for myself. The challenge spans machine learning, deep learning, AI engineering, and the mathematics that underlies all of it. I'm building each project as a portfolio artifact — documented, tested, and pushed to GitHub.
The matrix library is the foundation. Almost everything I'll build over the next 89 days — gradient descent, neural networks, PCA, transformers — lives on top of linear algebra. I wanted to meet that foundation on its own terms before using it as a black box.