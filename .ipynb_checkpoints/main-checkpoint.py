import cv2
from ultralytics import YOLO
import easyocr
from tkinter import Tk, filedialog
from PIL import Image, ImageTk
import tkinter as tk

# Load model
model = YOLO("runs/detect/train/weights/best.pt")

# OCR reader
reader = easyocr.Reader(['en'])

# Choose image
root = Tk()
root.withdraw()
image_path = filedialog.askopenfilename(title="اختر صورة سيارة")

img = cv2.imread(image_path)

# Run YOLO detection
results = model(img)[0]

plate_text = "لم يتم التعرف"

for box in results.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    # Crop plate region
    crop = img[y1:y2, x1:x2]

    # OCR
    text = reader.readtext(crop)
    if text:
        plate_text = text[0][1]

    # Draw rectangle and text
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, plate_text, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Convert BGR → RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_pil = Image.fromarray(img_rgb)

# Tkinter window for display
window = tk.Tk()
window.title("Plate Detection")

tk_img = ImageTk.PhotoImage(img_pil)
panel = tk.Label(window, image=tk_img)
panel.pack()

window.mainloop()
