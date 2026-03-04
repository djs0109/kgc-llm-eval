from LLM_eval_agent.utils.prompts import prompts
import pyperclip
import json
import matplotlib.pyplot as plt
import collections
import matplotlib

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Times New Roman']


task_mappings = {
    "1": "Identification of API Endpoints",
    "2": "Semantic Analysis of JSON Keys",
    "3": "Entity Type Mapping",
    "4": "Property Mapping",
    "5": "Validation of Ontology Classes",
    "6": "Mapping of Supplementary Entities",
    "7": "Connection Property Identification"
}

# todo task mapping for KGC

def metrics_evaluation(results_dict):
    bar_plot_cognitive(results_dict)
    line_plot_human_effort(results_dict)


def bar_plot_cognitive(results_dict):
    # count steps per Bloom-Level
    bloom_counter = collections.Counter()
    for steps in results_dict.values():
        for step in steps:
            bloom_counter[step.get('bloom_level', 'Unknown')] += 1
    levels = list(bloom_counter.keys())
    counts = [bloom_counter[l] for l in levels]
    # Calculate percentage
    percentages = [(count / sum(counts)) * 100 for count in counts]
    color = '#0073C0'
    plt.figure(figsize=(4.75, 2.3))
    bars = plt.bar(levels, percentages, color=color)
    plt.ylabel('Frequency of cognitive processes in percentage', fontsize=7)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.tight_layout()
    plt.show()


def line_plot_human_effort(results_dict):
    # calculate total_human_effort per task step
    efforts = []
    task_names = []
    for task_num, steps in results_dict.items():
        task_names.append(task_mappings[task_num])
        total = 0
        for step in steps:
            total += step.get('total_human_effort', 0)
        efforts.append(total)
    colors = ['#FFCF8E', '#2F8284', '#00B2B1', '#51BC4A']
    plt.figure(figsize=(4.75, 2.3))
    plt.plot(task_names, efforts, marker='o', color=colors[1])
    plt.ylabel('Human effort score', fontsize=7)
    plt.xticks(fontsize=7, rotation=15)
    plt.yticks(fontsize=7)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    path_cot = r"D:\Git\kgc-llm-eval\LLM_eval_agent\results\fiware_v1_context_gemini(example)\CoT.txt"
    path_evaluation_output = r"D:\Git\kgc-llm-eval\LLM_eval_agent\results\fiware_v1_context_gemini(example)\output_evaluation.json"

    # load the cot from the file
    with open(path_cot, "r") as f:
        cot = f.read()
    prompt_evaluation = prompts.evaluation_prompt(cot_content=cot)
    # copy the prompt to the clipboard
    pyperclip.copy(prompt_evaluation)
    print(prompt_evaluation)
    print("Prompt for CoT evaluation has been copied to the clipboard.")

    res = input("Paste the response from the LLM here and press Enter to continue...")
    # validate the json format of the response
    try:
        res_dict = json.loads(res)
        print("Response is a valid JSON, saving to file...")
        # save the response to a file
        with open(path_evaluation_output, "w") as f:
            json.dump(res_dict, f, indent=2)
    except json.JSONDecodeError as e:
        print("Response is not a valid JSON. Please check the format and try again.")
        print(f"Error details: {e}")
        raise e
    metrics_evaluation(results_dict=res_dict)
