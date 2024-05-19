import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.qt.zettelkasten import Zettelkasten
import traceback

# loc = 'C:/Users/Arman/Downloads'

def main():

    thisInstance = Zettelkasten()

    try:
        thisInstance.start()
    except:
        traceback.print_exc()
        print("Zettlekasten Crashed!")

if __name__ == "__main__":
    main()