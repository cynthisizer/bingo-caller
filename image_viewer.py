from pathlib import Path

from PIL import Image
from PIL import ImageTk


class ImageViewer:
    def __init__(self, root, image_label):
        self.root = root
        self.image_label = image_label
        self.current_photo = None

    def show(self, image_path: str):
        # Make sure geometry has been calculated.
        self.root.update_idletasks()

        image = Image.open(image_path)

        # Reserve space for controls.
        available_width = max(
            self.root.winfo_width() - 40,
            400
        )

        available_height = max(
            self.root.winfo_height() - 220,
            300
        )

        image.thumbnail(
            (
                available_width,
                available_height
            )
        )

        self.current_photo = ImageTk.PhotoImage(
            image
        )

        self.image_label.config(
            image=self.current_photo
        )

        self.root.title(
            Path(image_path).name
        )