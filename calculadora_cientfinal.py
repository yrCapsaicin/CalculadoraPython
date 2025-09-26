
from tkinter import *
from tkinter import ttk
import math, re
from fractions import Fraction
from math import log, log10, radians, cos, factorial

# -------- Variáveis globais 

values = ["#"]
operation = [0, "#", 0]
aIndex = 0
Alpha = False
Shift = False
memory_slots = {}
ans_value = None
historico = []  
current_mode = 'COMP'

# -------- Funções dos outros grupooix 

def Abc(x: float) -> str:
    frac = Fraction(x).limit_denominator()
    return f"{frac.numerator}/{frac.denominator}"

def Dc(x: float) -> str:
    frac = Fraction(x).limit_denominator()
    inteiro, resto = divmod(frac.numerator, frac.denominator)
    if inteiro == 0:
        return f"{resto}/{frac.denominator}"
    elif resto == 0:
        return str(inteiro)
    else:
        return f"{inteiro} {resto}/{frac.denominator}"

def ENG(x: float) -> str:
    if x == 0:
        return "0"
    exp = int((math.log10(abs(x)) / 3) * 3)
    mantissa = x / (10 ** exp)
    return f"{mantissa}×10^{exp}"

def fnLn(s: str) -> float:
    if "ln" in s:
        value = float(s.removeprefix("ln"))
    else:
        raise ValueError("log não está definido")
    if value <= 0:
        raise ValueError("ln indefinido para x <= 0")
    return log(value)

def fnLog10(s: str) -> float:
    if "log" in s:
        value = float(s.removeprefix("log"))
    else:
        raise ValueError("log não está definido")
    if value <= 0:
        raise ValueError("log indefinido para x <= 0")
    return log10(value)

def Pol(s) -> float:
    s = s.replace("Pol(", "")
    if ")" in s:
        s = s.replace(")", "")
    if "," not in s:
        raise ValueError("Faltando argumento em Pol(x, y)")
    n, k = s.split(",")
    if not n or not k:
        raise ValueError("Argumentos inválidos em Pol(x, y)")
    return ((float(n) ** 2 + float(k) ** 2) ** 0.5)

def Rec(s):
    s = s.replace("Rec(", "")
    s = s.replace(")", "")
    n, k = s.split(",")
    return (float(n) * cos(radians(float(k))))

def nCr(s):
    if "C" in s:
        n,k= s.split("C")
        return factorial(int(n)) // (factorial(int(k)) * factorial(int(n) - int(k)))
    else:
        raise ValueError("Formato inválido nCk")

def nPr(s):
    if "P" in s:
        n,k = s.split("P")
        return factorial(int(n)) // factorial(int(n) - int(k))
    else:
        raise ValueError("Formato inválido nPk")

def twoPoints(s):
    if("Ans" in s):
        s = s.replace("Ans", "")
        s = s.replace("x","*")
        expressions = s.split(":")
        for i in range(len(expressions)):
            if i==0:
                expressions[i] = eval(expressions[i])
            else:
                expression = str(expressions[i-1])+""+str(expressions[i])
                expressions[i] = eval(expression)
        return expressions
    else:
        raise ValueError("Sintax Error: Ans não informado")
    

def safe_get_float(var):
    s = var.get().strip().replace(",", ".")
    if s == "" or s == "0":
        return 0.0
    try:
        return float(s)
    except:
        m = re.search(r'-?\d+(\.\d+)?', s)
        if m:
            return float(m.group(0))
        raise ValueError("valor inválido")

