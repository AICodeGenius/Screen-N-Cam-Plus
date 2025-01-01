#decorator example
def my_decorator(func):
    x=10
    print("I am a decorator - start")
    def wrapper():
        print("Something is happening before the function is called." + str(x))
        func()
        print("Something is happening after the function is called.")
    x=20
    print("I am a decorator - finish")
    return wrapper

def say_hello():
    print("Hello!")

print('start program')
say_hello = my_decorator(say_hello)
print('say_hello assigned')
say_hello()
say_hello()