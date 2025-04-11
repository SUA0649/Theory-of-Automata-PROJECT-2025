import pygame
import math

"""
Keys (KYS)

/ => floating
// => rounds towards minus infinity
"""

#Initialize pygame
pygame.init()
width, height = 1200, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Turing machine for Binary Addition")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
font = pygame.font.Font(None, 36)

# Tape setup
TAPE_SIZE = 101
head_index = math.ceil(TAPE_SIZE/2)

Tapes = {
    "Input_1": ['_']*TAPE_SIZE,
    "Input_2": ['_']*TAPE_SIZE,
    "Output": ['_']*TAPE_SIZE
}

Tape_heads = {
    "Input_1": head_index,
    "Input_2": head_index,
    "Output": head_index
}

Tape_y_positions = {
    "Input_1": 100,
    "Input_2": 200,
    "Output": 300
}

#Animation parameters
cell_width = 60
center_cell_x = width // 2 - cell_width // 2 #center of a box to write at
visible_cells = 5 #How many cells i can see of each tape
steps = 60 #Frames in one second


#GPT gamme this formula for acceleration and deceleration between switching to and from boxes
def ease_in_out(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

def draw_tapes(offsets=None):
    screen.fill(WHITE)
    
    if offsets is None:
        offsets = {name: 0 for name in Tapes}
    
    for tape_name in Tapes:
        y = Tape_y_positions[tape_name]
        current_offset = offsets.get(tape_name, 0)
        
        # Draw tape label
        label_color = RED if current_offset != 0 else BLACK
        label = font.render(f"{tape_name.upper()}", True, label_color)
        screen.blit(label, (50, y - 40))
        
        # Draw tape cells
        for i in range(-visible_cells, visible_cells + 1):
            cell_pos = Tape_heads[tape_name] + i
            if 0 <= cell_pos < len(Tapes[tape_name]):
                cell_x = width // 2 + i * cell_width + current_offset
                
                # Highlight current head position
                if i == 0:
                    highlight_color = GREEN if current_offset != 0 else BLUE
                    pygame.draw.rect(screen, highlight_color, (cell_x - 2, y - 2, cell_width + 4, 54), 2)
                
                pygame.draw.rect(screen, BLACK, (cell_x, y, cell_width, 50), 2)
                text = font.render(Tapes[tape_name][cell_pos], True, BLACK)
                screen.blit(text, (cell_x + 20, y + 10))
        
        # Draw head
        head_x = width // 2 + 30
        head_color = RED if current_offset != 0 else BLACK
        pygame.draw.polygon(screen, head_color, [
            (head_x, y - 10),
            (head_x - 10, y - 30),
            (head_x + 10, y - 30)
        ])
    
    pygame.display.flip()

def move_head(tape_name, direction):
    """Move a single tape head"""
    offset = 0
    
    # Animate movement
    for step in range(steps):
        t = step / (steps - 1)
        eased_t = ease_in_out(t)
        offset = eased_t * cell_width * (-1 if direction == "Right" else 1)
        
        draw_tapes({tape_name: offset})
        pygame.time.delay(10)
    
    # Update head position after animation
    if direction == "Right":
        Tape_heads[tape_name] += 1
    elif direction == "Left":
        Tape_heads[tape_name] -= 1
    
    draw_tapes()

def move_two_heads(tape1, dir1, tape2, dir2):
    """Move two tape heads simultaneously"""
    offset1 = 0
    offset2 = 0
    
    # Animate movement
    for step in range(steps):
        t = step / (steps - 1)
        eased_t = ease_in_out(t)
        
        # Calculate offsets for both tapes
        offset1 = eased_t * cell_width * (-1 if dir1 == "Right" else 1)
        offset2 = eased_t * cell_width * (-1 if dir2 == "Right" else 1)
        
        draw_tapes({tape1: offset1, tape2: offset2})
        pygame.time.delay(10)
    
    # Update head positions after animation
    if dir1 == "Right":
        Tape_heads[tape1] += 1
    elif dir1 == "Left":
        Tape_heads[tape1] -= 1
        
    if dir2 == "Right":
        Tape_heads[tape2] += 1
    elif dir2 == "Left":
        Tape_heads[tape2] -= 1
    
    draw_tapes()

def get_input():
    input_text = ""
    active = True
    
    while active:
        screen.fill(BLACK)
        prompt = font.render("Enter the two binary digits in the form of (101+101):", True, WHITE)
        display_text = font.render(input_text, True, BLUE)
        screen.blit(prompt, (100, 100))
        screen.blit(display_text, (100, 160))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    
    return input_text

def initialize_tape(tape_name, input_str):
    pos = Tape_heads[tape_name]
    for char in input_str:
        Tapes[tape_name][pos] = char
        pos += 1

def setup_tape_2():
    i = Tape_heads["Input_1"]
    j = Tape_heads["Input_2"]
    
    # Find the '+' separator
    while i < len(Tapes["Input_1"]) and Tapes["Input_1"][i] != '+':
        i += 1
        move_head("Input_1", "Right")
    
    if i < len(Tapes["Input_1"]) and Tapes["Input_1"][i] == '+':
        Tapes["Input_1"][i] = '_'
        move_head("Input_1", "Right")
        i += 1
        
        # Copy the second number to Input_2
        while i < len(Tapes["Input_1"]) and Tapes["Input_1"][i] != '_':
            Tapes["Input_2"][j] = Tapes["Input_1"][i]    
            move_two_heads("Input_1", "Right", "Input_2", "Right")
            Tapes["Input_1"][i] = '_'
            i += 1
            j += 1
def move_three_heads(tape1, dir1, tape2, dir2, tape3, dir3):
    """Move all three tape heads simultaneously with independent directions"""
    offsets = {tape1: 0, tape2: 0, tape3: 0}
    
    # Animate movement
    for step in range(steps):
        t = step / (steps - 1)
        eased_t = ease_in_out(t)
        
        # Calculate offsets for all three tapes
        offsets[tape1] = eased_t * cell_width * (-1 if dir1 == "Right" else 1)
        offsets[tape2] = eased_t * cell_width * (-1 if dir2 == "Right" else 1)
        offsets[tape3] = eased_t * cell_width * (-1 if dir3 == "Right" else 1)
        
        draw_tapes(offsets)
        pygame.time.delay(10)
    
    # Update all head positions after animation
    if dir1 == "Right":
        Tape_heads[tape1] += 1
    elif dir1 == "Left":
        Tape_heads[tape1] -= 1
        
    if dir2 == "Right":
        Tape_heads[tape2] += 1
    elif dir2 == "Left":
        Tape_heads[tape2] -= 1
        
    if dir3 == "Right":
        Tape_heads[tape3] += 1
    elif dir3 == "Left":
        Tape_heads[tape3] -= 1
    
    draw_tapes()


def main():
    # Get user input
    user_input = get_input()
    
    # Initialize tapes
    initialize_tape("Input_1", user_input)
    setup_tape_2()
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Example usage of both movement functions
        # Move Input_1 right and Input_2 left simultaneously
        
        # Move Output tape separately
        move_three_heads("Input_1","Right","Input_2","Right","Output","Right")       
        
        running = False  # Just for demonstration
    
    pygame.quit()

if __name__ == "__main__":
    main()