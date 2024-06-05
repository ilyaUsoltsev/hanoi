import tkinter as tk
import random
from functools import partial

# GLOBAL VARIABLES
disk_colors = [
    "AliceBlue", "#FAEBD7", "Aqua", "#7FFFD4", "Azure", "#F5F5DC", "Beige", "#FFE4C4",
    "Black", "#FFEBCD", "Blue", "#0000FF", "BlueViolet", "#8A2BE2", "Brown", "#A52A2A",
    "BurlyWood", "#DEB887", "CadetBlue", "#5F9EA0", "Chartreuse", "#7FFF00", "Chocolate",
    "#D2691E", "Coral", "#FF7F50", "CornflowerBlue", "#6495ED", "Cornsilk", "#FFF8DC",
    "Crimson", "#DC143C", "Cyan", "#00FFFF", "DarkBlue", "#00008B", "DarkCyan", "#008B8B",
    "DarkGoldenRod", "#B8860B", "DarkGray", "#A9A9A9", "DarkGreen", "#006400",
    "DarkKhaki", "#BDB76B", "DarkMagenta", "#8B008B", "DarkOliveGreen", "#556B2F",
    "DarkOrange", "#FF8C00", "DarkOrchid", "#9932CC", "DarkRed", "#8B0000",
    "DarkSalmon", "#E9967A", "DarkSeaGreen", "#8FBC8F", "DarkSlateBlue", "#483D8B",
    "DarkSlateGray", "#2F4F4F", "DarkTurquoise", "#00CED1", "DarkViolet", "#9400D3",
    "DeepPink", "#FF1493", "DeepSkyBlue", "#00BFFF", "DimGray", "#696969",
    "DodgerBlue", "#1E90FF", "FireBrick", "#B22222", "FloralWhite", "#FFFAF0",
    "ForestGreen", "#228B22", "Fuchsia", "#FF00FF", "Gainsboro", "#DCDCDC",
    "GhostWhite", "#F8F8FF", "Gold", "#FFD700", "GoldenRod", "#DAA520"
];
random.shuffle(disk_colors);

student_id = '70256421'
counter = 0
max_counter = 0
limit_counter = 1e20
state = []

def draw_state(canvas, state):
    tower_width = 100  # Adding some padding for visual spacing
    x_start = 10
    y_start = 350
    disc_height = 10

    for tower_index, tower in enumerate(state):
        x = x_start + tower_index * tower_width
        y = y_start

        # Draw each disc in the tower
        for disc in tower:
            # Width of the disc is proportional to its value
            disc_width = disc
            # Calculate the top-left corner of the rectangle
            x1 = x + (tower_width - disc_width) / 2
            y1 = y - disc_height
            # Calculate the bottom-right corner of the rectangle
            x2 = x1 + disc_width
            y2 = y
            # Draw the rectangle for the disc
            canvas.create_rectangle(x1, y1, x2, y2, fill=disk_colors[disc], outline="grey")
            # Move up to draw the next disc on top
            y -= disc_height

        # Draw the tower base
        canvas.create_line(x, y_start + 5, x + tower_width, y_start + 5, width=4)

def get_init_state():
    state = []
    for i in range(len(student_id)):
        number_of_disks = int(student_id[i])
        state.append([number_of_disks - idx + (8 - i) * 10 for idx in range(number_of_disks)])
    return state

# Initialize main window
root = tk.Tk()
root.title("Hanoi state Visualization")
canvas = tk.Canvas(root, width=1200, height=400, bg="white")
canvas.pack()


def move_in_state(from_rod, to_rod):
    global state
    global counter
    global limit_counter

    if counter >= limit_counter:
        return True
    
    disk = state[from_rod].pop()
    state[to_rod].append(disk)
    counter += 1
    return False


def hanoi(n, from_rod, to_rod, aux_rod):
    if n == 0:
        return
    hanoi(n - 1, from_rod, aux_rod, to_rod)
    is_limit_reached = move_in_state(from_rod, to_rod)
    if(is_limit_reached):
        return
    hanoi(n - 1, aux_rod, to_rod, from_rod)



def start_moving_discs():
    for i in range(len(student_id) - 1, 0, -1):
        from_rod = i
        to_rod = i - 1
        aux_rod = i - 2 if i == len(student_id) - 1 else i + 1
        hanoi(len(state[i]), from_rod, to_rod, aux_rod)

state = get_init_state()
draw_state(canvas, state)
# move all discs to the first rod and bring counter to the maximum value
start_moving_discs()
max_counter = counter
print(f"Total number of moves: {counter}")


def on_button_click(limit):
    global limit_counter    
    global counter
    global max_counter
    global state
    state = get_init_state()
    counter = 0 
    limit_counter = max_counter * limit / 100
    print(f"Limit counter: {limit_counter}")
    start_moving_discs()
    canvas.delete("all")
    draw_state(canvas, state)


# Start button and End Buttons
button = tk.Button(root, text="End", command=lambda: on_button_click(100))
button.pack(pady=20) 
button = tk.Button(root, text="Start", command=lambda: on_button_click(0))
button.pack(pady=20) 

def break_into_blocks(number_string, block_size):
    # Initialize an empty list to store the blocks
    blocks = []
    # Iterate over the string in steps of block_size
    for i in range(0, len(number_string), block_size):
        # Slice the string and convert to integer
        block = int(number_string[i:i + block_size])
        blocks.append(block)
    return blocks

# Break the string into blocks of two digits
for block in break_into_blocks(student_id, 2):
    button = tk.Button(root, text=str(block), command=partial(on_button_click, block))
    button.pack(pady=20)



root.mainloop()