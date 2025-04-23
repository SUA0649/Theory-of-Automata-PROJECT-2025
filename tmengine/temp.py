import pygame
import math

"""
Keys (KYS)

/ => floating
// => rounds towards minus infinity

pygame.display.flip(), just updates the changes made to screens

"""

#Initialize pygame
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Turing machine for Binary Addition")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
LIGHT_GREY = (211, 211, 211)
GAINSBORO = (220, 220, 220)
DIMGREY = (105, 105, 105)
font = pygame.font.SysFont('arial', size = 30)
font_2 = pygame.font.SysFont('courier',size = 30)
font_3 = pygame.font.SysFont('arial',bold = True, italic = True,size = 30)

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
    "Input_1": 200,
    "Input_2": 300,
    "Output": 400
}

#Animation parameters
cell_width = 60
center_cell_x = width // 2 - cell_width // 2 #center of a box to write at
visible_cells = 5 #How many cells i can see of each tape
steps = 80 #Frames in one second
Delay = 100

#Normal Variables 
Steps = 0
current_state = 'q0'
STATES = {
    'q0': 'Start - move to end',
    'q1': 'Find rightmost bits',
    'q2': 'Process addition',
    'q3': 'Handle carry',
    'q4': 'Final carry check',
    'q_accept': 'Accept state',
    'q_reject': 'Reject state'
}
operation = ""

String_Output = ["Accepted","Rejected"]


