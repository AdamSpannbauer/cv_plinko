from collections import deque
import imutils
import cv2
from .utils import read_background, draw_bordered_line
from .game_piece_class import GamePiece
from .gate_class import Gate


class PlinkoBoard:
    """Class to turn images/videos into Plinko game boards

    :param background_path: path to image/video (if integer then assumed to be camera input for video);
                            valid image path extensions: [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]
    :param piece_size: radius (in pixels) for circle game pieces
    :param max_pieces: maximum number of pieces allowed on board; high numbers can affect performance
                       (uses a FIFO queue structure, if max_pieces exceeded then first piece in queue
                       is deleted to make room for new piece)
    :param background_width: pixel width that the input background should be resized to for display

    :ivar background_path: user provided path to image/video
    :ivar piece_size: radius (in pixels) for circle game pieces
    :ivar max_pieces: max number of plinko pieces allowed in play
    :ivar background_width: pixel width for displayed PlinkoBoard

    >>> from cv_plinko import PlinkoBoard
    >>> # create plinko board from webcam at index 0
    >>> plinko = PlinkoBoard(background_path=0)
    >>> plinko.play()
    """
    def __init__(self, background_path, piece_size=6, max_pieces=30, background_width=600):
        self._background, self._background_type = read_background(background_path, background_width=background_width)
        self.background_path = background_path
        self.background_width = background_width
        self.max_pieces = max_pieces
        self.piece_size = piece_size
        self._gates = []
        self._pieces = deque(maxlen=self.max_pieces)
        if self._background_type == 'image':
            self._board = self._create_board()
            self._background_vidcap = None
        else:
            self._background_vidcap = self._background

    def _create_edge_map(self, sigma=0.33, dilate_kernel_size=7):
        """Convert image into dilated edge map

        :param sigma: value to be passed to imutils.auto_canny
        :param dilate_kernel_size: kernel radius to be used during dilation step
        :return: numpy array/opencv gray image containing dilated edge map
        """
        edge_map = imutils.auto_canny(self._background, sigma=sigma)
        if dilate_kernel_size > 2:
            if dilate_kernel_size % 2 == 0:
                dilate_kernel_size -= 1
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_kernel_size, dilate_kernel_size))
            edge_map = cv2.dilate(edge_map, kernel)

        return edge_map

    def _create_gates(self, edge_map, gate_width=50):
        """Populate gates attribute with Gate objects

        :param edge_map: result of _create_edge_map method
        :param gate_width: pixel width of gates
        :return: None; populates PlinkoBoard.gates attribute
        """
        h, w = edge_map.shape[:2]
        gate_edges = list(range(0, w, gate_width)) + [w]
        for x0, x1 in zip(gate_edges[:-1], gate_edges[1:]):
            gate = Gate(x0, x1, h - 20, h)
            self._gates.append(gate)

    def _draw_gates_and_borders(self, edge_map):
        """Draw image borders & plinko gates

        :param edge_map: result of _create_edge_map method
        :return: edge map with gates/borders overlaid
        """
        h, w = edge_map.shape[:2]
        for gate in self._gates:
            gate.draw(self._background)
            gate.draw(edge_map)

        draw_bordered_line(edge_map, (0, h - 2), (w, h - 2), 255, 0, 3, 1)
        draw_bordered_line(self._background, (0, h - 2), (w, h - 2), (255, 255, 255), (0, 0, 0), 3, 1)

        draw_bordered_line(edge_map, (0, 0), (0, h), 255, 0, 5, 1)
        draw_bordered_line(self._background, (0, 0), (0, h), (255, 255, 255), (0, 0, 0), 5, 1)
        draw_bordered_line(edge_map, (w, 0), (w, h), 255, 0, 5, 1)
        draw_bordered_line(self._background, (w, 0), (w, h), (255, 255, 255), (0, 0, 0), 5, 1)

        return edge_map

    def _create_board(self, gate_width=50, sigma=0.33, dilate_kernel_size=7):
        """Create plinko board, create edge map, draw plinko gates & borders

        :param gate_width: pixel width of gates
        :param sigma: value to be passed to imutils.auto_canny
        :param dilate_kernel_size: kernel radius to be used during dilation step
        :return: plinko game board to be used in PlinkoBoard.play()
        """
        edge_map = self._create_edge_map(sigma=sigma, dilate_kernel_size=dilate_kernel_size)
        if not self._gates:
            self._create_gates(edge_map, gate_width=gate_width)
        board = self._draw_gates_and_borders(edge_map)

        return cv2.cvtColor(board, cv2.COLOR_GRAY2BGR)

    def _add_game_piece(self):
        """Create new plinko disc to be in play on board

        :return: None; populates PlinkoBoard.pieces
        """
        self._pieces.append(GamePiece(self._board, radius=self.piece_size))

    def play(self):
        """Play plinko with your input image/video

        Starts gameplay with PlinkoBoard object

        :return: None; Creates window where plinko can be played
        """
        score = 0
        edge_map_flag = False
        while True:
            if self._background_type == 'video':
                grabbed, self._background = self._background_vidcap.read()
                if not grabbed:
                    break
                self._background = imutils.resize(self._background, width=self.background_width)
                self._board = self._create_board()

            if edge_map_flag:
                board_i = self._board.copy()
            else:
                board_i = self._background.copy()

            for piece in self._pieces:
                if self._background_type == 'video':
                    piece.board = self._board.copy()
                piece.show(board_i)
                piece.update()
                if piece.in_play:
                    if piece.is_stagnant:
                        for gate in self._gates:
                            if gate.in_gate(piece.location):
                                piece.in_play = False
                                score += gate.value

            cv2.putText(board_i,
                        'Score: {}'.format(score),
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=4)
            cv2.putText(board_i,
                        'Score: {}'.format(score),
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=1)

            cv2.imshow('Plinko! (N - new piece; E - toggle edge map; R - reset; ESC - quit)', board_i)
            key = cv2.waitKey(10)

            if key == 27:
                break
            elif key == ord('n'):
                self._add_game_piece()
            elif key == ord('e'):
                edge_map_flag = not edge_map_flag
            elif key == ord('r'):
                self._pieces = deque(maxlen=self.max_pieces)
                score = 0
