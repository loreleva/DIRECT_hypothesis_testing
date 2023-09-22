addpath(genpath('/home/levantesi/MATLAB Add-Ons/Toolboxes/DIRECTGO/Algorithms'));
addpath(genpath('/directgo/bbo_functions'));

format longEng;

dim = 2%str2num(getenv("TEST_DIRECT_F_DIM"));	
d = [-15, 35]%[str2num(getenv("TEST_DIRECT_F_LB")), str2num(getenv("TEST_DIRECT_F_UB"))];
D = repmat(d, dim);
P.f = "ackley_function"%getenv("TEST_DIRECT_F_NAME");

opts.maxevals = 1000%str2num(getenv("TEST_DIRECT_MAXEVALS"));
opts.maxits = 100%str2num(getenv("TEST_DIRECT_MAXEVALS"));
opts.maxdeep = 100%str2num(getenv("TEST_DIRECT_MAXEVALS"));
opts.testflag = 1;
opts.tol = 0.000001%str2num(getenv("TEST_DIRECT_TOL"));
opts.globalmin = 0%str2num(getenv("TEST_DIRECT_GLOBALMIN"));
[f_min, x_min] = dDirect_GL(P, opts, D);

disp(f_min)
disp(f_min)
disp(x_min)
