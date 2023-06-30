import logic_2048
import time
import random
import tensorflow as tf


# Hyperparameters
learning_rate = 0.001
discount_factor = 0.99
epsilon = 0.1
#Number of epochs to train
num_episodes = 1000

# Initialize the game
game_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
game_board_rows = 4
game_board_cols = 4
game_matrix = logic_2048.place_new(game_board)
num_actions = 4
score = 0
n = 0
win_count = 0
lose_count = 0

# Define the Critic model
critic_model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(game_board_rows * game_board_cols,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Define the Actor model
actor_model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(game_board_rows * game_board_cols,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(num_actions, activation='softmax')
])

# Define the optimizer for the Critic model
critic_optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate)

# Define the optimizer for the Actor model
actor_optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate)

# Compile the Critic model
critic_model.compile(optimizer=critic_optimizer, loss='mse')

# Compile the Actor model
actor_model.compile(optimizer=actor_optimizer, loss='categorical_crossentropy')

def compute_gradients(predicted_value, target_value):
    with tf.GradientTape() as tape:
        critic_loss = tf.reduce_mean(tf.square(target_value - predicted_value))
    critic_gradients = tape.gradient(critic_loss, critic_model.trainable_variables)
    return critic_gradients


def compute_actor_gradients(action_value, action):
    with tf.GradientTape() as tape:
        actor_loss = -tf.reduce_mean(action_value * action)
    actor_gradients = tape.gradient(actor_loss, actor_model.trainable_variables)
    return actor_gradients


def update_critic_model(critic_gradients, critic_variables):
    try:
        critic_optimizer.apply_gradients(zip(critic_gradients, critic_variables))
    except:
        critic_optimizer.build(critic_model.trainable_variables)


def update_actor_model(actor_gradients, actor_variables):
    try:
        actor_optimizer.apply_gradients(zip(actor_gradients, actor_variables))
    except:
        actor_optimizer.build(actor_model.trainable_variables)

