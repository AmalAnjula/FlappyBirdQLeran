import matplotlib.pyplot as plt
import pandas as pd
#iteration,score,q_val,nowMem,pealMem
# Load the data from the CSV file
data = pd.read_csv('data/plotData.csv')

# Extract columns
iteration = data['iteration']
q_val = data['score']


window_size = 5  # Adjust this value as needed
running_avg = q_val.rolling(window=window_size).mean()


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(iteration, q_val,   linestyle='-', color='b')
plt.plot(iteration, running_avg, linestyle='-', color='r', label=f'Running Average (Window Size: {window_size})')

plt.title('Iteration vs Score')
plt.xlabel('Iteration')
plt.ylabel('Score')
plt.grid(True)
plt.show()
