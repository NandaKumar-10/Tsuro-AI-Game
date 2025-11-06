import pygame
import random
import math
from tile_data import tiles
pygame.init()

FPS = 60
WIN_WIDTH = 1200
WIN_HEIGHT = 800
GRID_SIZE = 6
CELL_SIZE = 90
GRID_LENGTH = GRID_SIZE * CELL_SIZE

BLUE = (109, 185, 252)
BROWN = (139, 69, 19)
DARK_BROWN = (100, 50, 10)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

GRID_X = 100
GRID_Y = (WIN_HEIGHT - GRID_LENGTH) // 2

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tsuro")

player_img = pygame.image.load("player_king.png")
comp_img = pygame.image.load("comp_king.png")
player_img = pygame.transform.scale(player_img, (50, 50))
comp_img = pygame.transform.scale(comp_img, (50, 50))

class GridBox:
    def __init__(self, row, col, rect):
        self.row = row
        self.col = col
        self.rect = rect
        self.tile = None

    def get_tile_ports_rects(self):
        x, y = self.rect.topleft
        w, h = self.rect.size
        
        offset_from_edge = 8
        pos1 = w // 3
        pos2 = 2 * w // 3
        
        return {
            0: (x + pos1, y + offset_from_edge),
            1: (x + pos2, y + offset_from_edge),
            
            2: (x + w - offset_from_edge, y + pos1),
            3: (x + w - offset_from_edge, y + pos2),
            
            4: (x + pos2, y + h - offset_from_edge),
            5: (x + pos1, y + h - offset_from_edge),

            6: (x + offset_from_edge, y + pos2),
            7: (x + offset_from_edge, y + pos1)
        }


