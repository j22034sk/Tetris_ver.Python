import tkinter as tk
import random

BLOCK_SIZE = 25
FIELD_WIDTH = 10
FIELD_HEIGHT = 20

MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2

class TetrisSquare():
    def __init__(self, x=0, y=0, color="#000000"):
        self.x = x
        self.y = y
        self.color = color

    def set_cord(self, x, y):
        self.x = x
        self.y = y

    def get_cord(self):
        return int(self.x), int(self.y)

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_moved_cord(self, direction):
        x, y = self.get_cord()
        if direction == MOVE_LEFT:
            return x - 1, y
        elif direction == MOVE_RIGHT:
            return x + 1, y
        elif direction == MOVE_DOWN:
            return x, y + 1
        else:
            return x, y

class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
        canvas_width = field.get_width() * BLOCK_SIZE
        canvas_height = field.get_height() * BLOCK_SIZE
        super().__init__(master, width=canvas_width, height=canvas_height, bg="#000000")
        self.place(x=25, y=25)
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="#000000", width=1,
                    fill=square.get_color()
                )
        self.before_field = field

    def update(self, field, block):
        new_field = TetrisField()
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                color = square.get_color()

                new_square = new_field.get_square(x, y)
                new_square.set_color(color)

        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                x, y = block_square.get_cord()
                color = block_square.get_color()

                new_field_square = new_field.get_square(x, y)
                new_field_square.set_color(color)

        for y in range(field.get_height()):
            for x in range(field.get_width()):
                new_square = new_field.get_square(x, y)
                new_color = new_square.get_color()

                before_square = self.before_field.get_square(x, y)
                before_color = before_square.get_color()
                if(new_color == before_color):
                    continue

                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(x1, y1, x2, y2, outline="#000000", width=1, fill=new_color)

        self.before_field = new_field

class TetrisField():
    def __init__(self):
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT
        self.squares = []
        for y in range(self.height):
            for x in range(self.width):
                self.squares.append(TetrisSquare(x, y, "#ffffff"))

    def clear_field(self):
        for square in self.squares:
            square.set_color("#ffffff")

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_squares(self):
        return self.squares

    def get_square(self, x, y):
        return self.squares[y * self.width + x]

    def judge_game_over(self, block):
        no_empty_cord = set(square.get_cord() for square
                            in self.get_squares() if square.get_color() != "#ffffff")

        block_cord = set(square.get_cord() for square
                         in block.get_squares())

        collision_set = no_empty_cord & block_cord

        if len(collision_set) == 0:
            ret = False
        else:
            ret = True

        return ret

    def judge_can_move(self, block, direction):
        no_empty_cord = set(square.get_cord() for square
                            in self.get_squares() if square.get_color() != "#ffffff")

        move_block_cord = set(square.get_moved_cord(direction) for square
                              in block.get_squares())

        for x, y in move_block_cord:
            if x < 0 or x >= self.width or \
                    y < 0 or y >= self.height:
                return False

        collision_set = no_empty_cord & move_block_cord

        if len(collision_set) == 0:
            ret = True
        else:
            ret = False

        return ret

    def fix_block(self, block):
        for square in block.get_squares():
            x, y = square.get_cord()
            color = square.get_color()
            field_square = self.get_square(x, y)
            field_square.set_color(color)

    def delete_line(self):
        for y in range(self.height):
            for x in range(self.width):
                square = self.get_square(x, y)
                if(square.get_color() == "#ffffff"):
                    break
            else:
                for down_y in range(y, 0, -1):
                    for x in range(self.width):
                        src_square = self.get_square(x, down_y - 1)
                        dst_square = self.get_square(x, down_y)
                        dst_square.set_color(src_square.get_color())
                for x in range(self.width):
                    square = self.get_square(x, 0)
                    square.set_color("#ffffff")

