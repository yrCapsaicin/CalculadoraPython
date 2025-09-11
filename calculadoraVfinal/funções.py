import math

# -------- Variáveis globais --------
values = ["#"]          # Lista de dígitos digitados
operation = [0, "#", 0] # [valor1, operador, valor2]
aIndex = 0              # Índice para operação
Alpha = False
Shift = False

def res():
    try:
        a = operation[0]
        b = operation[2]
        op = operation[1]

        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return "Erro" if b == 0 else a / b
        else:
            return b
    except:
        return "Erro"

def reset_values(result):
    global values, operation, aIndex
    values = ["#"]
    operation = [result, "#", 0]
    aIndex = 0

def calc_raiz(obj):
    n = float("".join(values)) if values[0] != "#" else 0
    res = math.sqrt(n)
    obj.set(str(res))
    reset_values(res)

def calc_raiz_cubica(obj):
    n = float("".join(values)) if values[0] != "#" else 0
    res = n ** (1/3)
    obj.set(str(res))
    reset_values(res)

def calc_radiciacao(obj):
    global values, operation, aIndex
    # Se já existe uma operação de rad aguardando o radicando
    if operation[1] == "rad" and values[0] != "#":
        radicando = float("".join(values))
        indice = operation[0]
        if indice == 0:
            res = "Erro"
        else:
            res = radicando ** (1/indice)
        obj.set(str(res))
        if res != "Erro":
            reset_values(res)
    else:
        # Primeiro clique: define o índice da raiz
        indice = float("".join(values)) if values[0] != "#" else 0
        operation[0] = indice
        operation[1] = "rad"
        values[:] = ["#"]
        obj.set(str(indice) + "√")


def calc_inverso(obj):
    n = float("".join(values)) if values[0] != "#" else 0
    if n == 0:
        res = "Erro"
    else:
        res = 1 / n
    obj.set(str(res))
    if res != "Erro":
        reset_values(res)
        
def calc_fatorial(obj):
    n = int(float("".join(values))) if values[0] != "#" else 0
    res = math.factorial(n) if n >= 0 else "Erro"
    obj.set(str(res))
    if res != "Erro":
        reset_values(res)

def calc_quadrado(obj):
    n = float("".join(values)) if values[0] != "#" else 0
    res = n**2
    obj.set(str(res))
    reset_values(res)

def calc_cubo(obj):
    n = float("".join(values)) if values[0] != "#" else 0
    res = n**3
    obj.set(str(res))
    reset_values(res)

def calc_exponenciacao(obj):
    global values, operation, aIndex
    # Se já existe uma operação com ^ aguardando o expoente
    if operation[1] == "^" and values[0] != "#":
        expoente = float("".join(values))
        base = operation[0]
        res = base ** expoente
        obj.set(str(res))
        reset_values(res)
    else:
        # Primeiro clique: define a base
        base = float("".join(values)) if values[0] != "#" else 0
        operation[0] = base
        operation[1] = "^"
        values[:] = ["#"]
        obj.set(str(base) + "^")
