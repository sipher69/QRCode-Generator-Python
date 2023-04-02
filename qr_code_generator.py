import qrcode
from PIL import Image, ImageOps
import requests
from io import BytesIO
import tkinter as tk
from tkinter import ttk


color_options = ["black", "red", "green", "blue", "purple"]


root = tk.Tk()
root.title("QR Code Generator")


screen_width = root.winfo_screenwidth()
window_width = int(screen_width * 0.5)
root.geometry(f"{window_width}x300")


img_url_label = tk.Label(root, text="Image URL:")
img_url_label.pack()
img_url_entry = tk.Entry(root)
img_url_entry.pack()

website_url_label = tk.Label(root, text="Website URL:")
website_url_label.pack()
website_url_entry = tk.Entry(root)
website_url_entry.pack()


color_label = tk.Label(root, text="QR Code Color:")
color_label.pack()
color_var = tk.StringVar(root)
color_var.set(color_options[0])
color_dropdown = ttk.Combobox(root, textvariable=color_var, values=color_options)
color_dropdown.pack()


def generate_qr():
    
    img_url = img_url_entry.get()
    website_url = website_url_entry.get()
    qr_color = color_var.get()
    
   
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

  
    img = img.resize((90, 90))
    img = ImageOps.fit(img, (100, 100), method=Image.LANCZOS)

    
    qr = qrcode.QRCode(version=1, box_size=15, border=2)
    qr.add_data(website_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=qr_color, back_color="white").convert("RGBA")

   
    qr_img.alpha_composite(img, dest=(qr_img.size[0]//2-img.size[0]//2, qr_img.size[1]//2-img.size[1]//2))

  
    qr_img.save("qr.png")
    qr_img.show()


generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack()

root.mainloop()
