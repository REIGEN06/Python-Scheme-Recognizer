import text_detection
import pdf2image
import os
import tempfile
from PIL import Image

temp_dir = tempfile.TemporaryDirectory()

def pdf2jpg(path):
    pdf_file = pdf2image.convert_from_path(path)
    count = 0
    for page in pdf_file:
        count += 1
        print(temp_dir.name)
        jpg_file_path = f'{temp_dir.name}/doc_{count}.jpg'
        page.save(jpg_file_path, 'JPEG')
        yield jpg_file_path


for jpg_image_path in pdf2jpg('pictures/doc.pdf'):
    image_jpg = Image.open(jpg_image_path)
    image_jpg_croped = image_jpg.crop((160, 40, image_jpg.width-1500, image_jpg.height-200))
    image_jpg_croped_resized = image_jpg_croped.resize((800, 420))
    image_jpg_croped_resized_path = f'{temp_dir.name}/doc_crop_resize.jpg' 
    image_jpg_croped_resized.save(image_jpg_croped_resized_path, optimize=True, quality=100)

    image = text_detection.Image(image_jpg_croped_resized_path)
    text = image.get_text()
    image.show_text(text)

temp_dir.cleanup()