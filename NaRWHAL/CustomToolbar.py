from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
class CustomToolbar(NavigationToolbar2TkAgg):
    """Creates custom toolbar for matplotlib display"""

    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Zoom', 'Manually zoom into image', 'zoom_to_rect', 'zoom'),
            ('Home', 'Revert to original image', 'home', 'home'),
        )
        NavigationToolbar2TkAgg.__init__(self, canvas_, parent_)

