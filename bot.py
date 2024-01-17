import json


class FlappyBirdQLearningBot(object):
    """
    The FlappyBirdQLearningBot class that applies the Q-learning logic to Flappy Bird game
    After every iteration (iteration = 1 game that ends with the bird dying) updates Q values
    After every DUMPING_N iterations, dumps the Q values to the local JSON file
    """

    def __init__(self):
        self.game_count = 0  # Game count of current run, incremented after every death
        self.dumping_interval = 25  # Number of iterations to dump Q values to JSON after
        self.discount_factor = 1.0
        self.rewards = {0: 1, 1: -1000}  # Reward function
        self.learning_rate = 0.7
        self.load_q_values()
        self.last_state = "420_240_0"   
        self.last_action = 0
        self.moves = []


        

    def load_q_values(self):
        """
        Load q values from a JSON file
        """
        self.q_values = {}
        try:
            file = open("data/qval.json", "r")
        except IOError:
            return
        self.q_values = json.load(file)
        file.close()

    def actions(self, x_diff, y_diff, velocity):
        """
        Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        """
        state = self.map_state(x_diff, y_diff, velocity)

        self.moves.append(
            (self.last_state, self.last_action, state)
        )  # Add the experience to the history

        self.last_state = state  # Update the last_state with the current state

        if self.q_values[state][0] >= self.q_values[state][1]:
            self.last_action = 0
            return 0
        else:
            self.last_action = 1
            return 1

    def writeQval(self, dump_q_values=True):
        """
        Update q_values via iterating over experiences
        """
        history = list(reversed(self.moves))

        # Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split("_")[1]) > 120 else False

        # Q-learning score updates
        t = 1
        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]

            # Select reward
            if t == 1 or t == 2:
                current_reward = self.rewards[1]
            elif high_death_flag and act:
                current_reward = self.rewards[1]
                high_death_flag = False
            else:
                current_reward = self.rewards[0]

            # Update
            self.q_values[state][act] = (1 - self.learning_rate) * (self.q_values[state][act]) + \
                                        self.learning_rate * (
                                                current_reward + self.discount_factor * max(self.q_values[res_state]))

            t += 1

        self.game_count += 1  # Increase game count
        if dump_q_values:
            self.dump_q_values()  # Dump q_values (if game count % DUMPING_N == 0)
        self.moves = []  # Clear history after updating strategies

    def map_state(self, x_diff, y_diff, velocity):
        """
        Map the (x_diff, y_diff, velocity) to the respective state, with regards to the grids
        The state is a string, "x_diff_y_diff_velocity"

        X -> [-40,-30...120] U [140, 210 ... 420]
        Y -> [-300, -290 ... 160] U [180, 240 ... 420]
        """
        if x_diff < 140:
            x_diff = int(x_diff) - (int(x_diff) % 10)
        else:
            x_diff = int(x_diff) - (int(x_diff) % 70)

        if y_diff < 180:
            y_diff = int(y_diff) - (int(y_diff) % 10)
        else:
            y_diff = int(y_diff) - (int(y_diff) % 60)

        return str(int(x_diff)) + "_" + str(int(y_diff)) + "_" + str(velocity)

    def dump_q_values(self, force=False):
        """
        Dump the q_values to the JSON file
        """
        if self.game_count % self.dumping_interval == 0 or force:
            file = open("data/flappy_bird_bot.json", "w")
            json.dump(self.q_values, file)
            file.close()
            print("Q-values updated on local file.", self.q_values)
