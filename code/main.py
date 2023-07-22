import subprocess, math, os, signal, argparse, sys
import sfu.objective_function_class as obj_func
from memory_profiler import memory_usage
import write_logs as log
from utils import *

def direct_run(obj, maxevals, bounds, filepath, correctness_thr, verbose):
	# init function name env var
	os.environ["TEST_DIRECT_F_NAME"] = obj.name
	os.environ["TEST_DIRECT_F_DIM"] = str(obj.dimension)
	os.environ["TEST_DIRECT_F_LB"] = str(bounds[0])
	os.environ["TEST_DIRECT_F_UB"] = str(bounds[1])
	os.environ["TEST_DIRECT_MAXEVALS"] = str(maxevals)

	comand = ["/usr/local/MATLAB/R2023a/bin/matlab", "-sd", "/home/loreleva/Desktop/DIRECT_test_MATLAB/code", "-batch", "run_DIRECT"]
	process = subprocess.Popen(comand, shell=False, stdout=subprocess.PIPE)
	max_ram_usage = 0
	iter_opt = ""
	f_eval_opt = ""
	while True:
		# obtain output
		output = process.stdout.readline()
		output = output.strip().decode('UTF-8').split()

		# exit when max evals are exceeded
		if output[0] == "Exceeded":
			break
		# log infos during runs
		if len(output) < 1 or output[0] != "Iter:":
			continue

		# save values of the iteration
		n_iter = int(output[1])
		f_min = float(output[3])
		time = float(output[5])
		f_eval = int(output[8])
		mem_usage = memory_usage(process.pid, max_usage=True)
		if mem_usage > max_ram_usage:
			max_ram_usage = mem_usage

		if iter_opt == "" and objective_function_error(obj.opt, f_min) <= correctness_thr:
			iter_opt = n_iter
			f_eval_opt = f_eval
		log.write_iteration_log(filepath, n_iter, f_min, obj.opt, f_eval, time, verbose)

	# obtain best value found
	output = process.stdout.readline()
	output = output.strip().decode('UTF-8').split()

	f_min = float(output[0])

	x_min = []
	while len(x_min) < obj.dimension:
		output = process.stdout.readline()
		output = output.strip().decode('UTF-8').split()

		if len(output) != 1:
			continue
		else:
			x_min.append(float(output[0]))

	log.write_results_log(filepath, n_iter, f_min, obj.opt, f_eval, time, max_ram_usage, obj.input_opt, x_min, iter_opt, f_eval_opt, verbose)


def main(argv):
	# define parser and pars arguments
	parser = argparse.ArgumentParser(description="run test of DIRECT")
	parser.add_argument("function_name", help="objective function name")
	parser.add_argument("--dimensions", "-d", type=int, nargs="+", help="explicitly define dimensions on which perform the tests")
	parser.add_argument("--bounds", "-b", type=float, nargs=2, help="define bounds of the feasible domain of the objective function")
	parser.add_argument("--verbose", "-v", action="store_true")
	args = parser.parse_args()

	# init logs dir
	path_dir_res = os.path.join(os.path.dirname(__file__),"log_results")
	if not os.path.exists(path_dir_res):
		os.mkdir(path_dir_res)

	# path of the function results
	path_dir_res = os.path.join(path_dir_res, f"{args.function_name}")
	if not os.path.exists(path_dir_res):
		os.mkdir(path_dir_res)

	# define dimensions to test
	if args.dimensions == None:
		dimensions = [2] + [10*(x+1) for x in range(10)]
	else:
		dimensions = args.dimensions

	obj_func.json_filepath = os.path.join("sfu", obj_func.json_filepath)

	# run tests for each dimension
	for dim in dimensions:
		# path of the results for the dimension dim
		path_dir_res_dim = os.path.join(path_dir_res, f"dimension_{dim}")
		if not os.path.exists(path_dir_res_dim):
			os.mkdir(path_dir_res_dim)

		# init objective function class to obtain infos about function
		obj = obj_func.objective_function(args.function_name, dim)

		# path of the logs
		path_dir_log_file = os.path.join(path_dir_res_dim, f"function_{obj.name}_dimension_{obj.dimension}")
		if not os.path.exists(path_dir_log_file):
			os.mkdir(path_dir_log_file)

		log.init_log_files(path_dir_log_file)
		
		f_eval = 10*10**6

		# rerun DIRECT to obtain x min
		direct_run(obj, f_eval, args.bounds, path_dir_log_file, 1e-6, args.verbose)

if __name__ == "__main__":
	main(sys.argv[1:])