grid = []
for r in range(GRID_SIZE):
    row = []
    for c in range(GRID_SIZE):
        rect = pygame.Rect(GRID_X + c * CELL_SIZE, GRID_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        row.append(GridBox(r, c, rect))
    grid.append(row)


def rotate_port(port, rotation):
    rotations = rotation // 90
    for _ in range(rotations):
        port = (port + 2) % 8
    return port


def rotate_connectivity(connectivity, rotation):
    if rotation == 0:
        return connectivity
    return [(rotate_port(a, rotation), rotate_port(b, rotation)) for a, b in connectivity]

class Piece:
    def __init__(self, row, col, port, image, edge_pos):
        self.row = row
        self.col = col
        self.port = port
        self.image = image
        self.edge_pos = edge_pos
        self.on_board = False
        self.alive = True
        self.exit_port = None

    def try_enter_board(self, grid):
        if self.on_board:
            return False
        
        tile = grid[self.row][self.col].tile
        if tile:
            self.on_board = True
            print(f"Position: ({self.row}, {self.col})")
            print(f"Entry port: {self.port}")
            print(f"Tile rotation: {tile.rotation}")
            print(f"Original connectivity: {tile.connectivity}")
            rotated = rotate_connectivity(tile.connectivity, tile.rotation)
            print(f"Rotated connectivity: {rotated}")
            
            found = False
            for conn in rotated:
                if self.port in conn:
                    exit_port = conn[1] if conn[0] == self.port else conn[0]
                    print(f"Entry port {self.port} connects to exit port {exit_port}")
                    found = True
                    break
            if not found:
                print(f"WARNING: Entry port {self.port} has NO CONNECTION in this tile!")
            return True
        return False

    def move(self, grid):
        if not self.on_board:
            return False
            
        tile = grid[self.row][self.col].tile
        if tile is None:
            print(f"ERROR: No tile at current position ({self.row}, {self.col})")
            return False

        rotated_conn = rotate_connectivity(tile.connectivity, tile.rotation)

        exit_point = None
        for conn in rotated_conn:
            if self.port in conn:
                exit_point = conn[1] if conn[0] == self.port else conn[0]
                break
        
        if exit_point is None:
            print(f"ERROR: Port {self.port} has no connection at ({self.row}, {self.col})")
            print(f"  Tile rotation: {tile.rotation}°")
            print(f"  Rotated connectivity: {rotated_conn}")
            return False

        print(f"At ({self.row},{self.col}) port {self.port} -> exiting port {exit_point}")

        port_mapping = {
            0: (-1, 0, 5),
            1: (-1, 0, 4), 
            2: (0, 1, 7),   
            3: (0, 1, 6),
            4: (1, 0, 1),   
            5: (1, 0, 0),   
            6: (0, -1, 3),   
            7: (0, -1, 2),
        }
        
        if exit_point not in port_mapping:
            print(f"Invalid exit point: {exit_point}")
            return False
            
        dr, dc, new_port = port_mapping[exit_point]
        new_row = self.row + dr
        new_col = self.col + dc

        print(f"  -> Moving to ({new_row},{new_col}) port {new_port}")

        if not (0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE):
            print(f"Piece exited board at port {exit_point}!")
            self.on_board = False
            self.alive = True
            self.exit_port = exit_point
            self.calculate_exit_position()
            return False

        self.row = new_row
        self.col = new_col
        self.port = new_port
        
        neighbor_tile = grid[new_row][new_col].tile
        if neighbor_tile:
            return True 
        else:
            print(f"  -> No tile at ({new_row},{new_col}), waiting")
            return False

    def calculate_exit_position(self):
        if self.exit_port in [0, 1]:
            cell_x = GRID_X + self.col * CELL_SIZE
            if self.exit_port == 0:
                x = cell_x + CELL_SIZE // 3
            else:
                x = cell_x + 2 * CELL_SIZE // 3
            y = GRID_Y - 15
            self.edge_pos = (x, y)
        elif self.exit_port in [2, 3]:
            cell_y = GRID_Y + self.row * CELL_SIZE
            if self.exit_port == 2:
                y = cell_y + CELL_SIZE // 3
            else:
                y = cell_y + 2 * CELL_SIZE // 3
            x = GRID_X + GRID_LENGTH + 15
            self.edge_pos = (x, y)
        elif self.exit_port in [4, 5]:  
            cell_x = GRID_X + self.col * CELL_SIZE
            if self.exit_port == 5:
                x = cell_x + CELL_SIZE // 3
            else:
                x = cell_x + 2 * CELL_SIZE // 3
            y = GRID_Y + GRID_LENGTH + 15
            self.edge_pos = (x, y)
        elif self.exit_port in [6, 7]:
            cell_y = GRID_Y + self.row * CELL_SIZE
            if self.exit_port == 7:
                y = cell_y + CELL_SIZE // 3
            else:
                y = cell_y + 2 * CELL_SIZE // 3
            x = GRID_X - 15
            self.edge_pos = (x, y)

    def copy(self):
        new_piece = Piece(self.row, self.col, self.port, self.image, self.edge_pos)
        new_piece.on_board = self.on_board
        new_piece.alive = self.alive
        new_piece.exit_port = self.exit_port
        return new_piece

def euclidean_distance_to_center(row, col):
    center_row = (GRID_SIZE - 1) / 2
    center_col = (GRID_SIZE - 1) / 2
    return math.sqrt((row - center_row) ** 2 + (col - center_col) ** 2)

def distance_to_nearest_border(row, col):
    return min(row, col, GRID_SIZE - 1 - row, GRID_SIZE - 1 - col)

def simulate_tile_placement(piece, tile, rotation, grid):
    sim_grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c].tile:
                sim_grid[r][c] = type('obj', (object,), {
                    'tile': grid[r][c].tile,
                    'rotation': grid[r][c].tile.rotation,
                    'connectivity': grid[r][c].tile.connectivity
                })()
    
    sim_tile = type('obj', (object,), {
        'rotation': rotation,
        'connectivity': tile.connectivity
    })()
    
    if sim_grid[piece.row][piece.col] is None:
        sim_grid[piece.row][piece.col] = type('obj', (object,), {'tile': sim_tile})()
    else:
        sim_grid[piece.row][piece.col].tile = sim_tile
    
    sim_piece = piece.copy()
    
    if not sim_piece.on_board:
        tile_obj = sim_grid[sim_piece.row][sim_piece.col]
        if tile_obj and tile_obj.tile:
            sim_piece.on_board = True
    
    iterations = 0
    max_iterations = 50
    
    if sim_piece.on_board:
        moved = True
        while moved and iterations < max_iterations:
            iterations += 1
            
            tile_obj = sim_grid[sim_piece.row][sim_piece.col]
            if tile_obj is None or tile_obj.tile is None:
                break
            
            rotated_conn = rotate_connectivity(tile_obj.tile.connectivity, tile_obj.tile.rotation)
            
            exit_point = None
            for conn in rotated_conn:
                if sim_piece.port in conn:
                    exit_point = conn[1] if conn[0] == sim_piece.port else conn[0]
                    break
            
            if exit_point is None:
                break
            
            
            port_mapping = {
                0: (-1, 0, 5), 1: (-1, 0, 4), 2: (0, 1, 7), 3: (0, 1, 6),
                4: (1, 0, 1), 5: (1, 0, 0), 6: (0, -1, 3), 7: (0, -1, 2),
            }
            
            if exit_point not in port_mapping:
                break
            
            dr, dc, new_port = port_mapping[exit_point]
            new_row = sim_piece.row + dr
            new_col = sim_piece.col + dc
            
            if not (0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE):
                sim_piece.on_board = False
                return (sim_piece.row, sim_piece.col, False)  
            
            sim_piece.row = new_row
            sim_piece.col = new_col
            sim_piece.port = new_port
            
            neighbor_tile = sim_grid[new_row][new_col]
            if neighbor_tile is None or neighbor_tile.tile is None:
                moved = False
            else:
                moved = True
    
    return (sim_piece.row, sim_piece.col, sim_piece.on_board)


