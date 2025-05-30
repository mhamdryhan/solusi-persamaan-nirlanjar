import math
import tkinter as tk
from tkinter import messagebox # Hanya messagebox yang dibutuhkan, ttk tidak lagi

# --- Fungsi Pembantu untuk Membuat Fungsi Matematika dari String ---

def create_function(func_str):
    def f(x):
        try:
            return eval(func_str, {"x": x, "math": math})
        except (SyntaxError, NameError) as e:
            raise ValueError(f"Fungsi f(x) tidak valid: {e}")
        except Exception as e:
            raise ValueError(f"Error saat mengevaluasi f(x) pada x={x}: {e}")
    return f

def create_derivative(func_str):
    def df(x):
        h = 1e-6 # Langkah kecil untuk turunan numerik
        try:
            fx_plus_h = eval(func_str, {"x": x + h, "math": math})
            fx = eval(func_str, {"x": x, "math": math})
            return (fx_plus_h - fx) / h
        except (SyntaxError, NameError) as e:
            raise ValueError(f"Fungsi turunan tidak valid: {e}")
        except Exception as e:
            raise ValueError(f"Error saat mengevaluasi turunan f(x) pada x={x}: {e}")
    return df

# --- Implementasi Metode Numerik untuk Mencari Akar (tanpa data iterasi dikembalikan) ---

def bisection(f, a, b, tol, max_iter=100): # tol diterima sebagai argumen
    try:
        if f(a) * f(b) >= 0:
            return None, "f(a) dan f(b) harus memiliki tanda yang berlawanan."
        
        for i in range(max_iter):
            c = (a + b) / 2
            error_val = abs(f(c))
            
            if error_val < tol:
                return c, f"Berhasil (iterasi {i+1})"
            
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return c, f"Peringatan: Maksimum iterasi ({max_iter}) tercapai."
    except ValueError as e:
        return None, f"Kesalahan internal dalam metode: {e}"

def regula_falsi(f, a, b, tol, max_iter=100): # tol diterima
    try:
        if f(a) * f(b) >= 0:
            return None, "f(a) dan f(b) harus memiliki tanda yang berlawanan."

        for i in range(max_iter):
            denominator = f(a) - f(b)
            if abs(denominator) < 1e-12:
                return None, f"Pembagian nol atau sangat kecil pada iterasi {i+1} (f(a) ~ f(b))."
            c = b - (f(b) * (a - b)) / denominator
            
            error_val = abs(f(c))

            if error_val < tol:
                return c, f"Berhasil (iterasi {i+1})"
            
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return c, f"Peringatan: Maksimum iterasi ({max_iter}) tercapai."
    except ValueError as e:
        return None, f"Kesalahan internal dalam metode: {e}"

def newton_raphson(f, df, x0, tol, max_iter=100): # tol diterima
    try:
        for i in range(max_iter):
            dfx = df(x0)
            if abs(dfx) < 1e-12:
                return None, f"Turunan nol atau sangat kecil di x={x0} pada iterasi {i+1}."
            x1 = x0 - f(x0) / dfx
            error_val = abs(x1 - x0)
            
            if error_val < tol:
                return x1, f"Berhasil (iterasi {i+1})"
            x0 = x1
        return x0, f"Peringatan: Maksimum iterasi ({max_iter}) tercapai."
    except ValueError as e:
        return None, f"Kesalahan internal dalam metode: {e}"

def secant(f, x0, x1, tol, max_iter=100): # tol diterima
    try:
        if abs(f(x1) - f(x0)) < 1e-12:
            return None, f"Pembagian nol atau sangat kecil (f(x1) ~ f(x0)) pada awal."
        
        for i in range(max_iter): 
            denominator = f(x1) - f(x0)
            if abs(denominator) < 1e-12:
                return None, f"Pembagian nol atau sangat kecil pada iterasi {i+1} (f(x1) ~ f(x0))."
            x2 = x1 - f(x1) * (x1 - x0) / denominator
            error_val = abs(x2 - x1)
            
            if error_val < tol:
                return x2, f"Berhasil (iterasi {i+1})"
            x0, x1 = x1, x2
        return x2, f"Peringatan: Maksimum iterasi ({max_iter}) tercapai."
    except ValueError as e:
        return None, f"Kesalahan internal dalam metode: {e}"