class TetrisBlock():
    def __init__(self):
        self.squares = []
        self.type = random.randint(1, 7)
        if self.type == 1:
            #水色(I)
            color = "#87ceeb"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2, 3],
            ]
        elif self.type == 2:
            #黄色(O)
            color = "#ffd700"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
        elif self.type == 3:
            #オレンジ(L)
            color = "#ff7f50"
            cords = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
            ]
        elif self.type == 4:
            #青(J)
            color = "#4682b4"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 - 1, 2],
            ]
        elif self.type == 5:
            #紫(T)
            color = "#9400d3"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 + 1, 1],
            ]
        elif self.type == 6:
            #赤(Z)
            color = "#dc143c"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 + 1, 1],
            ]
        elif self.type == 7:
            #緑(S)
            color = "#66cdaa"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 + 1, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 1],
            ]

        for cord in cords:
            self.squares.append(TetrisSquare(cord[0], cord[1], color))

    def get_squares(self):
        return self.squares

    def move(self, direction):
        for square in self.squares:
            x, y = square.get_cord()
            if direction == MOVE_LEFT:
                square.set_cord(x - 1, y)
            elif direction == MOVE_RIGHT:
                square.set_cord(x + 1, y)
            elif direction == MOVE_DOWN:
                square.set_cord(x, y + 1)

    def rotate(self, field):
        if self.type == 2:
            return
        pivot_square = self.squares[1]
        pivot_x, pivot_y = pivot_square.get_cord()
        new_squares = []
        for square in self.squares:
            x, y = square.get_cord()
            new_x = -(y - pivot_y) + pivot_x
            new_y = (x - pivot_x) + pivot_y
            new_squares.append(TetrisSquare(new_x, new_y, square.get_color()))
        for new_square in new_squares:
            x, y = new_square.get_cord()
            if x < 0 or x >= field.get_width() or \
                    y < 0 or y >= field.get_height() or \
                    field.get_square(x, y).get_color() != "#ffffff":
                return
        self.squares = new_squares

class EventHandller():
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.master.bind("<Left>", self.left_key_event)
        self.master.bind("<Right>", self.right_key_event)
        self.master.bind("<Down>", self.down_key_event)
        self.master.bind("<Up>", self.rotate_key_event)

    def left_key_event(self, event):
        if(self.game.field.judge_can_move(self.game.block, MOVE_LEFT)):
            self.game.block.move(MOVE_LEFT)
            self.game.canvas.update(self.game.field, self.game.block)

    def right_key_event(self, event):
        if(self.game.field.judge_can_move(self.game.block, MOVE_RIGHT)):
            self.game.block.move(MOVE_RIGHT)
            self.game.canvas.update(self.game.field, self.game.block)

    def down_key_event(self, event):
        if(self.game.field.judge_can_move(self.game.block, MOVE_DOWN)):
            self.game.block.move(MOVE_DOWN)
            self.game.canvas.update(self.game.field, self.game.block)

    def rotate_key_event(self, event):
        self.game.block.rotate(self.game.field)
        self.game.canvas.update(self.game.field, self.game.block)

class Game():
    def __init__(self, master):
        self.master = master
        self.field = TetrisField()
        self.canvas = TetrisCanvas(master, self.field)
        self.block = None
        self.event_handler = EventHandller(master, self)
        self.running = False

    def start_game(self):
        if not self.running:
            self.running = True
            self.field.clear_field()
            self.canvas.update(self.field, None)
            self.block = TetrisBlock()
            if(self.field.judge_game_over(self.block)):
                self.field.clear_field()
            self.canvas.update(self.field, self.block)
            self.timer()

    def stop_game(self):
        self.running = False
        self.field.clear_field()
        self.canvas.update(self.field, None)

    def timer(self):
        if not self.running:
            return

        if(self.field.judge_can_move(self.block, MOVE_DOWN)):
            self.block.move(MOVE_DOWN)
            self.canvas.update(self.field, self.block)
            self.canvas.after(400, self.timer)
        else:
            self.field.fix_block(self.block)
            self.field.delete_line()
            self.block = TetrisBlock()
            if(self.field.judge_game_over(self.block)):
                self.field.clear_field()
            self.canvas.update(self.field, self.block)
            self.canvas.after(400, self.timer)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("テトリス")
    root.geometry("400x600")
    root.configure(bg="#000000")

    game = Game(root)

    start_button = tk.Button(root, text="START", command=game.start_game, bg="#000000", fg="#ffffff", width=5, height=1, font=("Arial", 12))
    start_button.place(x=25 + BLOCK_SIZE * FIELD_WIDTH + 25, y=30)

    quit_button = tk.Button(root, text="QUIT", command=game.stop_game, bg="#000000", fg="#ffffff", width=5, height=1, font=("Arial", 12))
    quit_button.place(x=25 + BLOCK_SIZE * FIELD_WIDTH + 25, y=80)

    root.mainloop()
