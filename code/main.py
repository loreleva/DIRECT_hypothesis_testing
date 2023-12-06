import subprocess, psutil, math, os, signal, argparse, sys
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
	os.environ["TEST_DIRECT_TOL"] = str(correctness_thr)
	os.environ["TEST_DIRECT_GLOBALMIN"] = str(obj.opt)
	comand = ["matlab", "-sd", "/home/levantesi/direct_test/code", "-batch", "script_min_x"]
	process = subprocess.Popen(comand, shell=False, stdout=subprocess.PIPE)
	max_ram_usage_vms = 0
	max_ram_usage_rss = 0
	iter_opt = ""
	f_eval_opt = ""
	idx_file = 0
	f_min = None
	while True:
		# obtain output
		output = process.stdout.readline()
		output = output.strip().decode('UTF-8').split()

		# log infos during runs
		if len(output) < 1:
			continue
		if output[0] == "Minima":
			f_min = float(output[-1])
			break
		if output[0] == "Exceeded" or output[0] == "Minima":
			break
		if output[0] != "Iter:":
			continue
		# save values of the iteration
		n_iter = int(output[1])
		f_min = float(output[3])
		wall_clock_time = float(output[7])
		total_cpu_time = float(output[11])
		cpus_used = int(output[13])
		mean_cpu_time = float(output[19])
		f_eval = int(output[22])
		proc = psutil.Process(int(subprocess.check_output(["pidof", "MATLAB"]).decode("utf-8")))
		mem_usage_vms = proc.memory_info().vms / 1073741824
		mem_usage_rss = proc.memory_info().rss / 1073741824
		
		if mem_usage_vms > max_ram_usage_vms:
			max_ram_usage_vms = mem_usage_vms

		if mem_usage_rss > max_ram_usage_rss:
			max_ram_usage_rss = mem_usage_rss

		if iter_opt == "" and objective_function_error(obj.opt, f_min) <= correctness_thr:
			iter_opt = n_iter
			f_eval_opt = f_eval
		
		log.write_iteration_log(filepath, n_iter, f_min, obj.opt, f_eval, (wall_clock_time, total_cpu_time, mean_cpu_time), (mem_usage_vms, mem_usage_rss) ,verbose)

	# obtain best value found
	output = process.stdout.readline()
	output = output.strip().decode('UTF-8').split()

	if f_min == None:
		f_min = float(output[0])

	x_min = []
	while len(x_min) < obj.dimension:
		output = process.stdout.readline()
		output = output.strip().decode('UTF-8').split()

		if len(output) != 1:
			continue
		else:
			x_min.append(float(output[0]))
	log.write_results_log(filepath, n_iter, 
							f_min, 
							obj.opt, 
							f_eval, 
							(wall_clock_time, total_cpu_time, mean_cpu_time), 
							obj.input_opt, 
							x_min, 
							iter_opt, 
							f_eval_opt, 
							(max_ram_usage_vms, max_ram_usage_rss),
							verbose
						)

def main(argv):
	# define parser and pars arguments
	parser = argparse.ArgumentParser(description="run test of DIRECT")
	parser.add_argument("function_name", help="objective function name")
	parser.add_argument("--dimensions", "-d", type=int, nargs="+", help="explicitly define dimensions on which perform the tests")
	parser.add_argument("--bounds", "-b", type=float, nargs=2, help="define bounds of the feasible domain of the objective function")
	parser.add_argument("--verbose", "-v", action="store_true")
	parser.add_argument("--max_evals", type=int, nargs=1, required=True, help="maximum number of function evaluations for DIRECT")
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
		
		f_eval = args.max_evals

                # rerun DIRECT to obtain x min
		direct_run(obj, f_eval, args.bounds, path_dir_log_file, 1e-6, args.verbose)

if __name__ == "__main__":
	main(sys.argv[1:])