def ai_choose_best_tile(comp_piece, grid, available_tiles, difficulty):
    num_choices = min(difficulty * 2, len(available_tiles))
    if num_choices == 0:
        return None, 0
    
    candidate_tiles = random.sample(available_tiles, num_choices)
    
    print(f"\n AI Decision (Difficulty {difficulty})")
    print(f"AI piece at ({comp_piece.row}, {comp_piece.col}), port {comp_piece.port}")
    print(f"Current distance to center: {euclidean_distance_to_center(comp_piece.row, comp_piece.col):.2f}")
    print(f"Evaluating {num_choices} tiles...")
    
    best_tile = None
    best_rotation = 0
    best_score = float('-inf')
    
    current_dist_to_center = euclidean_distance_to_center(comp_piece.row, comp_piece.col)
    
    for tile in candidate_tiles:
        for rotation in [0, 90, 180, 270]:
            result = simulate_tile_placement(comp_piece, tile, rotation, grid)
            
            if result is None:
                continue
            
            final_row, final_col, on_board = result
            
            if not on_board:
                score = -1000
            else:
                final_dist_to_center = euclidean_distance_to_center(final_row, final_col)
                
                center_threshold = 1.5
                
                if current_dist_to_center > center_threshold:
                    score = -final_dist_to_center  
                else:
                    border_dist = distance_to_nearest_border(final_row, final_col)
                    score = -border_dist
                
                print(f"  Tile {tiles.index(tile)}, rot {rotation}: final ({final_row},{final_col}), dist_to_center={final_dist_to_center:.2f}, score={score:.2f}")
            
            if score > best_score:
                best_score = score
                best_tile = tile
                best_rotation = rotation
    
    if best_tile:
        print(f"AI chose tile {tiles.index(best_tile)} with rotation {best_rotation}°")
    else:
        print("AI found no valid moves!")
    
    return best_tile, best_rotation

