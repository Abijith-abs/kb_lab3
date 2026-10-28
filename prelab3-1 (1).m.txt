% Create a cosine signal with 30 samples at 10 samples per period.
n = [0:29];
x = cos(2*pi*n/10);

% Define 3 different values for N
N1 = 64;
N2 = 128;
N3 = 256;

% Take the transform of x[n] for each of the 3 values that were defined 
% The abs function finds the magnitude of the transform
X1 = abs(fft(x,N1));
X2 = abs(fft(x,N2));
X3 = abs(fft(x,N3));

% The frequency scale begins at 0 and extends to N - 1 for an N-point FFT.
% We normalize the scale so that it extends from 0 to 1/N
F1 = [0 : N1 - 1]/N1;
F2 = [0 : N2 - 1]/N2;
F3 = [0 : N3 - 1]/N3;

% Plot the transforms
subplot(3,1,1)
plot(F1,X1,'-x'),title('N = 64'),axis([0 1 0 30])
subplot(3,1,2)
plot(F2,X2,'-x'),title('N = 128'),axis([0 1 0 30])
subplot(3,1,3)
plot(F3,X3,'-x'),title('N = 256'),axis([0 1 0 30])

