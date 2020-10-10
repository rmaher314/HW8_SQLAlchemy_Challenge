# Import Dependencies
#%%+
import numpy as np

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#%%+
# Import Dependencies

# %%
engine = create_engine("sqlite:///Resources/hawaii.sqlite")