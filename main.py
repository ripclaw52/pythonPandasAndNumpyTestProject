import numpy as np
import pandas as pd
import plotly as po
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Display version for imported libraries
def library_version():
    print(f"numpy version: {np.__version__}\n"
          f"pandas version: {pd.__version__}\n"
          f"plotly version: {po.__version__}")

if __name__ == '__main__':
    library_version()