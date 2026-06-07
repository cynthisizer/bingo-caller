from enum import Enum
import tkinter as tk

from image_viewer import ImageViewer


class Mode(Enum):
    MAIN = "main"
    HISTORY = "history"


class MainWindow:
    def __init__(self, round_manager):
        self.round_manager = round_manager

        self.mode = Mode.MAIN

        self.root = tk.Tk()
        self.root.title("Random Image Rounds")

        #
        # Initial window size
        #
        self.root.geometry("1400x900")

        #
        # Image area
        #
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(
            fill="both",
            expand=True
        )

        #
        # Controls area
        #
        self.control_frame = tk.Frame(
            self.root,
            relief="ridge",
            bd=1
        )
        self.control_frame.pack(
            fill="x",
            side="bottom"
        )

        self.image_label = tk.Label(
            self.image_frame
        )
        self.image_label.pack(
            expand=True,
            padx=10,
            pady=10
        )

        self.status_label = tk.Label(
            self.control_frame,
            text="Press R to start a round",
            font=("Arial", 12)
        )
        self.status_label.pack(
            pady=(10, 5)
        )

        self.help_label = tk.Label(
            self.control_frame,
            justify="left",
            text=(
                "Main Mode\n"
                "N = Next Random Image\n"
                "R = New Round\n"
                "H = Browse History\n"
                "Q = Quit\n\n"
                "History Mode\n"
                "← Previous\n"
                "→ Next\n"
                "P Return"
            )
        )
        self.help_label.pack(
            pady=(0, 10)
        )

        self.viewer = ImageViewer(
            self.root,
            self.image_label
        )

        self.root.bind(
            "<Key>",
            self.handle_key
        )

    def start_round(self):
        self.round_manager.start_round()

        self.status_label.config(
            text=(
                f"New round started. "
                f"{self.round_manager.images_remaining()} "
                f"images available."
            )
        )

        self.show_next_image()

    def show_next_image(self):
        image = self.round_manager.next_random_image()

        if image is None:
            self.status_label.config(
                text=(
                    "Round complete. "
                    "Press R to start a new round."
                )
            )
            return

        self.viewer.show(image)

        self.status_label.config(
            text=(
                f"Remaining: "
                f"{self.round_manager.images_remaining()} | "
                f"History: "
                f"{self.round_manager.history_count()}"
            )
        )

    def enter_history_mode(self):
        image = self.round_manager.enter_history_mode()

        if image is None:
            self.status_label.config(
                text="No history available."
            )
            return

        self.mode = Mode.HISTORY

        self.viewer.show(image)

        self.status_label.config(
            text=(
                "History Mode | "
                "← Previous | → Next | P Return"
            )
        )

    def leave_history_mode(self):
        self.mode = Mode.MAIN

        self.status_label.config(
            text=(
                f"Main Mode | "
                f"History contains "
                f"{self.round_manager.history_count()} images"
            )
        )

    def history_previous(self):
        image = self.round_manager.history_previous()

        if image:
            self.viewer.show(image)

    def history_next(self):
        image = self.round_manager.history_next()

        if image:
            self.viewer.show(image)

    def handle_key(self, event):
        key = event.keysym.lower()

        if self.mode == Mode.MAIN:

            if key == "q":
                self.root.destroy()

            elif key == "r":
                self.start_round()

            elif key == "n":
                self.show_next_image()

            elif key == "h":
                self.enter_history_mode()

        elif self.mode == Mode.HISTORY:

            if key == "left":
                self.history_previous()

            elif key == "right":
                self.history_next()

            elif key == "p":
                self.leave_history_mode()

    def run(self):
        self.root.mainloop()