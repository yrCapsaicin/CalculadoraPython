from tkinter import *
from tkinter import ttk
import math

# -------- Variáveis globais --------
values = ["#"]          # Lista de dígitos digitados
operation = [0, "#", 0] # [valor1, operador, valor2]
aIndex = 0              # Índice para operação
Alpha = False
Shift = False

# -------- Funções de visor --------
def add_values(n, obj):
    global values
    if values[0] == "#":
        values[0] = n
    else:
        values.append(n)
    obj.set("".join(values))  # Atualiza visor

def clearone(obj):
    global values
    values = ["#"]
    obj.set("0")

def this_clearall(obj):
    global values, operation, aIndex
    values = ["#"]
    operation = [0, "#", 0]
    aIndex = 0
    obj.set("0")

# -------- Funções de operação básica --------
def add_signal(s, obj):
    global aIndex, operation, values
    try:
        current_value = float("".join(values))
    except ValueError:
        current_value = 0

    operation[aIndex] = current_value

    if aIndex == 2 or s == "=":
        result = res()
        operation[0] = result if isinstance(result, (int, float)) else 0
        operation[2] = 0
        operation[1] = "#" if s == "=" else s
        aIndex = 2
        values = ["#"]
        obj.set(str(result))
        return result
    else:
        operation[1] = s
        aIndex = 2
        values = ["#"]
        return 0

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
        elif op == "^":  # Exponenciação
            return a ** b
        elif op == "rad":  # Radiciação genérica
            return b ** (1/a)
        else:
            return b
    except:
        return "Erro"

# -------- Funções científicas simplificadas --------
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

# -------- Interface --------
def interface():
    global values
    calculator = Tk()
    calculator.title("Calculadora científica")
    calculator.tk.call('tk','scaling', 2.2)

    # Frames
    visor = ttk.Frame(calculator, padding=5)
    visor.grid(column=0, row=0)

    botoes1 = ttk.Frame(calculator)
    botoes1.grid(column=0, row=1)

    botoes2 = ttk.Frame(calculator)
    botoes2.grid(column=0, row=2)

    Calculo = StringVar(value="0")

    # Função de trocar para a calculadora normal
    def abrir_normal():
        calculator.destroy()  # fecha a científica
        from calc_normal import interface as normal_interface
        normal_interface().mainloop()  # abre a normal

