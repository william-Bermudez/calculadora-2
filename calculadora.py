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
        self.root.title("Calculadora de Cálculo")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        # Variable simbólica
        self.x = symbols('x')
        self.funcion_actual = None
        
        # Estilo
        self.configurar_estilo()
        
        # Frame principal
        self.crear_interfaz()
        
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff', 
                       font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), 
                       background='#4a90e2', foreground='#ffffff')
        style.map('TButton', background=[('active', '#357abd')])
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                       foreground='#4a90e2')
        
    def crear_interfaz(self):
        # Frame superior - Entrada de función
        frame_entrada = ttk.Frame(self.root, padding="10")
        frame_entrada.pack(fill=tk.X)
        
        ttk.Label(frame_entrada, text="Calculadora de Cálculo", 
                 style='Title.TLabel').pack()
        
        ttk.Label(frame_entrada, text="Ingresa tu función (usa x, pi, E, sqrt, sin, cos, tan, exp, log):").pack(pady=5)
        
        # Frame para entrada y botón
        frame_input = ttk.Frame(frame_entrada)
        frame_input.pack(fill=tk.X, pady=5)
        
        self.entry_funcion = ttk.Entry(frame_input, font=('Courier', 12), width=50)
        self.entry_funcion.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.entry_funcion.insert(0, "x**2 + 3*x + 2")
        
        ttk.Button(frame_input, text="Cargar Función", 
                  command=self.cargar_funcion).pack(side=tk.LEFT, padx=5)
        
        # Función cargada
        self.label_funcion = ttk.Label(frame_entrada, text="Función actual: No cargada", 
                                       font=('Courier', 11))
        self.label_funcion.pack(pady=5)
        
        # Frame de operaciones
        frame_ops = ttk.Frame(self.root)
        frame_ops.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Botones
        frame_botones = ttk.Frame(frame_ops, width=250)
        frame_botones.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Label(frame_botones, text="Operaciones:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        botones = [
            ("📊 Derivada Indefinida", self.derivada_indefinida),
            ("📍 Derivada en un Punto", self.derivada_definida),
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
            
        # Panel derecho - Resultados
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
        
    def cargar_funcion(self):
        expr_str = self.entry_funcion.get().strip()
        
        if not expr_str:
            messagebox.showwarning("Advertencia", "Por favor ingresa una función")
            return
        
        try:
            # Transformaciones para hacer el parsing más flexible
            transformations = (standard_transformations + 
                             (implicit_multiplication_application,))
            
            # Reemplazos comunes
            expr_str = expr_str.replace('^', '**')
            expr_str = expr_str.replace('√', 'sqrt')
            
            self.funcion_actual = parse_expr(expr_str, 
                                            transformations=transformations,
                                            local_dict={'x': self.x})
            
            # Mostrar función cargada
            funcion_latex = sp.latex(self.funcion_actual)
            self.label_funcion.config(text=f"f(x) = {self.funcion_actual}")
            
            self.agregar_resultado(f"\n{'='*60}\nFUNCIÓN CARGADA:\n{'='*60}")
            self.agregar_resultado(f"f(x) = {self.funcion_actual}\n")
            
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
            # Intentar convertir a fracción racional
            valor_racional = sp.nsimplify(valor)
            
            # Si es un número racional, mostrarlo como fracción
            if valor_racional.is_Rational and not valor_racional.is_Integer:
                numerador = valor_racional.p
                denominador = valor_racional.q
                valor_numerico = float(valor.evalf())
                return f"{numerador}/{denominador} ≈ {valor_numerico:.2f}"
            # Si es entero
            elif valor_racional.is_Integer:
                return f"{valor_racional}"
            # Si tiene forma simbólica
            elif valor.has(sp.pi, sp.E, sp.I) or not valor.is_number:
                try:
                    valor_numerico = float(valor.evalf())
                    return f"{valor} ≈ {valor_numerico:.2f}"
                except:
                    return f"{valor}"
            # Número decimal normal - intentar convertir a fracción
            else:
                try:
                    # Intentar expresar como fracción
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
    
    def derivada_indefinida(self):
        if not self.verificar_funcion():
            return
        
        try:
            derivada = diff(self.funcion_actual, self.x)
            
            self.agregar_resultado(f"\n{'='*60}\nDERIVADA INDEFINIDA:\n{'='*60}")
            self.agregar_resultado(f"f(x)  = {self.funcion_actual}")
            self.agregar_resultado(f"f'(x) = {derivada}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular derivada:\n{str(e)}")
    
    def derivada_definida(self):
        if not self.verificar_funcion():
            return
        
        # Ventana para pedir el punto
        ventana = tk.Toplevel(self.root)
        ventana.title("Derivada en un Punto")
        ventana.geometry("300x150")
        ventana.configure(bg='#2b2b2b')
        
        ttk.Label(ventana, text="Evaluar derivada en x =").pack(pady=10)
        entry_punto = ttk.Entry(ventana, font=('Courier', 12))
        entry_punto.pack(pady=5)
        entry_punto.insert(0, "0")
        
        def calcular():
            try:
                punto = float(entry_punto.get())
                derivada = diff(self.funcion_actual, self.x)
                valor = derivada.subs(self.x, punto)
                
                self.agregar_resultado(f"\n{'='*60}\nDERIVADA EN UN PUNTO:\n{'='*60}")
                self.agregar_resultado(f"f(x)  = {self.funcion_actual}")
                self.agregar_resultado(f"f'(x) = {derivada}")
                self.agregar_resultado(f"f'({punto}) = {self.formato_resultado(valor)}\n")
                
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")
        
        ttk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
    
    def integral_indefinida(self):
        if not self.verificar_funcion():
            return
        
        try:
            integral = integrate(self.funcion_actual, self.x)
            
            self.agregar_resultado(f"\n{'='*60}\nINTEGRAL INDEFINIDA:\n{'='*60}")
            self.agregar_resultado(f"f(x) = {self.funcion_actual}")
            self.agregar_resultado(f"∫ f(x) dx = {integral} + C\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular integral:\n{str(e)}")
    
    def integral_definida(self):
        if not self.verificar_funcion():
            return
        
        # Ventana para límites
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
        
        # Información
        info_label = ttk.Label(ventana, text="⚠️ Asegúrate que a < b para resultado positivo", 
                              font=('Arial', 8), foreground='#ffa500')
        info_label.pack(pady=2)
        
        def calcular():
            try:
                a_str = entry_a.get()
                b_str = entry_b.get()
                
                # Convertir a números exactos cuando sea posible
                try:
                    a = sp.sympify(a_str)
                except:
                    a = float(a_str)
                
                try:
                    b = sp.sympify(b_str)
                except:
                    b = float(b_str)
                
                # Calcular integral - IMPORTANTE: límite inferior primero, superior segundo
                integral = integrate(self.funcion_actual, (self.x, a, b))
                
                self.agregar_resultado(f"\n{'='*60}\nINTEGRAL DEFINIDA:\n{'='*60}")
                self.agregar_resultado(f"f(x) = {self.funcion_actual}")
                self.agregar_resultado(f"∫[{a}, {b}] f(x) dx = {self.formato_resultado(integral)}")
                
                # Advertencia si los límites están invertidos
                if float(a) > float(b):
                    self.agregar_resultado(f"⚠️  NOTA: a > b, por lo que el resultado es negativo")
                    self.agregar_resultado(f"    Si invertimos los límites: ∫[{b}, {a}] f(x) dx = {self.formato_resultado(-integral)}")
                
                self.agregar_resultado("")
                
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")
        
        ttk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
    
    def calcular_limite(self):
        if not self.verificar_funcion():
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Calcular Límite")
        ventana.geometry("300x200")
        ventana.configure(bg='#2b2b2b')
        
        ttk.Label(ventana, text="x tiende a:").pack(pady=5)
        entry_punto = ttk.Entry(ventana, font=('Courier', 12))
        entry_punto.pack(pady=5)
        entry_punto.insert(0, "0")
        
        ttk.Label(ventana, text="Dirección:").pack(pady=5)
        direccion = ttk.Combobox(ventana, values=["bilateral", "+", "-"], state="readonly")
        direccion.set("bilateral")
        direccion.pack(pady=5)
        
        def calcular():
            try:
                punto_str = entry_punto.get()
                dir_val = direccion.get()
                
                # Convertir punto
                if punto_str.lower() in ['inf', 'infinito', 'oo']:
                    punto = sp.oo
                elif punto_str.lower() in ['-inf', '-infinito', '-oo']:
                    punto = -sp.oo
                else:
                    punto = float(punto_str)
                
                # Calcular límite
                if dir_val == "bilateral":
                    lim = limit(self.funcion_actual, self.x, punto)
                else:
                    lim = limit(self.funcion_actual, self.x, punto, dir_val)
                
                self.agregar_resultado(f"\n{'='*60}\nLÍMITE:\n{'='*60}")
                self.agregar_resultado(f"f(x) = {self.funcion_actual}")
                self.agregar_resultado(f"lim (x → {punto}) f(x) = {lim}\n")
                
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")
        
        ttk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
    
    def serie_taylor(self):
        if not self.verificar_funcion():
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Serie de Taylor")
        ventana.geometry("300x200")
        ventana.configure(bg='#2b2b2b')
        
        ttk.Label(ventana, text="Punto de expansión (a):").pack(pady=5)
        entry_punto = ttk.Entry(ventana, font=('Courier', 12))
        entry_punto.pack(pady=5)
        entry_punto.insert(0, "0")
        
        ttk.Label(ventana, text="Orden (n):").pack(pady=5)
        entry_orden = ttk.Entry(ventana, font=('Courier', 12))
        entry_orden.pack(pady=5)
        entry_orden.insert(0, "4")
        
        def calcular():
            try:
                punto = float(entry_punto.get())
                orden = int(entry_orden.get())
                
                serie = series(self.funcion_actual, self.x, punto, n=orden+1).removeO()
                
                self.agregar_resultado(f"\n{'='*60}\nSERIE DE TAYLOR:\n{'='*60}")
                self.agregar_resultado(f"f(x) = {self.funcion_actual}")
                self.agregar_resultado(f"Expansión alrededor de x = {punto} (orden {orden}):")
                self.agregar_resultado(f"T_{orden}(x) = {serie}\n")
                
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")
        
        ttk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
    
    def simplificar_funcion(self):
        if not self.verificar_funcion():
            return
        
        try:
            simplificada = simplify(self.funcion_actual)
            
            self.agregar_resultado(f"\n{'='*60}\nSIMPLIFICACIÓN:\n{'='*60}")
            self.agregar_resultado(f"Original:     {self.funcion_actual}")
            self.agregar_resultado(f"Simplificada: {simplificada}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{str(e)}")
    
    def resolver_ecuacion(self):
        if not self.verificar_funcion():
            return
        
        try:
            soluciones = solve(self.funcion_actual, self.x)
            
            self.agregar_resultado(f"\n{'='*60}\nRESOLVER f(x) = 0:\n{'='*60}")
            self.agregar_resultado(f"f(x) = {self.funcion_actual}")
            
            if soluciones:
                self.agregar_resultado(f"Soluciones encontradas: {len(soluciones)}")
                for i, sol in enumerate(soluciones, 1):
                    self.agregar_resultado(f"x_{i} = {self.formato_resultado(sol)}")
            else:
                self.agregar_resultado("No se encontraron soluciones reales")
            
            self.agregar_resultado("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{str(e)}")
    
    def graficar_funcion(self):
        if not self.verificar_funcion():
            return
        
        try:
            # Crear ventana de gráfica
            ventana = tk.Toplevel(self.root)
            ventana.title("Gráfica de la Función")
            ventana.geometry("800x600")
            
            # Convertir a función numérica
            f_lambdified = sp.lambdify(self.x, self.funcion_actual, 'numpy')
            
            # Valores de x
            x_vals = np.linspace(-10, 10, 1000)
            
            try:
                y_vals = f_lambdified(x_vals)
            except:
                x_vals = np.linspace(-5, 5, 1000)
                y_vals = f_lambdified(x_vals)
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {self.funcion_actual}')
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('f(x)', fontsize=12)
            ax.set_title(f'Gráfica de f(x) = {self.funcion_actual}', fontsize=14)
            
            # Integrar en ventana
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