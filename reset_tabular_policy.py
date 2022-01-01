import pandas as pd
import numpy as np
import random


# For the tabular method with As in the state
file_Q = open("tabular_Q_As.csv","w")
file_Q_history = open("tabular_Q_As_history.csv","w")
file_total_episodes_trained = open("tabular_As_episodes_trained.txt","w")

Q =pd.DataFrame({"hand sum":np.tile(np.arange(0,22),4),\
                "usable A": np.tile(np.repeat([1,0],22),2),\
                "action":np.repeat([1,0],44),\
                "value": np.zeros((88,),dtype=int),\
                "times visited": np.zeros((88,),dtype=int)})

Q_history = Q.copy()
Q_history["training index"] = np.zeros((Q.shape[0],),dtype=int)

file_Q.write(Q.to_csv())
file_Q_history.write(Q_history.to_csv())
file_total_episodes_trained.write("0")

file_Q.close()
file_Q_history.close()
file_total_episodes_trained.close()
