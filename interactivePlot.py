import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

class Annotate(object):
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1, alpha=0.5, color='red')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

    def onPress(self, event):
        print('press')
        self.x0 = event.xdata
        self.y0 = event.ydata
        print('x0: {}'.format(self.x0))
        print('y0: {}'.format(self.y0))

    def onRelease(self, event):
        print('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()
        print('x1 {}'.format(self.x1))
        print('y1 {}'.format(self.y1))

a = Annotate()
x = range(0, 10)
y = np.random.randn(10)
plt.plot(x, y, '--')
plt.show()
# print(Annotate.x0)
a_list = []
for _ in range(2):
    a = Annotate()
    plt.plot(x, y, '--')
    plt.show()
    a_list.append(a)
    del a

print(a_list)
print(dir(a_list[0]))
for a in a_list:
    print(a.x0)
