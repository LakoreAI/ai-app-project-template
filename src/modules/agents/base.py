from src.modules.base import BaseModules


class BaseAgent(BaseModules):
    def __init__(self):
        super().__init__()

    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")

    async def aexecute(self):
        raise NotImplementedError("Subclasses must implement this method.")
