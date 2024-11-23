# TO RUN APP

# conda env create -f environment.yml
# conda create -n hack python=3.12
# conda env remove -n hack

# streamlit run main.py

# conda env export --name hack > environment.yml
# pip list --format=freeze > requirements.txt

# conda env export --name hack > environment.yml
# pip list --format=freeze > requirements.txt

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
