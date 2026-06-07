import random


class RoundManager:
    def __init__(self, images: list[str]):
        self.images = images

        self.remaining = []
        self.history = []
        self.history_index = None

    def start_round(self):
        self.remaining = self.images.copy()
        random.shuffle(self.remaining)

        self.history.clear()
        self.history_index = None

    def next_random_image(self):
        if not self.remaining:
            return None

        image = self.remaining.pop()

        self.history.append(image)

        return image

    def images_remaining(self):
        return len(self.remaining)

    def history_count(self):
        return len(self.history)

    def enter_history_mode(self):
        if not self.history:
            return None

        self.history_index = len(self.history) - 1

        return self.history[self.history_index]

    def history_previous(self):
        if self.history_index is None:
            return None

        if self.history_index > 0:
            self.history_index -= 1

        return self.history[self.history_index]

    def history_next(self):
        if self.history_index is None:
            return None

        if self.history_index < len(self.history) - 1:
            self.history_index += 1

        return self.history[self.history_index]