def fixed_point(g, x0, tol, max_iter=100): # tol diterima
    try:
        for i in range(max_iter):
            x1 = g(x0)
            error_val = abs(x1 - x0)
            
            if error_val < tol:
                return x1, f"Berhasil (iterasi {i+1})"
            x0 = x1
        return x0, f"Peringatan: Maksimum iterasi ({max_iter}) tercapai."
    except ValueError as e:
        return None, f"Kesalahan internal dalam metode: {e}"

# --- Aplikasi GUI (menggunakan Tkinter) ---

class KalkulatorAkarApp:
    def __init__(self, master):
        self.master = master
        master.title("Kalkulator Akar Numerik")
        master.geometry("550x450") # Ukuran jendela kembali lebih kecil
        master.resizable(False, False)

        # Variabel untuk menyimpan input
        self.func_str_var = tk.StringVar(master)
        self.epsilon_var = tk.StringVar(master)
        self.a_var = tk.StringVar(master)
        self.b_var = tk.StringVar(master)
        self.x0_var = tk.StringVar(master)
        self.x1_var = tk.StringVar(master)
        self.g_str_var = tk.StringVar(master)
        self.method_var = tk.StringVar(master)
        self.method_var.set("Bisection") # Nilai default

        # --- Bagian Input Fungsi ---
        func_frame = tk.LabelFrame(master, text="Definisi Fungsi f(x)", padx=10, pady=5)
        func_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(func_frame, text="f(x) = ").pack(side="left", padx=(5,0))
        tk.Entry(func_frame, textvariable=self.func_str_var, width=50).pack(side="left", fill="x", expand=True, padx=5)
        self.func_str_var.set("math.exp(x) - 5*x**2") # Contoh default

        # --- Bagian Pilihan Metode ---
        method_frame = tk.LabelFrame(master, text="Pilih Metode", padx=10, pady=5)
        method_frame.pack(pady=5, padx=10, fill="x")
        
        methods = [
            ("Metode Bagi Dua", "Bisection"),
            ("Metode Regula Falsi", "Regula Falsi"),
            ("Metode Iterasi Titik Tetap", "Fixed-Point Iteration"),
            ("Metode Newton-Raphson", "Newton-Raphson"),
            ("Metode Secant", "Secant")
        ]
        
        row, col = 0, 0
        for text, value in methods:
            rb = tk.Radiobutton(method_frame, text=text, variable=self.method_var, value=value, command=self._update_inputs)
            rb.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            col += 1
            if col > 1:
                col = 0
                row += 1
        method_frame.grid_columnconfigure(0, weight=1)
        method_frame.grid_columnconfigure(1, weight=1)

        # --- Bagian Parameter Input (dinamis dan epsilon) ---
        self.param_frame = tk.LabelFrame(master, text="Parameter Input", padx=10, pady=5)
        self.param_frame.pack(pady=5, padx=10, fill="x")
        
        # Input Epsilon (selalu terlihat)
        epsilon_input_frame = tk.Frame(self.param_frame)
        epsilon_input_frame.pack(fill="x", padx=5, pady=2)
        tk.Label(epsilon_input_frame, text="Toleransi (epsilon):", width=20, anchor="w").pack(side="left")
        tk.Entry(epsilon_input_frame, textvariable=self.epsilon_var, width=30).pack(side="left", fill="x", expand=True)
        self.epsilon_var.set("0.000001") # Default epsilon

        self.labels_entries = {} # Untuk menyimpan referensi label dan entry parameter spesifik metode

        # --- Bagian Tombol Hitung ---
        tk.Button(master, text="Hitung Akar", command=self.calculate_root, height=2, width=15, font=('Arial', 10, 'bold')).pack(pady=15)

        # --- Bagian Area Hasil Ringkasan ---
        # Tidak ada lagi tabel, hanya label ringkasan
        self.summary_result_label = tk.Label(master, text="Hasil ringkasan akan ditampilkan di sini.", wraplength=500, justify="left", fg="blue", font=('Arial', 10))
        self.summary_result_label.pack(pady=10, padx=10, fill="both", expand=True)

        # Panggil _update_inputs untuk inisialisasi awal
        self._update_inputs()

    def _clear_param_inputs(self):
        """Menghapus semua widget input parameter spesifik metode yang ada."""
        for widget in self.param_frame.winfo_children():
            # Jangan hapus input epsilon frame
            if widget != self.param_frame.winfo_children()[0]:
                widget.destroy()
        self.labels_entries.clear()

    def _add_param_input(self, label_text, var_obj, default_value=""):
        """Menambahkan satu baris input parameter spesifik metode (Label + Entry)."""
        frame = tk.Frame(self.param_frame)
        frame.pack(fill="x", padx=5, pady=2)
        label = tk.Label(frame, text=label_text, width=20, anchor="w")
        label.pack(side="left")
        entry = tk.Entry(frame, textvariable=var_obj, width=30)
        entry.pack(side="left", fill="x", expand=True)
        var_obj.set(default_value)
        self.labels_entries[label_text] = (label, entry)

    def _update_inputs(self):
        """Memperbarui input parameter spesifik metode berdasarkan metode yang dipilih."""
        self._clear_param_inputs()

        selected_method = self.method_var.get()

        if selected_method in ["Bisection", "Regula Falsi"]:
            self._add_param_input("Nilai a (batas bawah):", self.a_var, "0")
            self._add_param_input("Nilai b (batas atas):", self.b_var, "1")
        elif selected_method == "Fixed-Point Iteration":
            self._add_param_input("Fungsi g(x):", self.g_str_var, "(x + 2)**(1/3)")
            self._add_param_input("Nilai awal x0:", self.x0_var, "1.5")
        elif selected_method == "Newton-Raphson":
            self._add_param_input("Nilai awal x0:", self.x0_var, "0.5")
        elif selected_method == "Secant":
            self._add_param_input("Nilai awal x0:", self.x0_var, "0.5")
            self._add_param_input("Nilai awal x1:", self.x1_var, "1")
        
        self.summary_result_label.config(text="Silakan masukkan parameter dan klik 'Hitung Akar'.", fg="blue")


    def calculate_root(self):
        self.summary_result_label.config(fg="blue", text="Menghitung...") # Pesan saat mulai menghitung

        try:
            func_str = self.func_str_var.get()
            if not func_str:
                raise ValueError("Fungsi f(x) tidak boleh kosong.")
            f = create_function(func_str)
            df = create_derivative(func_str)

            tol = float(self.epsilon_var.get())
            max_iterations = 100 

            method = self.method_var.get()
            root = None
            message = "Terjadi kesalahan yang tidak diketahui."
            
            # Panggil metode yang sesuai, kini tanpa mengembalikan data iterasi
            if method == "Bisection":
                a = float(self.a_var.get())
                b = float(self.b_var.get())
                root, message = bisection(f, a, b, tol, max_iterations)
            elif method == "Regula Falsi":
                a = float(self.a_var.get())
                b = float(self.b_var.get())
                root, message = regula_falsi(f, a, b, tol, max_iterations)
            elif method == "Fixed-Point Iteration":
                g_str = self.g_str_var.get()
                if not g_str:
                    raise ValueError("Fungsi g(x) tidak boleh kosong.")
                g = create_function(g_str)
                x0 = float(self.x0_var.get())
                root, message = fixed_point(g, x0, tol, max_iterations)
            elif method == "Newton-Raphson":
                x0 = float(self.x0_var.get())
                root, message = newton_raphson(f, df, x0, tol, max_iterations)
            elif method == "Secant":
                x0 = float(self.x0_var.get())
                x1 = float(self.x1_var.get())
                root, message = secant(f, x0, x1, tol, max_iterations)
            
            # Tampilkan hasil di label ringkasan
            if root is not None:
                f_at_root = f(root)
                self.summary_result_label.config(text=f"Akar ditemukan: {root:.6f}\nNilai f({root:.6f}): {f_at_root:.6e}\nStatus: {message}", fg="green")
            else:
                self.summary_result_label.config(text=f"Akar tidak ditemukan.\nStatus: {message}", fg="red")

        except ValueError as ve:
            self.summary_result_label.config(text=f"Error Input/Fungsi: {ve}\nHarap periksa format input atau fungsi Anda.", fg="red")
            messagebox.showerror("Error Input/Fungsi", str(ve))
        except Exception as e:
            self.summary_result_label.config(text=f"Terjadi kesalahan tak terduga: {e}", fg="red")
            messagebox.showerror("Error", f"Terjadi kesalahan tak terduga:\n{e}")


# --- Bagian Eksekusi Utama Aplikasi ---
if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorAkarApp(root)
    root.mainloop()