# Function to evaluate the state and action
def evaluate_state_action(state, action):
    # Compute the evaluation score based on the state and action

    # Obtain the dimensions of the game board
    rows = len(state)
    cols = len(state[0])

    # Initialize the evaluation score
    score = 0

    # Calculate the sum of the values on the game board
    sum_values = sum(sum(row) for row in state)
    score += sum_values

    # Find the maximum value on the game board
    max_value = max(max(row) for row in state)
    score += max_value

    # Count the number of empty cells on the game board
    num_empty_cells = sum(row.count(0) for row in state)
    score += num_empty_cells

    # Apply additional heuristics based on the chosen action
    if action == "a":
        # Heuristics for the "left" action
        # 1. Favor states where the larger values are concentrated on the left side
        left_sum = sum(state[row][col] for row in range(rows) for col in range(cols // 2))
        right_sum = sum(state[row][col] for row in range(rows) for col in range(cols // 2, cols))
        score += (left_sum - right_sum)

        # 2. Give higher scores for states where adjacent cells have similar values
        adjacency_bonus = 0
        for row in range(rows):
            for col in range(cols - 1):
                if state[row][col] == state[row][col + 1]:
                    adjacency_bonus += state[row][col]
        score += adjacency_bonus

    elif action == "s":
        # Heuristics for the "down" action
        # 1. Favor states where the larger values are concentrated at the bottom
        bottom_sum = sum(state[row][col] for row in range(rows // 2, rows) for col in range(cols))
        top_sum = sum(state[row][col] for row in range(rows // 2) for col in range(cols))
        score += (bottom_sum - top_sum)

        # 2. Give higher scores for states where adjacent cells have similar values
        adjacency_bonus = 0
        for row in range(rows - 1):
            for col in range(cols):
                if state[row][col] == state[row + 1][col]:
                    adjacency_bonus += state[row][col]
        score += adjacency_bonus

    elif action == "w":
        # Heuristics for the "up" action
        # 1. Favor states where the larger values are concentrated at the top
        top_sum = sum(state[row][col] for row in range(rows // 2) for col in range(cols))
        bottom_sum = sum(state[row][col] for row in range(rows // 2, rows) for col in range(cols))
        score += (top_sum - bottom_sum)

        # 2. Give higher scores for states where adjacent cells have similar values
        adjacency_bonus = 0
        for row in range(1, rows):
            for col in range(cols):
                if state[row][col] == state[row - 1][col]:
                    adjacency_bonus += state[row][col]
        score += adjacency_bonus

    elif action == "d":
        # Heuristics for the "right" action
        # 1. Favor states where the larger values are concentrated on the right side
        right_sum = sum(state[row][col] for row in range(rows) for col in range(cols // 2, cols))
        left_sum = sum(state[row][col] for row in range(rows) for col in range(cols // 2))
        score += (right_sum - left_sum)

        # 2. Give higher scores for states where adjacent cells have similar values
        adjacency_bonus = 0
        for row in range(rows):
            for col in range(cols - 1):
                if state[row][col] == state[row][col + 1]:
                    adjacency_bonus += state[row][col]
        score += adjacency_bonus

    return score


def choose_action(state, epsilon):
    if random.random() < epsilon:
        # Explore: choose a random action
        action = random.choice(["a", "s", "w", "d"])
    else:
        # Exploit: choose the action with the highest evaluation
        action_values = {
            "a": evaluate_state_action(state, "a"),
            "s": evaluate_state_action(state, "s"),
            "w": evaluate_state_action(state, "w"),
            "d": evaluate_state_action(state, "d")
        }
        action = max(action_values, key=action_values.get)
    return action

def choose_best_action(state):
    action_values = {
        "a": evaluate_state_action(state, "a"),
        "s": evaluate_state_action(state, "s"),
        "w": evaluate_state_action(state, "w"),
        "d": evaluate_state_action(state, "d")
    }
    best_action = max(action_values, key=action_values.get)
    return best_action


critic_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
actor_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

# Define a dictionary mapping actions to indices
# Required for actor`s one-hot tensor
action_indices = {'a': 0, 'w': 1, 's': 2, 'd': 3}

for episode in range(num_episodes):
    #Load existing models or continue with new ones
    try:
        critic_model = tf.keras.models.load_model('critic_model.h5')
        actor_model = tf.keras.models.load_model('actor_model.h5')
    except:
        print("Nie znaleziono modelu, używam nowego")
        time.sleep(5)

    game_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    game_matrix = logic_2048.place_new(game_board)
    print("Nowa epoka. Numer epoki: ", episode)
    trainingTime = 1
    n = 0
    reward = 0
    print("Liczba zwycięstw ", win_count)
    print("Liczba porażek ", lose_count)
# Training loop
    while trainingTime == 1:

        # Get the trainable variables for the Critic model
        critic_variables = critic_model.trainable_variables

        # Get the trainable variables for the Actor model
        actor_variables = actor_model.trainable_variables
        state = game_matrix

        # Choose action based on the current state and policy (Actor model)
        action = choose_action(state, epsilon)

        # Apply the chosen action to the game and observe the new state, reward, and whether the game is over
        new_game_matrix, success, reward,  = logic_2048.transform_matrix(game_matrix, action)
        success = logic_2048.check_loss_or_stuck(game_matrix, action)
        # Update the game matrix, score, and check if the game is over or won
        game_matrix = new_game_matrix
        score += reward
        #print(success)
        # Compute the target value for the Critic model
        next_state = game_matrix
        next_action = choose_best_action(next_state)  # Choose the best action based on the evaluation
        next_state_value = evaluate_state_action(next_state, next_action)
        target_value = reward + discount_factor * next_state_value

        # Compute the predicted value for the current state (Critic model)
        predicted_value = evaluate_state_action(state, action)

        # Compute the TD error
        td_error = target_value - predicted_value

        # Compute the gradients of the Critic model
        # Compute the gradients of the Critic model
        with tf.GradientTape() as tape:
            predicted_value = critic_model(tf.zeros((1, game_board_rows * game_board_cols)))
            critic_loss = tf.reduce_mean(tf.square(target_value - predicted_value))
        critic_gradients = tape.gradient(critic_loss, critic_model.trainable_variables)

    #    print("Predicted value:", predicted_value)
    #    print("Target value:", target_value)
    #    print("Critic gradients:", critic_gradients)

        #  print(critic_model.trainable_variables)

        # Apply the gradients to update the Critic model
        update_critic_model(critic_gradients, critic_model.trainable_variables)

        # Compute the action value for the current state and chosen action (Actor model)
        action_value = evaluate_state_action(state, action)

        # Compute the gradients of the Actor model
        with tf.GradientTape() as tape:
            predicted_value = actor_model(tf.zeros((1, game_board_rows * game_board_cols)))

            # Convert the action to a one-hot tensor
            action_index = action_indices[action]
            action_one_hot = tf.one_hot([action_index], depth=num_actions)

            actor_loss = -tf.reduce_mean(predicted_value * action_one_hot)  # Compute the actor loss

        actor_gradients = tape.gradient(actor_loss, actor_model.trainable_variables)

        # Apply the gradients to update the Actor model
        update_actor_model(actor_gradients, actor_model.trainable_variables)

        if logic_2048.win_check(game_matrix):
            print("------------")
            print("CONGRATS! YOU WON!")
            print("Numer epoki ", episode)
            print("Liczba ruchów ", n)
            print("Osiągnięta wartość ", reward)
            print("Wynik: ", score)
            for row in (game_matrix):
                print(row)
            print("------------")
            reward += 100 #Extra reward for winning the game
            print("Zapisywanie modelu treningowego ")
            critic_model.save('critic_model.h5')
            actor_model.save('actor_model.h5')
            print("Zapisano model!")
            win_count += 1
            trainingTime = 0
            #time.sleep(10)
            break

        elif success == -2:
            print("------------")
            print("Game over")
            print("Numer epoki ", episode)
            print("Liczba ruchów ", n)
            print("Osiągnięta wartość ", reward)
            print("Wynik: ", score)
            for row in (game_matrix):
                print(row)
            print("------------")
            print("Zapisywanie modelu treningowego ")
            critic_model.save('critic_model.h5')
            actor_model.save('actor_model.h5')
            print("Zapisano model!")
            lose_count += 1
            trainingTime = 0
            #time.sleep(5)
            break

        if(success == 0):
            n += 1
           # print("------------")
           # print("Nagroda: ", reward)
           # print("Prawidłowa akcja ",action)
           # for row in (game_matrix):
           #     print(row)
           # print("------------")

        elif(success == -1):
            td_error *= -1  # Zwiększamy wartość błędu TD przez pomnożenie przez -1
            #print("------------")
            #print("Model wykonał niedozowolny ruch ", action)
            #for row in (game_matrix):
            #    print(row)
            #print("------------")
        time.sleep(0.001)  # Introduce a delay before the next move

"""------------------------------------------------------------------"""

print("Ogólna liczba zwycięstw ", win_count)
print("Ogólna liczba porażek ", lose_count)

print("Ukończono trening, zapisywanie modelu")
#Le last save
critic_model.save('critic_model_final.h5')
actor_model.save('actor_model_final.h5')
print("Pomyślnie zapisano model. Miłego dnia!")