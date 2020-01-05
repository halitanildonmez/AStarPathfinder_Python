from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, \
    QGridLayout, QLabel, QPushButton
import sys
import time, math
from PyQt5.QtCore import QTimer


class Node:
    def __init__(self, x_loc=0, y_loc=0, g_score=0, f_score=0, h_score=0, scalable=True):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.g_score = g_score
        self.f_score = f_score
        self.h_score = h_score
        self.scalable = scalable


class App(QDialog):
    NUM_ROWS = 100
    NUM_COLS = 100
    BOX_DIM_X = 10
    BOX_DIM_Y = 10

    move_neighs = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    nodes = []
    labels = []

    start_x, start_y, goal_x, goal_y = 14, 8, 66, 79
    wall_start_row = 50
    wall_start_col = 70
    wall_face_down = range(50, 70)

    layout = QGridLayout()

    def __init__(self):
        super().__init__()
        self.horizontalGroupBox = QGroupBox("")
        self.title = 'Pathfinder'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.layout.setColumnStretch(1, 4)
        self.layout.setColumnStretch(2, 4)
        self.layout.setSpacing(0)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_grid_layout()
        self.horizontalGroupBox.setLayout(self.layout)
        button1 = QPushButton()
        button1.setText("Redo")
        button1.clicked.connect(self.button1_clicked)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(button1)
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
        QTimer.singleShot(1, self.astar_pathfind)

    def showEvent(self, event):
        self.initUI()

    def resetMap(self, i, j):
        oned_index = int(i * self.NUM_ROWS + j)
        style_val = "background-color: white;border: 1px solid black;"
        label = QLabel()
        label.setFixedSize(self.BOX_DIM_X, self.BOX_DIM_Y)
        curNode = Node(i, j, math.inf, math.inf, math.inf)
        if curNode.x_loc == self.start_x and curNode.y_loc == self.start_y:
            curNode.g_score = 0
            curNode.f_score = self.manhattanDistance(i, j)
        elif curNode.x_loc == self.goal_x and curNode.y_loc == self.goal_y:
            style_val += "background-color: blue;"
        elif (j in self.wall_face_down and i == self.wall_start_row) or (
                j == self.wall_start_col and i in self.wall_face_down):
            style_val += "background-color: black;"
            curNode.scalable = False
        self.labels[oned_index].setStyleSheet(style_val)
        self.labels[oned_index].setText(str(curNode.g_score))
        self.nodes.append(curNode)

    def button1_clicked(self):
        self.nodes.clear()
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                self.resetMap(i, j)
        QTimer.singleShot(1, self.astar_pathfind)

    def getNeighs(self, i, j):
        neighs = []
        for n in self.move_neighs:
            x_loc = n[0] + i
            y_loc = n[1] + j
            if 0 < x_loc < self.NUM_ROWS and 0 < y_loc < self.NUM_COLS:
                neighs.append([x_loc, y_loc])
        return neighs

    def manhattanDistance(self, i, j):
        dx = abs(i - self.goal_x)
        dy = abs(j - self.goal_y)
        return dx + dy

    def reconstructPath(self, came_from, cur_node):
        total_path = [cur_node]
        while cur_node in came_from.keys():
            cur_node = came_from[cur_node]
            total_path.append(cur_node)
        return total_path

    def astar_pathfind(self):
        oned_loc = int(self.NUM_ROWS * self.start_x + self.start_y)
        open_set = [self.nodes[oned_loc]]
        cameFrom = {}
        while len(open_set) != 0:
            min_f = math.inf
            node_min_f = None
            for cur_node in open_set:
                if cur_node.f_score < min_f:
                    min_f = cur_node.f_score
                    node_min_f = cur_node
                    open_set.remove(node_min_f)
            self.labels[int(self.NUM_ROWS * node_min_f.x_loc + node_min_f.y_loc)].setStyleSheet(
                "background-color: green;")
            self.repaint()
            if node_min_f.x_loc == self.goal_x and node_min_f.y_loc == self.goal_y:
                self.labels[int(self.NUM_ROWS * node_min_f.x_loc + node_min_f.y_loc)].setStyleSheet(
                    "background-color: yellow;")
                self.repaint()
                all_paths = self.reconstructPath(cameFrom, node_min_f)
                for p in all_paths:
                    self.labels[int(self.NUM_ROWS * p.x_loc + p.y_loc)].setStyleSheet(
                        "background-color: yellow;")
                return 1
            for node in self.getNeighs(node_min_f.x_loc, node_min_f.y_loc):
                oned_index = int(node[0] * self.NUM_ROWS + node[1])
                cur_neigh = self.nodes[oned_index]
                tentative_g_score = node_min_f.g_score + 1
                if tentative_g_score < cur_neigh.g_score and cur_neigh.scalable is True:
                    cameFrom[cur_neigh] = node_min_f
                    if cur_neigh not in open_set:
                        cur_neigh.g_score = tentative_g_score
                        cur_neigh.f_score = tentative_g_score + self.manhattanDistance(node[0], node[1])
                        self.nodes[oned_index] = cur_neigh
                        open_set.append(cur_neigh)
                        self.labels[oned_index].setStyleSheet("background-color: red;")
                        self.labels[oned_index].setText(str(self.nodes[oned_index].f_score))
                        self.repaint()
        return -1

    def create_grid_layout(self):
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                style_val = "background-color: white;border: 1px solid black;"
                label = QLabel()
                label.setFixedSize(self.BOX_DIM_X, self.BOX_DIM_Y)
                curNode = Node(i, j, math.inf, math.inf, math.inf)
                if curNode.x_loc == self.start_x and curNode.y_loc == self.start_y:
                    curNode.g_score = 0
                    curNode.f_score = self.manhattanDistance(i, j)
                elif curNode.x_loc == self.goal_x and curNode.y_loc == self.goal_y:
                    style_val += "background-color: blue;"
                elif (j in self.wall_face_down and i == self.wall_start_row) or (
                        j == self.wall_start_col and i in self.wall_face_down):
                    style_val += "background-color: black;"
                    curNode.scalable = False
                label.setStyleSheet(style_val)
                label.setText(str(curNode.g_score))
                self.nodes.append(curNode)
                self.layout.addWidget(label, i, j)
                self.labels.append(label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
