import json
from collections import Counter

def analyze_learning():
    filename = "agent_log.jsonl"
    logs = []

    try:
        # 1. Load the Experience Buffer (JSONL)
        with open(filename, "r") as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        
        if not logs:
            print("Error: The log file is empty. Run the agent first!")
            return

        # 2. Extract Key Performance Indicators (KPIs)
        total_steps = len(logs)
        # Check if the goal was ever reached
        success_steps = [i for i, log in enumerate(logs) if log['success']]
        
        # 3. Environment Knowledge (Objects seen by YOLO during RL)
        all_seen = [obj for entry in logs for obj in entry['seen']]
        knowledge_base = Counter(all_seen)

        # 4. Generate the Report
        print("\n" + "="*35)
        print("  AI2-THOR VQA-RL AGENT REPORT  ")
        print("="*35)
        
        print(f"Total Experience:  {total_steps} frames/steps")
        
        if success_steps:
            first_success = success_steps[0] + 1
            print(f"Goal Status:       SUCCESS")
            print(f"Discovery Time:    Found target at step {first_success}")
            print(f"Efficiency:        {round((1/first_success)*100, 2)}% search speed")
        else:
            print(f"Goal Status:       STILL SEARCHING (No success recorded)")

        print("\n--- Environment Knowledge Base ---")
        if not knowledge_base:
            print("No objects detected yet.")
        else:
            print(f"{'Object Name':<15} | {'Times Seen':<10}")
            print("-" * 28)
            for obj, count in knowledge_base.most_common(5): # Show top 5
                print(f"{obj:<15} | {count:<10}")

        print("="*35)
        print("Report Generated Successfully.")

    except FileNotFoundError:
        print(f"Error: {filename} not found. Ensure your agent is logging data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyze_learning()