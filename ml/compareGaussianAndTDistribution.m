function compareGaussianAndTDistribution(pts)
    X = sampleFromGaussian(pts, 0, 1)';
    gaussianF = fitdist(X, 'Normal');
    studentTF = fitdist(X, 'tLocationScale');
    subplot(2, 2, 1);
    plot(gaussianF, 'r-');
    subplot(2, 2, 2);
    plot(studentTF, 'b--');

    noisyX = sampleFromGaussianWithGaussianNoise(pts, 0, 1, 0, 0.1)';
    gaussianNoisyF = fitdist(noisyX, 'Normal');
    studentTNoisyF = fitdist(noisyX, 'tLocationScale');
    subplot(2, 2, 3);
    plot(gaussianNoisyF, 'g-');
    subplot(2, 2, 4);
    plot(studentTNoisyF, 'y--');
end

function ret = sampleFromGaussian(pts, mean, sigma)
% pts is the number of one dimensional data points to sample
    ret = normrnd(mean, sigma, [1, pts]);
end

function ret = sampleFromGaussianWithGaussianNoise(pts, mean, sigma, noiseMean, noiseSigma)
% pts is the number of one dimensional data points to sample
    ret = normrnd(mean, sigma, [1, pts]) + normrnd(pts, noiseMean, noiseSigma);
end

function [mu, sigma] = maximumLikelihoodEstimationForOneDGaussian(X)
% X is a one dimensional vector [X1, X2, ..., Xn]
    n = length(X);
    mu = mean(X);
    sigma = sqrt(1/n*sum(X.*X) - mu*mu);
end

function [mu, sigma] = methodOfMomentsEstimationForOneDGaussian(X)
% X is a one dimensional vector [X1, X2, ..., Xn]
    n = length(X);
    mu = mean(X);
    sigma = sqrt(1/n*sum(X.*X) - mu*mu);
end
