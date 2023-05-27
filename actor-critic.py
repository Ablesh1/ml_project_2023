import tensorflow as tf
import numpy as np
from collections import deque
from logic_2048 import compress_ltr, compress_rtl, place_new, transform_matrix, win_check


class ActorCriticModel:
    def __init__(self, input_shape, action_space_size, learning_rate=0.001, gamma=0.99, entropy_beta=0.01):
        self.input_shape = input_shape
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.entropy_beta = entropy_beta
        self.optimizer = tf.optimizers.Adam(learning_rate=self.learning_rate)

        self.actor, self.critic = self.create_actor_critic_networks()
        self.actor.summary()
        self.critic.summary()

    def create_actor_critic_networks(self):
        input_layer = tf.keras.layers.Input(shape=self.input_shape)
        flatten_layer = tf.keras.layers.Flatten()(input_layer)

        # Create actor network
        dense_1 = tf.keras.layers.Dense(128, activation='relu')(flatten_layer)
        dense_2 = tf.keras.layers.Dense(128, activation='relu')(dense_1)
        action_logits = tf.keras.layers.Dense(self.action_space_size)(dense_2)
        action_probs = tf.keras.layers.Softmax()(action_logits)

        # Create critic network
        dense_3 = tf.keras.layers.Dense(128, activation='relu')(flatten_layer)
        dense_4 = tf.keras.layers.Dense(128, activation='relu')(dense_3)
        value = tf.keras.layers.Dense(1)(dense_4)

        actor = tf.keras.models.Model(inputs=input_layer, outputs=action_probs)
        critic = tf.keras.models.Model(inputs=input_layer, outputs=value)

        return actor, critic

    def get_action(self, state):
        # Add batch dimension to state
        state = np.expand_dims(state, axis=0)

        # Predict action probabilities using actor network
        action_probs = self.actor.predict(state)[0]

        # Sample action from action probability distribution
        action = np.random.choice(self.action_space_size, p=action_probs)

        return action, action_probs

    def train(self, state_history, action_history, reward_history, next_state_history, done_history):
        # Convert lists to numpy arrays
        state_history = np.array(state_history)
        action_history = np.array(action_history)
        reward_history = np.array(reward_history)
        next_state_history = np.array(next_state_history)
        done_history = np.array(done_history)

        # Calculate discounted rewards
        discounted_rewards = self.get_discounted_rewards(reward_history, done_history)

        # Calculate advantages
        critic_predictions = self.critic.predict(state_history)
        next_state_value = self.critic.predict(next_state_history)
        advantages = reward_history + self.gamma * (
                    1 - done_history) * next_state_value.flatten() - critic_predictions.flatten()

        # Compute actor loss
        action_mask = tf.one_hot(action_history, self.action_space_size)
        with tf.GradientTape() as tape:
            log_probs = tf.math.log(self.actor(state_history) + 1e-10)
            entropy = -tf.math.reduce_sum(self.actor(state_history) * log_probs)
            actor_loss = -tf.math.reduce_sum(action_mask * log_probs * advantages) - self.entropy_beta * entropy

        # Compute critic loss
        critic_target = reward_history + self.gamma * (1 - done_history) * next_state_value.flatten()
        critic_loss = tf.keras.losses.mean_squared_error(critic_target, critic_predictions)
        critic_loss = tf.math.reduce_mean(critic_loss)

        # Update actor and critic networks
        actor_gradients = tape.gradient(actor_loss, self.actor.trainable_variables)
        critic_gradients = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.optimizer.apply_gradients(zip(actor_gradients, self.actor.trainable_variables))
        self.optimizer.apply_gradients(zip(critic_gradients, self.critic.trainable_variables))