# Arquivo de projeção da interface da calculadora!
# Deve ser passado para render.py depois

from tkinter import *
from tkinter import ttk
import math

calculator = Tk()
calculator.title("Calculadora")
calculator.tk.call('tk','scaling', 2.2)

# Frames
tela = ttk.Frame(calculator, padding=20)
tela.grid()
botoes = ttk.Frame(calculator, padding=5)
botoes.grid(column=0, row=1)
visor = ttk.Frame(calculator, padding=5)
visor.grid(column=0, row=0)

# Função para abrir a calculadora científica
def abrir_cientifica():
    calculator.destroy()
    from calc_cientifica import interface as cientifica_interface
    cientifica_interface().mainloop()

# Variável que guarda o que está no visor
Calculo = StringVar(value="0")

# Funções
def add_values(v):
    atual = Calculo.get()
    if atual == "0":
        Calculo.set(v)
    else:
        Calculo.set(atual + v)

def clear_one():
    Calculo.set("0")

def backspace():
    atual = Calculo.get()
    if len(atual) > 1:
        Calculo.set(atual[:-1])
    else:
        Calculo.set("0")

def calc_result():
    try:
        Calculo.set(str(eval(Calculo.get().replace("÷","/").replace("X","*"))))
    except:
        Calculo.set("Erro")

def inv_number():
    try:
        Calculo.set(str(1 / float(Calculo.get())))
    except:
        Calculo.set("Erro")

def square():
    try:
        Calculo.set(str(float(Calculo.get()) ** 2))
    except:
        Calculo.set("Erro")

def square_root():
    try:
        Calculo.set(str(math.sqrt(float(Calculo.get()))))
    except:
        Calculo.set("Erro")

def percent():
    try:
        Calculo.set(str(float(Calculo.get()) / 100))
    except:
        Calculo.set("Erro")
        


# ----------------- VISOR -----------------
btnModo = Button(visor, text="🧪", bg="#1a1217", fg="#c40202", width=2, command=abrir_cientifica).grid(column=0, row=0)
EntradaCalcul = Entry(visor, textvariable=Calculo, width=23, borderwidth=3, justify='right').grid(column=1, row=0)

# ----------------- BOTÕES -----------------

# linha n1
btnPercent = Button(botoes, bg="#1a1217", fg="#fafafa", text="%", width=5, command=percent).grid(column=1, row=1, padx=2, pady=2)
btnCE = Button(botoes, bg="#1a1217", fg="#fafafa", text="CE", width=5, command=clear_one).grid(column=2, row=1, padx=2, pady=2)
btnC = Button(botoes, bg="#1a1217", fg="#fafafa", text="C", width=5, command=clear_one).grid(column=3, row=1, padx=2, pady=2)
btnBackspace = Button(botoes, bg="#1a1217", fg="#fafafa", text="⌫", width=5, command=backspace).grid(column=4, row=1, padx=2, pady=2)

# linha n2
btnDecimalFunction = Button(botoes, bg="#1a1217", fg="#fafafa", text="1/x", width=5, command=inv_number).grid(column=1, row=2, padx=2, pady=2)
btnPower = Button(botoes, bg="#1a1217", fg="#fafafa", text="x²", width=5, command=square).grid(column=2, row=2, padx=2, pady=2)
btnSquareRoot = Button(botoes, bg="#1a1217", fg="#fafafa", text="²√x", width=5, command=square_root).grid(column=3, row=2, padx=2, pady=2)
btnDivision = Button(botoes, bg="#1a1217", fg="#fafafa", text="÷", width=5, command=lambda: add_values("÷")).grid(column=4, row=2, padx=2, pady=2)

# linha n3
btnSeven = Button(botoes, bg="#1a1217", fg="#fafafa", text="7", width=5, command=lambda: add_values("7")).grid(column=1, row=3, padx=2, pady=2)
btnEight = Button(botoes, bg="#1a1217", fg="#fafafa", text="8", width=5, command=lambda: add_values("8")).grid(column=2, row=3, padx=2, pady=2)
btnNine = Button(botoes, bg="#1a1217", fg="#fafafa", text="9", width=5, command=lambda: add_values("9")).grid(column=3, row=3, padx=2, pady=2)
btnMultiplication = Button(botoes, bg="#1a1217", fg="#fafafa", text="X", width=5, command=lambda: add_values("X")).grid(column=4, row=3, padx=2, pady=2)

# linha n4
btnFour = Button(botoes, bg="#1a1217", fg="#fafafa", text="4", width=5, command=lambda: add_values("4")).grid(column=1, row=4, padx=2, pady=2)
btnFive = Button(botoes, bg="#1a1217", fg="#fafafa", text="5", width=5, command=lambda: add_values("5")).grid(column=2, row=4, padx=2, pady=2)
btnSix = Button(botoes, bg="#1a1217", fg="#fafafa", text="6", width=5, command=lambda: add_values("6")).grid(column=3, row=4, padx=2, pady=2)
btnMinus = Button(botoes, bg="#1a1217", fg="#fafafa", text="-", width=5, command=lambda: add_values("-")).grid(column=4, row=4, padx=2, pady=2)

# linha n5
btnOne = Button(botoes, bg="#1a1217", fg="#fafafa", text="1", width=5, command=lambda: add_values("1")).grid(column=1, row=5, padx=2, pady=2)
btnTwo = Button(botoes, bg="#1a1217", fg="#fafafa", text="2", width=5, command=lambda: add_values("2")).grid(column=2, row=5, padx=2, pady=2)
btnThree = Button(botoes, bg="#1a1217", fg="#fafafa", text="3", width=5, command=lambda: add_values("3")).grid(column=3, row=5, padx=2, pady=2)
btnPlus = Button(botoes, bg="#1a1217", fg="#fafafa", text="+", width=5, command=lambda: add_values("+")).grid(column=4, row=5, padx=2, pady=2)

# linha n6
btnZero = Button(botoes, bg="#1a1217", fg="#fafafa", text="0", width=5, command=lambda: add_values("0")).grid(column=1, row=6, padx=2, pady=2)
btnComma = Button(botoes, bg="#1a1217", fg="#fafafa", text=",", width=5, command=lambda: add_values(".")).grid(column=2, row=6, padx=2, pady=2)
btnEquals = Button(botoes, fg="#ffebfc", bg="#c40202", text="=", width=5, command=calc_result).grid(column=3, row=6, sticky=EW, columnspan=2, padx=2, pady=2)

calculator.mainloop()
