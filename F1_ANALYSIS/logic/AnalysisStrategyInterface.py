from abc import ABC, abstractmethod

class AnalysisStrategyInterface(ABC):
    @abstractmethod
    def calculate(self, data):
        pass




