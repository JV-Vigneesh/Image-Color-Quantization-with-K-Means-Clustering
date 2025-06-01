import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import image_processor
from kmeans_clustering import KMeansClustering
import threading


class ImageQuantizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Quantisation")
        self.root.resizable(False, False)
        self.image_path = None
        self.height = None
        self.width = None
        self.quantised_pixels = None
        self.pixels = None
        self.processing_label = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Browse an Image:").grid(row=0, column=0, padx=5, pady=5)
        self.browse_button = tk.Button(self.root, text="Browse Image", command=self.load_image)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Number of Colours:").grid(row=1, column=0, padx=5, pady=5)
        self.num_colours_entry = tk.Entry(self.root)
        self.num_colours_entry.grid(row=1, column=1, padx=5, pady=5)

        self.quantise_button = tk.Button(self.root, text="Quantise Image", command=self.quantise_image)
        self.quantise_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_button = tk.Button(self.root, text="Save Quantised Image", command=self.save_quantised_image)
        self.save_button.grid(row=1, column=3, padx=5, pady=5)

        self.original_label = tk.Label(self.root, text="Original Image")
        self.original_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.quantised_label = tk.Label(self.root, text="Quantised Image")
        self.quantised_label.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

    def load_image(self):
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All Files", "*.*")]
        self.image_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.image_path:
            self.pixels, self.height, self.width = image_processor.load_image_and_get_dimensions(self.image_path)
            if self.pixels is None:
                messagebox.showerror("Error", "Failed to load the image.")
            else:
                self.display_image(self.pixels, self.original_label)
        else:
            messagebox.showerror("Error", "No image selected.")

    def quantise_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        num_colours = self.num_colours_entry.get()
        if not num_colours:
            messagebox.showerror("Error", "Please enter the number of colours.")
            return

        try:
            num_colours = int(num_colours)
            if num_colours <= 0:
                raise ValueError("Number of colours must be greater than 0.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return

        if self.pixels is not None:
            self.show_processing_message()
            self.disable_buttons()

            thread = threading.Thread(target=self.run_quantisation, args=(num_colours,))
            thread.start()
        else:
            messagebox.showerror("Error", "Failed to load the image.")

    def show_processing_message(self):
        self.processing_label = tk.Label(self.root, text="Processing...", font=('Arial', 12), fg="blue")
        self.processing_label.place(relx=0.5, rely=0.4, anchor="center")

    def hide_processing_message(self):
        if self.processing_label:
            self.processing_label.destroy()
            self.processing_label = None

    def disable_buttons(self):
        self.browse_button.config(state="disabled")
        self.quantise_button.config(state="disabled")
        self.save_button.config(state="disabled")

    def enable_buttons(self):
        self.browse_button.config(state="normal")
        self.quantise_button.config(state="normal")
        self.save_button.config(state="normal")

    def run_quantisation(self, num_colours):
        kmeans = KMeansClustering(num_clusters=num_colours)
        self.quantised_pixels = kmeans.fit(self.pixels)
        self.root.after(0, self.show_quantised_result)

    def show_quantised_result(self):
        self.hide_processing_message()
        self.enable_buttons()
        self.display_image(self.quantised_pixels, self.quantised_label)

    def save_quantised_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        if self.quantised_pixels is None:
            messagebox.showerror("Error", "No quantised image available to save.")
            return

        filetypes = [("JPEG", "*.jpg"), ("PNG", "*.png"), ("Bitmap", "*.bmp"), ("TIFF", "*.tiff")]
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=filetypes)
        if save_path:
            image_processor.create_image_from_pixels(self.quantised_pixels, self.height, self.width, save_path)
            messagebox.showinfo("Success", "Image saved successfully.")

    def display_image(self, pixels, label):
        if pixels is not None:
            image = image_processor.create_image_from_pixels(pixels, self.height, self.width)
            image = image.resize((300, 300))
            image = ImageTk.PhotoImage(image)
            label.configure(image=image)
            label.image = image
        else:
            messagebox.showerror("Error", "Failed to create image from pixels.")


def run_gui():
    root = tk.Tk()
    app = ImageQuantizationApp(root)
    root.mainloop()
