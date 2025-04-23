import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv, dotenv_values

extracted_data = pd.read_csv("~/analytics-repo/analytics-repo/data-files/Airbnb_Open_Data.csv", low_memory=False)

print(extracted_data)
print(extracted_data.columns)   