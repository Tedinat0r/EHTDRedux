import sqlite3
from datetime import *
connection = sqlite3.connect("EH2Tasks")
cursor = connection.cursor()


class Task:
    def __init__(self, priority, urgency, dictionary):
        connection = sqlite3.connect("EH2Tasks")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Tasks (TaskName TEXT, TaskDL TEXT);')
        connection.commit()
        self.urgency = urgency
        self.priority = priority
        self.complete = False
        self.name = f'{self.priority}'
        self.store_task()
        #energies_table = cursor.execute("SELECT * FROM Energies").fetchall()
        #type = ''
        #energy_quant = 0
        #for word in priority.split():
            #for row in energies_table:
                #for value in row:
                    #if word == value:
                        #if row.index(value) == 0:
                            #type = 'mental'
                        #else:
                            #type = 'physical'
        #self.energy = [type]
        cursor.execute("SELECT * FROM PriorityScores")
        for word in self.priority.split():
            for row in cursor.fetchall():
                for value in row:
                    if str(value).find(word) > -1:
                        self.priority = int(row.index(value) + 1)

        dictionary.__setitem__(self.name, self)

    def task_done(self):
        self.complete = True

    def task_undone(self):
        self.complete = False

    def store_task(self):
        taskname = self.priority
        taskdl = self.urgency
        cursor.execute('INSERT INTO Tasks (TaskName, TaskDL) VALUES (?,?)', (taskname, taskdl))
        connection.commit()
