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