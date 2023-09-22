import os, math
from utils import *

csv_sep = ";"


# ADD IN RESULTS LOG THE ITERATION NUMBER AND NUMBER OF FUNCTION EVALS OF WHEN, IF ANY, THE OBJECTIVE FUNCTION IS FOUND WITH ACCURACY 1E-6


# create all the csv files with the corresponding header
def init_log_files(filepath):
	# single runs log
	filepath_log = os.path.join(filepath, "log_iterations.csv")
	header = (
				f"Index{csv_sep} "
				f"Iteration{csv_sep} "
				f"Optimum Found{csv_sep} "
				f"Function Optimum{csv_sep} "
				f"Objective Function Error{csv_sep} "
				f"Seconds{csv_sep} "
				f"Time{csv_sep} "
				f"Function EvaluationsP{csv_sep} "
				f"VMS ram usage{csv_sep} "
				f"RSS ram usage\n"
			)
	with open(filepath_log, "w") as f:
		f.write(header)
		f.close()

	# result log
	filepath_log = os.path.join(filepath, "log_results.csv")
	header = (
				f"Iterations{csv_sep} "
				f"Iteration when optimum found{csv_sep} "
				f"Function Evaluations when optimum found{csv_sep} "
				f"Optimum Found{csv_sep} "
				f"Function Optimum{csv_sep} "
				f"Input Optimum Found{csv_sep} "
				f"Function Input Optimum{csv_sep} "
				f"Objective Function Error{csv_sep} "
				f"Solution Error{csv_sep} "
				f"Seconds{csv_sep} "
				f"Time{csv_sep} "
				f"Function Evaluations{csv_sep} "
				f"Max VMS ram usage{csv_sep} "
				f"Max RSS ram usage\n"
			)
	with open(filepath_log, "w") as f:
		f.write(header)
		f.close()


def write_iteration_log(filepath, n_iter, f_min, global_f_min, f_eval, seconds, ram_usage, verbose=False):
	filepath_log = os.path.join(filepath, "log_iterations.csv")
	log_str = (
				f"{n_iter-1}{csv_sep} "
				f"{n_iter}{csv_sep} "
				f"{f_min}{csv_sep} "
				f"{global_f_min}{csv_sep} "
				f"{objective_function_error(global_f_min, f_min)}{csv_sep} "
				f"{seconds}{csv_sep} "
				f"{time_to_str(seconds)}{csv_sep} "
				f"{f_eval}{csv_sep} "
				f"{ram_usage[0]}{csv_sep} "
				f"{ram_usage[1]}\n"
			)

	if verbose:
		print("Single Iteration Log:\n" + log_str)
	
	with open(filepath_log, "a") as f:
		f.write(log_str)
		f.close()

def write_results_log(filepath, n_iter, f_min, global_f_min, f_eval, seconds, input_opt, x_min, iter_opt, f_eval_opt, max_ram_usage, verbose=False):
	filepath_log = os.path.join(filepath, "log_results.csv")
	log_str = (
				f"{n_iter}{csv_sep} "
				f"{iter_opt}{csv_sep} "
				f"{f_eval_opt}{csv_sep} "
				f"{f_min}{csv_sep} "
				f"{global_f_min}{csv_sep} "
				f"{x_min}{csv_sep} "
				f"{input_opt}{csv_sep} "
				f"{objective_function_error(global_f_min, f_min)}{csv_sep} "
				f"{solution_error(input_opt, x_min)}{csv_sep} "
				f"{seconds}{csv_sep} "
				f"{time_to_str(seconds)}{csv_sep} "
				f"{f_eval}{csv_sep} "
				f"{max_ram_usage[0]}{csv_sep} "
				f"{max_ram_usage[1]}\n"	
			)

	if verbose:
		print("Results Log:\n" + log_str)
	
	with open(filepath_log, "a") as f:
		f.write(log_str)
		f.close()