#!/usr/bin/env python3

"""
Este modulo permite hacer calculos con notación RPN.
"""

import math
import sys


class RPNError(Exception):
    """
    Clase que contiene las excepciones relacionadas con RPN.
    """


def is_num(x):
    """
    Verifica si el parametro x es un numero valido
    """
    try:
        float(x)
        return True
    except Exception:
        return False


def deg(x):
    """
    Convierte grados a radianes
    """
    return math.radians(x)


def rad(x):
    """
    Convierte radianes a grados
    """
    return math.degrees(x)


def eval_rpn(expr):
    """
    Lee el string ingresado y hace el calculo
    """
    stack = []
    mem = [0.0] * 10

    def need(n):
        if len(stack) < n:
            raise RPNError("Pila insuficiente")

    tokens = expr.split()
    i = 0

    ops = {
        "+": lambda a,b: a+b,
        "-": lambda a,b: a-b,
        "*": lambda a,b: a*b,
        "/": lambda a,b: a/b if b != 0 else (_ for _ in ())
            .throw(RPNError("División por cero"))
    }

    def asin(x):
        if -1 <= x <= 1:
            return rad(math.asin(x))
        raise RPNError("fuera de dominio")

    def acos(x):
        if -1 <= x <= 1:
            return rad(math.acos(x))
        raise RPNError("fuera de dominio")

    trig = {
        "sin": lambda x: math.sin(deg(x)),
        "cos": lambda x: math.cos(deg(x)),
        "tg": lambda x: math.tan(deg(x)),
        "asin": lambda x: asin(x),
        "acos": lambda x: acos(x),
        "atg": lambda x: rad(math.atan(x)),
    }

    while i < len(tokens):
        t = tokens[i]

        if is_num(t):
            stack.append(float(t))

        elif t in ops:
            need(2)
            b, a = stack.pop(), stack.pop()
            stack.append(ops[t](a, b))

        elif t == "dup":
            need(1)
            stack.append(stack[-1])

        elif t == "swap":
            need(2)
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif t == "drop":
            need(1)
            stack.pop()

        elif t == "clear":
            stack.clear()

        elif t in ("p", "pi"):
            stack.append(math.pi)
        elif t == "e":
            stack.append(math.e)
        elif t == "j":
            stack.append((1 + 5**0.5) / 2)

        elif t == "chs":
            need(1)
            stack[-1] = -stack[-1]

        elif t == "sqrt":
            need(1)
            x = stack.pop()
            if x < 0:
                raise RPNError("Raíz de número negativo")
            stack.append(math.sqrt(x))

        elif t == "log":
            need(1)
            x = stack.pop()
            if x <= 0:
                raise RPNError("Logaritmo de número negativo")
            stack.append(math.log10(x))

        elif t == "ln":
            need(1)
            x = stack.pop()
            if x <= 0:
                raise RPNError("Logaritmo de número negativo")
            stack.append(math.log(x))

        elif t == "ex":
            need(1)
            stack.append(math.exp(stack.pop()))

        elif t == "10x":
            need(1)
            stack.append(10 ** stack.pop())

        elif t == "yx":
            need(2)
            b, a = stack.pop(), stack.pop()
            stack.append(a**b)

        elif t == "1/x":
            need(1)
            x = stack.pop()
            if x == 0:
                raise RPNError("División por cero")
            stack.append(1 / x)

        elif t in trig:
            need(1)
            x = stack.pop()
            stack.append(trig[t](x))

        elif t in ("sto", "rcl"):
            if i + 1 >= len(tokens):
                raise RPNError("Falta índice de memoria")

            idx = tokens[i + 1]
            if not idx.isdigit():
                raise RPNError("Índice de memoria inválido")

            idx = int(idx)
            if not 0 <= idx <= 9:
                raise RPNError("Memoria fuera de rango (00-09)")
            idx = int(idx)

            if t == "sto":
                need(1)
                mem[idx] = stack.pop()  # 🔥 FIX
            else:
                stack.append(mem[idx])

            i += 1

        else:
            raise RPNError(f"Token inválido: {t}")

        i += 1

    if len(stack) != 1:
        raise RPNError("La pila no terminó con un solo valor")

    return stack[0]


def main():
    """
    Busca el string en los argumentos o lo pide al usuario
    mediante input, luego llama a eval_rpn
    """
    try:
        expr = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("RPN> ")
        if not expr.strip():
            raise RPNError("Expresión vacía")
        print(eval_rpn(expr))
    except RPNError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