def wrapper_Abc(var):
    global Shift, values
    try:
        val = safe_get_float(var)
        if Shift:
            out = Dc(val)
        else:
            out = Abc(val)
        var.set(str(out))
        values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_ENG(var):
    global Shift, values
    try:
        val = safe_get_float(var)
        if Shift:
            s = var.get().replace("×", "*").replace("^", "**")
            try:
                v = eval(s)
                var.set(str(v))
                values = list(str(v))
                return
            except:
                pass
        var.set(ENG(val))
        values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_ln(var):
    global Shift, values
    s = var.get().strip().replace(",", ".")
    try:
        if Shift:
            val = safe_get_float(var)
            var.set(str(math.e ** val))
            values = ["#"]
        else:
            var.set(str(fnLn("ln" + s)))
            values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_log10(var):
    global Shift, values
    s = var.get().strip().replace(",", ".")
    try:
        if Shift:
            val = safe_get_float(var)
            var.set(str(10 ** val))
            values = ["#"]
        else:
            var.set(str(fnLog10("log" + s)))
            values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_Pol(var):
    global Shift, values
    try:
        s = var.get().strip()
        if Shift:
            var.set(str(Rec(s)))
        else:
            var.set(str(Pol(s)))
        values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_nCr(var):
    global values
    try:
        s = var.get().strip()
        if "," in s and "C" not in s:
            n,k = s.split(",")
            s2 = n + "C" + k
        else:
            s2 = s
        var.set(str(nCr(s2)))
        values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_nPr(var):
    global values
    try:
        s = var.get().strip()
        if "," in s and "P" not in s:
            n,k = s.split(",")
            s2 = n + "P" + k
        else:
            s2 = s
        var.set(str(nPr(s2)))
        values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def wrapper_twoPoints(var):
    global values
    try:
        s = var.get().strip()
        out = twoPoints(s)
        var.set(str(out))
        values = ["#"]
    except Exception as e:
        var.set("Erro: " + str(e))
        values = ["#"]

def do_sto(var):
    try:
        memory_slots['M'] = var.get()
    except:
        memory_slots['M'] = None

def do_rcl(var):
    if 'M' in memory_slots:
        v = memory_slots['M']
        var.set(str(v))
        global values
        values = list(str(v)) if v is not None else ["#"]

def toggle_shift():
    global Shift, shift_label_var
    Shift = not Shift
    try:
        shift_label_var.set("SHIFT" if Shift else "")
    except Exception:
        pass

def call_and_clear_shift(fn, var):
    """Call function fn(var) and clear SHIFT (one-shot)"""
    global Shift, shift_label_var
    try:
        fn(var)
    finally:
        Shift = False
        try:
            shift_label_var.set("")
        except Exception:
            pass

def wrapper_sin(var):
    global values
    try:
        val = safe_get_float(var)
        res = math.sin(math.radians(val))
        var.set(str(res))
        values = ["#"]
    except Exception as e:
        var.set("Erro: "+str(e))
        values = ["#"]

def wrapper_cos(var):
    global values
    try:
        val = safe_get_float(var)
        res = math.cos(math.radians(val))
        var.set(str(res))
        values = ["#"]
    except Exception as e:
        var.set("Erro: "+str(e))
        values = ["#"]

def wrapper_tan(var):
    global values
    try:
        val = safe_get_float(var)
        res = math.tan(math.radians(val))
        var.set(str(res))
        values = ["#"]
    except Exception as e:
        var.set("Erro: "+str(e))
        values = ["#"]

# -------- Visor e operações originais LMTM
def add_values(n, obj):
    global values
    if values[0] == "#":
        values[0] = n
    else:
        values.append(n)
    obj.set("".join(values))

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

def add_signal(s, obj):
    global aIndex, operation, values, ans_value
    try:
        current_value = float("".join(values))
    except Exception:
        try:
            current_value = float(obj.get().replace(",", "."))
        except:
            current_value = 0.0
    operation[aIndex] = current_value
    if aIndex == 2 or s == "=":
        result = res()
        operation[0] = result if isinstance(result, (int, float)) else 0
        operation[2] = 0
        operation[1] = "#" if s == "=" else s
        aIndex = 2
        values = ["#"]
        obj.set(str(result))
        ans_value = result
        return result
    try:
        historico.append((operation[0], operation[1], operation[2], result))
    except:
        pass
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
        elif op == "^":
            return a ** b
        elif op == "rad":
            return b ** (1/a)
        else:
            return b
    except:
        return "Erro"

def reset_values(result):
    global values, operation, aIndex
    values = ["#"]
    operation = [result, "#", 0]
    aIndex = 0

