from abc import ABC, abstractmethod

class ReportRenderer(ABC):
    @abstractmethod
    def render(self, data):
        pass