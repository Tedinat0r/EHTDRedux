import datetime

mental_energy = 100
physical_energy = 100


energy_start = datetime.datetime.timestamp(datetime.datetime.now())

def prioritise_energy():
    global mental_energy
    global physical_energy

    if (mental_energy < physical_energy):
        return physical_energy
    else:
        return mental_energy

def subtract_energy(x, y):
    x -= y

def energy_decrement():
    global mental_energy
    global physical_energy
    global energy_start
    time_elapsed = datetime.datetime.now() - datetime.datetime.fromtimestamp(energy_start)
    hours_elapsed = (datetime.timedelta.total_seconds(time_elapsed) / 3600) / 60
    mental_energy = mental_energy - (5 * hours_elapsed)
    mental_energy = mental_energy + (1.5 * hours_elapsed)
    physical_energy = physical_energy - (5 * hours_elapsed)
    physical_energy = physical_energy + (1.5 * hours_elapsed)

def task_energy_expend(x, mental_energy, physical_energy):
    if prioritise_energy(mental_energy, physical_energy) == mental_energy:
        subtract_energy(mental_energy, x)
    else:
        subtract_energy(physical_energy, x)

