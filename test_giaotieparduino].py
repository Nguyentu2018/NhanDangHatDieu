import g2
import time
import random as rd
g2.com("COM1")
g2.open()
data = ["A", "B", "C"]
time.sleep(1)
print("Start")
for i in range(100000):
    for a in range(0, 3):
        # print(str(data[a]))
        g2.send(data[rd.randrange(0, 3, 1)])
        print(g2.read())
        time.sleep(0.01)
        # print(rd.uniform(0.1, 0.05))
