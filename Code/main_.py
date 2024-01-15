import tkinter as tk
from tkinter import messagebox
from image_steganography import ImageEncoderDecoder
from text_steganography import SteganographyApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry('450x300')
        self.root.configure(bg="#222222")

        heading_label = tk.Label(root, text="Choose Steganography Type", font=("Times New Roman", 20, "bold"), bg="#222222", fg="#fff", padx=10, pady=30)
        heading_label.pack()

        image_button = tk.Button(root, text="Image Steganography", command=self.run_image_steganography, width=30, height=2, bg="#3498db", fg="white", font=("Times New Roman", 12, "bold"))
        image_button.pack(pady=10)

        text_button = tk.Button(root, text="Text Steganography", command=self.run_text_steganography, width=30, height=2, bg="#800080", fg="white", font=("Times New Roman", 12, "bold"))
        text_button.pack(pady=10)

    def run_image_steganography(self):
        try:
            image_root = tk.Toplevel(self.root)
            app = ImageEncoderDecoder(image_root)

        except Exception as e:
            messagebox.showerror("Error", f"Error running image steganography: {str(e)}")

    def run_text_steganography(self):
        try:
            text_root = tk.Toplevel(self.root)
            app = SteganographyApp(text_root)

        except Exception as e:
            messagebox.showerror("Error", f"Error running text steganography: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
