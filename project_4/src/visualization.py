"""Pygame decision tree renderer. See tasks/06_pygame_tree_visualization.md for the
full spec."""
import os

os.environ["SDL_AUDIODRIVER"] = "dummy"  # same WSL2 audio fix as project_1/project_2

import pygame

BOX_W, BOX_H = 160, 50
LEVEL_GAP = 110
LEAF_GAP = 40
MARGIN = 40

COLOR_INTERNAL = (173, 216, 230)   # light blue
COLOR_YES = (144, 238, 144)        # green -- "ask for help"
COLOR_NO = (250, 160, 120)         # orange/red -- "robot decides"
COLOR_BORDER = (40, 40, 40)
COLOR_EDGE = (90, 90, 90)
COLOR_BG = (255, 255, 255)
COLOR_TEXT = (20, 20, 20)


def _layout(root):
    """Returns dict node -> (x, y) center position, and the (width, height) needed."""
    positions = {}
    next_leaf_x = [MARGIN + BOX_W // 2]

    def assign(node, depth):
        y = MARGIN + depth * (BOX_H + LEVEL_GAP) + BOX_H // 2
        if node.is_leaf:
            x = next_leaf_x[0]
            next_leaf_x[0] += BOX_W + LEAF_GAP
        else:
            child_xs = [assign(child, depth + 1) for child in node.branches.values()]
            x = sum(child_xs) / len(child_xs)
        positions[id(node)] = (x, y)
        return x

    assign(root, 0)
    max_x = max(x for x, _ in positions.values())
    max_y = max(y for _, y in positions.values())
    width = int(max_x + BOX_W // 2 + MARGIN)
    height = int(max_y + BOX_H // 2 + MARGIN)
    return positions, width, height


def _draw_node(screen, font, node, positions):
    x, y = positions[id(node)]
    rect = pygame.Rect(0, 0, BOX_W, BOX_H)
    rect.center = (x, y)
    if node.is_leaf:
        color = COLOR_YES if node.label == "Yes" else COLOR_NO
        text = node.label
    else:
        color = COLOR_INTERNAL
        text = node.attribute
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_BORDER, rect, width=2, border_radius=8)
    label_surf = font.render(text, True, COLOR_TEXT)
    label_rect = label_surf.get_rect(center=rect.center)
    screen.blit(label_surf, label_rect)


def _draw_edges(screen, font, node, positions):
    if node.is_leaf:
        return
    px, py = positions[id(node)]
    for value, child in node.branches.items():
        cx, cy = positions[id(child)]
        start = (px, py + BOX_H // 2)
        end = (cx, cy - BOX_H // 2)
        pygame.draw.line(screen, COLOR_EDGE, start, end, 2)
        mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        edge_label = font.render(str(value), True, COLOR_EDGE)
        screen.blit(edge_label, edge_label.get_rect(center=mid))
        _draw_edges(screen, font, child, positions)


def _draw_tree(screen, font, root, positions):
    _draw_edges(screen, font, root, positions)

    def draw_all(node):
        _draw_node(screen, font, node, positions)
        if not node.is_leaf:
            for child in node.branches.values():
                draw_all(child)

    draw_all(root)


def show_tree(root, attributes, train_size=None):
    pygame.init()
    positions, width, height = _layout(root)
    title = "Decision Tree"
    if train_size is not None:
        title += f" (trained on {train_size} examples)"
    screen = pygame.display.set_mode((max(width, 400), max(height, 200)))
    pygame.display.set_caption(title)
    font = pygame.font.SysFont(None, 20)

    screen.fill(COLOR_BG)
    _draw_tree(screen, font, root, positions)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
        pygame.time.wait(16)
    pygame.quit()
