import pygame

# Constants
TAPE_SIZE = 50
HEAD_POSITION = TAPE_SIZE // 2
CELL_WIDTH = 15
CELL_HEIGHT = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# State Definitions
STATE_IDLE = 'IDLE'
STATE_RUNNING = 'RUNNING'
STATE_STOPPED = 'STOPPED'

# Function to draw the tape
def draw_tape(screen, tape, head_pos, font):
    for i, cell in enumerate(tape):
        pygame.draw.rect(screen, WHITE, (i * CELL_WIDTH, 200, CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(screen, BLACK, (i * CELL_WIDTH, 200, CELL_WIDTH, CELL_HEIGHT), 2)
        text = font.render(cell, True, BLACK)
        screen.blit(text, (i * CELL_WIDTH + CELL_WIDTH // 4, 210))
    
    pygame.draw.line(screen, RED, 
                     (head_pos * CELL_WIDTH + CELL_WIDTH // 2, 200),
                     (head_pos * CELL_WIDTH + CELL_WIDTH // 2, 240), 3)

# Function to move the tape head
def move_head(head_pos, direction, tape_size):
    if direction == 'R':
        return (head_pos + 1) % tape_size
    elif direction == 'L':
        return (head_pos - 1) % tape_size
    return head_pos

# Function to apply 2's complement subtraction logic
def binary_subtraction(tape, head_pos):
    # Move the second input (subtracting part) to the tape
    while tape[head_pos] != ' ' and head_pos < len(tape):
        head_pos = move_head(head_pos, 'R', len(tape))

    # Flip bits (1's complement)
    for i in range(head_pos, len(tape)):
        tape[i] = '1' if tape[i] == '0' else '0'

    # Add 1 to LSB (least significant bit)
    if tape[head_pos] == '0':
        tape[head_pos] = '1'
    else:
        tape[head_pos] = '0'
        head_pos = move_head(head_pos, 'R', len(tape))
        while tape[head_pos] != ' ':
            if tape[head_pos] == '0':
                tape[head_pos] = '1'
                break
            else:
                tape[head_pos] = '0'
                head_pos = move_head(head_pos, 'R', len(tape))

    # Perform binary addition (call the addition function)
    binary_addition(tape, head_pos)
    
# Function for binary addition (the same as before)
def binary_addition(tape, head_pos):
    carry = 0
    while head_pos < len(tape):
        if tape[head_pos] == '0' and carry == 1:
            tape[head_pos] = '1'
            carry = 0
        elif tape[head_pos] == '1' and carry == 1:
            tape[head_pos] = '0'
            carry = 1
        elif tape[head_pos] == '0' and carry == 0:
            tape[head_pos] = '0'
        elif tape[head_pos] == '1' and carry == 0:
            tape[head_pos] = '1'

        head_pos = move_head(head_pos, 'R', len(tape))

    if carry == 1:
        tape[head_pos] = '1'

# Main Function to Run the Turing Machine
def run_turing_machine():
    pygame.init()
    screen = pygame.display.set_mode((TAPE_SIZE * CELL_WIDTH, 300))
    pygame.display.set_caption("Turing Machine: Binary Addition & Subtraction")
    font = pygame.font.SysFont(None, 32)

    tape = [' ' for _ in range(TAPE_SIZE)]
    tape[HEAD_POSITION] = '1'
    tape[HEAD_POSITION + 1] = '0'
    tape[HEAD_POSITION + 2] = '1'
    tape[HEAD_POSITION + 3] = '0'

    tape[HEAD_POSITION + 10] = '1'
    tape[HEAD_POSITION + 11] = '0'

    head_pos = HEAD_POSITION
    state = STATE_IDLE
    running = True
    operation = '+'  # Can switch to '-' for subtraction
    
    while running:
        screen.fill(BLUE)

        draw_tape(screen, tape, head_pos, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = STATE_RUNNING
                    operation = '+'
                if event.key == pygame.K_s:
                    state = STATE_RUNNING
                    operation = '-'

        if state == STATE_RUNNING:
            if operation == '+':
                binary_addition(tape, head_pos)
                state = STATE_STOPPED
            elif operation == '-':
                binary_subtraction(tape, head_pos)
                state = STATE_STOPPED

        pygame.display.flip()

    pygame.quit()

# Run the Turing Machine simulation
if __name__ == '__main__':
    run_turing_machine()