class Board:
    def __init__(self):
        self.line_rects = []
        self.selection_done = False
        self.player_pos = None
        self.comp_pos = None
        self.player_piece = None
        self.comp_piece = None
        self.selected_tile = None  
        self.ai_selected_tiles = []  
        self.current_turn = "player" 
        self.waiting_for_ai = False
        self.ai_delay_timer = 0
        self.ai_delay_duration = 60  
        self.player_has_placed_tile = False
        self.comp_has_placed_tile = False
        self.game_over = False
        self.winner = None  
        self.difficulty = 3 
        self.difficulty_selected = False

    def draw(self, surface):
        surface.fill(BLUE)

        if not self.difficulty_selected:
            self.draw_difficulty_selection(surface)
            return
        
        self.line_rects.clear()
        self.draw_grid(surface)
        self.draw_edge_lines(surface)
        self.draw_pieces(surface)
        self.draw_tiles(surface)
        self.draw_preview(surface)
        self.draw_turn_indicator(surface)
        self.draw_game_over(surface)

    def draw_grid(self, surface):
        for row in grid:
            for box in row:
                pygame.draw.rect(surface, BROWN, box.rect, 2)
                if box.tile:
                    img = pygame.transform.rotate(
                        pygame.transform.scale(box.tile.image, (CELL_SIZE, CELL_SIZE)),
                        box.tile.rotation
                    )
                    rect = img.get_rect(center=box.rect.center)
                    surface.blit(img, rect)

    def draw_edge_lines(self, surface):
        line_length = 15
        offsets = [30, 60]

        def add_line(side, index, rect, center):
            self.line_rects.append({'side': side, 'index': index, 'rect': rect, 'center': center})

        side = 1
        for col in range(GRID_SIZE):
            x_start = GRID_X + col * CELL_SIZE
            for idx, off in enumerate(offsets, start=1):
                x = x_start + off
                y = GRID_Y
                pygame.draw.line(surface, DARK_BROWN, (x, y), (x, y - line_length), 3)
                rect = pygame.Rect(x - 3, y - line_length, 6, line_length)
                add_line(side, col*2+idx, rect, (x, y - line_length//2))
        side = 2
        for row_idx in range(GRID_SIZE):
            y_start = GRID_Y + row_idx * CELL_SIZE
            for idx, off in enumerate(offsets, start=1):
                y = y_start + off
                x = GRID_X + GRID_LENGTH
                pygame.draw.line(surface, DARK_BROWN, (x, y), (x + line_length, y), 3)
                rect = pygame.Rect(x, y - 3, line_length, 6)
                add_line(side, row_idx*2+idx, rect, (x + line_length//2, y))
        side = 3
        for col in range(GRID_SIZE):
            x_start = GRID_X + col * CELL_SIZE
            for idx, off in enumerate(offsets, start=1):
                x = x_start + off
                y = GRID_Y + GRID_LENGTH
                pygame.draw.line(surface, DARK_BROWN, (x, y), (x, y + line_length), 3)
                rect = pygame.Rect(x - 3, y, 6, line_length)
                add_line(side, col*2+idx, rect, (x, y + line_length//2))
        side = 4
        for row_idx in range(GRID_SIZE):
            y_start = GRID_Y + row_idx * CELL_SIZE
            for idx, off in enumerate(offsets, start=1):
                y = y_start + off
                x = GRID_X
                pygame.draw.line(surface, DARK_BROWN, (x, y), (x - line_length, y), 3)
                rect = pygame.Rect(x - line_length, y - 3, line_length, 6)
                add_line(side, row_idx*2+idx, rect, (x - line_length//2, y))

    def draw_pieces(self, surface):
        if self.player_piece and self.player_piece.alive:
            if self.player_piece.on_board:
                box = grid[self.player_piece.row][self.player_piece.col]
                ports = box.get_tile_ports_rects()
                pos = ports[self.player_piece.port]
            else:
                pos = self.player_piece.edge_pos
            rect = self.player_piece.image.get_rect(center=pos)
            surface.blit(self.player_piece.image, rect)

        if self.comp_piece and self.comp_piece.alive:
            if self.comp_piece.on_board:
                box = grid[self.comp_piece.row][self.comp_piece.col]
                ports = box.get_tile_ports_rects()
                pos = ports[self.comp_piece.port]
            else:
                pos = self.comp_piece.edge_pos
            rect = self.comp_piece.image.get_rect(center=pos)
            surface.blit(self.comp_piece.image, rect)

    def draw_tiles(self, surface):
        tile_size = 70
        spacing = 10
        start_x = GRID_X + GRID_LENGTH + 50
        start_y = GRID_Y
        cols = 5
        for i, tile in enumerate(tiles):
            row = i // cols
            col = i % cols
            x = start_x + col * (tile_size + spacing)
            y = start_y + row * (tile_size + spacing)
            resized = pygame.transform.scale(tile.image, (tile_size, tile_size))
            
            if tile in self.ai_selected_tiles:
                pygame.draw.rect(surface, YELLOW, (x-3, y-3, tile_size+6, tile_size+6), 3)
            
            if hasattr(tile, "placed") and tile.placed:
                dark = resized.copy()
                dark.fill((50, 50, 50, 100), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(dark, (x, y))
            else:
                surface.blit(resized, (x, y))
            pygame.draw.rect(surface, DARK_BROWN, (x, y, tile_size, tile_size), 2)
            tile.rect = pygame.Rect(x, y, tile_size, tile_size)

    def draw_preview(self, surface):
        if self.selected_tile:
            mx, my = pygame.mouse.get_pos()
            img = pygame.transform.rotate(
                pygame.transform.scale(self.selected_tile.image, (CELL_SIZE, CELL_SIZE)),
                getattr(self.selected_tile, "rotation", 0)
            )
            rect = img.get_rect(center=(mx, my))
            surface.blit(img, rect)

    def draw_turn_indicator(self, surface):
        font = pygame.font.Font(None, 36)
        if self.waiting_for_ai:
            text = font.render("AI is thinking...", True, (255, 165, 0))
        elif self.current_turn == "player":
            text = font.render("Your Turn", True, (0, 0, 255))
        else:
            text = font.render("AI Turn", True, (255, 0, 0))
        surface.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, 20))

    def draw_game_over(self, surface):
        if self.game_over:
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            box_width = 400
            box_height = 200
            box_x = (WIN_WIDTH - box_width) // 2
            box_y = (WIN_HEIGHT - box_height) // 2
            
            pygame.draw.rect(surface, (255, 255, 255), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, (0, 0, 0), (box_x, box_y, box_width, box_height), 5)
            
            font_large = pygame.font.Font(None, 72)
            font_small = pygame.font.Font(None, 36)
            
            if self.winner == "player":
                text = font_large.render("YOU WIN!", True, (0, 200, 0))
                subtext = font_small.render("AI exited the board", True, (0, 0, 0))
            else:
                text = font_large.render("YOU LOSE!", True, (200, 0, 0))
                subtext = font_small.render("You exited the board", True, (0, 0, 0))
            
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 20))
            subtext_rect = subtext.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 40))
            
            surface.blit(text, text_rect)
            surface.blit(subtext, subtext_rect)

    def draw_difficulty_selection(self, surface):
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        title = font_large.render("Tsuro", True, DARK_BROWN)
        title_rect = title.get_rect(center=(WIN_WIDTH // 2, 150))
        surface.blit(title, title_rect)
        subtitle = font_medium.render("Select Difficulty", True, DARK_BROWN)
        subtitle_rect = subtitle.get_rect(center=(WIN_WIDTH // 2, 250))
        surface.blit(subtitle, subtitle_rect)

        slider_x = WIN_WIDTH // 2 - 200
        slider_y = 350
        slider_width = 400
        slider_height = 10

        pygame.draw.rect(surface, DARK_GRAY, (slider_x, slider_y, slider_width, slider_height))

        for i in range(5):
            mark_x = slider_x + (slider_width // 4) * i
            pygame.draw.circle(surface, DARK_BROWN, (mark_x, slider_y + slider_height // 2), 8)

            label = font_small.render(str(i + 1), True, DARK_BROWN)
            label_rect = label.get_rect(center=(mark_x, slider_y + 40))
            surface.blit(label, label_rect)
        
        handle_x = slider_x + (slider_width // 4) * (self.difficulty - 1)
        pygame.draw.circle(surface, BROWN, (handle_x, slider_y + slider_height // 2), 15)
        pygame.draw.circle(surface, DARK_BROWN, (handle_x, slider_y + slider_height // 2), 15, 3)
        
        descriptions = {
            1: "Very Easy (2 tiles evaluated)",
            2: "Easy (4 tiles evaluated)",
            3: "Medium (6 tiles evaluated)",
            4: "Hard (8 tiles evaluated)",
            5: "Very Hard (10 tiles evaluated)"
        }
        desc = font_small.render(descriptions[self.difficulty], True, DARK_BROWN)
        desc_rect = desc.get_rect(center=(WIN_WIDTH // 2, 450))
        surface.blit(desc, desc_rect)

        button_width = 200
        button_height = 60
        button_x = WIN_WIDTH // 2 - button_width // 2
        button_y = 550
        
        pygame.draw.rect(surface, BROWN, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(surface, DARK_BROWN, (button_x, button_y, button_width, button_height), 3)
        
        button_text = font_medium.render("START", True, WHITE)
        button_text_rect = button_text.get_rect(center=(WIN_WIDTH // 2, button_y + button_height // 2))
        surface.blit(button_text, button_text_rect)
        
        self.start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        self.slider_rect = pygame.Rect(slider_x - 15, slider_y - 15, slider_width + 30, 40)
        self.slider_x = slider_x
        self.slider_width = slider_width

    def get_clicked_cell(self, pos):
        for row in grid:
            for box in row:
                if box.rect.collidepoint(pos):
                    return box
        return None

    def get_tile_at_pos(self, pos):
        for tile in tiles:
            if hasattr(tile, "rect") and tile.rect.collidepoint(pos) and not getattr(tile, "placed", False):
                return tile
        return None

    def get_clicked_line(self, pos):
        for line in self.line_rects:
            if line['rect'].collidepoint(pos):
                return line
        return None

    def place_pieces(self, line):
        self.player_pos = line
        available = [l for l in self.line_rects if l != line]
        comp_choice = random.choice(available)
        self.comp_pos = comp_choice
        self.selection_done = True
        print(f"Player piece at side={line['side']}, index={line['index']}")
        print(f"Comp piece at side={comp_choice['side']}, index={comp_choice['index']}")

        player_row, player_col, player_port = self.get_starting_position(line)
        self.player_piece = Piece(player_row, player_col, player_port, player_img, line['center'])

        comp_row, comp_col, comp_port = self.get_starting_position(comp_choice)
        self.comp_piece = Piece(comp_row, comp_col, comp_port, comp_img, comp_choice['center'])
        
        self.current_turn = "player"

    def get_starting_position(self, line):
        side = line['side']
        index = line['index']
        
        col_or_row = (index - 1) // 2
        port_offset = (index - 1) % 2
        
        if side == 1:
            return 0, col_or_row, 0 + port_offset
        elif side == 2:
            return col_or_row, GRID_SIZE - 1, 2 + port_offset
        elif side == 3:
            return GRID_SIZE - 1, col_or_row, 5 - port_offset
        elif side == 4:
            return col_or_row, 0, 7 - port_offset

    def process_movement(self):
        iterations = 0
        max_iterations = 50
        player_exited = False
        comp_exited = False
        
        if self.player_piece and self.player_piece.alive:
            iterations = 0
            if not self.player_piece.on_board:
                if self.player_piece.try_enter_board(grid):
                    print(f"[Player] Entered board")
            
            if self.player_piece.on_board:
                moved = True
                while moved and iterations < max_iterations:
                    iterations += 1
                    old_pos = (self.player_piece.row, self.player_piece.col, self.player_piece.port)
                    moved = self.player_piece.move(grid)
                    if moved:
                        print(f"[Player] Moved from {old_pos} to ({self.player_piece.row}, {self.player_piece.col}), port {self.player_piece.port}")
                    elif not self.player_piece.on_board:
                        print(f"[Player] Exited board!")
                        if self.player_has_placed_tile:
                            player_exited = True
                
                if iterations >= max_iterations:
                    print("Warning: Player movement loop limit reached!")
        
        if self.comp_piece and self.comp_piece.alive:
            iterations = 0
            if not self.comp_piece.on_board:
                if self.comp_piece.try_enter_board(grid):
                    print(f"[Comp] Entered board")
            
            if self.comp_piece.on_board:
                moved = True
                while moved and iterations < max_iterations:
                    iterations += 1
                    old_pos = (self.comp_piece.row, self.comp_piece.col, self.comp_piece.port)
                    moved = self.comp_piece.move(grid)
                    if moved:
                        print(f"[Comp] Moved from {old_pos} to ({self.comp_piece.row}, {self.comp_piece.col}), port {self.comp_piece.port}")
                    elif not self.comp_piece.on_board:
                        print(f"[Comp] Exited board!")
                        if self.comp_has_placed_tile:
                            comp_exited = True
                
                if iterations >= max_iterations:
                    print("Warning: Comp movement loop limit reached!")
        
        return player_exited, comp_exited

    def ai_make_move(self):
        available_tiles = [t for t in tiles if not getattr(t, "placed", False)]
        
        if not available_tiles:
            print("No tiles available for AI!")
            return
        
        best_tile, best_rotation = ai_choose_best_tile(self.comp_piece, grid, available_tiles, self.difficulty)
        
        if best_tile:
            box = grid[self.comp_piece.row][self.comp_piece.col]
            box.tile = best_tile
            best_tile.rotation = best_rotation
            best_tile.placed = True
            self.comp_has_placed_tile = True
            
            print(f"AI placed tile at ({box.row}, {box.col}) with rotation {best_rotation}°")
            
            player_exited, comp_exited = self.process_movement()
            
            if player_exited and comp_exited:
                print("Both players exited! Game Over!")
                self.game_over = True
                self.winner = "draw"
            elif player_exited:
                print("Player exited! AI Wins!")
                self.game_over = True
                self.winner = "comp"
            elif comp_exited:
                print("AI exited! Player Wins!")
                self.game_over = True
                self.winner = "player"
            else:
                self.current_turn = "player"
        else:
            print("AI has no valid moves!")
            self.comp_piece.alive = False
            self.current_turn = "player"


def main():
    clock = pygame.time.Clock()
    board = Board()
    run = True
    dragging_slider = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not board.difficulty_selected:
                        if hasattr(board, 'start_button_rect') and board.start_button_rect.collidepoint(event.pos):
                            board.difficulty_selected = True
                            print(f"Starting game with difficulty {board.difficulty}")
                            continue
                        
                        if hasattr(board, 'slider_rect') and board.slider_rect.collidepoint(event.pos):
                            dragging_slider = True
                            rel_x = event.pos[0] - board.slider_x
                            board.difficulty = max(1, min(5, int(rel_x / (board.slider_width / 4)) + 1))
                        continue
                    
                    if not board.selection_done:
                        line = board.get_clicked_line(event.pos)
                        if line:
                            board.place_pieces(line)
                            continue

                    if board.current_turn == "player" and not board.waiting_for_ai and not board.game_over:
                        tile = board.get_tile_at_pos(event.pos)
                        if tile:
                            board.selected_tile = tile
                            print(f"Selected tile index: {tiles.index(tile)}")
                            continue

                        box = board.get_clicked_cell(event.pos)
                        if box and board.selected_tile and not box.tile:
                            box.tile = board.selected_tile
                            board.selected_tile.placed = True
                            board.selected_tile = None
                            board.player_has_placed_tile = True
                            print(f"Placed tile in grid: ({box.row}, {box.col})")

                            player_exited, comp_exited = board.process_movement()
                            
                            if player_exited and comp_exited:
                                print("Both players exited! Game Over!")
                                board.game_over = True
                                board.winner = "draw"
                            elif player_exited:
                                print("Player exited! AI Wins!")
                                board.game_over = True
                                board.winner = "comp"
                            elif comp_exited:
                                print("AI exited! Player Wins!")
                                board.game_over = True
                                board.winner = "player"
                            else:
                                board.current_turn = "comp"
                                board.waiting_for_ai = True
                                board.ai_delay_timer = board.ai_delay_duration

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_slider = False

            if event.type == pygame.MOUSEMOTION:
                if dragging_slider and not board.difficulty_selected:
                    rel_x = event.pos[0] - board.slider_x
                    board.difficulty = max(1, min(5, int(rel_x / (board.slider_width / 4)) + 1))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if board.selected_tile and not getattr(board.selected_tile, "placed", False):
                        board.selected_tile.rotation = (getattr(board.selected_tile, "rotation", 0) - 90) % 360
                elif event.key == pygame.K_LEFT:
                    if board.selected_tile and not getattr(board.selected_tile, "placed", False):
                        board.selected_tile.rotation = (getattr(board.selected_tile, "rotation", 0) + 90) % 360

        if board.waiting_for_ai and board.current_turn == "comp":
            board.ai_delay_timer -= 1
            if board.ai_delay_timer <= 0:
                board.waiting_for_ai = False
                board.ai_make_move()

        board.draw(WIN)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()