import text_detection
import pdf2image
import tempfile
import os
from PIL import Image

temp_dir = tempfile.TemporaryDirectory()

def pdf2jpg(path):
    pdf = pdf2image.convert_from_path(path)
    count = 0
    for page in pdf:
        count += 1
        base_file_name = os.path.basename(path)
        jpg_path = f'{temp_dir.name}/{base_file_name}{count}.jpg'
        page.save(jpg_path, 'JPEG')
        yield jpg_path


# TODO: crop doesn't work with other file sizes
def preprocess_image(image_jpg_path):
    image_jpg = Image.open(image_jpg_path)
    image_jpg = image_jpg.resize((800, 420))
    image_jpg = image_jpg.crop((27, 20, image_jpg.width/2+150, image_jpg.height-50))
    return image_jpg


source_image_path = 'pictures/doc.pdf'
for image_jpg_path in pdf2jpg(source_image_path):
    image_jpg = preprocess_image(image_jpg_path)
    image_jpg.save(image_jpg_path, optimize=True, quality=100)

    image = text_detection.Image(image_jpg_path)
    text = image.get_text(languages=['ru'])
    image.show_text(text)

temp_dir.cleanup()