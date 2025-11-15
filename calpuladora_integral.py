import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sympy as sp
from sympy import symbols, diff, integrate, limit, series, solve, simplify
from sympy import pi, E, sqrt, sin, cos, tan, exp, log, ln
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                         implicit_multiplication_application)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class CalculadoraCalculo:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Cálcul")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        
        self.x = symbols('x')
        self.y = symbols('y')
        self.u = symbols('u')
        self.t = symbols('t')
        self.variable_actual = self.x  
        self.funcion_actual = None
        
        
        self.configurar_estilo()
        
      
        self.crear_interfaz()
        
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff', 
                       font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), 
                       background='#4a90e2', foreground='#ffffff')
        style.map('TButton', background=[('active', '#357abd')])
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                       foreground='#4a90e2')
        
    def crear_interfaz(self):
       
        frame_entrada = ttk.Frame(self.root, padding="10")
        frame_entrada.pack(fill=tk.X)
        
        ttk.Label(frame_entrada, text="Calculadora de Cálcula", 
                 style='Title.TLabel').pack()
        
        ttk.Label(frame_entrada, text="Ingresa tu función (usa x, y, u, t, pi, sqrt, sin, cos, tan,):").pack(pady=5)
        
    
        frame_input = ttk.Frame(frame_entrada)
        frame_input.pack(fill=tk.X, pady=5)
        
        self.entry_funcion = ttk.Entry(frame_input, font=('Courier', 12), width=50)
        self.entry_funcion.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.entry_funcion.insert(0, "x**2 + 3*x + 2")
        
        ttk.Button(frame_input, text="Cargar Función", 
                  command=self.cargar_funcion).pack(side=tk.LEFT, padx=5)
        
      
        frame_var = ttk.Frame(frame_entrada)
        frame_var.pack(pady=5)
        
        ttk.Label(frame_var, text="Variable de integración:").pack(side=tk.LEFT, padx=5)
        self.combo_variable = ttk.Combobox(frame_var, values=["x", "y", "u", "t"], 
                                          state="readonly", width=5)
        self.combo_variable.set("x")
        self.combo_variable.pack(side=tk.LEFT, padx=5)
        self.combo_variable.bind("<<ComboboxSelected>>", self.cambiar_variable)
        
        
       
        self.label_funcion = ttk.Label(frame_entrada, text="Función actual: No cargada", 
                                       font=('Courier', 11))
        self.label_funcion.pack(pady=5)
        
        
        frame_ops = ttk.Frame(self.root)
        frame_ops.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
      
        frame_botones = ttk.Frame(frame_ops, width=250)
        frame_botones.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Label(frame_botones, text="Operaciones:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        botones = [
            ("∫ Integral Indefinida", self.integral_indefinida),
            ("∫ᵇₐ Integral Definida", self.integral_definida),
            ("📈 Graficar", self.graficar_funcion),
            ("🗑️ Limpiar Resultados", self.limpiar_resultados)
        ]
        
        for texto, comando in botones:
            btn = tk.Button(frame_botones, text=texto, command=comando,
                          bg='#4a90e2', fg='white', font=('Arial', 10, 'bold'),
                          relief=tk.RAISED, bd=2, cursor='hand2')
            btn.pack(fill=tk.X, pady=3, padx=5)
            
       
        frame_resultados = ttk.Frame(frame_ops)
        frame_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(frame_resultados, text="Resultados:", 
                 font=('Arial', 12, 'bold')).pack()
        
        self.text_resultados = scrolledtext.ScrolledText(frame_resultados, 
                                                         font=('Courier', 11),
                                                         bg='#1e1e1e', fg='#00ff00',
                                                         insertbackground='white',
                                                         wrap=tk.WORD)
        self.text_resultados.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def cambiar_variable(self, event=None):
        """Cambia la variable de integración"""
        var_seleccionada = self.combo_variable.get()
        
        if var_seleccionada == 'x':
            self.variable_actual = self.x
        elif var_seleccionada == 'y':
            self.variable_actual = self.y
        elif var_seleccionada == 'u':
            self.variable_actual = self.u
        elif var_seleccionada == 't':
            self.variable_actual = self.t
        
        
        if self.funcion_actual is not None:
            self.label_funcion.config(text=f"f({var_seleccionada}) = {self.funcion_actual}")
    
    def cargar_funcion(self):
        expr_str = self.entry_funcion.get().strip()
        
        if not expr_str:
            messagebox.showwarning("Advertencia", "Por favor ingresa una función")
            return
        
        try:
           
            transformations = (standard_transformations + 
                             (implicit_multiplication_application,))
            
        
            expr_str = expr_str.replace('^', '**')
            expr_str = expr_str.replace('√', 'sqrt')
            
           
            variables_dict = {
                'x': self.x, 
                'y': self.y, 
                'u': self.u, 
                't': self.t
            }
            
            self.funcion_actual = parse_expr(expr_str, 
                                            transformations=transformations,
                                            local_dict=variables_dict)
            vars_en_funcion = self.funcion_actual.free_symbols
            if self.y in vars_en_funcion:
                self.variable_actual = self.y
                self.combo_variable.set('y')
            elif self.u in vars_en_funcion:
                self.variable_actual = self.u
                self.combo_variable.set('u')
            elif self.t in vars_en_funcion:
                self.variable_actual = self.t
                self.combo_variable.set('t')
            else:
                self.variable_actual = self.x
                self.combo_variable.set('x')
            
           
            var_actual = self.combo_variable.get()
            self.label_funcion.config(text=f"f({var_actual}) = {self.funcion_actual}")
            
            self.agregar_resultado(f"\n{'='*60}\nFUNCIÓN CARGADA:\n{'='*60}")
            self.agregar_resultado(f"f({var_actual}) = {self.funcion_actual}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la función:\n{str(e)}\n\nAsegúrate de usar sintaxis correcta.")
    
    def verificar_funcion(self):
        if self.funcion_actual is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar una función")
            return False
        return True
    
    def agregar_resultado(self, texto):
        self.text_resultados.insert(tk.END, texto + "\n")
        self.text_resultados.see(tk.END)
    
    def formato_resultado(self, valor):
        """Formatea un resultado mostrando forma exacta y numérica"""
        try:
            
            valor_racional = sp.nsimplify(valor)
            
           
            if valor_racional.is_Rational and not valor_racional.is_Integer:
                numerador = valor_racional.p
                denominador = valor_racional.q
                valor_numerico = float(valor.evalf())
                return f"{numerador}/{denominador} ≈ {valor_numerico:.2f}"
            
            elif valor_racional.is_Integer:
                return f"{valor_racional}"
           
            elif valor.has(sp.pi, sp.E, sp.I) or not valor.is_number:
                try:
                    valor_numerico = float(valor.evalf())
                    return f"{valor} ≈ {valor_numerico:.2f}"
                except:
                    return f"{valor}"
            
            else:
                try:
                   
                    fraccion = sp.Rational(valor).limit_denominator(1000)
                    if abs(float(fraccion) - float(valor)) < 0.0001:
                        valor_numerico = float(valor.evalf())
                        return f"{fraccion} ≈ {valor_numerico:.2f}"
                    else:
                        valor_numerico = float(valor.evalf())
                        return f"{valor_numerico:.2f}"
                except:
                    valor_numerico = float(valor.evalf())
                    return f"{valor_numerico:.2f}"
        except:
            return f"{valor}"
    
    def integral_indefinida(self):
        if not self.verificar_funcion():
            return
        
        try:
            var_actual = self.combo_variable.get()
            integral = integrate(self.funcion_actual, self.variable_actual)
            
            
            integral_expandida = sp.expand(integral)
            
            self.agregar_resultado(f"\n{'='*60}\nINTEGRAL INDEFINIDA:\n{'='*60}")
            self.agregar_resultado(f"f({var_actual}) = {self.funcion_actual}")
            
           
            terminos = self.formatear_polinomio(integral_expandida, self.variable_actual)
            if terminos:
                self.agregar_resultado(f"\n∫ f({var_actual}) d{var_actual} = {terminos} + C\n")
            else:
                self.agregar_resultado(f"\n∫ f({var_actual}) d{var_actual} = {integral_expandida} + C\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular integral:\n{str(e)}")
    
    def formatear_polinomio(self, expr, variable):
        """Formatea un polinomio de forma ordenada y legible"""
        try:
           
            poli = sp.Poly(expr, variable)
            coeficientes = poli.all_coeffs()
            grado = poli.degree()
            
            
            var_str = str(variable)
            
            terminos = []
            for i, coef in enumerate(coeficientes):
                exponente = grado - i
                
                if coef == 0:
                    continue
                
               
                coef_racional = sp.nsimplify(coef)
                
                
                if exponente == 0:
                   
                    if coef_racional.is_Rational and not coef_racional.is_Integer:
                        terminos.append(f"{coef_racional.p}/{coef_racional.q}")
                    else:
                        terminos.append(str(coef_racional))
                elif exponente == 1:
                 
                    if coef_racional == 1:
                        terminos.append(var_str)
                    elif coef_racional == -1:
                        terminos.append(f"-{var_str}")
                    elif coef_racional.is_Rational and not coef_racional.is_Integer:
                        terminos.append(f"({coef_racional.p}/{coef_racional.q}){var_str}")
                    else:
                        terminos.append(f"{coef_racional}{var_str}")
                else:
                   
                    if coef_racional == 1:
                        terminos.append(f"{var_str}^{exponente}")
                    elif coef_racional == -1:
                        terminos.append(f"-{var_str}^{exponente}")
                    elif coef_racional.is_Rational and not coef_racional.is_Integer:
                        terminos.append(f"({coef_racional.p}/{coef_racional.q}){var_str}^{exponente}")
                    else:
                        terminos.append(f"{coef_racional}{var_str}^{exponente}")
            
          
            if not terminos:
                return None
            
            resultado = terminos[0]
            for termino in terminos[1:]:
                if termino.startswith('-'):
                    resultado += f" - {termino[1:]}"
                else:
                    resultado += f" + {termino}"
            
            return resultado
            
        except Exception as e:
          
            try:
                return self.formatear_expresion_general(expr)
            except:
                return None
    
    def formatear_expresion_general(self, expr):
        """Formatea expresiones no polinómicas"""
        try:
            
            expr_str = str(expr)
            
           
            expr_str = expr_str.replace('**', '^')
            
           
            terminos = expr_str.split(' + ')
            terminos_formateados = []
            
            for termino in terminos:
                
                if ' - ' in termino:
                    partes = termino.split(' - ')
                    terminos_formateados.append(partes[0])
                    for parte in partes[1:]:
                        terminos_formateados.append('-' + parte)
                else:
                    terminos_formateados.append(termino)
            
            resultado = terminos_formateados[0]
            for termino in terminos_formateados[1:]:
                if termino.startswith('-'):
                    resultado += f" - {termino[1:]}"
                else:
                    resultado += f" + {termino}"
            
            return resultado
        except:
            return None
    
    def integral_definida(self):
        if not self.verificar_funcion():
            return
        
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Integral Definida")
        ventana.geometry("350x250")
        ventana.configure(bg='#2b2b2b')
        
        ttk.Label(ventana, text="Límite inferior (a):").pack(pady=5)
        entry_a = ttk.Entry(ventana, font=('Courier', 12))
        entry_a.pack(pady=5)
        entry_a.insert(0, "0")
        entry_a.focus()
        
        ttk.Label(ventana, text="Límite superior (b):").pack(pady=5)
        entry_b = ttk.Entry(ventana, font=('Courier', 12))
        entry_b.pack(pady=5)
        entry_b.insert(0, "1")
        
        
        info_label = ttk.Label(ventana, text="⚠️ Asegúrate que a < b para resultado positivo", 
                              font=('Arial', 8), foreground='#ffa500')
        info_label.pack(pady=2)
        
        def calcular():
            try:
                a_str = entry_a.get()
                b_str = entry_b.get()
               
                try:
                    a = sp.sympify(a_str)
                except:
                    a = float(a_str)
                
                try:
                    b = sp.sympify(b_str)
                except:
                    b = float(b_str)
                
              
                integral = integrate(self.funcion_actual, (self.variable_actual, a, b))
                
                var_actual = self.combo_variable.get()
                self.agregar_resultado(f"\n{'='*60}\nINTEGRAL DEFINIDA:\n{'='*60}")
                self.agregar_resultado(f"f({var_actual}) = {self.funcion_actual}")
                self.agregar_resultado(f"∫[{a}, {b}] f({var_actual}) d{var_actual} = {self.formato_resultado(integral)}")
                
  
               
                self.agregar_resultado("")
                
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")
        
        ttk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
    
    def graficar_funcion(self):
        if not self.verificar_funcion():
            return
        
        try:
           
            ventana = tk.Toplevel(self.root)
            ventana.title("Gráfica de la Función")
            ventana.geometry("800x600")
            
         
            f_lambdified = sp.lambdify(self.x, self.funcion_actual, 'numpy')
            
          
            x_vals = np.linspace(-10, 10, 1000)
            
            try:
                y_vals = f_lambdified(x_vals)
            except:
                x_vals = np.linspace(-5, 5, 1000)
                y_vals = f_lambdified(x_vals)
            
          
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {self.funcion_actual}')
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('f(x)', fontsize=12)
            ax.set_title(f'Gráfica de f(x) = {self.funcion_actual}', fontsize=14)
            
         
            canvas = FigureCanvasTkAgg(fig, master=ventana)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar:\n{str(e)}")
    
    def limpiar_resultados(self):
        self.text_resultados.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCalculo(root)
    root.mainloop()