from TaskGeneration import TaskGeneration as tg
from TaskSorting import TaskSorting as ts
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import sqlite3
import datetime

energies_1 = ['python','Python', 'Project', 'project', 'CS', 'cs', 'Compsci', 'CompSci', 'compsci']
energies_2 = ['Workout', 'workout', 'Hike', 'hike', 'Gym', 'gym']


connection = sqlite3.connect("EH2Tasks")
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Tasks (TaskName TEXT, TaskDL TEXT);')
cursor.execute('CREATE TABLE IF NOT EXISTS Energies (Mental TEXT, Physical TEXT);')
cursor.execute('INSERT INTO Energies (Mental, Physical) VALUES (?,?);', (str(energies_1), str(energies_2)))
connection.commit()

tasks_dict = {}


class TaskInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.priority = ""
        self.urgency = ""
        box = QHBoxLayout()
        self.inputfield = QLineEdit(parent=self)
        self.datefield = QLineEdit(parent=self)
        self.inputfield.setPlaceholderText("Enter your task")
        self.inputfield.returnPressed.connect(self.input_task)
        self.datefield.returnPressed.connect(self.input_date)
        box.addWidget(self.inputfield)
        box.addWidget(self.datefield)
        self.setLayout(box)
    def input_task(self):
        self.priority = str(self.inputfield.text())
        self.inputfield.setPlaceholderText("Enter the deadline")

    def input_date(self):
        self.today = datetime.datetime.now()
        self.urgency = datetime.datetime(int(self.datefield.text().split()[2]), int(self.datefield.text().split()[1]),
                                            int(self.datefield.text().split()[0]), 0, 0, 0)
        self.urgency -= self.today
        self.urgency = datetime.timedelta.total_seconds(self.urgency) / 3600
        if str(self.inputfield.text()) != "":
            tg.Task(self.priority, self.urgency, tasks_dict)
            self.inputfield.clear()
            self.datefield.clear()
            window.refresh()
            task_display()
            complete_display()

        else:
            print("oops!")

class TaskBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        box = QHBoxLayout()
        self.checkbox = QRadioButton('', self)
        box.addWidget(self.checkbox)
        self.setLayout(box)
        self.checkbox.toggled.connect(self.complete_check)
        self.show()
    def complete_check(self):
        rb = self.sender()
        if not isinstance(self, CompletedTask) and rb.isChecked():
            tasks_dict[self.checkbox.text()].task_done()
            window.refresh()
            task_display()
            complete_display()
        else:
            try:
                tasks_dict[self.checkbox.text()].task_undone()
                window.refresh()
                task_display()
                complete_display()
            except KeyError:
                pass

class CompletedTask(TaskBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkbox.setChecked(True)
def task_display():
    for item in ts.task_sort(ts.sorting_dict_struct(tasks_dict)[0]):
        for value in item:
            task = TaskBox()
            task.checkbox.setText(value[0])
            mainlay.addWidget(task)
def complete_display():
    for key in ts.task_sort(ts.sorting_dict_struct(tasks_dict)[1]):
        for value in key:
            task = CompletedTask()
            task.checkbox.setText(value[0])
            mainlay.addWidget(task)



mainlay = QVBoxLayout()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QVBoxLayout()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Eisenhower R E D U X bitch')
        self.groupbox = QGroupBox()
        self.groupbox.setLayout(mainlay)
        self.setCentralWidget(self.groupbox)
        mainlay.addWidget(TaskInput())

    def refresh(self):
        for item in self.groupbox.children():
            if isinstance(item, TaskBox):
                item.setParent(None)


def main():
    app = QApplication(sys.argv)
    global window
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
