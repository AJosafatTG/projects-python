import tkinter as tk
from tkinter import messagebox
import re
from sympy import symbols, Not, And, Or, Implies, Equivalent # type: ignore

sentencias_guardadas = {}

def limpiar_formula():
    entrada_formula.delete(0, tk.END)

def guardar_sentencias():
    for entrada, letra in zip([entrada_p, entrada_q, entrada_r, entrada_s], ['P', 'Q', 'R', 'S']):
        texto = entrada.get().strip().lower()
        texto = re.sub(r'[áéíóúü]', lambda m: {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}[m.group()], texto)
        if texto:
            sentencias_guardadas[texto] = letra

def evaluar_formula():
    guardar_sentencias()
    
    formula = entrada_formula.get().lower().strip()

    if not formula.startswith(" "):
        formula = " " + formula

    formula = re.sub(r'[^a-záéíóúüñ ]', '', formula)
    formula = re.sub(r'[áéíóúü]', lambda m: {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}[m.group()], formula)

    # Reemplazamos las sentencias simples por letras (P, Q, R, S) en la fórmula
    formula_wff = formula
    for texto, letra in sentencias_guardadas.items():
        formula_wff = re.sub(r'\b' + re.escape(texto) + r'\b', letra, formula_wff)

    # Convertimos las operaciones lógicas a su representación simbólica
    formula_wff = formula_wff.replace(" no ", " ¬")
    formula_wff = formula_wff.replace(" y ", " ∧ ")
    formula_wff = formula_wff.replace(" o ", " ∨ ")
    formula_wff = formula_wff.replace(" si ", "") 
    formula_wff = formula_wff.replace(" entonces ", " → ")
    formula_wff = formula_wff.replace(" igual a ", " ↔ ")

    wff.set(formula_wff)

def ejecutar_formula():
    try:
        valor_p = var_p.get()
        valor_q = var_q.get()
        valor_r = var_r.get()
        valor_s = var_s.get()

        formula_wff = wff.get().upper()
        formula_eval = formula_wff.replace('P', 'p')
        formula_eval = formula_eval.replace('Q', 'q')
        formula_eval = formula_eval.replace('R', 'r')
        formula_eval = formula_eval.replace('S', 's')

        formula_eval = formula_eval.replace('∧', '&')
        formula_eval = formula_eval.replace('∨', '|')
        formula_eval = formula_eval.replace('¬', '~')
        formula_eval = formula_eval.replace('→', '>>')
        formula_eval = formula_eval.replace('↔', '==')

        p, q, r, s = symbols('p q r s')
        expr = eval(formula_eval)

        # Asignar valores a las variables
        valores = {p: valor_p, q: valor_q, r: valor_r, s: valor_s}
        resultado = expr.subs(valores)

        # Registrar los pasos de la evaluación
        pasos = []
        pasos.append(f"Fórmula original: {formula_wff}")
        
        # Reemplazar las variables por sus valores en la fórmula evaluada
        formula_eval_valores = formula_eval.replace('p', 'V' if valor_p else 'F')
        formula_eval_valores = formula_eval_valores.replace('q', 'V' if valor_q else 'F')
        formula_eval_valores = formula_eval_valores.replace('r', 'V' if valor_r else 'F')
        formula_eval_valores = formula_eval_valores.replace('s', 'V' if valor_s else 'F')
        
        pasos.append(f"Fórmula evaluada: {formula_eval_valores}")
        pasos.append(f"Valores: P={'V' if valor_p else 'F'}, Q={'V' if valor_q else 'F'}, R={'V' if valor_r else 'F'}, S={'V' if valor_s else 'F'}")
        pasos.append(f"Resultado: {'V' if resultado else 'F'}")

        value.set("Verdadero" if resultado else "Falso")
        messagebox.showinfo("Pasos de Evaluación", "\n".join(pasos))
    except Exception as e:
        messagebox.showerror("Error", f"Error en la evaluación: {e}")

def terminar():
    entrada_p.delete(0, tk.END)
    entrada_q.delete(0, tk.END)
    entrada_r.delete(0, tk.END)
    entrada_s.delete(0, tk.END)
    limpiar_formula()
    wff.set("")
    value.set("")

def salir():
    ventana.quit()

ventana = tk.Tk()
ventana.title("Lógica Proposicional")

var_p = tk.BooleanVar()
var_q = tk.BooleanVar()
var_r = tk.BooleanVar()
var_s = tk.BooleanVar()
wff = tk.StringVar()
value = tk.StringVar()

tk.Label(ventana, text="Sentencia Simple 1 (P)").grid(row=0, column=0)
entrada_p = tk.Entry(ventana, width=30)
entrada_p.grid(row=0, column=1)
tk.Radiobutton(ventana, text="V", variable=var_p, value=True).grid(row=0, column=2)
tk.Radiobutton(ventana, text="F", variable=var_p, value=False).grid(row=0, column=3)

tk.Label(ventana, text="Sentencia Simple 2 (Q)").grid(row=1, column=0)
entrada_q = tk.Entry(ventana, width=30)
entrada_q.grid(row=1, column=1)
tk.Radiobutton(ventana, text="V", variable=var_q, value=True).grid(row=1, column=2)
tk.Radiobutton(ventana, text="F", variable=var_q, value=False).grid(row=1, column=3)

tk.Label(ventana, text="Sentencia Simple 3 (R)").grid(row=2, column=0)
entrada_r = tk.Entry(ventana, width=30)
entrada_r.grid(row=2, column=1)
tk.Radiobutton(ventana, text="V", variable=var_r, value=True).grid(row=2, column=2)
tk.Radiobutton(ventana, text="F", variable=var_r, value=False).grid(row=2, column=3)

tk.Label(ventana, text="Sentencia Simple 4 (S)").grid(row=3, column=0)
entrada_s = tk.Entry(ventana, width=30)
entrada_s.grid(row=3, column=1)
tk.Radiobutton(ventana, text="V", variable=var_s, value=True).grid(row=3, column=2)
tk.Radiobutton(ventana, text="F", variable=var_s, value=False).grid(row=3, column=3)

tk.Label(ventana, text="Fórmula WFF").grid(row=4, column=0)
entrada_formula = tk.Entry(ventana, width=40)
entrada_formula.grid(row=4, column=1, columnspan=3)

tk.Button(ventana, text="Limpiar", command=limpiar_formula).grid(row=5, column=0)
tk.Button(ventana, text="Evaluar", command=evaluar_formula).grid(row=5, column=1)
tk.Button(ventana, text="Ejecutar", command=ejecutar_formula).grid(row=5, column=2)
tk.Button(ventana, text="Terminar", command=terminar).grid(row=6, column=1)
tk.Button(ventana, text="Salir", command=salir).grid(row=6, column=2)

tk.Label(ventana, text="WFF Resultado:").grid(row=7, column=0)
tk.Label(ventana, textvariable=wff).grid(row=7, column=1, columnspan=3)

tk.Label(ventana, text="Resultado:").grid(row=8, column=0)
tk.Label(ventana, textvariable=value).grid(row=8, column=1, columnspan=3)

ventana.mainloop()
