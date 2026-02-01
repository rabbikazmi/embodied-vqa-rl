import json
import matplotlib.pyplot as plt

def plot_reward_curve():
    rewards = []
    cumulative_reward = 0
    rewards_history = []

    try:
        with open("agent_log.jsonl", "r") as f:
            for line in f:
                data = json.loads(line)
                cumulative_reward += data['reward']
                rewards_history.append(cumulative_reward)
        
        if not rewards_history:
            print("Log file is empty!")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(rewards_history, color='green', linewidth=2)
        plt.title('Agent Learning Progress (Cumulative Reward)')
        plt.xlabel('Steps (Frames)')
        plt.ylabel('Total Reward')
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # Save as image for README
        plt.savefig('reward_curve1.png')
        print("Success! Created 'reward_curve1.png'. You can now add this to your README.")
        
    except FileNotFoundError:
        print("Error: agent_log.jsonl not found.")

if __name__ == "__main__":
    plot_reward_curve()