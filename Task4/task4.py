from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.__length = length
        self.__width = width

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def area(self):
        return self.__length * self.__width

class Circle(Shape):
    def __init__(self, radius):
        self.__radius = radius

    def get_radius(self):
        return self.__radius

    def area(self):
        return math.pi * self.__radius ** 2

def print_area(shape: Shape):
    print(f"Площа: {shape.area():.2f}")

if __name__ == "__main__":
    r = Rectangle(5, 3)
    c = Circle(2)

    print("Прямокутник:")
    print(f"Довжина: {r.get_length()}, Ширина: {r.get_width()}")
    print_area(r)

    print("\nКоло:")
    print(f"Радіус: {c.get_radius()}")
    print_area(c)