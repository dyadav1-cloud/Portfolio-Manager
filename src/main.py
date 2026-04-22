import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os


APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)




