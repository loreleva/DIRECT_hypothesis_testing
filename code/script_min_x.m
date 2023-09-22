addpath(genpath('/home/levantesi/MATLAB Add-Ons/Toolboxes/DIRECTGO/Algorithms'));
addpath(genpath('/directgo/bbo_functions'));

format longEng;

dim = str2num(getenv("TEST_DIRECT_F_DIM"));	
d = [str2num(getenv("TEST_DIRECT_F_LB")), str2num(getenv("TEST_DIRECT_F_UB"))];
D = repmat(d, dim);
P.f = getenv("TEST_DIRECT_F_NAME");

opts.maxevals = str2num(getenv("TEST_DIRECT_MAXEVALS"));
opts.maxits = str2num(getenv("TEST_DIRECT_MAXEVALS"));
opts.maxdeep = str2num(getenv("TEST_DIRECT_MAXEVALS"));
opts.testflag = 1;
opts.tol = str2num(getenv("TEST_DIRECT_TOL"));
opts.globalmin = str2num(getenv("TEST_DIRECT_GLOBALMIN"));
[f_min, x_min] = dDirect_GL(P, opts, D);

disp(f_min)
disp(x_min)
