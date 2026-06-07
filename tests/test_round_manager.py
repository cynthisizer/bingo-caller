from round_manager import RoundManager

# Verify all images load
def test_start_round_loads_all_images(sample_images):
    manager = RoundManager(sample_images)
    manager.start_round()

    assert len(manager.remaining) == len(sample_images)
    assert manager.history == []

# Verify that round does not try to show duplicate images
def test_round_contains_no_duplicates(sample_images):
    manager = RoundManager(sample_images)
    manager.start_round()
    shown = []

    for _ in range(len(sample_images)):
        image = manager.next_random_image()
        shown.append(image)

    assert len(shown) == len(set(shown))


def test_round_returns_none_when_empty():
    manager = RoundManager(["one.png"])
    manager.start_round()
    manager.next_random_image()

    assert manager.next_random_image() is None


def test_history_tracks_images(sample_images):
    manager = RoundManager(sample_images)
    manager.start_round()
    image = manager.next_random_image()

    assert manager.history == [image]


def test_history_count(sample_images):
    manager = RoundManager(sample_images)
    manager.start_round()
    manager.next_random_image()
    manager.next_random_image()

    assert manager.history_count() == 2


def test_images_remaining(sample_images):
    manager = RoundManager(sample_images)
    manager.start_round()
    manager.next_random_image()

    assert manager.images_remaining() == (
        len(sample_images) - 1
    )


def test_enter_history_mode_starts_at_latest():
    manager = RoundManager(
        [
            "first.png",
            "second.png",
        ]
    )

    manager.start_round()
    first = manager.next_random_image()
    second = manager.next_random_image()
    latest = manager.enter_history_mode()

    assert latest == second


def test_history_previous_moves_back():
    manager = RoundManager(
        [
            "first.png",
            "second.png",
        ]
    )

    manager.start_round()
    first = manager.next_random_image()
    manager.next_random_image()
    manager.enter_history_mode()
    previous = manager.history_previous()

    assert previous == first


def test_history_previous_stops_at_beginning():
    manager = RoundManager(
        [
            "first.png",
            "second.png",
        ]
    )

    manager.start_round()
    first = manager.next_random_image()
    manager.next_random_image()
    manager.enter_history_mode()
    manager.history_previous()
    still_first = manager.history_previous()

    assert still_first == first


def test_history_next_moves_forward():
    manager = RoundManager(
        [
            "first.png",
            "second.png",
        ]
    )

    manager.start_round()
    first = manager.next_random_image()
    second = manager.next_random_image()
    manager.enter_history_mode()
    manager.history_previous()
    image = manager.history_next()

    assert image == second


def test_enter_history_mode_returns_none_when_empty():
    manager = RoundManager(["one.png"])
    result = manager.enter_history_mode()

    assert result is None