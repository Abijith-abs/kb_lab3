function [xx, tt] = cosgen2(A, f, phi, t_start, dur, fs)
% COSGEN2 Function to generate Cos wave with varying amplitude, phase shift
% [xx,tt] = cosgen2(A, f,phi, t_start, dur, fs)
% A = amplitude
% f = desired frequency
% phi = phase (in degrees)
% t_start = starting time (in seconds)
% dur = duration of waveform in seconds
% fs = sampling frequency   (Note: number of samples per period = fs/f)
if (nargin < 6)
    fs = 50*f;                  % gives 50 samples per period by default
end;
    
tt = [t_start:1/fs: t_start+dur];  % gives 20 samples per period
xx = A*cos((2*pi*f*tt)+(phi*pi/180));
