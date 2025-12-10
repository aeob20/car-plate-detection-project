import cv2
from ultralytics import YOLO
import easyocr
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label

# ------------------ إعداد النموذج والقارئ ------------------
model = YOLO("runs/detect/train/weights/best.pt")
reader = easyocr.Reader(['en'])


# ==================== دالة معالجة الصورة ====================
def process_image():

    # اختيار الصورة
    img_path = filedialog.askopenfilename(
        title="Choose a car image",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
    )

    if img_path == "":
        return

    print("Selected:", img_path)

    # قراءة الصورة
    img = cv2.imread(img_path)

    # تشغيل YOLO
    results = model(img)[0]

    plate_text = "No found number"

    # استخراج اللوحة
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        crop = img[y1:y2, x1:x2]

        # OCR
        text = reader.readtext(crop, detail=0)
        if len(text) > 0:
            plate_text = text[0]

        # رسم البوكس
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(img, plate_text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # عرض الصورة
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(8, 6))
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.title(f"Detected Plate: {plate_text}", fontsize=20)
    plt.show()


# ==================== عرض الواجهة ====================
root = Tk()
root.title("License Plate Reader")
root.geometry("300x200")

Label(root, text="License Plate Detection", font=("Arial", 15)).pack(pady=10)

Button(root, text="Choose Image", font=("Arial", 12),
       command=process_image, width=20).pack(pady=10)

Button(root, text="Exit", font=("Arial", 12),
       command=root.quit, width=20).pack(pady=10)

root.mainloop()
