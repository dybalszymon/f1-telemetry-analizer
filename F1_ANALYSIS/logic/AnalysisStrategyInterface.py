from abc import ABC, abstractmethod

class AnalysisStrategyInterface(ABC):
    @abstractmethod
    def calculate(self, data: list):
        #list of jsons
        pass

    @abstractmethod
    def get_name(self) -> str:
        #return name of analysis
        pass




