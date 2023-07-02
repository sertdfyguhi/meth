# meth: A mathematical expression parser.

A python package to parse and evaluate mathematical expressions.

# Installation

```sh
pip install meth
```

or install it from source:

```sh
git clone https://github.com/sertdfyguhi/meth/
cd meth
python3 -m build
pip install dist/*.whl
```

# Examples

> _More examples in the [examples/](https://github.com/sertdfyguhi/meth/tree/master/examples) directory._

```py
import meth

# tokenizing equations
meth.tokenize("5 + 2") # INT(5), PLUS, INT(2)

# parsing equations
meth.parse("2 * 10") # BinaryOpNode(INT(2), MUL, INT(10))

# evaluating equations
meth.evaluate("2 + 2") # 4
meth.evaluate("sqrt(9)") # 3

# evaluation with variables
evaluator = meth.Evaluator()
evaluator.evaluate("x = 5")
evaluator.evaluate("x") # 5
```

# Todo

- [x] Lexer
- [x] Parser
  - [x] Bracketing
  - [x] Multiplication using brackets
  - [x] Negative Numbers
  - [x] Variables
  - [x] Functions
- [x] Interpreter
  - [x] Binary Operations
  - [x] Unary Operations
  - [x] Variables
  - [x] Functions
- [x] Add mathematical functions
- [ ] Accurate float calculations
- [ ] Simplify an expression
- [ ] Expand an expression
- [x] AST to Equation String
- [ ] Documentation
- [x] Publish to PyPI
