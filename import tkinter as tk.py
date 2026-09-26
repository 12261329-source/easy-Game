import tkinter as tk
import random

# ===== 設定 =====
WIDTH = 600
HEIGHT = 400
CELL = 20

# ===== ウィンドウ =====
root = tk.Tk()
root.title("Python スネークゲーム")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ===== 初期状態 =====
snake = [
    [300, 200],
    [280, 200],
    [260, 200]
]

direction = "Right"
next_direction = "Right"

score = 0
game_over = False

# ===== エサを作る =====
def create_food():
    x = random.randrange(0, WIDTH, CELL)
    y = random.randrange(0, HEIGHT, CELL)
    return [x, y]

food = create_food()


# ===== キーボード操作 =====
def key_press(event):
    global next_direction

    if event.keysym == "Up" and direction != "Down":
        next_direction = "Up"

    elif event.keysym == "Down" and direction != "Up":
        next_direction = "Down"

    elif event.keysym == "Left" and direction != "Right":
        next_direction = "Left"

    elif event.keysym == "Right" and direction != "Left":
        next_direction = "Right"


root.bind("<KeyPress>", key_press)


# ===== 描画 =====
def draw():
    canvas.delete("all")

    # ヘビ
    for i, part in enumerate(snake):
        x, y = part

        if i == 0:
            canvas.create_rectangle(
                x, y, x + CELL, y + CELL,
                fill="lime"
            )
        else:
            canvas.create_rectangle(
                x, y, x + CELL, y + CELL,
                fill="green"
            )

    # エサ
    x, y = food
    canvas.create_oval(
        x, y,
        x + CELL, y + CELL,
        fill="red"
    )

    # スコア
    canvas.create_text(
        50, 20,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 14)
    )


# ===== ゲーム更新 =====
def update():
    global direction
    global food
    global score
    global game_over

    if game_over:
        return

    direction = next_direction

    # 頭の位置
    head_x, head_y = snake[0]

    if direction == "Up":
        head_y -= CELL

    elif direction == "Down":
        head_y += CELL

    elif direction == "Left":
        head_x -= CELL

    elif direction == "Right":
        head_x += CELL

    new_head = [head_x, head_y]

    # 壁にぶつかった
    if (
        head_x < 0
        or head_x >= WIDTH
        or head_y < 0
        or head_y >= HEIGHT
    ):
        end_game()
        return

    # 自分自身にぶつかった
    if new_head in snake:
        end_game()
        return

    # 頭を追加
    snake.insert(0, new_head)

    # エサを食べた
    if new_head == food:
        score += 1
        food = create_food()
    else:
        # 食べてなければ尻尾を削除
        snake.pop()

    draw()

    # 100msごとに更新
    root.after(100, update)


# ===== ゲームオーバー =====
def end_game():
    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="GAME OVER",
        fill="red",
        font=("Arial", 35, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 50,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 20)
    )


# ===== スタート =====
draw()
update()

root.mainloop()