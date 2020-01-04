from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, \
    QGridLayout, QLabel
import sys
import time
from PyQt5.QtCore import Qt, QTimer


class Node:
    def __init__(self, x_loc=0, y_loc=0, g_score=0, f_score=0, h_score=0):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.g_score = g_score
        self.f_score = f_score
        self.h_score = h_score


class App(QDialog):
    NUM_ROWS = 100
    NUM_COLS = 100
    BOX_DIM_X = 10
    BOX_DIM_Y = 10

    move_neighs = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    nodes = []
    labels = []

    start_x, start_y, goal_x, goal_y = 14, 8, 25, 25

    def __init__(self):
        super().__init__()
        self.horizontalGroupBox = QGroupBox("")
        self.title = 'Pathfinder'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_grid_layout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
        QTimer.singleShot(15, self.astar_pathfind)

    def showEvent(self, event):
        self.initUI()

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

    def astar_pathfind(self):
        oned_loc = int(self.NUM_ROWS * self.start_x + self.start_y)
        open_set = [self.nodes[oned_loc]]
        while len(open_set) != 0:
            min_f = 100000
            node_min_f = None
            for cur_node in open_set:
                if cur_node.f_score < min_f:
                    min_f = cur_node.f_score
                    node_min_f = cur_node
                    open_set.remove(node_min_f)
            if node_min_f.x_loc == self.goal_x and node_min_f.y_loc == self.goal_y:
                print("found the goal")
                return
            self.labels[int(self.NUM_ROWS * node_min_f.x_loc + node_min_f.y_loc)].setStyleSheet("background-color: green;")
            for node in self.getNeighs(node_min_f.x_loc, node_min_f.y_loc):
                oned_index = int(node[0] * self.NUM_ROWS + node[1])
                cur_neigh = self.nodes[oned_index]
                tentative_g_score = node_min_f.g_score + 1
                if tentative_g_score < cur_neigh.g_score:
                    if cur_neigh not in open_set:
                        open_set.append(cur_neigh)
                        self.nodes[oned_index].g_score = tentative_g_score
                        self.nodes[oned_index].f_score = tentative_g_score + self.manhattanDistance(node[0], node[1])
                        self.labels[oned_index].setStyleSheet("background-color: red;")
                        self.labels[oned_index].setText(str(self.nodes[oned_index].f_score))
                        self.repaint()
        return 1

    def create_grid_layout(self):
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.setSpacing(0)
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                style_val = "background-color: white;border: 1px solid black;"
                label = QLabel()
                label.setFixedSize(self.BOX_DIM_X, self.BOX_DIM_Y)
                curNode = Node(i, j, 100000, 100000, 100000)
                if curNode.x_loc == self.start_x and curNode.y_loc == self.start_y:
                    curNode.g_score = 0
                    curNode.f_score = self.manhattanDistance(i, j)
                if curNode.x_loc == self.goal_y and curNode.y_loc == self.goal_y:
                    style_val += "background-color: blue;"
                label.setStyleSheet(style_val)
                label.setText(str(curNode.g_score))
                self.nodes.append(curNode)
                layout.addWidget(label, i, j)
                self.labels.append(label)
        self.horizontalGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
