from TaskGeneration import TaskGeneration as tg
from TaskSorting import TaskSorting as ts
from EnergiesManagement import EnergyManager as em
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import sqlite3
import datetime


connection = sqlite3.connect("EH2Tasks")
cursor = connection.cursor()
connection.commit()


physical_energy = 100
mental_energy = 100
energy_start = datetime.datetime.timestamp(datetime.datetime.now())

energy_priority = em.prioritise_energy()
tasks_dict = {}
first_load = True


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
        self.datefield.setPlaceholderText("Enter the deadline")
        box.addWidget(self.inputfield)
        box.addWidget(self.datefield)



        self.setLayout(box)
    def input_task(self):
        self.priority = str(self.inputfield.text())

    def input_date(self):
        self.today = datetime.datetime.now()
        try:
            self.urgency = datetime.datetime(int(self.datefield.text().split()[2]), int(self.datefield.text().split()[1]),
                                             int(self.datefield.text().split()[0]), 0, 0, 0)
            self.urgency -= self.today
            self.urgency = datetime.timedelta.total_seconds(self.urgency) / 3600
            if str(self.inputfield.text()) != "":
                tg.Task(self.priority, self.urgency, tasks_dict)

                if tasks_dict[self.priority].priority == self.priority:
                    self.inputfield.clear()
                    self.datefield.clear()
                    self.inputfield.setPlaceholderText("1 is high priority, 2 is low")
                    self.datefield.setPlaceholderText("Mental or physical energy?")
                    self.inputfield.returnPressed.disconnect()
                    self.datefield.returnPressed.disconnect()
                    self.inputfield.returnPressed.connect(self.new_task_input)
                    self.datefield.returnPressed.connect(self.new_task_input)
                else:
                    self.inputfield.clear()
                    self.datefield.clear()
                    self.reset_display()

        except ValueError:
            self.inputfield.clear()
            self.datefield.clear()
            window.refresh()


    def new_task_input(self):
        try:
            int(self.inputfield.text())
            if self.datefield.text() != "":
                tasks_dict[self.priority].priority = self.inputfield.text()
                tasks_dict[self.priority].energy = self.datefield.text()
                self.inputfield.clear()
                self.datefield.clear()
                self.inputfield.setPlaceholderText("Out of 1 - 10, how much energy does this consume?")
                self.datefield.setPlaceholderText("")
                self.inputfield.disconnect()
                self.datefield.disconnect()
                self.inputfield.returnPressed.connect(self.new_task_input_2)
                self.datefield.returnPressed.connect(self.new_task_input_2)
        except ValueError:
            self.inputfield.clear()
            self.datefield.clear()

    def new_task_input_2(self):
        tasks_dict[self.priority].energy_quant = self.inputfield.text()
        print(tasks_dict[self.priority].energy_quant)
        self.inputfield.clear()
        self.datefield.clear()
        self.reset_display()

    def reset_display(self):
        energy_upkeep()
        window.refresh()
        task_display(tasks_dict)
        complete_display(tasks_dict)

class TaskBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("TaskBox")
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
            em.subtract_energy(energy_priority, tasks_dict[self.checkbox.text()].energy_quant)
            window.refresh()
            task_display(tasks_dict)
            complete_display(tasks_dict)
        else:
            try:
                tasks_dict[self.checkbox.text()].task_undone()
                window.refresh()
                task_display(tasks_dict)
                complete_display(tasks_dict)
            except KeyError:
                pass

class CompletedTask(TaskBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkbox.setChecked(True)

def task_display(dict):
    for item in ts.energy_sort(ts.task_sort(ts.sorting_dict_struct(dict)[0]), energy_priority):
        for value in item:
            task = TaskBox()
            task.setStyleSheet("""
            color: white;
            background: #ff00bf;
            border-radius: 5px;
            """)
            task.checkbox.setText(value[0])
            mainlay.addWidget(task)

def complete_display(dict):
    line = TaskInput()
    for key in ts.task_sort(ts.sorting_dict_struct(dict)[1]):
        for value in key:
            task = CompletedTask()
            task.checkbox.setText(value[0])
            mainlay.addWidget(task)

def energy_upkeep():
    em.energy_decrement()

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
        self.input = TaskInput()
        mainlay.addWidget(self.input)

    def refresh(self):
        for item in self.groupbox.children():
            if isinstance(item, TaskBox):
                item.setParent(None)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
        background-color : "#eabfff";
        color: "white";
        }
        QLineEdit {
        border: none;
        border-color: "transparent";
        border-bottom: 2px solid #d580ff;
        position: static;
        }
        QLineEdit:focus {
        border-bottom: 2px solid #ff00ff;
        }
        QRadioButton {
        border: black;
        }
    """)
    global window
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
