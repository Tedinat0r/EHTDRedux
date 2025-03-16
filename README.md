### Eisenhower To-Do List

Inspired by my personal pursuit of maximising the output of all my daily activities, I thought it would be interesting to develop a to-do list app that algorithmically utilises the elegance of the eisenhower matrix. The app provides a simple UI, however the value is found in the backend through the sorting and reordering of tasks based on their priority and urgency. I have since expanded the project to also assist in selecting tasks for the user based on their current level of physical and mental energy, further increasing their productive output

## How it’s Made

### Technologies: Python, SQLite, PyQT

The projects modus operandi hinges on sorting tasks, first by calculating their urgency (i.e. their time sensitivity or proximity to a certain deadline), and then their priority. To make this as streamlined as possible for the user, the object which stores this and other task information is initialized with a method of comparing the terms of the user’s to-do entry to a SQLite database that has terms associated with their priority; there is similar functionality related to retrieving the mental and physical energy scores linked to certain tasks.

Once the tasks are initialised, they are parsed by the TaskSorting module, and those which are not set as complete are grouped by their priority scores, then sorted in ascending order of urgency. A dynamic element of the sorting implemented here is sorting by energy. The EnergyManagement module includes functionality to determine which type of energy a user has expended less of so far, and prioritises tasks of that nature until the other returns to a level where they can remain as productive as possible. 

The most challenging part of this project was integrating this system with the UI, and interweaving the functionality within the PyQT event loop. As the majority of the user interaction with the UI happens on a single thread, great attention had to be paid to the flow of the functions.

## Optimizations

One of the largest improvements made to the project through it’s development was the use of the incremental sorting. In the first iteration, I naively tried to sort the task entries in one method which attempted to manage values of various dimensions of a nested list structure. The optimisation arrived by splitting the sorting process to first sort all items by priority into separate subarrays, then among the items apply python’s inbuilt sorted object. Another key revelation in this regard was utilising lambdas in conjunction with the object to bypass the superfluous writing of numerous nested loops to access the respect elements of these nested arrays. 

The process of this project also taught me much about the utility of composition in OOP, as the UI makes full use of this concept.

## Future Improvements and Features

One of the main pieces of functionality I would like to add to the project is a dialogue box to deal with tasks that are not already in the database. This would give users a more tailored experience and heighten the overall utility of the app. There would also be a significant amount of value added with some machine learning, to be able to detect patterns of tasks and automatically generate urgency and priority scores.

In terms of the UI, it would be both an enjoyable challenge and valuable learning experience to implement an calendar view into the project. It would require that the interfaces and general internal API to be standardized, along with a more profound understanding of many-to-many database relationships to implement the 'links' between the tables which represent tasks and their attributes.


