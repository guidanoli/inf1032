from sys import argv, exit
try:
    width = float(argv[1])
    height = float(argv[2])
except:
    print('Usage: %s <width> <height>' % argv[0])
    exit(1)

left, top = input('Upper left coords: ').split()
right, bottom = input('Lower right coords: ').split()
left = float(left)/width
right = float(right)/width
top = float(top)/height
bottom = float(bottom)/height
area = (100*top, 100*left, 100*bottom, 100*right)
print(area)
