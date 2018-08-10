from collections import deque
import imutils
import cv2
import numpy as np
from .game_piece_class import GamePiece
from .gate_class import Gate


class PlinkoBoard:
    def __init__(self, image, max_pieces=30):
        self.image = image
        self.gates = []
        self.pieces = deque(maxlen=max_pieces)
        self.board = self.create_board()

    def _create_edge_map(self, sigma=0.33, dilate_kernel_size=7):
        edge_map = imutils.auto_canny(self.image, sigma=sigma)
        if dilate_kernel_size > 2:
            if dilate_kernel_size % 2 == 0:
                dilate_kernel_size -= 1
            kernel = np.ones((dilate_kernel_size, dilate_kernel_size), dtype='uint8')
            edge_map = cv2.dilate(edge_map, kernel)

        return edge_map

    @staticmethod
    def draw_bordered_line(img, pt1, pt2, col1, col2, w1, w2):
        cv2.line(img, pt1, pt2, col1, w1)
        cv2.line(img, pt1, pt2, col2, w2)

    def _add_gates(self, edge_map, gate_width=50):
        h, w = edge_map.shape[:2]
        gate_edges = list(range(0, w, gate_width)) + [w]
        for x0, x1 in zip(gate_edges[:-1], gate_edges[1:]):
            gate = Gate(x0, x1, h - 20, h)
            gate.draw(self.image)
            gate.draw(edge_map)
            self.gates.append(gate)

        self.draw_bordered_line(edge_map, (0, h - 2), (w, h - 2), 255, 0, 3, 1)
        self.draw_bordered_line(self.image, (0, h - 2), (w, h - 2), (255, 255, 255), (0, 0, 0), 3, 1)

        self.draw_bordered_line(edge_map, (0, 0), (0, h), 255, 0, 5, 1)
        self.draw_bordered_line(self.image, (0, 0), (0, h), (255, 255, 255), (0, 0, 0), 5, 1)
        self.draw_bordered_line(edge_map, (w, 0), (w, h), 255, 0, 5, 1)
        self.draw_bordered_line(self.image, (w, 0), (w, h), (255, 255, 255), (0, 0, 0), 5, 1)

        return edge_map

    def create_board(self, gate_width=50, sigma=0.33, dilate_kernel_size=7):
        edge_map = self._create_edge_map(sigma=sigma, dilate_kernel_size=dilate_kernel_size)
        board = self._add_gates(edge_map, gate_width=gate_width)

        return cv2.cvtColor(board, cv2.COLOR_GRAY2BGR)

    def add_game_piece(self):
        self.pieces.append(GamePiece(self.board))

    def play(self):
        score = 0
        edge_map_flag = False
        while True:
            if edge_map_flag:
                board_i = self.board.copy()
            else:
                board_i = self.image.copy()

            for piece in self.pieces:
                piece.show(board_i)
                if piece.in_play:
                    if piece.is_stagnant:
                        for gate in self.gates:
                            if gate.in_gate(piece.location):
                                piece.in_play = False
                                score += gate.value
                    else:
                        piece.update()

            cv2.putText(board_i,
                        'Score: {}'.format(score),
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=4)
            cv2.putText(board_i,
                        'Score: {}'.format(score),
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=1)

            cv2.imshow('Plinko (Press N for new piece, E to toggle edge map, ESC to quit)', board_i)
            key = cv2.waitKey(10)

            if key == 27:
                break
            elif key == ord('n'):
                self.add_game_piece()
            elif key == ord('e'):
                edge_map_flag = not edge_map_flag
