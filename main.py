import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PyPDF2 import PdfReader, PdfWriter

# ----------------------
# PDF Operations
# ----------------------
def inject_js(inPDF, outPDF, js_file_path):
    try:
        pdf = PdfReader(inPDF)
        writer = PdfWriter()
    except FileNotFoundError:
        messagebox.showerror("Error", f"PDF not found: {inPDF}")
        return

    try:
        with open(js_file_path, 'r') as f:
            js_code = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"JS file not found: {js_file_path}")
        return

    # Clean JS for PDF injection
    js_payload = re.sub(r'([a-zA-Z0-9_]+)\(', r'app.\1(', js_code)
    js_payload = re.sub(r'(\w+)\.app.(\w+)\(', r'app.\1.\2(', js_payload)

    writer.add_js(js_payload)
    for page in pdf.pages:
        writer.add_page(page)

    with open(outPDF, 'wb') as f:
        writer.write(f)

    messagebox.showinfo("Success", f"JS injected!\nSaved as: {outPDF}")

def check_js(inPDF):
    try:
        with open(inPDF, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"PDF not found: {inPDF}")
        return

    if b"/JavaScript" in content or b"/JS (" in content or b"/JS <" in content:
        messagebox.showwarning("Alert", "PDF contains JavaScript!")
    else:
        messagebox.showinfo("Clean", "No JavaScript detected.")

def clean_pdf(inPDF, outPDF):
    try:
        pdf = PdfReader(inPDF)
        writer = PdfWriter()
    except FileNotFoundError:
        messagebox.showerror("Error", f"PDF not found: {inPDF}")
        return

    for page in pdf.pages:
        writer.add_page(page)

    writer._root_object.update({"/Names": {}})  # Remove JS references

    with open(outPDF, "wb") as f:
        writer.write(f)

    messagebox.showinfo("Success", f"PDF cleaned!\nSaved as: {outPDF}")

# ----------------------
# GUI
# ----------------------
class PDFToolBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Tool Box v1.0")
        self.geometry("600x500")
        self.configure(bg="#1c1c1c")
        self.resizable(False, False)

        # Matte glass panel
        self.panel = tk.Frame(self, bg="#2a2a2a", bd=2, relief="ridge")
        self.panel.place(relx=0.5, rely=0.5, anchor="center", width=560, height=450)

        # Title
        tk.Label(self.panel, text="PDF Tool Box", font=("Segoe UI Semibold", 28, "bold"),
                 fg="#00ffcc", bg="#2a2a2a").pack(pady=15)
        tk.Label(self.panel, text="Educational purposes only. Author not liable.",
                 font=("Segoe UI", 10), fg="#bbbbbb", bg="#2a2a2a").pack(pady=2)
        tk.Label(self.panel, text="GitHub: https://github.com/cmdkill3r",
                 font=("Segoe UI", 10), fg="#bbbbbb", bg="#2a2a2a").pack(pady=2)

        # Buttons
        self.buttons_frame = tk.Frame(self.panel, bg="#2a2a2a")
        self.buttons_frame.pack(pady=40)

        # Add buttons with icons & hover
        self.add_button("Inject JS Payload", self.inject_js_action, "#00ffcc", "icons/js.png")
        self.add_button("Check for JS", self.check_js_action, "#ffcc00", "icons/check.png")
        self.add_button("Clean PDF (Remove JS)", self.clean_pdf_action, "#ff5555", "icons/clean.png")
        self.add_button("Exit", self.quit, "#ff4444", "icons/exit.png")

    # ---------------- Button Helper ----------------
    def add_button(self, text, command, color, icon_path=None):
        frame = tk.Frame(self.buttons_frame, bg="#2a2a2a")
        frame.pack(pady=8)

        if icon_path and os.path.exists(icon_path):
            icon = PhotoImage(file=icon_path)
            btn = tk.Button(frame, text="  "+text, image=icon, compound="left",
                            bg="#333333", fg=color, font=("Segoe UI", 12, "bold"),
                            relief="flat", width=260, anchor="w", command=command)
            btn.image = icon
        else:
            btn = tk.Button(frame, text=text, bg="#333333", fg=color,
                            font=("Segoe UI", 12, "bold"), relief="flat", width=28, command=command)

        btn.pack()
        btn.bind("<Enter>", lambda e: btn.configure(bg="#444444"))
        btn.bind("<Leave>", lambda e: btn.configure(bg="#333333"))

    # ---------------- Button Actions ----------------
    def inject_js_action(self):
        inPDF = filedialog.askopenfilename(title="Select PDF to inject JS", filetypes=[("PDF Files","*.pdf")])
        if not inPDF: return
        js_file = filedialog.askopenfilename(title="Select JS payload", filetypes=[("JS Files","*.js")])
        if not js_file: return
        outPDF = filedialog.asksaveasfilename(title="Save injected PDF as", defaultextension=".pdf", filetypes=[("PDF Files","*.pdf")])
        if not outPDF: return
        inject_js(inPDF, outPDF, js_file)

    def check_js_action(self):
        inPDF = filedialog.askopenfilename(title="Select PDF to check", filetypes=[("PDF Files","*.pdf")])
        if not inPDF: return
        check_js(inPDF)

    def clean_pdf_action(self):
        inPDF = filedialog.askopenfilename(title="Select PDF to clean", filetypes=[("PDF Files","*.pdf")])
        if not inPDF: return
        outPDF = filedialog.asksaveasfilename(title="Save cleaned PDF as", defaultextension=".pdf", filetypes=[("PDF Files","*.pdf")])
        if not outPDF: return
        clean_pdf(inPDF, outPDF)

# ---------------- Run ----------------
if __name__ == "__main__":
    app = PDFToolBox()
    app.mainloop()
