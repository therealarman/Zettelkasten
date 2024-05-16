import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.qt.zettlekasten import Zettlekasten
import traceback

# loc = 'C:/Users/Arman/Downloads'

def main():

    thisInstance = Zettlekasten()

    try:
        thisInstance.start()
    except:
        traceback.print_exc()
        print("Zettlekasten Crashed!")

if __name__ == "__main__":
    main()