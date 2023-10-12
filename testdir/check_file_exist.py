import os

def check_file_exist(file_path):
    """
    Check if a file exists and print the result.

    Args:
        file_path (str): The path to the file to be checked.
    """
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
    else:
        print(f"The file '{file_path}' does not exist.")

# Example usage:
root_path=" "
cups_id="sub-CUPS003"
fname=rootpath+"PipelineOutputs/bids/derivatives/fmriprep/"cups_id+"/figures/"+cups_id+"_ses-A_task-rest_dir-PA_run-1_desc-sdc_bold.svg"
fname2=root_path+"PipelineOutputs/bids/derivatives/qsiprep/"+cups_id+"/figures/"+cups_id+"_ses-A_run-1_desc-sdc_b0.svg"
#or list of files:
file_lists=[fname1, fname2]
for f in file_lists:
    check_file_exist(f)
