import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import matplotlib
import numpy as np
import pandas as pd

def wrap_text(text, width=15, max_lines=4):
    def wrap_word(word, width):
        # Wrap a single word if it's longer than the width
        return [word[i:i+width] for i in range(0, len(word), width)]

    # Split the text into words
    words = text.split()
    wrapped_lines = []
    current_line = ""

    for word in words:
        # If the word is longer than the width, wrap it separately
        if len(word) > width:
            wrapped_word_parts = wrap_word(word, width)
            for part in wrapped_word_parts:
                if len(current_line) + len(part) + 1 > width:
                    if current_line:
                        wrapped_lines.append(current_line)
                    current_line = part
                    if len(wrapped_lines) >= max_lines:
                        break
                else:
                    if current_line:
                        current_line += ' '
                    current_line += part
            if len(wrapped_lines) >= max_lines:
                break
        else:
            # If adding the next word would exceed the width, start a new line
            if len(current_line) + len(word) + 1 > width:
                if current_line:
                    wrapped_lines.append(current_line)
                current_line = word
                if len(wrapped_lines) >= max_lines:
                    break
            else:
                # Add the word to the current line
                if current_line:
                    current_line += ' '
                current_line += word

    # Append the last line if it's not empty and max_lines is not exceeded
    if current_line and len(wrapped_lines) < max_lines:
        wrapped_lines.append(current_line)

    # Join the lines into a single string with newline characters
    result = "\n".join(wrapped_lines)

    # If the text is truncated, add an ellipsis
    if len(wrapped_lines) == max_lines and len(current_line) + len(word) + 1 > width:
        result = result.rstrip() + "..."

    return result