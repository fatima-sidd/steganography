
#!/usr/bin/python

import os
import sys
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

def add_leading_zeros(binary_number, expected_length):
        length = len(binary_number)
        return (expected_length - length) * '0' + binary_number

def rgb_to_binary(r, g, b):
        return add_leading_zeros(bin(r)[2:], 8), add_leading_zeros(bin(g)[2:], 8), add_leading_zeros(bin(b)[2:], 8)

class ImageEncoderDecoder:

    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("Image Encoder/Decoder")
        self.master.geometry('1000x1000')
        self.master.configure(bg="#222222")

        # Heading label
        heading_label = tk.Label(master, text="Image Steganography", font=("Times New Roman", 20, "bold"), bg="#222222", fg="#fff", padx=20, pady=40)
        heading_label.pack()

        # Frame for visible image selection
        frame1 = tk.Frame(self.master, bg="#222222")
        frame1.pack()

        # Label and entry for visible image path
        self.img_visible_path_label = tk.Label(frame1, text="Select Visible Image:", bg="#222222", fg="#fff", font=("Times New Roman", 12))
        self.img_visible_path_label.pack(side="left", padx=5, pady=5)
        self.img_visible_path_entry = tk.Entry(frame1, width=60, bg="#222222", fg="#fff", font=("Times New Roman", 10))
        self.img_visible_path_entry.pack(side="left", padx=5, pady=5)
        self.browse_visible_button = tk.Button(frame1, text="Browse", bg="#222222", fg="#fff", command=self.browse_visible_img, width=10)
        self.browse_visible_button.pack(side="left", padx=5, pady=5)

        # Spacing
        tk.Label(self.master, text="", bg="#222222").pack()

        # Frame for hidden image selection
        frame2 = tk.Frame(self.master, bg="#222222")
        frame2.pack()

        # Label and entry for hidden image path
        self.img_hidden_path_label = tk.Label(frame2, text="Select Hidden Image:", font=("Times New Roman", 12), bg="#222222", fg="#fff",)
        self.img_hidden_path_label.pack(side="left", padx=5, pady=5)
        self.img_hidden_path_entry = tk.Entry(frame2, width=60, bg="#222222", fg="#fff", font=("Times New Roman", 10))
        self.img_hidden_path_entry.pack(side="left", padx=5, pady=5)
        self.browse_hidden_button = tk.Button(frame2, text="Browse", bg="#222222", fg="#fff", command=self.browse_hidden_img, width=10)
        self.browse_hidden_button.pack(side="left", padx=5, pady=5)

        # Frame for buttons
        button_frame = tk.Frame(self.master, pady=25, bg="#222222")
        button_frame.pack()

        # Encode and Decode buttons
        self.encode_button = tk.Button(button_frame, text="Encode Image", command=self.encode, width=30, height=2, bg="#c0392b", fg="white", font=("Times New Roman", 12, "bold"))
        self.encode_button.pack(side="left", padx=10, pady=5)
        self.decode_button = tk.Button(button_frame, text="Decode Image", command=self.decode, width=30, height=2, bg="#27ae60", fg="white", font=("Times New Roman", 12, "bold"))
        self.decode_button.pack(side="left", padx=10, pady=5)

        # Frame for image display
        self.images_frame = tk.Frame(self.master, bg="#222222")
        self.images_frame.pack(side=tk.TOP, pady=10)

        # Labels for original and encoded images
        self.original_image_label = tk.Label(self.images_frame, text="Original Image", bg="#222222", fg="#fff", font=("Times New Roman", 12, "bold"))
        self.original_image_label.pack(side=tk.LEFT, padx=10)
        self.encoded_image_label = tk.Label(self.images_frame, text="Encoded Image", bg="#222222", fg="#fff", font=("Times New Roman", 12, "bold"))
        self.encoded_image_label.pack(side=tk.LEFT, padx=10)

        # Variables to store image data and photo objects
        self.original_image = None
        self.encoded_image = None
        self.original_image_photo = None
        self.encoded_image_photo = None

        # Clear button
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_images, width=20, height=1, fg="black", font=("Times New Roman", 10, "bold"))
        self.clear_button.pack(padx=10, pady=5)

    def browse_visible_img(self):
       
        # Open a file dialog window to select a visible image file
        img_path = filedialog.askopenfilename(title="Select Visible Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
       
        # Clear the entry field for visible image path
        self.img_visible_path_entry.delete(0, tk.END)
        
        # Insert the selected image file path into the entry field
        self.img_visible_path_entry.insert(0, img_path)

    def browse_hidden_img(self):
        
        # Open a file dialog window to select a hidden image file
        img_path = filedialog.askopenfilename(title="Select Hidden Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        
        # Clear the entry field for hidden image path
        self.img_hidden_path_entry.delete(0, tk.END)
        
        # Insert the selected image file path into the entry field
        self.img_hidden_path_entry.insert(0, img_path)

    def display_image(self, img, label):
        # Check if the image exists
        if img is not None:
            # If there are existing images in the label, clear them before displaying a new one
            for child in label.winfo_children():
                child.destroy()

            # Resize the image to create a thumbnail
            img_thumbnail = ImageTk.PhotoImage(img.resize((200, 200)))
            
            # Configure the label to display the thumbnail image
            label.config(image=img_thumbnail)
            label.image = img_thumbnail

            # Store the thumbnail image based on the label it's associated with
            if label == self.original_image_label:
                self.original_image_photo = img_thumbnail
            elif label == self.encoded_image_label:
                self.encoded_image_photo = img_thumbnail
        else:
            # If the image doesn't exist, print a message and skip the display
            print("Image is None. Skipping display.")

    def clear_images(self):
        # Reset the stored images to None
        self.original_image = None
        self.encoded_image = None

        # Delete the stored thumbnail images if they exist
        if self.original_image_photo:
            self.original_image_photo.__del__()  # Delete the reference to the image object
            self.original_image_photo = None  # Reset the stored thumbnail to None

        if self.encoded_image_photo:
            self.encoded_image_photo.__del__()  # Delete the reference to the image object
            self.encoded_image_photo = None  # Reset the stored thumbnail to None

        # Reset the displayed images in the GUI labels to None (clears the displayed thumbnails)
        self.original_image_label.config(image=None)
        self.encoded_image_label.config(image=None)

        # Clear the text in the entry fields for visible and hidden image paths
        self.img_visible_path_entry.delete(0, tk.END)
        self.img_hidden_path_entry.delete(0, tk.END)

    def display_imagewind(self, image, title):
        # Display the image in a separate window with the given title
        image.show(title=title)

    def get_binary_pixel_values(self, img, width, height):
        # Retrieve the binary pixel values from the given image
        hidden_image_pixels = ''
        for col in range(width):
            for row in range(height):
                pixel = img[col, row]
                # Extract individual RGB values
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                # Convert RGB values to binary
                r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
                # Concatenate the binary values
                hidden_image_pixels += r_binary + g_binary + b_binary
        return hidden_image_pixels

    def change_binary_values(self, img_visible, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden):
        # Modify the binary values in the visible image using the hidden image's pixels
        idx = 0
        for col in range(width_visible):
            for row in range(height_visible):
                if row == 0 and col == 0:
                    # Embed the width and height of the hidden image in the first pixel
                    width_hidden_binary = add_leading_zeros(bin(width_hidden)[2:], 12)
                    height_hidden_binary = add_leading_zeros(bin(height_hidden)[2:], 12)
                    w_h_binary = width_hidden_binary + height_hidden_binary
                    img_visible[col, row] = (int(w_h_binary[0:8], 2), int(w_h_binary[8:16], 2), int(w_h_binary[16:24], 2))
                    continue
                r, g, b = img_visible[col, row]
                r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
                # Change the LSBs of RGB values with hidden image pixel values
                r_binary = r_binary[0:4] + hidden_image_pixels[idx:idx+4]
                g_binary = g_binary[0:4] + hidden_image_pixels[idx+4:idx+8]
                b_binary = b_binary[0:4] + hidden_image_pixels[idx+8:idx+12]
                idx += 12
                img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
                if idx >= len(hidden_image_pixels):
                    return img_visible

        return img_visible

    def encode_images(self, img_visible, img_hidden):

        # Load the pixels of the visible image
        encoded_image = img_visible.load()

        # Load the pixels of the hidden image
        img_hidden_copy = img_hidden.load()

        # Get dimensions of both images
        width_visible, height_visible = img_visible.size
        width_hidden, height_hidden = img_hidden.size

        # Retrieve binary pixel values from the hidden image
        hidden_image_pixels = self.get_binary_pixel_values(img_hidden_copy, width_hidden, height_hidden)

        # Change binary values in the visible image based on the hidden image's pixels
        encoded_image = self.change_binary_values(encoded_image, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden)
        
        # Return the modified visible image
        return img_visible  

    def extract_hidden_pixels(self, image, width_visible, height_visible, pixel_count):
        # Initialize variable to store extracted hidden pixels
        hidden_image_pixels = ''
        idx = 0

        # Traverse through the visible image pixels to extract hidden pixel values
        for col in range(width_visible):
            for row in range(height_visible):
                
                # Skip the first pixel which stores metadata
                if row == 0 and col == 0:
                    continue 

                r, g, b = image[col, row]
                r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)

                # Extract the least significant bits of RGB values
                hidden_image_pixels += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
                idx += 1

                # If enough hidden pixels have been extracted, return the values
                if idx >= pixel_count * 2:
                    return hidden_image_pixels
        
        # Return the extracted hidden pixel values
        return hidden_image_pixels  

    def reconstruct_image(self, image_pixels, width, height):
        # Create a new blank image with given width and height
        image = Image.new("RGB", (width, height))
        image_copy = image.load()
        idx = 0
        
        # Iterate through the pixels in the image_pixels string
        for col in range(width):
            for row in range(height):
                # Extract binary values for RGB from image_pixels
                r_binary = image_pixels[idx:idx+8]
                g_binary = image_pixels[idx+8:idx+16]
                b_binary = image_pixels[idx+16:idx+24]

                # Check if the binary values exist and convert them to integers to set pixel values
                if r_binary and g_binary and b_binary:
                    try:
                        # Convert binary strings to integers and set the pixel in the image
                        image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
                    except ValueError as e:
                        # Handle error if conversion fails
                        print(f"Error converting binary string to int: {e}")
                        print(f"Problematic index: {idx}")
                        print(f"Current portion of image_pixels: {image_pixels[idx:idx+24]}")
                        return None  # Return None in case of conversion errors
                else:
                    print("Binary strings are empty. Skipping conversion.")

                idx += 24  # Move to the next set of binary values for the next pixel
                
        return image  # Return the reconstructed image
    
    def decode_images(self, image):

        # Load pixels of the provided image
        image_copy = image.load()

        # Get dimensions of the visible image
        width_visible, height_visible = image.size

        # Extract metadata from the first pixel of the visible image
        r, g, b = image_copy[0, 0]
        r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)

        # Retrieve width and height of the hidden image from the metadata
        w_h_binary = r_binary + g_binary + b_binary
        width_hidden = int(w_h_binary[0:12], 2)
        height_hidden = int(w_h_binary[12:24], 2)

        # Calculate the number of pixels in the hidden image
        pixel_count = width_hidden * height_hidden

        # Extract hidden image pixels from the visible image
        hidden_image_pixels = self.extract_hidden_pixels(image_copy, width_visible, height_visible, pixel_count)

        try:
            # Reconstruct the hidden image using the extracted hidden pixels
            decoded_image = self.reconstruct_image(hidden_image_pixels, width_hidden, height_hidden)

            # Return the decoded hidden image
            return decoded_image 
        
        except ValueError as e:
            # Handle errors during image reconstruction
            messagebox.showerror("Error", f"Error decoding image: {str(e)}")

        # Return None if decoding fails
        return None  

    def display_pixel_values(self, img, title):
        # Create a new window for displaying pixel values
        pixel_values_window = tk.Toplevel(self.master)
        pixel_values_window.title(title)

        # Create a text widget to display pixel values
        pixel_values_text = tk.Text(pixel_values_window, wrap=tk.WORD, height=20, width=40)
        pixel_values_text.pack()

        # Output RGB values of pixels
        for col in range(img.width):
            for row in range(img.height):
                pixel = img.getpixel((col, row))
                pixel_values_text.insert(tk.END, f"Pixel at ({col}, {row}): {pixel}\n")

    def encode(self):
            img_visible_path = self.img_visible_path_entry.get()
            img_hidden_path = self.img_hidden_path_entry.get()

            if not img_visible_path or not img_hidden_path:
                messagebox.showerror("Error", "Please select both visible and hidden images.")
                return

            try:
                img_visible = Image.open(img_visible_path)
                img_hidden = Image.open(img_hidden_path)

                # Check if the cover image size is greater than the hidden image size
                if img_visible.size[0] < img_hidden.size[0] or img_visible.size[1] < img_hidden.size[1]:
                    messagebox.showerror("Error", "Cover image size must be greater than hidden image size.")
                    return

                # Output RGB values of pixels for the original image
                self.display_pixel_values(img_visible, "Encoding: Original Image Pixel Values")

                encoded_image = self.encode_images(img_visible, img_hidden)
                encoded_image.save("encoded_image.png")

                # Output RGB values of pixels for the hidden image
                self.display_pixel_values(img_hidden, "Ecoding: Hidden Image Pixel Values")

                # Output RGB values of pixels for the encoded image
                self.display_pixel_values(encoded_image, "Encoding: Encoded Image Pixel Values")

                # Display the images
                self.display_imagewind(img_visible, "Original Image")

                #self.display_imagewind(img_hidden, "Hidden Image")
                self.display_imagewind(encoded_image, "Encoded Image")

                self.original_image = img_visible
                self.encoded_image = encoded_image

                # Display the original image
                self.display_image(self.original_image, self.original_image_label)

                # Display the encoded image
                self.display_image(self.encoded_image, self.encoded_image_label)

                

            except Exception as e:
                messagebox.showerror("Error", f"Error encoding image: {str(e)}")

    def decode(self):
        # Ask user to select an encoded image
        encoded_img_path = filedialog.askopenfilename(
            title="Select Encoded Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )

        if not encoded_img_path:
            messagebox.showerror("Error", "Please select an encoded image for decoding.")
            return

        try:
            encoded_image = Image.open(encoded_img_path)

            # Output RGB values of pixels for the original (encoded) image
            self.display_pixel_values(encoded_image, "Decoding: Encoded Image Pixel Values")

            decoded_image = self.decode_images(encoded_image)

            # Output RGB values of pixels for the decoded image
            self.display_pixel_values(decoded_image, "Decoding: Decoded Image Pixel Values")

            if decoded_image:
                # Save the decoded image to a file
                decoded_image.save("decoded_image.png")

                # Display the decoded image
                self.display_imagewind(decoded_image, "Decoded Image")
        except Exception as e:
            messagebox.showerror("Error", f"Error decoding image: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageEncoderDecoder(root)
    root.mainloop()