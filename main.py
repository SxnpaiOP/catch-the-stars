
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label


class CatchStars(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.score = 0
        self.lives = 3
        self.stars = []
        self.started = False
        self.game_over = False
        self.basket_x = 0
        self.direction = 0
        self.timer = 0

        self.hud = Label(
            text="SCORE: 0       LIVES: 3",
            font_size="22sp",
            size_hint=(1, None),
            height=60,
            pos_hint={"top": 1}
        )
        self.add_widget(self.hud)

        self.message = Label(
            text="CATCH THE STARS\n\nClassic Arcade Game ⭐",
            font_size="27sp",
            bold=True,
            size_hint=(1, None),
            height=160,
            pos_hint={"center_y": .60}
        )
        self.add_widget(self.message)

        self.play = Button(
            text="START GAME",
            size_hint=(.55, .09),
            pos_hint={"center_x": .5, "center_y": .40}
        )
        self.play.bind(on_press=self.start_game)
        self.add_widget(self.play)

        self.left = Button(
            text="◀",
            font_size="32sp",
            size_hint=(.27, .09),
            pos_hint={"x": .04, "y": .02}
        )
        self.right = Button(
            text="▶",
            font_size="32sp",
            size_hint=(.27, .09),
            pos_hint={"right": .96, "y": .02}
        )

        self.left.bind(on_press=lambda x: self.move(-1))
        self.right.bind(on_press=lambda x: self.move(1))
        self.left.bind(on_release=lambda x: self.move(0))
        self.right.bind(on_release=lambda x: self.move(0))

        self.add_widget(self.left)
        self.add_widget(self.right)

        Clock.schedule_interval(self.update, 1 / 60)

    def move(self, direction):
        self.direction = direction

    def start_game(self, instance):
        self.score = 0
        self.lives = 3
        self.stars = []
        self.timer = 0
        self.basket_x = self.width / 2
        self.started = True
        self.game_over = False

        self.message.text = ""
        self.play.opacity = 0
        self.play.disabled = True

        self.update_hud()

    def update_hud(self):
        self.hud.text = (
            f"SCORE: {self.score}       LIVES: {self.lives}"
        )

    def finish_game(self):
        self.game_over = True
        self.started = False
        self.message.text = (
            "GAME OVER!\n\n"
            f"FINAL SCORE: {self.score}"
        )
        self.play.text = "PLAY AGAIN"
        self.play.opacity = 1
        self.play.disabled = False

    def update(self, dt):

        self.canvas.before.clear()

        with self.canvas.before:
            Color(.035, .055, .16, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Background stars
            Color(.35, .4, .65, 1)
            for i in range(25):
                x = (i * 73) % max(1, int(self.width))
                y = (i * 137) % max(1, int(self.height))
                Ellipse(pos=(x, y), size=(3, 3))

        if not self.started:
            return

        self.basket_x += self.direction * 450 * dt
        self.basket_x = max(
            45, min(self.width - 45, self.basket_x)
        )

        self.timer += dt

        if self.timer > max(.25, .8 - self.score * .008):
            self.stars.append({
                "x": random.randint(20, int(self.width - 20)),
                "y": self.height + 20,
                "speed": random.randint(180, 300) + self.score * 2,
                "bomb": random.random() < .22
            })
            self.timer = 0

        with self.canvas:

            # Basket
            Color(.1, .5, 1, 1)
            Rectangle(
                pos=(self.basket_x - 45, 105),
                size=(90, 24)
            )

            Color(1, 1, 1, 1)
            Rectangle(
                pos=(self.basket_x - 35, 124),
                size=(70, 4)
            )

            for obj in self.stars[:]:

                obj["y"] -= obj["speed"] * dt

                if obj["bomb"]:
                    Color(1, .12, .12, 1)
                    Ellipse(
                        pos=(obj["x"] - 14, obj["y"] - 14),
                        size=(28, 28)
                    )
                else:
                    Color(1, .85, .05, 1)
                    Ellipse(
                        pos=(obj["x"] - 13, obj["y"] - 13),
                        size=(26, 26)
                    )

                    Color(1, 1, 1, 1)
                    Ellipse(
                        pos=(obj["x"] - 5, obj["y"] - 5),
                        size=(10, 10)
                    )

                caught = (
                    abs(obj["x"] - self.basket_x) < 55
                    and abs(obj["y"] - 117) < 30
                )

                if caught:

                    if obj["bomb"]:
                        self.lives -= 1
                    else:
                        self.score += 1

                    self.stars.remove(obj)
                    self.update_hud()

                elif obj["y"] < 0:

                    if not obj["bomb"]:
                        self.lives -= 1
                        self.update_hud()

                    self.stars.remove(obj)

                if self.lives <= 0:
                    self.finish_game()
                    break


class CatchStarsApp(App):

    def build(self):
        self.title = "Catch The Stars"
        return CatchStars()


if __name__ == "__main__":
    CatchStarsApp().run()

