from typing import Callable

def contador_invocaciones(func):
    def wrapper(*args, **kwargs):
        wrapper.cuenta += 1
        return func(*args, **kwargs)
    wrapper.cuenta = 0
    return wrapper

@contador_invocaciones
def validate(b=True)->bool|int:
    if b:
        return True
    return validate.cuenta
        

print(validate())
print(validate())
print(validate())
print(validate())
print(validate())
print(validate(False))


def tostr(func:Callable[[],int])->Callable[[],str]:
    def wrapper()->str:
        return str(func())
    return wrapper

@tostr
def cinco()->int:
    return 5

    
a="hola"
b=a+cinco()
print(b)