# ----------------------------------------------------- #

    Calculo = StringVar(value="0");

    btnModo = Button(visor, text="🧪", bg="#1a1217", fg="#c40202", width=2, command=abrir_normal).grid(column=0, row=0)

    EntradaCalcul = Entry(visor, textvariable=Calculo, width=35, borderwidth=3, justify="right").grid(column=1, row=0)


    # linha n1

    btnShift = Button(botoes1, bg="#1a1217", fg="#fafafa", text="SHIFT", width=5).grid(column=1, row=1, padx=2, pady=2)

    btnAlpha = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ALPHA", width=5, command=lambda: clearone(Calculo)).grid(column=2, row=1, padx=2, pady=2)

    btnReplay = Button(botoes1, fg="#FAFAFA", bg="#c40202", text="REPLAY", width=11).grid(column=3, row=1, sticky=NS, columnspan=2,rowspan=3, padx=2, pady=2)

    btnMode = Button(botoes1, bg="#1a1217", fg="#fafafa", text="MODE", width=5).grid(column=5, row=1, padx=2, pady=2)

    btnOn = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ON", width=5).grid(column=6, row=1, padx=2, pady=2)



    #linha n2


    lblX = Label(botoes1, fg="#1a1217", text="x!", width=5, font=("Arial", 4, "bold")).grid(column=1, row=2, padx=2, pady=2)


    lblNPR = Label(botoes1, fg="#1a1217", text="nPr", width=5, font=("Arial", 4, "bold")).grid(column=2, row=2, padx=2, pady=2)


    lblREC = Label(botoes1, fg="#1a1217", text="REC( :", width=5, font=("Arial", 4, "bold")).grid(column=5, row=2, padx=2, pady=2)


    lblRaiz = Label(botoes1, fg="#1a1217", text="³√", width=5, font=("Arial", 4, "bold")).grid(column=6, row=2, padx=2, pady=2)


    btnX1 =  Button(botoes1, bg="#1a1217", fg="#fafafa", text="x⁻¹", width=5, command=lambda: calc_inverso(Calculo)).grid(column=1, row=3, padx=2, pady=2)


    btnnCr = Button(botoes1, bg="#1a1217", fg="#fafafa", text="nCr", width=5).grid(column=2, row=3, padx=2, pady=2)


    btnPol = Button(botoes1, bg="#1a1217", fg="#fafafa", text="Pol(", width=5).grid(column=5, row=3, padx=2, pady=2)


    btnx3 = Button(botoes1, bg="#1a1217", fg="#fafafa", text="x³", width=5, command=lambda: calc_cubo(Calculo)).grid(column=6, row=3, padx=2, pady=2)


    #linha n3


    lblDC = Label(botoes1, fg="#1a1217", text="d/c", width=5, font=("Arial", 4, "bold")).grid(column=1, row=4, padx=2, pady=2)


    lblElevaX = Label(botoes1, fg="#1a1217", text="ˣ√", width=5, font=("Arial", 4, "bold")).grid(column=4, row=4, padx=2, pady=2)


    lblDezX = Label(botoes1, fg="#1a1217", text="10ˣ", width=5, font=("Arial", 4, "bold")).grid(column=5, row=4, padx=2, pady=2)


    lblEX = Label(botoes1, fg="#1a1217", text="eˣ", width=5, font=("Arial", 4, "bold")).grid(column=6, row=4, padx=2, pady=2)


    btnAbc = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ab/c", width=5, command=lambda: add_values("7", Calculo)).grid(column=1, row=5, padx=2, pady=2)


    btnRaiz = Button(botoes1, bg="#1a1217", fg="#fafafa", text="√", width=5, command=lambda: calc_raiz(Calculo)).grid(column=2, row=5, padx=2, pady=2)


    btx2 =  Button(botoes1, bg="#1a1217", fg="#fafafa", text="x²", width=5, command=lambda: calc_quadrado(Calculo)).grid(column=3, row=5, padx=2, pady=2)


    btnElevado =  Button(botoes1, bg="#1a1217", fg="#fafafa", text="^", width=5, command=lambda: calc_exponenciacao(Calculo)).grid(column=4, row=5, padx=2, pady=2)


    btnLog = Button(botoes1, bg="#1a1217", fg="#fafafa", text="log", width=5, command=lambda: add_signal("*", Calculo)).grid(column=5, row=5, padx=2, pady=2)


    btnLn = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ln", width=5, command=lambda: add_signal("*", Calculo)).grid(column=6, row=5, padx=2, pady=2)



    #linha n4


    lblA = Label(botoes1, fg="#1a1217", text="A", width=5, font=("Arial", 4, "bold")).grid(column=1, row=6, padx=2, pady=2)


    lblTraco = Label(botoes1, fg="#1a1217", text="← B", width=5, font=("Arial", 4, "bold")).grid(column=2, row=6, padx=2, pady=2)


    lblC = Label(botoes1, fg="#1a1217", text="C", width=5, font=("Arial", 4, "bold")).grid(column=3, row=6, padx=2, pady=2)


    lblSin = Label(botoes1, fg="#1a1217", text="Sin⁻¹ D", width=5, font=("Arial", 4, "bold")).grid(column=4, row=6, padx=2, pady=2)


    lblCos = Label(botoes1, fg="#1a1217", text="Cos⁻¹ E", width=5, font=("Arial", 4, "bold")).grid(column=5, row=6, padx=2, pady=2)


    lblTan = Label(botoes1, fg="#1a1217", text="Tan⁻¹ F", width=5, font=("Arial", 4, "bold")).grid(column=6, row=6, padx=2, pady=2)


    btnPMP = Button(botoes1, bg="#1a1217", fg="#fafafa", text="(-)", width=5, command=lambda: add_values("4", Calculo)).grid(column=1, row=7, padx=2, pady=2)


    btnPontoVVV = Button(botoes1, bg="#1a1217", fg="#fafafa", text=". ,,,", width=5, command=lambda: add_values("5", Calculo)).grid(column=2, row=7, padx=2, pady=2)


    btnHyp = Button(botoes1, bg="#1a1217", fg="#fafafa", text="hyp", width=5, command=lambda: add_values("6", Calculo)).grid(column=3, row=7, padx=2, pady=2)


    btnSin = Button(botoes1, bg="#1a1217", fg="#fafafa", text="sin", width=5, command=lambda: add_signal("-", Calculo)).grid(column=4, row=7, padx=2, pady=2)


    btnCos = Button(botoes1, bg="#1a1217", fg="#fafafa", text="cos", width=5, command=lambda: add_signal("-", Calculo)).grid(column=5, row=7, padx=2, pady=2)


    btnTan = Button(botoes1, bg="#1a1217", fg="#fafafa", text="tan", width=5, command=lambda: add_signal("-", Calculo)).grid(column=6, row=7, padx=2, pady=2)


    #linha n5


    lblSTO = Label(botoes1, fg="#1a1217", text="STO", width=5, font=("Arial", 4, "bold")).grid(column=1, row=8, padx=2, pady=2)


    lblSeta2 = Label(botoes1, fg="#1a1217", text="←", width=5, font=("Arial", 4, "bold")).grid(column=2, row=8, padx=2, pady=2)


    lblX = Label(botoes1, fg="#1a1217", text="X", width=5, font=("Arial", 4, "bold")).grid(column=4, row=8, padx=2, pady=2)


    lblPontVir = Label(botoes1, fg="#1a1217", text="; Y", width=5, font=("Arial", 4, "bold")).grid(column=5, row=8, padx=2, pady=2)


    lblM = Label(botoes1, fg="#1a1217", text="M- M", width=5, font=("Arial", 4, "bold")).grid(column=6, row=8, padx=2, pady=2)


    btnRCL = Button(botoes1, bg="#1a1217", fg="#fafafa", text="RCL", width=5, command=lambda: add_values("1", Calculo)).grid(column=1, row=9, padx=2, pady=2)


    btnENG = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ENG", width=5, command=lambda: add_values("2", Calculo)).grid(column=2, row=9, padx=2, pady=2)


    btnP1 = Button(botoes1, bg="#1a1217", fg="#fafafa", text="(", width=5, command=lambda: add_values("3", Calculo)).grid(column=3, row=9, padx=2, pady=2)


    btnP2 = Button(botoes1, bg="#1a1217", fg="#fafafa", text=")", width=5, command=lambda: add_signal("+", Calculo)).grid(column=4, row=9, padx=2, pady=2)


    btnVirgula = Button(botoes1, bg="#1a1217", fg="#fafafa", text=",", width=5, command=lambda: add_signal("+", Calculo)).grid(column=5, row=9, padx=2, pady=2)


    btnMmais = Button(botoes1, bg="#1a1217", fg="#fafafa", text="M+", width=5, command=lambda: add_signal("+", Calculo)).grid(column=6, row=9, padx=2, pady=2)



    #linha n6


    lblIns = Label(botoes2, fg="#1a1217", text="INS", width=5, font=("Arial", 4, "bold")).grid(column=4, row=10, padx=2, pady=2)


    lblOFF = Label(botoes2, fg="#1a1217", text="OFF", width=5, font=("Arial", 4, "bold")).grid(column=5, row=10, padx=2, pady=2)


    btnSete = Button(botoes2, bg="#1a1217", fg="#fafafa", text="7", width=6, command=lambda: add_values("7", Calculo)).grid(column=1, row=11, padx=2, pady=2, sticky=EW)


    btnOito = Button(botoes2, bg="#1a1217", fg="#fafafa", text="8", width=6, command=lambda: add_values("8", Calculo)).grid(column=2, row=11, padx=2, pady=2, sticky=EW)


    btnNove = Button(botoes2, bg="#1a1217", fg="#fafafa", text="9", width=6, command=lambda: add_values("9", Calculo)).grid(column=3, row=11, padx=2, pady=2, sticky=EW)


    btnDEL = Button(botoes2, bg="#c40202", fg="#fafafa", text="DEL", width=6, command=lambda: clearone(Calculo)).grid(column=4, row=11, padx=2, pady=2)


    btnAC = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="AC", width=6, command=lambda: this_clearall(Calculo)).grid(column=5, row=11, padx=2, pady=2)


    #linha n7


    lblEspaco = Label(botoes2, fg="#1a1217", text="", font=("Arial", 4, "bold")).grid(column=1, row=12, padx=2, pady=2)


    btnQuatro = Button(botoes2, bg="#1a1217", fg="#fafafa", text="4", width=6, command=lambda: add_values("4", Calculo)).grid(column=1, row=13, padx=2, pady=2)


    btnCinco = Button(botoes2, bg="#1a1217", fg="#fafafa", text="5", width=6, command=lambda: add_values("5", Calculo)).grid(column=2, row=13, padx=2, pady=2)


    btnSeis = Button(botoes2, bg="#1a1217", fg="#fafafa", text="6", width=6, command=lambda: add_values("6", Calculo)).grid(column=3, row=13, padx=2, pady=2)


    btnX = Button(botoes2, bg="#c40202", fg="#fafafa", text="×", width=6, command=lambda: add_signal("*", Calculo)).grid(column=4, row=13, padx=2, pady=2)


    btnDivisao = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="÷", width=6, command=lambda: add_signal("/", Calculo)).grid(column=5, row=13, padx=2, pady=2)


    #linha n8


    lblSum = Label(botoes2, fg="#1a1217", text="S-SUM", font=("Arial", 4, "bold")).grid(column=1, row=14, padx=2, pady=2)


    lblSVAR = Label(botoes2, fg="#1a1217", text="S-VAR", font=("Arial", 4, "bold")).grid(column=2, row=14, padx=2, pady=2)


    btnUm = Button(botoes2, bg="#1a1217", fg="#fafafa", text="1", width=6, command=lambda: add_values("1", Calculo)).grid(column=1, row=15, padx=2, pady=2)


    btnDois = Button(botoes2, bg="#1a1217", fg="#fafafa", text="2", width=6, command=lambda: add_values("2", Calculo)).grid(column=2, row=15, padx=2, pady=2)


    btnTres = Button(botoes2, bg="#1a1217", fg="#fafafa", text="3", width=6, command=lambda: add_values("3", Calculo)).grid(column=3, row=15, padx=2, pady=2)


    btnMais = Button(botoes2, bg="#c40202", fg="#fafafa", text="+", width=6, command=lambda: add_signal("+", Calculo)).grid(column=4, row=15, padx=2, pady=2)


    btnMenos = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="-", width=6, command=lambda: add_signal("-", Calculo)).grid(column=5, row=15, padx=2, pady=2)


    #linha n9


    lblRND = Label(botoes2, fg="#1a1217", text="RND", width=5, font=("Arial", 4, "bold")).grid(column=1, row=16, padx=2, pady=2)


    lblRan = Label(botoes2, fg="#1a1217", text="Ran#", width=5, font=("Arial", 4, "bold")).grid(column=2, row=16, padx=2, pady=2)


    lblPI = Label(botoes2, fg="#1a1217", text="π", width=5, font=("Arial", 4, "bold")).grid(column=3, row=16, padx=2, pady=2)

    lblDRG = Label(botoes2, fg="#1a1217", text="DRG", width=5, font=("Arial", 4, "bold")).grid(column=4, row=16, padx=2, pady=2)


    lblPorcentagem = Label(botoes2, fg="#1a1217", text="%", width=5, font=("Arial", 4, "bold")).grid(column=5, row=16, padx=2, pady=2)


    btnZero = Button(botoes2, bg="#1a1217", fg="#fafafa", text="0", width=6, command=lambda: add_values("0", Calculo)).grid(column=1, row=17, padx=2, pady=2)


    btnPonto = Button(botoes2, bg="#1a1217", fg="#fafafa", text="•", width=6).grid(column=2, row=17, padx=2, pady=2)


    btnEXP = Button(botoes2, bg="#1a1217", fg="#fafafa", text="EXP", width=6).grid(column=3, row=17, padx=2, pady=2)


    btnAns = Button(botoes2, bg="#1a1217", fg="#fafafa", text="Ans", width=6).grid(column=4, row=17, padx=2, pady=2)


    btnIgual = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="=", width=6, command=lambda: add_signal("=", Calculo)).grid(column=5, row=17, padx=2, pady=2)

    return calculator;

interface().mainloop();