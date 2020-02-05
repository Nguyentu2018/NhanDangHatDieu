import psutil
# gives a single float value
a = psutil.cpu_percent()
# gives an object with many fields
b = psutil.virtual_memory()
# you can convert that object to a dictionary
dict(psutil.virtual_memory()._asdict())
print("DONE")