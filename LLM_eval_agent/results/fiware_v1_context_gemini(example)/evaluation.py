from LLM_eval_agent.utils.prompts import prompts
import pyperclip
import json


def metrics_evaluation(results_dict):
    # TODO: process the metrics
    pass


if __name__ == '__main__':
    path_cot = r"D:\Git\kgc-llm-eval\LLM_eval_agent\results\fiware_v1_context_gemini(example)\prompt_cot_evaluation.txt"
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
