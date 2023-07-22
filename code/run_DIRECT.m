addpath(genpath('/home/loreleva/MATLAB Add-Ons/Toolboxes/DIRECTGO/Algorithms'))
addpath(genpath('/usr/local/MATLAB/R2023a/bbo_functions'))

format longEng

dim = str2num(getenv("TEST_DIRECT_F_DIM"));	
d = [str2num(getenv("TEST_DIRECT_F_LB")), str2num(getenv("TEST_DIRECT_F_UB"))];
D = repmat(d, dim);
P.f = getenv("TEST_DIRECT_F_NAME");

opts.maxevals = str2num(getenv("TEST_DIRECT_MAXEVALS"));
[f_min, x_min] = dDirect_GL(P, opts, D);

disp(f_min)
disp(x_min)