#GPT gamme this formula for acceleration and deceleration between switching to and from boxes
def ease_in_out(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

#Drawing each tape (in 1 frame)
def draw_tapes(offsets=None):
    

    #Since draw_tapes is being used many times in 1 second, I thought why not just use this for closing window (handling)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    screen.fill(LIGHT_GREY)
    
    #offset is essntial for smooth animation
    if offsets is None:
        offsets = {name: 0 for name in Tapes}
    
    for tape_name in Tapes:
        #Step_Label = font_4.render(f"Steps: {Steps}",True,)

        y = Tape_y_positions[tape_name]
        current_offset = offsets.get(tape_name, 0)
        
        #Draw tape label
        label_color = RED if current_offset != 0 else BLACK
        label = font_3.render(f"{tape_name.upper()}", True, label_color)
        screen.blit(label, (50, y))
        
        #Draw tape cells
        for i in range(-visible_cells, visible_cells + 1):
            cell_pos = Tape_heads[tape_name] + i
            if 0 <= cell_pos < len(Tapes[tape_name]):
                cell_x = width // 2 + i * cell_width + current_offset
                
                #Making a square and filling that square with black
                pygame.draw.rect(screen, BLACK, (cell_x, y, cell_width, 50))
                #Drawing its border
                pygame.draw.rect(screen, LIGHT_GREY, (cell_x, y, cell_width, 50), 2)
                
                #Highlight current head position
                if i == 0:
                    highlight_color = GREEN if current_offset != 0 else BLUE
                    pygame.draw.rect(screen, highlight_color, (cell_x - 1, y - 1, cell_width + 1, 52), 4)
                

                #Writing text with white Color
                text = font.render(Tapes[tape_name][cell_pos], True, WHITE)
                screen.blit(text, (cell_x + 20, y + 10))
        
        #Draw head(the arrow thingy)
        head_x = width // 2 + 30
        head_color = RED if current_offset != 0 else BLACK
        pygame.draw.polygon(screen, head_color, [
            (head_x, y - 10),
            (head_x - 10, y - 30),
            (head_x + 10, y - 30)
        ])

    state_text = font.render(f"State: {current_state} ({STATES[current_state]})", True, BLACK)
    screen.blit(state_text, (50, 500))
    
    pygame.display.flip()

def move_head(tape_name, direction):
    """Move a single tape head"""
    offset = 0
    
    # Animate movement
    for step in range(steps):
     
        #t is simulating time interval
        t = step / (steps - 1)
        
        
        eased_t = ease_in_out(t)

        #Multiplying by -1 because the tape itself moves left
        offset = eased_t * cell_width * (-1 if direction == "Right" else 1)
        
        draw_tapes({tape_name: offset})
        
        pygame.time.delay(10)
    
    # Update head position after animation
    if direction == "Right":
        Tape_heads[tape_name] += 1
    elif direction == "Left":
        Tape_heads[tape_name] -= 1
    
    draw_tapes()

    
    pygame.time.delay(Delay)

def move_two_heads(tape1, dir1, tape2, dir2):
    """Move two tape heads simultaneously"""
    
    offset1 = 0
    offset2 = 0
    
    #Animate movement
    for step in range(steps):
        t = step / (steps - 1)
        eased_t = ease_in_out(t)
        
        # Calculate offsets for both tapes
        offset1 = eased_t * cell_width * (-1 if dir1 == "Right" else 1)
        offset2 = eased_t * cell_width * (-1 if dir2 == "Right" else 1)
        
        draw_tapes({tape1: offset1, tape2: offset2})
        pygame.time.delay(10)
    
    #Update head positions after animation
    if dir1 == "Right":
        Tape_heads[tape1] += 1
    elif dir1 == "Left":
        Tape_heads[tape1] -= 1
        
    if dir2 == "Right":
        Tape_heads[tape2] += 1
    elif dir2 == "Left":
        Tape_heads[tape2] -= 1
    
    draw_tapes()

    pygame.time.delay(Delay)

    
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

    
    pygame.time.delay(Delay)

def get_input():
    input_text = ""
    active = True
    
    while active:
        screen.fill(BLACK)
        prompt = font.render("Enter the two binary digits in the form of (101+101):", True, WHITE)
        display_text = font.render(input_text, True, CYAN)
        
        #(100,100) here = x and y co-ordinates
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
            Tapes["Input_1"][i] = '_'
            move_two_heads("Input_1", "Right", "Input_2", "Right")
            i += 1
            j += 1

    while i >= 0 and Tapes["Input_1"][i-1] == '_':
        i -= 1
        move_head("Input_1", "Left")


def binary_addition_turing():
    global current_state
    carry = '0'
    current_state = 'q0'
    
    # State machine implementation
    while current_state not in ['q_accept', 'q_reject']:
        draw_tapes()
        pygame.time.delay(500)
        
        if current_state == 'q0':
            # Validate input before processing
            valid = True
            for tape in ["Input_1", "Input_2"]:
                pos = Tape_heads[tape]
                while pos < len(Tapes[tape]) and Tapes[tape][pos] != '_':
                    if Tapes[tape][pos] not in ['0', '1']:
                        valid = False
                        break
                    pos += 1
            
            if not valid:
                current_state = 'q_reject'
                continue
                
            # Move all heads to the rightmost digit
            for tape in ["Input_1", "Input_2"]:
                while Tapes[tape][Tape_heads[tape]] != '_':
                    move_head(tape, "Right")
                    pygame.time.delay(200)
                move_head(tape, "Left")
                pygame.time.delay(200)
            current_state = 'q1'
            
        elif current_state == 'q1':
            # Check if we've processed all digits
            a = Tapes["Input_1"][Tape_heads["Input_1"]]
            b = Tapes["Input_2"][Tape_heads["Input_2"]]
            
            if a == '_' and b == '_':
                current_state = 'q4'
            else:
                current_state = 'q2'
            pygame.time.delay(300)
                
        elif current_state == 'q2':
            # Get current digits
            a = Tapes["Input_1"][Tape_heads["Input_1"]] if Tapes["Input_1"][Tape_heads["Input_1"]] != '_' else '0'
            b = Tapes["Input_2"][Tape_heads["Input_2"]] if Tapes["Input_2"][Tape_heads["Input_2"]] != '_' else '0'
            
            # Additional input validation during processing
            if a not in ['0', '1'] or b not in ['0', '1']:
                current_state = 'q_reject'
                continue
                
            sum_bits = int(a) + int(b) + int(carry)
            result = str(sum_bits % 2)
            carry = '1' if sum_bits > 1 else '0'
            
            Tapes["Output"][Tape_heads["Output"]] = result
            draw_tapes()
            pygame.time.delay(500)
            
            if Tapes["Input_1"][Tape_heads["Input_1"]] != '_':
                Tapes["Input_1"][Tape_heads["Input_1"]] = '_'
            if Tapes["Input_2"][Tape_heads["Input_2"]] != '_':
                Tapes["Input_2"][Tape_heads["Input_2"]] = '_'
            draw_tapes()
            pygame.time.delay(300)
            
            current_state = 'q3'
            
        elif current_state == 'q3':
            move_three_heads("Input_1", "Left", "Input_2", "Left", "Output", "Left")
            pygame.time.delay(400)
            current_state = 'q1'
            
        elif current_state == 'q4':
            if carry == '1':
                Tapes["Output"][Tape_heads["Output"]] = '1'
                draw_tapes()
                pygame.time.delay(500)
                move_head("Output", "Left")
                pygame.time.delay(300)
            current_state = 'q_accept'
    
    # Final state handling
    if current_state == 'q_accept':
        while Tapes["Output"][Tape_heads["Output"]] == '_':
            move_head("Output", "Right")
            pygame.time.delay(200)
        pygame.time.delay(300)
        
        result_text = font.render("Addition Complete!", True, GREEN)
        screen.blit(result_text, (width//2 - 100, 550))
    elif current_state == 'q_reject':
        draw_tapes()
        error_text = font.render("Invalid Input - Rejected!", True, RED)
        screen.blit(error_text, (width//2 - 150, 550))
    
    pygame.display.flip()
    pygame.time.delay(2000)



        
def perform_operation():
    """Perform the appropriate operation based on the operand"""
    
    if operation == '+':
        binary_addition_turing()
    elif operation == '-':
        pass  # Will implement subtraction later
    elif operation == '*':
        pass  # Will implement multiplication later
    else:
        raise ValueError("Unsupported operation")

def set_operation():
    global operation
    for symbol in Tapes["Input_1"]:
        if symbol == '+':
            operation = '+'
            break


def main():
    # Get user input
    user_input = get_input()
    
    # Initialize tapes
    initialize_tape("Input_1", user_input)
    set_operation()
    
    setup_tape_2()
    # Perform the operation
    perform_operation()

if __name__ == "__main__":
    main()