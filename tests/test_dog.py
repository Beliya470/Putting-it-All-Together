import pytest
from lib.dog import Dog

def test_dog_creation():
    dog = Dog(name="Buddy", breed="Golden Retriever")
    assert dog.name == "Buddy"
    assert dog.breed == "Golden Retriever"