# -------- Funções científicas
 
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
    if operation[1] == "rad" and values[0] != "#":
        try:
            radicando = float("".join(values))
        except:
            radicando = 0.0
        operation[2] = radicando
        indice = operation[0]
        if indice == 0:
            res = "Erro"
        else:
            try:
                res = radicando ** (1.0 / indice)
            except Exception:
                res = "Erro"
        obj.set(str(res))
        if res != "Erro":
            reset_values(res)
    else:
        try:
            indice = float("".join(values)) if values[0] != "#" else 0.0
        except:
            indice = 0.0
        operation[0] = indice
        operation[1] = "rad"
        aIndex = 2
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
    if operation[1] == "^" and values[0] != "#":
        try:
            expoente = float("".join(values))
        except:
            try:
                expoente = float(obj.get().replace(",", "."))
            except:
                expoente = 0.0
        operation[2] = expoente
        base = operation[0]
        try:
            res = base ** expoente
        except Exception:
            res = "Erro"
        obj.set(str(res))
        if res != "Erro":
            reset_values(res)
    else:
        try:
            base = float("".join(values)) if values[0] != "#" else 0.0
        except:
            try:
                base = float(obj.get().replace(",", "."))
            except:
                base = 0.0
        operation[0] = base
        operation[1] = "^"
        aIndex = 2
        values[:] = ["#"]
        obj.set(str(base) + "^")

