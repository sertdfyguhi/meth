# setup to allow for usage of modules in the parent directory, ignore
# import sys
# import os

# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# start of actual code
import meth

if __name__ == "__main__":
    print("Calculator made using meth.")

    evaluator = meth.Evaluator()

    while True:
        try:
            expr = input("> ")
        except KeyboardInterrupt:
            # dont print keyboard interrupt error
            break

        try:
            if (result := evaluator.evaluate(expr)) is not None:
                print(result)
        except meth.error.BaseError as e:
            print(e)
