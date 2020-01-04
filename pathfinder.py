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

    start_x, start_y, goal_x, goal_y = 14, 8, 55, 55

    def __init__(self):
        super().__init__()
        self.horizontalGroupBox = QGroupBox("")
        self.title = 'Pathfinder'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        QTimer.singleShot(1500, self.astar_pathfind)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_grid_layout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()

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
        startLabel = self.labels[oned_loc]
        if startLabel is not None:
            startLabel.setStyleSheet("background-color: green;")
        endLabel = self.labels[int(self.NUM_ROWS * self.goal_x + self.goal_y)]
        endLabel.setStyleSheet("background-color: blue;")
        open_set = [self.nodes[oned_loc]]
        while len(open_set) != 0:
            min_f = 0
            node_min_f = None
            for cur_node in open_set:
                if cur_node.f_score > min_f:
                    min_f = cur_node.f_score
                    node_min_f = cur_node
                    open_set.remove(node_min_f)
            if node_min_f.x_loc == self.goal_x and node_min_f.y_loc == self.goal_y:
                print("found the goal")
                return
            for node in self.getNeighs(node_min_f.x_loc, node_min_f.y_loc):
                cur_neigh = self.nodes[int(node[0] * self.NUM_ROWS + node[1])]
                tentative_g_score = node_min_f.g_score + 1
                if tentative_g_score < cur_neigh.g_score:
                    self.nodes[int(node[0] * self.NUM_ROWS + node[1])].g_score = tentative_g_score
                    self.nodes[int(node[0] * self.NUM_ROWS + node[1])].f_score = tentative_g_score + self.manhattanDistance(node[0], node[1])
                    time.sleep(0.1)
                    self.labels[int(node[0] * self.NUM_ROWS + node[1])].setStyleSheet("background-color: red;")
                    self.labels[int(node_min_f.x_loc * self.NUM_ROWS + node_min_f.y_loc)].setStyleSheet("background-color: green;")
                    self.repaint()
                    if cur_neigh not in open_set:
                        open_set.append(cur_neigh)
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
                label.setStyleSheet(style_val)
                curNode = Node(i, j, 100000, 100000, 100000)
                if curNode.x_loc == self.start_x and curNode.y_loc == self.start_y:
                    print("Update the start location")
                    curNode.g_score = 0
                    curNode.f_score = self.manhattanDistance(i, j)
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
