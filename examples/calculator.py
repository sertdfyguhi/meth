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
