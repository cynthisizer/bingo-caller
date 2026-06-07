from pathlib import Path

import yaml

class ImageRepository:
    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".webp",
    }

    def __init__(self, yaml_file: str | Path):
        self.yaml_path = Path(yaml_file).expanduser().resolve()

    def load_images(self) -> list[str]:
        """
        Load all supported image files from the directory
        specified in the YAML configuration.
        """
        image_directory = self._load_image_directory()

        images = self._discover_images(image_directory)

        if not images:
            raise RuntimeError(
                f"No image files found in {image_directory}"
            )

        print(
            f"Loaded {len(images)} images "
            f"from {image_directory}"
        )

        return images

    def _load_image_directory(self) -> Path:
        """
        Read image_directory from YAML and return an
        absolute Path object.
        """
        if not self.yaml_path.exists():
            raise FileNotFoundError(
                f"YAML file does not exist: {self.yaml_path}"
            )

        with open(
            self.yaml_path,
            "r",
            encoding="utf-8"
        ) as file:
            config = yaml.safe_load(file)

        if not config:
            raise RuntimeError(
                f"Empty configuration file: {self.yaml_path}"
            )

        image_directory = config.get(
            "image_directory"
        )

        if not image_directory:
            raise RuntimeError(
                "Missing 'image_directory' in YAML file"
            )

        image_directory = Path(image_directory)

        #
        # Relative paths are resolved relative
        # to the YAML file location.
        #
        if not image_directory.is_absolute():
            image_directory = (
                self.yaml_path.parent
                / image_directory
            )

        image_directory = image_directory.resolve()

        if not image_directory.exists():
            raise FileNotFoundError(
                f"Image directory does not exist: "
                f"{image_directory}"
            )

        if not image_directory.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {image_directory}"
            )

        return image_directory

    def _discover_images(
        self,
        image_directory: Path
    ) -> list[str]:
        """
        Recursively discover supported image files.
        """
        images = [
            str(file)
            for file in image_directory.rglob("*")
            if file.is_file()
            and file.suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        ]

        images.sort()

        return images