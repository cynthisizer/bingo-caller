from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
from image_viewer import ImageViewer
import pytest

def create_mock_root():
    root = MagicMock()
    root.winfo_width.return_value = 1400
    root.winfo_height.return_value = 900

    return root

def test_constructor():
    root = MagicMock()
    label = MagicMock()

    viewer = ImageViewer(
        root,
        label
    )

    assert viewer.root is root
    assert viewer.image_label is label
    assert viewer.current_photo is None

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_updates_window_title(mock_open, mock_photo,):
    root = create_mock_root()
    label = MagicMock()
    image = MagicMock()

    mock_open.return_value = image

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "/tmp/pikachu.png"
    )

    root.title.assert_called_once_with(
        "pikachu.png"
    )

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_opens_image(
    mock_open,
    mock_photo,
):
    root = create_mock_root()

    label = MagicMock()

    image = MagicMock()

    mock_open.return_value = image

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "pikachu.png"
    )

    mock_open.assert_called_once_with(
        "pikachu.png"
    )

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_resizes_image(
    mock_open,
    mock_photo,
):
    root = create_mock_root()

    label = MagicMock()

    image = MagicMock()

    mock_open.return_value = image

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "pikachu.png"
    )

    image.thumbnail.assert_called_once()

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_uses_dynamic_window_size(
    mock_open,
    mock_photo,
):
    root = create_mock_root()
    label = MagicMock()
    image = MagicMock()

    mock_open.return_value = image

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "pikachu.png"
    )

    image.thumbnail.assert_called_once_with(
        (
            1360,
            680,
        )
    )

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_updates_label(
    mock_open,
    mock_photo,
):
    root = create_mock_root()
    label = MagicMock()
    image = MagicMock()
    photo = MagicMock()

    mock_open.return_value = image
    mock_photo.return_value = photo

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "pikachu.png"
    )

    label.config.assert_called_once_with(
        image=photo
    )

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_stores_photo_reference(
    mock_open,
    mock_photo,
):
    root = create_mock_root()
    label = MagicMock()
    image = MagicMock()
    photo = MagicMock()

    mock_open.return_value = image
    mock_photo.return_value = photo

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "pikachu.png"
    )

    assert viewer.current_photo is photo

@patch("image_viewer.ImageTk.PhotoImage")
@patch("image_viewer.Image.open")
def test_show_enforces_minimum_size(
    mock_open,
    mock_photo,
):
    root = MagicMock()
    root.winfo_width.return_value = 100
    root.winfo_height.return_value = 100
    label = MagicMock()
    image = MagicMock()

    mock_open.return_value = image

    viewer = ImageViewer(
        root,
        label
    )

    viewer.show(
        "pikachu.png"
    )

    image.thumbnail.assert_called_once_with(
        (
            400,
            300,
        )
    )