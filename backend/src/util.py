from PIL import Image, ImageFilter

def preprocess_image(img):
    gray = img.convert('L')
    new_size = (int(gray.width * 1.5), int(gray.height * 1.5))
    resized = gray.resize(new_size, Image.LANCZOS)
    sharpened = resized.filter(ImageFilter.SHARPEN)
    sharpened = sharpened.filter(ImageFilter.SHARPEN)
    return sharpened