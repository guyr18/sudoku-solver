from abc import abstractmethod

class Screen:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.sprites = []
        self.util = None
        self.disabled = False

    """
    Init() handles any additional initialization instructions that need to be performed.
    """
    @abstractmethod
    def init(self):
        pass

    """
    Draw() renders all fixed surfaces of this Screen object.
    """
    @abstractmethod
    def draw(self):
        pass

    """
    Handle_event() handles gameplay run-time loop events and calls the update method, when needed.
    """
    @abstractmethod
    def handle_event(self):
        pass

    """
    Update() renders and updates different sprites when required.
    """
    @abstractmethod
    def update(self):
        pass

    """
    SwitchScreen(target) renders the target screen, 'target', to the display window.
    """
    def switchScreen(self, target):
        if self.util != None:
            if self.name != target:
                if target == "Grid":
                    self.util.GRID.handle_event()
                elif target == "Start":
                    self.util.START.draw()

    """
    SetUtil(target) sets the .util property to parameter target for referencing all screens.
    """
    def setUtil(self, target):
        self.util = target

