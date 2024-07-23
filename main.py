import tkinter as tk
import random

class BreakoutGame:
    def __init__(self, root):
        self.window = root
        self.window.title("Breakout Game")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=500, height=400, bg="black")
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(0, 390, 80, 400, fill="white")
        self.paddle_speed = 20

        self.ball = self.canvas.create_oval(240, 240, 260, 260, fill="red")
        self.ball_speed_x = random.choice([-4, -3, -2, 2, 3, 4])
        self.ball_speed_y = -4

        self.bricks = [self.canvas.create_rectangle(j * (500 // 7), i * 20, (j + 1) * (500 // 7), (i + 1) * 20, fill="blue")
                       for i in range(5) for j in range(7)]
        self.score = 0

        self.setup_controls()
        self.move_ball()

    def setup_controls(self):
        self.window.bind("<Left>", self.move_paddle)
        self.window.bind("<Right>", self.move_paddle)
        self.window.bind("<r>", self.restart_game)
        self.window.bind("<q>", self.quit_game)

    def move_paddle(self, event):
        direction = -self.paddle_speed if event.keysym == "Left" else self.paddle_speed
        self.canvas.move(self.paddle, direction, 0)
        paddle_pos = self.canvas.coords(self.paddle)
        if paddle_pos[0] < 0:
            self.canvas.move(self.paddle, -paddle_pos[0], 0)
        elif paddle_pos[2] > 500:
            self.canvas.move(self.paddle, 500 - paddle_pos[2], 0)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        ball_pos = self.canvas.coords(self.ball)
        paddle_pos = self.canvas.coords(self.paddle)

        if ball_pos[0] <= 0 or ball_pos[2] >= 500:
            self.ball_speed_x = -self.ball_speed_x
        if ball_pos[1] <= 0:
            self.ball_speed_y = -self.ball_speed_y
        if ball_pos[3] >= 400:
            self.game_over("Game Over")
            return

        if paddle_pos[0] <= ball_pos[2] <= paddle_pos[2] and paddle_pos[1] <= ball_pos[3] <= paddle_pos[3]:
            self.ball_speed_y = -self.ball_speed_y

        for brick in self.bricks:
            brick_pos = self.canvas.coords(brick)
            if brick_pos[0] <= ball_pos[2] <= brick_pos[2] and brick_pos[1] <= ball_pos[3] <= brick_pos[3]:
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_speed_y = -self.ball_speed_y
                self.score += 10
                break

        if not self.bricks:
            self.game_over("You Win!")

        self.window.after(20, self.move_ball)

    def game_over(self, message):
        self.canvas.create_text(250, 200, text=message, fill="white", font=("Helvetica", 24))
        self.canvas.create_text(250, 240, text=f"Score: {self.score}", fill="white", font=("Helvetica", 16))
        self.window.unbind("<Left>")
        self.window.unbind("<Right>")

    def restart_game(self, event=None):
        self.canvas.delete("all")
        self.__init__(self.window)

    def quit_game(self, event=None):
        self.window.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()
