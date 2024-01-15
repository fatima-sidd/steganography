import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import os

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Steganography App")
        self.master.geometry('1000x1000')
        self.master.configure(bg="#222222")

        heading_label = tk.Label(master, text="Image Steganography", font=("Times New Roman", 20, "bold"), bg="#222222" ,  fg="#fff", padx=20, pady=10)
        heading_label.pack()
        
        frame1 = tk.Frame(self.master, bg="#222222")
        frame1.pack()  # Using expand to fill the available space
        # Create GUI components
        self.original_image_label = tk.Label(frame1, text="Select Cover Image:", bg="#222222", fg="#fff", font=("Times New Roman", 10))
        self.original_image_label.pack(side="left", padx=5, pady=5)  

        self.original_image_path = tk.Entry(frame1, width=60, bg="#222222", fg="#fff", font=("Times New Roman", 10)) 
        self.original_image_path.pack(side="left", padx=5, pady=5)

        self.select_image_button = tk.Button(frame1, text="Browse", bg="#222222", fg="#fff", command=self.select_image, width=10)
        self.select_image_button.pack(side="left", padx=5, pady=5) 

        tk.Label(self.master, text="", bg="#222222").pack()

       
        frame2 = tk.Frame(self.master, bg="#222222")
        frame2.pack()  # 
        
        self.message_label  = tk.Label(frame2, text="Enter the Message", bg="#222222", fg="#fff",font=("Times New Roman", 10),  height=4)
        self.message_label .pack(side="left", padx=5, pady=5)  

        self.message_entry = tk.Text(frame2, width=75, height=5, bg="#222222", fg="#fff",font=("Times New Roman", 10), wrap="word", insertwidth=4, padx=2, pady=2)
        self.message_entry.pack(side="left", padx=5, pady=5)

        button_frame = tk.Frame(self.master, pady=25, bg="#222222", padx = 20)
        button_frame.pack()

        # Encode Button
        self.encode_button = tk.Button(button_frame, text="Encode Image", command=self.encrypt, width=30, height= 2, bg="#c0392b" , fg="white" , font=("Times New Roman", 10,"bold"))
        self.encode_button.pack(side="left", padx=10, pady=5)  # Reduced vertical space above the button

        # Decode Button
        self.decode_button = tk.Button(button_frame,  text="Decode Image", command=self.decrypt,  width=30, height= 2, bg="#27ae60", fg="white", font=("Times New Roman", 10,"bold"))
        self.decode_button.pack(side="left", padx=10, pady=5)  # Adding horizontal and vertical space

         # Create a frame for displaying images horizontally
        self.images_frame = tk.Frame(self.master, bg="#222222")
        self.images_frame.pack(side=tk.TOP, pady=10)
        
        

        # Create labels for displaying images in the frame
        self.original_image_display = tk.Label(self.images_frame, bg="#222222", fg="#fff", text="Original Image", font=("Times New Roman", 10, "bold"))
        self.original_image_display.pack(side=tk.LEFT, padx=10)

        self.steg_image_display = tk.Label(self.images_frame, bg="#222222", fg="#fff", text="Encoded Image", font=("Times New Roman", 10, "bold"))
        self.steg_image_display.pack(side=tk.LEFT, padx=10)

        # Create a frame for displaying images horizontally
        self.images_label = tk.Frame(self.master, bg="#222222")
        self.images_label.pack(side=tk.TOP, pady=10)
        # Labels to display image sizes
        self.original_size_label = tk.Label(self.images_label, bg="#222222", fg="#fff", text="Original Image Size", font=("Times New Roman", 10))
        self.original_size_label.pack(side=tk.LEFT, padx=10)

        self.steg_size_label = tk.Label(self.images_label, bg="#222222", fg="#fff",text="Encoded Image Size", font=("Times New Roman", 10))
        self.steg_size_label.pack(side=tk.LEFT, padx=10)
        
        
        self.extracted_msg = tk.Frame(self.master, bg="#222222")
        self.extracted_msg.pack(side=tk.TOP, pady=10)
        
        
        
        self.extracted_label = tk.Label(self.extracted_msg,  bg="#222222", fg="#fff",text="Extracted Message:", font=("Times New Roman", 13))
        self.extracted_label.pack(side=tk.LEFT, padx=10)

        self.extracted_message_display = tk.Text(self.extracted_msg, bg="#222222", fg="#fff", width=75, height=4, font=("Times New Roman", 10))
        self.extracted_message_display.pack()


        self.clear_label = tk.Frame(self.master, bg="#222222")
        self.clear_label.pack(side=tk.TOP, pady=5)
        
        
        self.select_image_button = tk.Button(self.clear_label, text="Clear", command=self.clear,  width=20, height= 1, fg="black", font=("Times New Roman", 10,"bold"))
        self.select_image_button.pack(side="left", padx=10, pady=15)  # Adding horizontal and vertical space

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.original_image_path.delete(0, tk.END)
        self.original_image_path.insert(0, file_path)

    def encrypt(self):
        original_image_path = self.original_image_path.get()

        try:
            if not os.path.isfile(original_image_path):
                raise FileNotFoundError(f"The file '{original_image_path}' does not exist.")

            im = Image.open(original_image_path)
            x, y = list(im.size)
            rgb = np.asarray(im).reshape(-1)
            new_img = np.array(rgb)

            # Ask the user for the private key using a dialog box
            message = self.message_entry.get("1.0", "end-1c")

            private_key = self.get_private_key()

            # Encrypt the message using Caesar cipher
            enc = self.get_byte(self.encrypt_text(message, private_key))
            encrypted = self.encrypt_pixel(new_img, enc)
            final_img = encrypted.reshape(y, x, 3)
            im = Image.fromarray(final_img)
            im.save("textsteg_img.png")

            # Display original and steganographed images
            self.display_images(original_image_path, "textsteg_img.png")

            # Display image sizes
            original_size = os.path.getsize(original_image_path)
            steg_size = os.path.getsize("textsteg_img.png")
            self.original_size_label.config(text=f"Original Image Size: {original_size} bytes")
            self.steg_size_label.config(text=f"Steganographed Image Size: {steg_size} bytes")

            messagebox.showinfo("Success", "Encryption completed successfully!")

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"File not found: {str(e)}")

        except Exception as e:
            messagebox.showerror("Error", f"Error during encryption: {str(e)}")

    def decrypt(self):
        steg_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        try:
            # Ask the user for the private key using a dialog box
            private_key = self.get_private_key()

            im = Image.open(steg_image_path)
            x, y = list(im.size)
            rgb = np.asarray(im).reshape(-1)
            new_img = np.array(rgb)
            decrypted = self.decrypt_pixel(new_img)
            decrypted_message = self.extract_message(decrypted)
            
                   

            # Decrypt the message using Caesar cipher
            decrypted_text = self.decrypt_text(decrypted_message, private_key)

            #self.extracted_message_display.delete("1.0", "end")
            self.extracted_message_display.insert("1.0", decrypted_text) 

        except Exception as e:
            messagebox.showerror("Error", f"Error during decryption: {str(e)}")

    def encrypt_text(self, text, key):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                shift = key % 26
                if char.isupper():
                    encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
                else:
                    encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt_text(self, text, key):
        decrypted_text = ""
        for char in text:
            if char.isalpha():
                shift = key % 26
                if char.isupper():
                    decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
                else:
                    decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
            else:
                decrypted_text += char
        return decrypted_text

    def encrypt_pixel(self, img, byte_array):
        c = -1

        for pix in img:
            c += 1
            try:
                if byte_array[c] == '1':
                    if img[c] % 2 == 0:
                        img[c] -= 1
                elif byte_array[c] == '0':
                    if img[c] % 2 != 0:
                        img[c] -= 1
                elif byte_array[c] == ' ':
                    if img[c] % 2 != 0:
                        img[c] -= 1
            except:
                if img[c] % 2 == 0:
                    img[c] -= 1
                break
        return img

    def get_byte(self, a):
        a_bytes = bytes(a, "ascii")
        return ' '.join(format(ord(x), '08b') for x in a)

    def decrypt_pixel(self, pix):
        st = ''
        c = 0
        for i in pix:
            c += 1
            if i % 2 != 0 and c % 9 == 0:
                break
            elif i % 2 == 0 and c % 9 == 0:
                st += ' '
            elif i % 2 == 0:
                st += '0'
            elif i % 2 != 0:
                st += '1'
        return st

    def extract_message(self, decrypted):
        de_array = decrypted.split(' ')
        final_message = ''
        for i in de_array:
            final_message += self.binary_to_decimal(int(i))
        return final_message

    def binary_to_decimal(self, binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while binary1 != 0:
            dec = binary1 % 10
            decimal = decimal + dec * pow(2, i)
            binary1 = binary1 // 10
            i += 1
        return chr(decimal)


    def get_private_key(self):

        # Use simpledialog to prompt the user for the private key
        private_key = simpledialog.askinteger("Private Key", "Enter the private key (digits only): ")
        return private_key

    def clear(self):
        # Clear the entry fields
        self.original_image_path.delete(0, tk.END)
        self.message_entry.delete("1.0", tk.END)

        # Clear the displayed images
        self.original_image_display.config(image=None)
        self.original_image_display.image = None
        self.steg_image_display.config(image=None)
        self.steg_image_display.image = None

        # Clear the labels
        self.original_size_label.config(text="Original Image Size:")
        self.steg_size_label.config(text="Steganographed Image Size:")
        self.extracted_message_display.delete("1.0", tk.END) 

    def display_images(self, original_path, steg_path):
        # Remove the previous displayed images
        self.original_image_display.config(image=None)
        self.steg_image_display.config(image=None)

        # Display original image
        original_img = Image.open(original_path)
        original_img.thumbnail((100, 100))
        original_img = ImageTk.PhotoImage(original_img)
        self.original_image_display.config(image=original_img)
        self.original_image_display.image = original_img

        # Display steganographed image
        steg_img = Image.open(steg_path)
        steg_img.thumbnail((100, 100))
        steg_img = ImageTk.PhotoImage(steg_img)
        self.steg_image_display.config(image=steg_img)
        self.steg_image_display.image = steg_img


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()