import cv2
import easyocr
import matplotlib.pyplot as plt
class Image:
    def __init__(self, path):
        self.image = cv2.imread(path)

    def show_text(self, text):
        for t in text:
            bbox, text, score = t
            cv2.rectangle(self.image, [int(bbox[0][0]), int(bbox[0][1])], [int(bbox[2][0]), int(bbox[2][1])], (0, 255, 0), 5)
            cv2.putText(self.image, text, [int(bbox[0][0]), int(bbox[0][1])], cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.show()
    
    def get_text(self, language='ru'):
        reader = easyocr.Reader([language], gpu=False)
        return reader.readtext(self.image)

if __name__ == '__main__':
    import pdf2image
    from PIL import Image as Img

    def pdf2jpg(path):
        pdf_file = pdf2image.convert_from_path(path)
        count = 0
        for page in pdf_file:
            count += 1
            jpg_file_path = f'pictures/doc_{count}.jpg'
            page.save(jpg_file_path, 'JPEG')
            yield jpg_file_path
    

    for jpg_image_path in pdf2jpg('pictures/doc.pdf'):
        image = Img.open(jpg_image_path)
        image_croped = image.crop((160, 40, image.width-1500, image.height-200))
        image_croped_resized = image_croped.resize((800, 420))

        image_croped_resized_path = 'pictures/doc_crop_resize.jpg' 
        image_croped_resized.save(image_croped_resized_path, optimize=True, quality=100)

        image = Image(image_croped_resized_path)
        text = image.get_text()
        image.show_text(text)
