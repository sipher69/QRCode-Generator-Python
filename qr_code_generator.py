import qrcode
from PIL import Image, ImageOps
import requests
from io import BytesIO
import tkinter as tk
from tkinter import ttk, filedialog


color_options = ["black", "red", "green", "blue", "purple"]


root = tk.Tk()

root.title("QR Code Generator")
root.geometry("300x400+500+100")
root.iconbitmap('C:\\Users\\DELL\\Desktop\\py\\qr.ico')

 


img_url_label = tk.Label(root, text="Image URL:")
img_url_label.pack()
img_url_entry = tk.Entry(root)
img_url_entry.pack()

browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(img_url_entry))
browse_button.pack()


def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


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
    
    if not img_url or not website_url:
        return
        
    if img_url.startswith("http"):
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
    else:
        img = Image.open(img_url).convert("RGBA")

   
    img = img.resize((90, 90))
    img = ImageOps.fit(img, (100, 100), method=Image.LANCZOS)

    
    qr = qrcode.QRCode(version=1, box_size=15, border=2)
    qr.add_data(website_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=qr_color, back_color="white").convert("RGBA")

   
    qr_img.alpha_composite(img, dest=(qr_img.size[0]//2-img.size[0]//2, qr_img.size[1]//2-img.size[1]//2))

  
    qr_img.save("qr.png")
    qr_img.show()


generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr, state="disabled")
generate_button.pack()


def check_fields(*args):
    if img_url_entry.get() and website_url_entry.get():
        generate_button.config(state="normal")
    else:
        generate_button.config(state="disabled")

img_url_entry.bind("<KeyRelease>", check_fields)
website_url_entry.bind("<KeyRelease>", check_fields)


root.mainloop()
