from pathlib import Path
import pytest
import yaml
from image_repository import ImageRepository


def create_yaml(yaml_path, image_directory):
    yaml_path.write_text(
        yaml.dump(
            {
                "image_directory": str(image_directory)
            }
        )
    )

# Verify images are discovered by app
def test_load_images_from_directory(tmp_path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    (image_dir / "one.png").touch()
    (image_dir / "two.jpg").touch()
    yaml_file = tmp_path / "images.yaml"

    create_yaml(
        yaml_file,
        image_dir,
    )

    repo = ImageRepository(yaml_file)
    images = repo.load_images()

    assert len(images) == 2

# Verify Non-Image files are ingored
def test_ignore_non_image_files(tmp_path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    (image_dir / "one.png").touch()
    (image_dir / "notes.txt").touch()
    yaml_file = tmp_path / "images.yaml"

    create_yaml(
        yaml_file,
        image_dir,
    )

    repo = ImageRepository(yaml_file)
    images = repo.load_images()
    assert len(images) == 1

#Verify recursive directory image discovery
def test_recursive_image_discovery(tmp_path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()

    nested = image_dir / "gen1"
    nested.mkdir()
    (nested / "pikachu.png").touch()

    yaml_file = tmp_path / "images.yaml"
    create_yaml(
        yaml_file,
        image_dir,
    )
    repo = ImageRepository(yaml_file)
    images = repo.load_images()

    assert len(images) == 1

# Verify missing yaml file configurations
def test_missing_yaml_file():
    repo = ImageRepository(
        "does_not_exist.yaml"
    )

    with pytest.raises(FileNotFoundError):
        repo.load_images()

# Verify missing image directory
def test_missing_image_directory_key( tmp_path,):
    yaml_file = tmp_path / "images.yaml"
    yaml_file.write_text(
        yaml.dump({})
    )

    repo = ImageRepository(yaml_file)
    with pytest.raises(RuntimeError):
        repo.load_images()

# Verify directory does not exist throws error
def test_image_directory_does_not_exist(tmp_path, ):
    yaml_file = tmp_path / "images.yaml"

    yaml_file.write_text(
        yaml.dump(
            {
                "image_directory":
                "missing_folder"
            }
        )
    )

    repo = ImageRepository(yaml_file)
    with pytest.raises(FileNotFoundError):
        repo.load_images()

# Handle empty directories - must have some images
def test_empty_directory(tmp_path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()

    yaml_file = tmp_path / "images.yaml"
    create_yaml(
        yaml_file,
        image_dir,
    )

    repo = ImageRepository(yaml_file)
    with pytest.raises(RuntimeError):
        repo.load_images()

# Verify path resolutions
def test_relative_path_resolution(tmp_path,):
    image_dir = tmp_path / "pokemon"
    image_dir.mkdir()
    (image_dir / "pikachu.png").touch()

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    yaml_file = config_dir / "images.yaml"
    yaml_file.write_text(
        yaml.dump(
            {
                "image_directory":
                "../pokemon"
            }
        )
    )

    repo = ImageRepository(yaml_file)
    images = repo.load_images()

    assert len(images) == 1