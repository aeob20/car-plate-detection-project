import os
import xml.etree.ElementTree as ET

xml_folder = "."
output_folder = "labels"
os.makedirs(output_folder, exist_ok=True)

def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[1]) / 2.0 * dw
    y_center = (box[2] + box[3]) / 2.0 * dh
    w = (box[1] - box[0]) * dw
    h = (box[3] - box[2]) * dh
    return x_center, y_center, w, h

for file in os.listdir(xml_folder):
    if not file.endswith(".xml"):
        continue

    xml_path = os.path.join(xml_folder, file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    filename = root.find("filename").text.replace(".png", "")
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    obj = root.find("object")
    bbox = obj.find("bndbox")

    xmin = float(bbox.find("xmin").text)
    ymin = float(bbox.find("ymin").text)
    xmax = float(bbox.find("xmax").text)
    ymax = float(bbox.find("ymax").text)

    x_center, y_center, ww, hh = convert((w, h), (xmin, xmax, ymin, ymax))

    label_path = os.path.join(output_folder, filename + ".txt")
    with open(label_path, "w") as f:
        f.write(f"0 {x_center} {y_center} {ww} {hh}")
