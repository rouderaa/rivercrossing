from abc import ABC, abstractmethod
from typing import List


class Subject:
    def __init__(self):
        self._observers: List['Observer'] = []

    def attach(self, observer: 'Observer') -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject):  # Updated to receive subject reference
        pass


# Example concrete implementations
# class ConcreteObserverA(Observer):
#     def update(self, subject: Subject):
#         print(f"ConcreteObserverA: Reacted to state change: {subject.state}")
#
#
# class ConcreteObserverB(Observer):
#     def update(self, subject: Subject):
#         print(f"ConcreteObserverB: Reacted to state change: {subject.state}")

# Example usage
# def main():
#     subject = Subject()
#
#     observer_a = ConcreteObserverA()
#     observer_b = ConcreteObserverB()
#
#     subject.attach(observer_a)
#     subject.attach(observer_b)
#
#     subject.state = "New State"
#
#     # Output will be:
#     # ConcreteObserverA: Reacted to state change: New State
#     # ConcreteObserverB: Reacted to state change: New State
#
#
# if __name__ == "__main__":
#     main()