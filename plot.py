import matplotlib.pyplot as plt
import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('data/plotData.csv')

# Extract columns
iteration = data['iteration']
q_val = data['q_val']
score = data['score']

# Calculate the running average with a larger window size
window_size = 10  # Adjust this value as needed
running_avg_q_val = q_val.rolling(window=window_size).mean()
running_avg_score = score.rolling(window=window_size).mean()


# Identify top values in the "score" column
top_score_indices = score.nlargest(2000).index  # Adjust the number (5) based on how many top values you want to connect
top_score_values = score.loc[top_score_indices]



#plt.scatter(iteration.loc[top_score_indices], top_score_values, color='g', label='Top Score', zorder=5)
#plt.plot(iteration.loc[top_score_indices], top_score_values, linestyle='-', color='g', zorder=5)

'''
# Plotting
plt.figure(figsize=(10, 6))
#plt.plot(iteration, q_val,   linestyle='-', color='b', label='Q-value')
#plt.plot(iteration, running_avg_q_val, linestyle='--', color='r', label=f'Running Avg Q-value (Window Size: {window_size})')
plt.plot(iteration, score,  linestyle='-', color='g', label='Score')
plt.plot(iteration, running_avg_score, linestyle='--', color='orange', label=f'Running Avg Score (Window Size: {window_size})')
'''
plt.title('Iteration vs Q-value and Score with Running Averages')
plt.xlabel('Iteration')
plt.ylabel('Values')
plt.legend()
plt.grid(True)
plt.show()