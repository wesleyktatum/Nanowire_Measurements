from matplotlib.patches import Rectangle


class UpdatingRect(Rectangle):
	"""Overwrites rectangle to make it flexible"""
    def __call__(self, ax):
        self.set_bounds(*ax.viewLim.bounds)
        ax.figure.canvas.draw_idle()


