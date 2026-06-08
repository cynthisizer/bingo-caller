# Tests

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

