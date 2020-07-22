from PIL import Image, ImageDraw


class ImageWorker:
    def __init__(self, path_to_image: str) -> None:
        photo = Image.open(path_to_image)
        width, height = Image.open(path_to_image).size
        self.transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        self.transparent.paste(photo, (0, 0))
        self.drawing = ImageDraw.Draw(self.transparent)

    def text_drawing(self, x_cordinate: int, y_cordinate: int, text: str, color: tuple, font) -> None:
        self.drawing.text((x_cordinate, y_cordinate), text, fill=color, font=font)

    def save(self, path: str) -> None:
        self.transparent.save(path)
