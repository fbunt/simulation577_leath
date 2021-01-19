import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Leath:
    def __init__(self, n=80, p=0.6):
        self.n = n
        self.p = p
        self.perimeter = {}
        # Add out of bounds
        for i in [-1, n]:
            for j in range(0, n):
                self.perimeter[(i, j)] = False
        for j in [-1, n]:
            for i in range(0, n):
                self.perimeter[(i, j)] = False
        seed = (n // 2, n // 2)
        self.cluster = set([seed])
        self.world = np.zeros((n, n), dtype=np.int8)
        self.world[seed] = 1
        self.add_perimeter(seed)

    def add_perimeter(self, pt):
        """
        Given a point pt (tuple), add to perimeter all 4 neighbors that are not
        in cluster.
        """
        nn = [
            (pt[0] + i, pt[1] + j)
            for i, j in zip([1, -1, 0, 0], [0, 0, 1, -1])
        ]
        for p in nn:
            if p not in self.cluster and p not in self.perimeter:
                self.perimeter[p] = True

    def grow_cluster(self):
        """
        Iterate through each point in perimeter, if uniform random [0, 1) is
        less than p, add perimeter point to cluster. Else, mark point as
        inaccessible. Do something to keep cluster from leaving domain.
        """
        pts = [p for p, v in self.perimeter.items() if v]
        rand = np.random.rand(len(pts))
        new_cluster_pts = []
        for pt, r in zip(pts, rand):
            if self.p >= r:
                new_cluster_pts.append(pt)
            else:
                self.perimeter[pt] = False
        for pt in new_cluster_pts:
            self.cluster.add(pt)
            self.perimeter.pop(pt, None)
            self.world[pt] = 1
            self.add_perimeter(pt)


class LeathAnimation:
    def __init__(self, sim, interval):
        self.sim = sim
        self.fig = plt.figure()
        self.im = None
        self.ani = None
        self.interval = interval
        self.paused = False

    def init(self):
        self.im = plt.imshow(
            self.sim.world, interpolation="none", animated=True, cmap="gray"
        )
        return (self.im,)

    def update(self, *args):
        self.sim.grow_cluster()
        self.im.set_data(self.sim.world)
        return (self.im,)

    def on_click(self, event):
        if event.key != " ":
            return
        if self.paused:
            self.ani.event_source.start()
            self.paused = False
        else:
            self.ani.event_source.stop()
            self.paused = True

    def run(self):
        self.fig.canvas.mpl_connect("key_press_event", self.on_click)
        self.ani = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init,
            interval=self.interval,
            blit=True,
        )
        plt.show()


if __name__ == "__main__":
    sim = Leath(50, 0.6)
    anim = LeathAnimation(sim, 100)
    anim.run()
