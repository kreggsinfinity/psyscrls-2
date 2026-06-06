from PIL import Image

img_path = r"c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube bots automation\PsychologyScrolls\Psychology Scrolls.png"
img = Image.open(img_path)
print(f"Dimensions: {img.size}")
# Look for non-black pixels to find the logo position
bbox = img.getbbox()
print(f"BBox of non-black content: {bbox}")
