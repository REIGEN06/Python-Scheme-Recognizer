import cv2


def rotate_image(image):
    h, w = image.shape[:2]
    center = int(w / 2), int(h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, -45, 0.6)
    image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return image


def calculate_image_hash(file_name):
    image = __prepare_image(file_name)
    pixel_mean = image.mean()
    image = cv2.threshold(image, pixel_mean, 255, 0) # Бинаризация по порогу

    hash = __calculate_prepared_hash(image)
    return hash

def __prepare_image(file_name):
    image = cv2.imread(file_name)
    image = cv2.resize(image, (16,16), interpolation = cv2.INTER_AREA)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
    return image

def __calculate_prepared_hash(image):
    hash=[]
    for x in range(16):
        for y in range(16):
            if image[x,y]==255:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def count_hash_difference(hash1, hash2):
    count=0
    for i in range(len(hash1)):
        if hash1[i]!=hash2[i]:
            count+=1
    return count


if __name__ == '__main__':
    images = []
    image = cv2.imread('pictures/doc_copy.jpg')
    for _ in range(4):
        images.append(image)
        image = rotate_image(image)

    hash1 = calculate_image_hash('pictures/doc.jpg')
    for hash2 in map(calculate_image_hash, images):
        if count_hash_difference(hash1, hash2) < 80:
            print('Совпадение')
            break
        print('Несовпадение')