from collections import deque
import cv2
import numpy as np


class GamePiece:
    def __init__(self, game_board, radius=6, mass=10, color=None):
        self.board = game_board
        self.board_h, self.board_w = game_board.shape[:2]
        self.radius = radius
        self.mass = mass
        if color is None:
            self.color = tuple(np.random.randint(256) for _ in range(3))
        else:
            self.color = color
        self.border_color = tuple(np.random.randint(256) for _ in range(3))
        self.location = np.array([np.random.randint(radius + 1, self.board_w - radius), 0], dtype='float')
        self.loc_hist = deque(maxlen=60)
        self.is_stagnant = False
        self.stagnant_counter = 0
        self.in_play = True
        self.velocity = np.array([0, 0], dtype='float')
        self.gravity = np.array([0, 0.3], dtype='float')
        self.speed_limit = 3

    def show(self, game_board):
        if self.stagnant_counter <= 30:
            location = self.location.astype('int')
            cv2.circle(game_board, tuple(location), self.radius + 1, self.border_color, -1)
            cv2.circle(game_board, tuple(location), self.radius, self.color, -1)

    def update(self):
        self.loc_hist.append(self.location.copy())
        self.check_stagnant()
        if not self.is_stagnant:
            self.fall()
            self.bounce()
            self.bound_velocity()
            self.location += self.velocity
        else:
            self.stagnant_counter += 1

    def check_stagnant(self):
        if len(self.loc_hist) == self.loc_hist.maxlen:
            delta_loc = self.loc_hist[0] - self.loc_hist[-1]
            max_move = max(abs(delta_loc))
            if max_move <= 0.1:
                self.is_stagnant = True

    def fall(self):
        self.velocity += self.gravity
        self.velocity *= np.array([0.975, 1])
        if np.random.random() > 0.8:
            self.velocity += np.array([(np.random.random() - 0.5) * 0.2, 0])

    def bounce(self):
        location = self.location.astype('int')
        x1, y1 = tuple(location - self.radius)
        x2, y2 = tuple(location + self.radius)
        x1 = np.clip(int(x1), 0, self.board_w)
        y1 = np.clip(int(y1), 0, self.board_h)
        x2 = np.clip(int(x2), 0, self.board_w)
        y2 = np.clip(int(y2), 0, self.board_h)
        area = self.board[y1:y2, x1:x2]

        if np.any(area == (255, 255, 255)):
            edge_locs = np.where(area == (255, 255, 255))
            edge_xys = np.vstack([np.array((x, y)) for x, y in zip(edge_locs[1], edge_locs[0])])
            edge_xy_diffs = edge_xys - np.array([self.radius, self.radius])
            edge_dists = [np.linalg.norm(d) for d in edge_xy_diffs]

            closest_ind = np.argmin(edge_dists)
            closest_edge_diff = edge_xy_diffs[closest_ind]
            if closest_edge_diff[0] == 0:
                closest_edge_diff[0] = -self.velocity[0]
            if closest_edge_diff[1] == 0:
                closest_edge_diff[1] = -self.velocity[1]
            self.velocity = np.interp(-1 * closest_edge_diff,
                                      (-self.speed_limit, self.speed_limit),
                                      (-max(self.velocity) * 0.8, max(self.velocity) * 0.8))

    def bound_velocity(self):
        self.velocity = np.clip(self.velocity, -self.speed_limit, self.speed_limit)
