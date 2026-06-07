# Bingo Caller with Iamges

This python desktop application can be used to displaying images at random without repeats during a bingo round. The current setup is based off:
* [Pokemon Bingo Cards 1](https://www.teacherspayteachers.com/Product/Pokemon-Bingo-30-Boards-25-Pictures-16028119) - Images in local directory `pokemon-1`
  * Center image is the "Free Space" so there will be no generated image for it 
* [Pokemon Bingo Cards 2](https://www.teacherspayteachers.com/Product/Pokemon-Bingo-30-Boards-25-Pictures-16028119) - Images in local directory `pokemon-2`
  * Center image is the "Free Space" so there will be no generated image for it

Your choice of images are loaded automatically from a configured directory, and previously shown images within the current round can be reviewed using a history browser.

## Features

* Load images from a configured directory
  * Automatic discovery of image files in subdirectories
* Random image selection with a counter of how many have been shown during the current round
* No duplicate images within a round
* Start a new round at any time
* Option to Browse previously shown images
* Keyboard-driven interface

---

# Requirements

## Python

Python 3.14 or newer is recommended.

## Dependencies

Install required packages:

```bash
pip install pillow pyyaml
```

Or run:
```bash
python -m pip install -r requirements.txt
```
If you have multiple python versions installed:
```bash
python3 -m pip install -r requirements.txt
```
---

# Configuration

The application uses an `images.yaml` file located in the same directory as `app.py` that defines where the images are for the bingo caller. You can configure the relative or absolute path of the image directory.

Below is an example of defining the image from the relative path of the project. Relative paths are resolved from the location of `app.py`.

```yaml
image_directory: pokemon-1
```

This tells the application to load all supported image files from the `pokemon-1` directory.

You may also specify a full path.

macOS / Linux:

```yaml
image_directory: /Users/username/path/to/images
```

Windows:

```yaml
image_directory: C:\Users\username\path\to\images
```
## Supported Image Formats

The application automatically loads:

* PNG (`.png`)
* JPEG (`.jpg`, `.jpeg`)
* GIF (`.gif`)
* BMP (`.bmp`)
* WebP (`.webp`)

Image discovery is recursive, meaning images contained in subdirectories are automatically included.

Example:

```text
pokemon/
├── gen1/
├── gen2/
├── gen3/
└── gen4/
```

All supported images within these folders will be discovered automatically.

---

# Running the Application

From the project directory:

```bash
python app.py
```
or
```bash
python3 app.py
```

---

# Controls

## Main Mode

| Key | Action                 |
| --- | ---------------------- |
| R   | Start a new round      |
| N   | Show next random image |
| H   | Browse image history   |
| Q   | Quit application       |

### Round Behavior

When a round starts:

1. All images become eligible.
2. Images are shuffled randomly.
3. Each image is shown at most once during the round.
4. When all images have been shown, the round is complete.
5. Press `R` to begin a new round.

---

## History Mode

Press `H` while in Main Mode.

| Key | Action              |
| --- | ------------------- |
| ←   | Previous image      |
| →   | Next image          |
| P   | Return to Main Mode |

History contains all images shown during the current round.

### Example Round

1. Launch the application using `python app.py` or `python3 app.py`
2. Press: `R` to start a round.
3. A random image appears.
4. Press: `N` to display another random image.
5. Press: `H` to review images already shown.
6. Press `←`(Previous) | `→` (Most Recent) to move through image history.
7. Press: `P` to return to Main Mode.
8. When all images have been shown or to start a new round, press: `R`

The history counter should reset to 1 and a starting image of the new round is displayed

# Troubleshooting
## "Image directory does not exist"
Verify that the path specified in `images.yaml` is correct.

Example with starting directory: `image_directory: pokemon-1`

Ensure the directory actually exists:

```text
bingo-caller/
├── app.py
├── images.yaml
└── pokemon-1/
...
```

## "No images found"

Verify that the configured directory contains supported image file types.

## Images appear too large or too small

Images are dynamically scaled based on the current window size.

The application automatically:
- Preserves aspect ratio
- Reserves space for status and help controls
- Adjusts image size when the window is resized

For larger image viewing, maximize the application window.

---
# Running tests

The project uses pytests to run unit/integration tests of the application. To run the pytest make sure your terminal is set to the current project repo to execute the following commands:
* Run all tests: `pytest`
* Run with rebose output: `pytest -v`
* Run with coverage run:
  * `pip install pytest-cov` - installs the coverage plugin
  * `pytest --cov=. --cov-report=term-missing`

## Test Coverage Overview
### Current Coverage
The automated test suite primarily validates:

* Round management logic
* History navigation logic
* YAML configuration loading
* Image file discovery
* Image viewer sizing calculations
* Error handling and edge cases

The following areas are intentionally excluded from unit testing:

* Actual Tkinter rendering behavior
* Keyboard event handling
* Window management performed by the operating system
* Manual visual verification of image appearance

These areas are better validated through manual testing because they depend on GUI framework behavior rather than application logic.

### RoundManager Tests (tests/test_round_manager.py)
Coverage includes:

#### Round Initialization
* Verifies a new round loads all available images.
* Verifies history is cleared when a new round starts.

#### Random Image Selection
* Verifies images are not repeated within a round.
* Verifies all images can be shown exactly once.
* Verifies `None` is returned when a round is exhausted.

#### History Tracking
* Verifies displayed images are added to history.
* Verifies history count is tracked correctly.
* Verifies remaining image count is tracked correctly.

#### History Navigation
* Verifies history mode begins with the most recently displayed image.
* Verifies navigation to previous images.
* Verifies navigation to more recent images.
* Verifies navigation stops correctly at the beginning of history.
* Verifies history mode cannot be entered when no images have been shown.

### ImageRepository Tests (tests/test_image_repository.py)
Coverage includes:

#### Configuration Loading
* Verifies YAML configuration files can be loaded.
* Verifies image directories are read correctly from configuration.

#### Image Discovery
* Verifies supported image files are discovered.
* Verifies image discovery works recursively through subdirectories.
* Verifies non-image files are ignored.
* Verifies discovered image lists are returned correctly.

#### Error Handling
* Verifies missing YAML files raise `FileNotFoundError`.
* Verifies missing `image_directory` configuration raises an exception.
* Verifies nonexistent image directories raise `FileNotFoundError`.
* Verifies empty image directories raise an exception.

#### Path Resolution
* Verifies relative paths are resolved relative to the YAML file location.
* Verifies absolute paths are supported.

### ImageViewer Tests (tests/test_image_viewer.py)
Coverage includes:

#### Image Loading
* Verifies images are opened correctly.
* Verifies image rendering is initiated correctly.

#### Dynamic Scaling
* Verifies image resizing logic is executed.
* Verifies image dimensions are calculated from the current window size.
* Verifies minimum display dimensions are enforced.

#### User Interface Updates
* Verifies the window title is updated with the current image name.
* Verifies the image label is updated with the rendered image.
* Verifies image references are retained to prevent Tkinter garbage collection issues.

#### Resilience
* Verifies rendering logic functions correctly for both large and small window dimensions.

---
### Manual Testing Checklist

Before using the application for Bingo, you should execute following workflow to verify the application's core behavior:

* Start a new round.
* Display multiple random images.
* Confirm images are not repeated within a round.
* Confirm all images become available again after starting a new round.
* Enter history mode.
* Navigate backward and forward through history.
* Return to main mode.
* Resize the application window.
* Verify images resize appropriately.
* Verify status and help text remain visible.
* Verify application exits cleanly.

---
# Future Enhancements - Whenever I get free time from parenting

Potential future improvements:

* Multiple image directories
* Image categories and tags
* Persistent history between sessions
* Slideshow mode
* Guess-before-reveal mode
* Favorites and ratings
* Full-screen display
* Smoother dynamic rendering when resizing the window

---
# More Nitty Gritty Details
## Project Structure
```text
bingo-image-caller/
├── app.py
├── image_repository.py
├── round_manager.py
├── image_viewer.py
├── main_window.py
├── images.yaml
└── pokemon-1/
    └── ...png
└── pokemon-2/
    └── ...png

```

### Components
#### app.py
Application entry point.

Responsibilities:
* Load application configuration
* Create application components
* Start the user interface


#### image_repository.py
Image discovery and configuration loading

Responsibilities:
* Read `images.yaml`
* Locate image directories
* Find supported image files


#### round_manager.py
Core application logic

Responsibilities:
* Start new rounds
* Randomize image order
* Prevent duplicate images within a round
* Track image history
* Support history navigation


#### image_viewer.py
Image display functionality.

Responsibilities:
* Load images
* Resize images to fit the window
* Display images using Tkinter


#### main_window.py
Main User interface 

Responsibilities:
* Create application window
* Handle keyboard input
* Coordinate UI interactions with the round manager