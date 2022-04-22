import cv2
import csv
import numpy as np
import pandas as pd

class ParkingSpot:
  def __init__(self, isTaken, dimensions, pixels):
    self.isTaken = isTaken
    self.dimensions = dimensions
    self.pixels = pixels