# -------- Interface (layout preserved) --------
def interface():
    global values, Shift
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

    def abrir_normal():
        calculator.destroy()
        return

    Calculo = StringVar(value="0");

    btnModo = Button(visor, text="🧪", bg="#1a1217", fg="#c40202", width=2, command=abrir_normal)
    btnModo.grid(column=0, row=0)

    EntradaCalcul = Entry(visor, textvariable=Calculo, width=35, borderwidth=3, justify="right")
    EntradaCalcul.grid(column=1, row=0)

    # linha n1
    btnShift = Button(botoes1, bg="#1a1217", fg="#fafafa", text="SHIFT", width=5, command=lambda: toggle_shift(Calculo))
    btnShift.grid(column=1, row=1, padx=2, pady=2)

    btnAlpha = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ALPHA", width=5, command=lambda: clearone(Calculo))
    btnAlpha.grid(column=2, row=1, padx=2, pady=2)

    btnReplay = Button(botoes1, fg="#FAFAFA", bg="#c40202", text="REPLAY", width=11, command=lambda: replay_history(calculator, Calculo))
    btnReplay.grid(column=3, row=1, sticky=NS, columnspan=2,rowspan=3, padx=2, pady=2)

    btnMode = Button(botoes1, bg="#1a1217", fg="#fafafa", text="MODE", width=5, command=lambda: toggle_mode(calculator))
    btnMode.grid(column=5, row=1, padx=2, pady=2)

    btnOn = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ON", width=5)
    btnOn.grid(column=6, row=1, padx=2, pady=2)

    # linha n2
    lblX = Label(botoes1, fg="#1a1217", text="x!", width=5, font=("Arial", 4, "bold"))
    lblX.grid(column=1, row=2, padx=2, pady=2)

    lblNPR = Label(botoes1, fg="#1a1217", text="nPr", width=5, font=("Arial", 4, "bold"))
    lblNPR.grid(column=2, row=2, padx=2, pady=2)

    lblREC = Label(botoes1, fg="#1a1217", text="REC( :", width=5, font=("Arial", 4, "bold"))
    lblREC.grid(column=5, row=2, padx=2, pady=2)

    lblRaiz = Label(botoes1, fg="#1a1217", text="³√", width=5, font=("Arial", 4, "bold"))
    lblRaiz.grid(column=6, row=2, padx=2, pady=2)

    btnX1 =  Button(botoes1, bg="#1a1217", fg="#fafafa", text="x⁻¹", width=5, command=lambda: (call_and_clear_shift(calc_fatorial, Calculo) if Shift else calc_inverso(Calculo)))
    btnX1.grid(column=1, row=3, padx=2, pady=2)

    btnnCr = Button(botoes1, bg="#1a1217", fg="#fafafa", text="nCr", width=5, command=lambda: wrapper_nCr(Calculo))
    btnnCr.grid(column=2, row=3, padx=2, pady=2)

    btnPol = Button(botoes1, bg="#1a1217", fg="#fafafa", text="Pol(", width=5, command=lambda: wrapper_Pol(Calculo))
    btnPol.grid(column=5, row=3, padx=2, pady=2)

    btnx3 = Button(botoes1, bg="#1a1217", fg="#fafafa", text="x³", width=5, command=lambda: calc_cubo(Calculo))
    btnx3.grid(column=6, row=3, padx=2, pady=2)

    # linha n3
    lblDC = Label(botoes1, fg="#1a1217", text="d/c", width=5, font=("Arial", 4, "bold"))
    lblDC.grid(column=1, row=4, padx=2, pady=2)

    lblElevaX = Label(botoes1, fg="#1a1217", text="ˣ√", width=5, font=("Arial", 4, "bold"))
    lblElevaX.grid(column=4, row=4, padx=2, pady=2)

    lblDezX = Label(botoes1, fg="#1a1217", text="10ˣ", width=5, font=("Arial", 4, "bold"))
    lblDezX.grid(column=5, row=4, padx=2, pady=2)

    lblEX = Label(botoes1, fg="#1a1217", text="eˣ", width=5, font=("Arial", 4, "bold"))
    lblEX.grid(column=6, row=4, padx=2, pady=2)

    btnAbc = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ab/c", width=5, command=lambda: wrapper_Abc(Calculo))
    btnAbc.grid(column=1, row=5, padx=2, pady=2)

    btnRaiz = Button(botoes1, bg="#1a1217", fg="#fafafa", text="√", width=5, command=lambda: calc_raiz(Calculo))
    btnRaiz.grid(column=2, row=5, padx=2, pady=2)

    btx2 =  Button(botoes1, bg="#1a1217", fg="#fafafa", text="x²", width=5, command=lambda: calc_quadrado(Calculo))
    btx2.grid(column=3, row=5, padx=2, pady=2)

    btnElevado =  Button(botoes1, bg="#1a1217", fg="#fafafa", text="^", width=5, command=lambda: calc_exponenciacao(Calculo))
    btnElevado.grid(column=4, row=5, padx=2, pady=2)

    btnLog = Button(botoes1, bg="#1a1217", fg="#fafafa", text="log", width=5, command=lambda: wrapper_log10(Calculo))
    btnLog.grid(column=5, row=5, padx=2, pady=2)

    btnLn = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ln", width=5, command=lambda: wrapper_ln(Calculo))
    btnLn.grid(column=6, row=5, padx=2, pady=2)

    # linha n4
    lblA = Label(botoes1, fg="#1a1217", text="A", width=5, font=("Arial", 4, "bold"))
    lblA.grid(column=1, row=6, padx=2, pady=2)

    lblTraco = Label(botoes1, fg="#1a1217", text="← B", width=5, font=("Arial", 4, "bold"))
    lblTraco.grid(column=2, row=6, padx=2, pady=2)

    lblC = Label(botoes1, fg="#1a1217", text="C", width=5, font=("Arial", 4, "bold"))
    lblC.grid(column=3, row=6, padx=2, pady=2)

    lblSin = Label(botoes1, fg="#1a1217", text="Sin⁻¹ D", width=5, font=("Arial", 4, "bold"))
    lblSin.grid(column=4, row=6, padx=2, pady=2)

    lblCos = Label(botoes1, fg="#1a1217", text="Cos⁻¹ E", width=5, font=("Arial", 4, "bold"))
    lblCos.grid(column=5, row=6, padx=2, pady=2)

    lblTan = Label(botoes1, fg="#1a1217", text="Tan⁻¹ F", width=5, font=("Arial", 4, "bold"))
    lblTan.grid(column=6, row=6, padx=2, pady=2)

    btnPMP = Button(botoes1, bg="#1a1217", fg="#fafafa", text="(-)", width=5, command=lambda: add_values("-", Calculo))
    btnPMP.grid(column=1, row=7, padx=2, pady=2)

    btnPontoVVV = Button(botoes1, bg="#1a1217", fg="#fafafa", text=". ,,,", width=5, command=lambda: add_values(".", Calculo))
    btnPontoVVV.grid(column=2, row=7, padx=2, pady=2)

    btnHyp = Button(botoes1, bg="#1a1217", fg="#fafafa", text="hyp", width=5, command=lambda: add_values("hyp", Calculo))
    btnHyp.grid(column=3, row=7, padx=2, pady=2)

    btnSin = Button(botoes1, bg="#1a1217", fg="#fafafa", text="sin", width=5, command=lambda: wrapper_sin(Calculo))
    btnSin.grid(column=4, row=7, padx=2, pady=2)

    btnCos = Button(botoes1, bg="#1a1217", fg="#fafafa", text="cos", width=5, command=lambda: wrapper_cos(Calculo))
    btnCos.grid(column=5, row=7, padx=2, pady=2)

    btnTan = Button(botoes1, bg="#1a1217", fg="#fafafa", text="tan", width=5, command=lambda: wrapper_tan(Calculo))
    btnTan.grid(column=6, row=7, padx=2, pady=2)

    # linha n5
    lblSTO = Label(botoes1, fg="#1a1217", text="STO", width=5, font=("Arial", 4, "bold"))
    lblSTO.grid(column=1, row=8, padx=2, pady=2)

    lblSeta2 = Label(botoes1, fg="#1a1217", text="←", width=5, font=("Arial", 4, "bold"))
    lblSeta2.grid(column=2, row=8, padx=2, pady=2)

    lblX = Label(botoes1, fg="#1a1217", text="X", width=5, font=("Arial", 4, "bold"))
    lblX.grid(column=4, row=8, padx=2, pady=2)

    lblPontVir = Label(botoes1, fg="#1a1217", text="; Y", width=5, font=("Arial", 4, "bold"))
    lblPontVir.grid(column=5, row=8, padx=2, pady=2)

    lblM = Label(botoes1, fg="#1a1217", text="M- M", width=5, font=("Arial", 4, "bold"))
    lblM.grid(column=6, row=8, padx=2, pady=2)

    btnRCL = Button(botoes1, bg="#1a1217", fg="#fafafa", text="RCL", width=5, command=lambda: do_rcl(Calculo))
    btnRCL.grid(column=1, row=9, padx=2, pady=2)

    btnENG = Button(botoes1, bg="#1a1217", fg="#fafafa", text="ENG", width=5, command=lambda: wrapper_ENG(Calculo))
    btnENG.grid(column=2, row=9, padx=2, pady=2)

    btnP1 = Button(botoes1, bg="#1a1217", fg="#fafafa", text="(", width=5, command=lambda: add_values("(", Calculo))
    btnP1.grid(column=3, row=9, padx=2, pady=2)

    btnP2 = Button(botoes1, bg="#1a1217", fg="#fafafa", text=")", width=5, command=lambda: wrapper_twoPoints(Calculo))
    btnP2.grid(column=4, row=9, padx=2, pady=2)

    btnVirgula = Button(botoes1, bg="#1a1217", fg="#fafafa", text=":", width=5, command=lambda: add_values(":", Calculo))
    btnVirgula.grid(column=5, row=9, padx=2, pady=2)

    btnMmais = Button(botoes1, bg="#1a1217", fg="#fafafa", text="M+", width=5, command=lambda: do_sto(Calculo))
    btnMmais.grid(column=6, row=9, padx=2, pady=2)

    # linha n6
    lblIns = Label(botoes2, fg="#1a1217", text="INS", width=5, font=("Arial", 4, "bold"))
    lblIns.grid(column=4, row=10, padx=2, pady=2)

    lblOFF = Label(botoes2, fg="#1a1217", text="OFF", width=5, font=("Arial", 4, "bold"))
    lblOFF.grid(column=5, row=10, padx=2, pady=2)

    btnSete = Button(botoes2, bg="#1a1217", fg="#fafafa", text="7", width=6, command=lambda: add_values("7", Calculo))
    btnSete.grid(column=1, row=11, padx=2, pady=2, sticky=EW)

    btnOito = Button(botoes2, bg="#1a1217", fg="#fafafa", text="8", width=6, command=lambda: add_values("8", Calculo))
    btnOito.grid(column=2, row=11, padx=2, pady=2, sticky=EW)

    btnNove = Button(botoes2, bg="#1a1217", fg="#fafafa", text="9", width=6, command=lambda: add_values("9", Calculo))
    btnNove.grid(column=3, row=11, padx=2, pady=2, sticky=EW)

    btnDEL = Button(botoes2, bg="#c40202", fg="#fafafa", text="DEL", width=6, command=lambda: clearone(Calculo))
    btnDEL.grid(column=4, row=11, padx=2, pady=2)

    btnAC = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="AC", width=6, command=lambda: this_clearall(Calculo))
    btnAC.grid(column=5, row=11, padx=2, pady=2)

    # linha n7
    btnQuatro = Button(botoes2, bg="#1a1217", fg="#fafafa", text="4", width=6, command=lambda: add_values("4", Calculo))
    btnQuatro.grid(column=1, row=13, padx=2, pady=2)

    btnCinco = Button(botoes2, bg="#1a1217", fg="#fafafa", text="5", width=6, command=lambda: add_values("5", Calculo))
    btnCinco.grid(column=2, row=13, padx=2, pady=2)

    btnSeis = Button(botoes2, bg="#1a1217", fg="#fafafa", text="6", width=6, command=lambda: add_values("6", Calculo))
    btnSeis.grid(column=3, row=13, padx=2, pady=2)

    btnX = Button(botoes2, bg="#c40202", fg="#fafafa", text="×", width=6, command=lambda: add_signal("*", Calculo))
    btnX.grid(column=4, row=13, padx=2, pady=2)

    btnDivisao = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="÷", width=6, command=lambda: add_signal("/", Calculo))
    btnDivisao.grid(column=5, row=13, padx=2, pady=2)

    # linha n8
    btnUm = Button(botoes2, bg="#1a1217", fg="#fafafa", text="1", width=6, command=lambda: add_values("1", Calculo))
    btnUm.grid(column=1, row=15, padx=2, pady=2)

    btnDois = Button(botoes2, bg="#1a1217", fg="#fafafa", text="2", width=6, command=lambda: add_values("2", Calculo))
    btnDois.grid(column=2, row=15, padx=2, pady=2)

    btnTres = Button(botoes2, bg="#1a1217", fg="#fafafa", text="3", width=6, command=lambda: add_values("3", Calculo))
    btnTres.grid(column=3, row=15, padx=2, pady=2)

    btnMais = Button(botoes2, bg="#c40202", fg="#fafafa", text="+", width=6, command=lambda: add_signal("+", Calculo))
    btnMais.grid(column=4, row=15, padx=2, pady=2)

    btnMenos = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="-", width=6, command=lambda: add_signal("-", Calculo))
    btnMenos.grid(column=5, row=15, padx=2, pady=2)

    # linha n9
    btnRND = Button(botoes2, fg="#1a1217", text="RND", width=5, font=("Arial", 4, "bold"), command=lambda: wrapper_rnd(Calculo))
    btnRND.grid(column=1, row=16, padx=2, pady=2)

    lblRan = Label(botoes2, fg="#1a1217", text="Ran#", width=5, font=("Arial", 4, "bold"))
    lblRan.grid(column=2, row=16, padx=2, pady=2)

    lblPI = Label(botoes2, fg="#1a1217", text="π", width=5, font=("Arial", 4, "bold"))
    lblPI.grid(column=3, row=16, padx=2, pady=2)

    lblDRG = Label(botoes2, fg="#1a1217", text="DRG", width=5, font=("Arial", 4, "bold"))
    lblDRG.grid(column=4, row=16, padx=2, pady=2)

    lblPorcentagem = Label(botoes2, fg="#1a1217", text="%", width=5, font=("Arial", 4, "bold"))
    lblPorcentagem.grid(column=5, row=16, padx=2, pady=2)

    btnZero = Button(botoes2, bg="#1a1217", fg="#fafafa", text="0", width=6, command=lambda: add_values("0", Calculo))
    btnZero.grid(column=1, row=17, padx=2, pady=2)

    btnPonto = Button(botoes2, bg="#1a1217", fg="#fafafa", text="•", width=6, command=lambda: add_values(".", Calculo))
    btnPonto.grid(column=2, row=17, padx=2, pady=2)

    btnEXP = Button(botoes2, bg="#1a1217", fg="#fafafa", text="EXP", width=6, command=lambda: add_values("e", Calculo))
    btnEXP.grid(column=3, row=17, padx=2, pady=2)

    btnAns = Button(botoes2, bg="#1a1217", fg="#fafafa", text="Ans", width=6, command=lambda: add_values("Ans", Calculo))
    btnAns.grid(column=4, row=17, padx=2, pady=2)

    btnIgual = Button(botoes2, fg="#FAFAFA", bg="#c40202", text="=", width=6, command=lambda: add_signal("=", Calculo))
    btnIgual.grid(column=5, row=17, padx=2, pady=2)

    return calculator

if __name__ == "__main__":
    interface().mainloop()
