# meth: A mathematical expression evaluator.

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

# tokenizing expression
meth.tokenize("5 + 2") # [Token(TokenType.NUMBER, 5), Token(TokenType.ADD), Token(TokenType.NUMBER, 2)]

# parsing expression
meth.parse("7 * 2") # BinaryOp(Number(7), TokenType.MUL, Number(2))

# evaluating expression
meth.evaluate("4 ^ 2") # 16
meth.evaluate("3(1 + 2)") # 9
meth.evaluate("sqrt(9)") # 3

# evaluation with variables
evaluator = meth.Evaluator()
evaluator.evaluate("x = 5")
evaluator.evaluate("x") # 5
```
