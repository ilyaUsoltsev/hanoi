import tkinter as tk
import random
from functools import partial
class HanoiModel:
    def __init__(self, student_id):
        self.student_id = student_id
        self.state = self.get_init_state()
        self.counter = 0
        self.max_counter = 0
        self.limit_counter = 1e10
    
    def get_init_state(self):
        state = []
        for i in range(len(self.student_id)):
            number_of_disks = int(self.student_id[i])
            state.append([number_of_disks - idx + (8 - i) * 10 for idx in range(number_of_disks)])
        return state
    
    def set_student_id(self, student_id):
        self.student_id = student_id
        self.state = self.get_init_state()
        self.counter = 0
        self.max_counter = 0
        self.limit_counter = 1e10
    
    def move_in_state(self, from_rod, to_rod):
        if self.counter >= self.limit_counter:
            return True
        disk = self.state[from_rod].pop()
        self.state[to_rod].append(disk)
        self.counter += 1
        return False
    
    def hanoi(self, n, from_rod, to_rod, aux_rod):
        if n == 0:
            return
        self.hanoi(n - 1, from_rod, aux_rod, to_rod)
        is_limit_reached = self.move_in_state(from_rod, to_rod)
        if(is_limit_reached):
            return
        self.hanoi(n - 1, aux_rod, to_rod, from_rod)

    def reset_state(self):
        self.state = self.get_init_state()
        self.counter = 0
        
    def set_max_counter(self):
        self.max_counter = self.counter
        print(self.max_counter)
        
    def set_limit_counter(self, limit):
        self.limit_counter = self.max_counter * limit / 100
        print(self.limit_counter, 'limit counter')
        
    def start_moving_discs(self):
        for i in range(len(self.student_id) - 1, 0, -1):
            from_rod = i
            to_rod = i - 1
            aux_rod = i - 2 if i == len(self.student_id) - 1 else i + 1
            self.hanoi(len(self.state[i]), from_rod, to_rod, aux_rod)


class HanoiView:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.grid(row=0, columnspan=10, padx=10, pady=20)
        self.disk_colors = [
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
        random.shuffle(self.disk_colors)
    
    def draw_state(self):
        self.canvas.delete("all")
        tower_width = 100
        x_start = 10
        y_start = 350
        disc_height = 10
        
        for tower_index, tower in enumerate(self.model.state):
            x = x_start + tower_index * tower_width
            y = y_start
            for disc in tower:
                disc_width = disc
                x1 = x + (tower_width - disc_width) / 2
                y1 = y - disc_height
                x2 = x1 + disc_width
                y2 = y
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.disk_colors[disc], outline="grey")
                y -= disc_height
            self.canvas.create_line(x, y_start + 5, x + tower_width, y_start + 5, width=4)

    # make from '12345678' to [12, 34, 56, 78]
    def break_into_blocks(self, number_string, block_size):
        blocks = []
        for i in range(0, len(number_string), block_size):
            block = int(number_string[i:i + block_size])
            blocks.append(block)
        return blocks
    
class HanoiController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def start(self):
        self.model.start_moving_discs()
        self.model.set_max_counter()
        self.model.reset_state()
        self.view.draw_state()
        self.create_buttons_and_inputs()
        

    def move_disks(self, limit):
        self.model.reset_state()
        self.model.set_limit_counter(limit)
        self.model.start_moving_discs()
        self.view.draw_state()
        
    def restrict_input(self, entry, event):
        # Allow only numeric input and limit to two characters
        valid_keys = "0123456789"
        content = entry.get()
        if len(content) >= 2 and event.keysym not in ["Delete", "BackSpace"]:
            return "break"
        if event.char not in valid_keys and event.keysym not in ["Delete", "BackSpace", "Return"]:
            return "break"
        
    def format_and_print(self, entry, block_index, event):
        content = entry.get()
        if(len(content) == 0):
            content = '00'
        if(len(content) == 1):
            content = '0' + content
        two_digit_blocks = self.view.break_into_blocks(self.model.student_id, 2);
        two_digit_blocks[block_index] = content
        self.model.set_student_id(''.join(map(str, two_digit_blocks)))
        print(self.model.student_id)
        self.start()
        
    def create_buttons_and_inputs(self):
        # Start making inputs
        two_digit_blocks = self.view.break_into_blocks(self.model.student_id, 2);
        for block_index, two_digits in enumerate(two_digit_blocks):
            text_var = tk.StringVar()
            text_var.set(str(two_digits))
            entry = tk.Entry(self.view.root, textvariable=text_var)
            entry.grid(row=1, column=block_index + 1, padx=10, pady=20)
            # Bind the keypress event to restrict input to numeric and limit length
            entry.bind("<KeyPress>", partial(self.restrict_input, entry))
            # Bind the Return (Enter) key to process and print the input
            entry.bind("<Return>", partial(self.format_and_print, entry, block_index))
            
        # End making inputs
        
        # Start of making buttons
        start_button = tk.Button(self.view.root, text="Start", command=lambda: self.move_disks(0))
        start_button.grid(row=2, column=0, padx=10, pady=20)
        
        two_digit_blocks = self.view.break_into_blocks(self.model.student_id, 2);
        for block_index, two_digits in enumerate(two_digit_blocks):
            button = tk.Button(self.view.root, text=f"# {block_index+1}", command=partial(self.move_disks, two_digits))
            button.grid(row=2, column=block_index + 1, padx=10, pady=20)
        
        end_button = tk.Button(self.view.root, text="End", command=lambda: self.move_disks(100))
        end_button.grid(row=2, column=len(two_digit_blocks)+1, padx=10, pady=20)
        # End of making buttons

def main():
    # Init model, view and controller
    # Create a tkinter window
    # Show init state, calculate the max counter and reset the state
    root = tk.Tk()
    root.title("Hanoi state Visualization")
    student_id = '70256421'
    model = HanoiModel(student_id)
    view = HanoiView(root, model)
    controller = HanoiController(model, view)
    controller.start()
    root.mainloop()

if __name__ == "__main__":
    main()
