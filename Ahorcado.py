import tkinter as tk
from tkinter import messagebox
import random
import sys

class AhorcadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado")
        
        self.intentos_restantes = 3
        self.letras_adivinadas = set()
        
        # Cargar palabras y seleccionar una
        self.palabras = self.cargar_palabras("palabras.txt")
        if not self.palabras:
            self.mostrar_error("El archivo 'palabras.txt' está vacío o no se pudo cargar.")
            self.root.quit()
        self.palabra_seleccionada = self.seleccionar_palabra()
        
        # Crear widgets
        self.progreso_label = tk.Label(root, text=self.mostrar_progreso())
        self.progreso_label.pack()
        
        self.intentos_label = tk.Label(root, text=f"Intentos restantes: {self.intentos_restantes}")
        self.intentos_label.pack()
        
        self.entrada_letra = tk.Entry(root)
        self.entrada_letra.pack()
        
        self.adivinaciones = tk.Button(root, text="Adivinar letra", command=self.adivinar_letra)
        self.adivinaciones.pack()
        
    def cargar_palabras(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                palabras = [line.strip() for line in file.readlines()]
            return palabras
        except FileNotFoundError:
            self.mostrar_error(f"ERROR: El archivo '{filename}' no se encontró.")
            sys.exit(1)
        except UnicodeDecodeError:
            self.mostrar_error(f"ERROR: No se pudo decodificar el archivo '{filename}'. Asegúrate de que esté en UTF-8.")
            sys.exit(1)

    def seleccionar_palabra(self):
        return random.choice(self.palabras)

    def mostrar_progreso(self):
        progreso = ''.join([letra if letra in self.letras_adivinadas else '_' for letra in self.palabra_seleccionada])
        return progreso

    def adivinar_letra(self):
        letra = self.entrada_letra.get().lower()
        if len(letra) != 1 or not letra.isalpha():
            self.mostrar_error("ERROR: Debes ingresar solo una letra.")
            return
        
        if letra in self.palabra_seleccionada:
            self.letras_adivinadas.add(letra)
            if all(letra in self.letras_adivinadas for letra in self.palabra_seleccionada):
                self.mostrar_mensaje("¡Felicidades! Has adivinado la palabra: " + self.palabra_seleccionada)
                self.root.quit()
        else:
            self.intentos_restantes -= 1
            if self.intentos_restantes <= 0:
                self.mostrar_mensaje("¡Game Over! Has agotado todos tus intentos. La palabra era: " + self.palabra_seleccionada)
                self.root.quit()
            else:
                self.intentos_label.config(text=f"Intentos restantes: {self.intentos_restantes}")
                self.mostrar_error(f"La letra '{letra}' no está en la palabra.")

        self.progreso_label.config(text=self.mostrar_progreso())
        self.entrada_letra.delete(0, tk.END)

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Información", mensaje)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AhorcadoApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
