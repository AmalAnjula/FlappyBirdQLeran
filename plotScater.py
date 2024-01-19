import matplotlib.pyplot as plt
import pandas as pd
#iteration,score,q_val,nowMem,pealMem
# Load the data from the CSV file
data = pd.read_csv('data/plotData.csv')

# Extract columns
iteration = data['iteration']
score = data['nowMem']

# Identify top values in the "score" column
top_score_indices = score.nlargest(3000).index  # Adjust the number (5) based on how many top values you want to plot
top_score_values = score.loc[top_score_indices]

window_size = 100  # Adjust this value as needed
running_avg_score = score.rolling(window=window_size).mean()


# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(iteration.loc[top_score_indices], top_score_values, color='g', label='Top Memory')
plt.plot(iteration, running_avg_score, linestyle='-', color='r', label=f'Running Avg Score (Window Size: {window_size})')

plt.title('Iteration vs Memory (Scatter Plot)')
plt.xlabel('Iteration')
plt.ylabel('Q Value')
plt.legend()
plt.grid(True)
plt.savefig('data/Memory_scatterl.png')
plt.show()
 