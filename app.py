from image_repository import ImageRepository
from round_manager import RoundManager
from main_window import MainWindow


def main():
    repository = ImageRepository(
        "images.yaml"
    )

    images = repository.load_images()

    round_manager = RoundManager(
        images
    )

    window = MainWindow(
        round_manager
    )

    window.run()


if __name__ == "__main__":
    main()