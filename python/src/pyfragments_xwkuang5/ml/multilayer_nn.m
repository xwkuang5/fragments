function ret = multilayer_nn(unit_type, data, mini_batch_size, architecture, epochs, weight_decay, learning_rate, momentum_multiplier)
% input is a matrix of size [num_training_case, num_dim]
% target is a matrix of size [num_training_case, 1]
    more off;

    training_input = data.training_input;
    training_target = data.training_target;
    validation_input = data.validation_input;
    validation_target = data.validation_target;
    test_input = data.test_input;
    test_target = data.test_target;
    num_training_case = size(training_input, 1);
    num_layers = size(architecture, 2);

    model = initialize_model(architecture);
    theta = model_to_theta(model);
    momentum_speed = theta * 0;
    training_data_losses = [];
    validation_data_losses = [];

    test_gradient_batch.input = training_input;
    test_gradient_batch.target = training_target;
    test_gradient(model, architecture, test_gradient_batch, unit_type, weight_decay);

    for epoch = 1:epochs
        training_batch_start = mod((epoch-1) * mini_batch_size, num_training_case) + 1;
        training_batch.input = training_input(training_batch_start:training_batch_start + mini_batch_size - 1, :);
        training_batch.target = training_target(training_batch_start:training_batch_start + mini_batch_size - 1, :);

        switch unit_type
            case 'linear'
                activities = linear_fprop(model, training_batch.input);
                gradient = linear_bprop(model, training_batch, activities, weight_decay);
            case 'sigmoid'
                activities = sigmoid_fprop(model, training_batch.input);
                gradient = sigmoid_bprop(model, training_batch, activities, weight_decay);
            case 'softmax'
                activities = softmax_fprop(model, training_batch.input);
                gradient = softmax_bprop(model, training_batch, activities, weight_decay);
            otherwise
                error('unit_type is not supported!');
        end

        momentum_speed = momentum_speed * momentum_multiplier - gradient;
        theta = theta + learning_rate * momentum_speed;
        model = theta_to_model(theta, architecture);
        training_data_losses = [training_data_losses, loss(unit_type, model, training_batch, weight_decay)];
        validation_data_losses = [validation_data_losses, loss(unit_type, model, training_batch, weight_decay)];
        if mod(epoch, round(epochs / 10)) == 0,
            fprintf('After %d epoch, training data loss is %f, and validation data loss is %f\n', epoch, training_data_losses(end), validation_data_losses(end));
        end
    end
    
    switch unit_type
        case 'linear'
            output = linear_fprop(model, training_input){end}
        case 'sigmoid'
            output = sigmoid_fprop(model, training_input){end}
        case 'softmax'
            output = softmax_fprop(model, training_input){end}
        otherwise
            error('unit_type is not supported!');
    end
end

% This function initializes a model given an architecture specified in vector format [num_input, num_hid_1, ..., num_hid_n, num_output]
function model = initialize_model(architecture)
% model is a [1 x num_layers-1] cell of weight matrices
    init_w = 0.1;
    num_layers = size(architecture, 2);
    for i = 1:num_layers-1
        model{i} = init_w .* randn(architecture(i), architecture(i + 1));
    end
end

% This function converts a model into a long vector
function ret = model_to_theta(model)
    ret = [];
    for i = 1:size(model, 2)
        ret = [ret, reshape(model{i}, 1, [])];
    end
end

% This function converts a long vector back into a model
function ret = theta_to_model(theta, architecture)
    num_layers = size(architecture, 2);
    left = 1;
    for i = 1:num_layers-1
        right = left + architecture(i) * architecture(i + 1) - 1;
        ret{i} = reshape(theta(left:right), architecture(i), architecture(i + 1));
        left = right + 1;
    end
end

% This function implements the forward propagation procedure for linear output neurons
function ret = linear_fprop(model, training_batch)
% training_batch is a matrix(tensor if input dimension > 2) of size [mini_batch_size, num_dim]
% ret is a [1 x num_layers] cell of activities vector of size [num_dim, mini_batch_size]
    num_layers = size(model, 2) + 1;
    for i = 1:num_layers
        if i == 1
            ret{1} = training_batch';
        else
            ret{i} = model{i-1}' * ret{i-1};
        end
    end
end

% This function implements the forward propagation procedure for logistic output neurons with cross-entropy loss
function ret = sigmoid_fprop(model, training_batch)
% training_batch is a matrix(tensor if input dimension > 2) of size [mini_batch_size, num_dim]
% ret is a [1 x num_layers] cell of activities vector of size [num_dim, mini_batch_size]
    num_layers = size(model, 2) + 1;
    for i = 1:num_layers
        if i == 1
            ret{1} = training_batch';
        else
            ret{i} = logistic(model{i-1}' * ret{i-1});
        end
    end
end

% This function implements the forward propagation procedure for softmax output neurons with cross-entropy loss
function ret = softmax_fprop(model, training_batch)
% training_batch is a matrix(tensor if input dimension > 2) of size [mini_batch_size, num_dim]
% ret is a [1 x num_layers] cell of activities vector of size [num_dim, mini_batch_size]
    num_layers = size(model, 2) + 1;
    for i = 1:num_layers-1
        if i == 1
            ret{1} = training_batch';
        else
            ret{i} = logistic(model{i-1}' * ret{i-1});
        end
    end
    net_input = model{num_layers-1}' * ret{num_layers-1};
    output_normalizer = log_sum_exp_over_rows(net_input);

    log_output_prob = net_input - repmat(output_normalizer, [size(net_input, 1), 1]); % log of probability of each class. size: <number of classes, i.e. 10> by <number of data cases>
    output_prob = exp(log_output_prob); % probability of each class. Each column (i.e. each case) sums to 1. size: <number of classes, i.e. 10> by <number of data cases>
    ret{num_layers} = output_prob;
end

% This function implements the backpropagation procedure for linear output neurons with l2loss
function gradient = linear_bprop(model, training_batch, activities, weight_decay)
% ret is a long gradient vector of size [1 x num_dim * num_hid_1 * ... * num_hid_n * num_output]
    num_layers = size(model, 2) + 1;
    mini_batch_size = size(training_batch.input, 1);

    error_derivatives = activities{num_layers} - training_batch.target';
    for i = num_layers-1:-1:1
        d_loss_by_d_model{i} = activities{i} * error_derivatives' ./ mini_batch_size;
        error_derivatives = model{i} * error_derivatives;
    end
    gradient = model_to_theta(d_loss_by_d_model) + weight_decay .* model_to_theta(model);
end

% This function implements the backpropagation procedure for logistic output neurons
function gradient = sigmoid_bprop(model, training_batch, activities, weight_decay)
% ret is a long gradient vector of size [1 x num_dim * num_hid_1 * ... * num_hid_n * num_output]
    num_layers = size(model, 2) + 1;
    mini_batch_size = size(training_batch.input, 1);

    error_derivatives = activities{num_layers} - training_batch.target';
    for i = num_layers-1:-1:1
        d_loss_by_d_model{i} = activities{i} * error_derivatives' ./ mini_batch_size;
        error_derivatives = model{i} * error_derivatives .* activities{i} .* (1 - activities{i});
    end
    gradient = model_to_theta(d_loss_by_d_model) + weight_decay .* model_to_theta(model);
end

% This function implements the backpropagation procedure for softmax output neurons
function gradient = softmax_bprop(model, training_batch, activities, weight_decay)
% ret is a long gradient vector of size [1 x num_dim * num_hid_1 * ... * num_hid_n * num_output]
    num_layers = size(model, 2) + 1;
    mini_batch_size = size(training_batch.input, 1);

    error_derivatives = activities{num_layers} - training_batch.target';
    for i = num_layers-1:-1:1
        d_loss_by_d_model{i} =  activities{i} * error_derivatives' ./ mini_batch_size;
        error_derivatives = model{i} * error_derivatives .* activities{i} .* (1 - activities{i});
    end
    gradient = model_to_theta(d_loss_by_d_model) + weight_decay .* model_to_theta(model);
end

% This function computes the loss of the current model on the given data
function ret = loss(unit_type, model, training_batch, weight_decay)
    theta = model_to_theta(model);
    mini_batch_size = size(training_batch.input, 1);
    num_layers = size(model, 2) + 1;
    switch unit_type
        case 'linear'
            for i = 1:num_layers
                if i == 1
                    activities{1} = training_batch.input';
                else
                    activities{i} = model{i-1}' * activities{i-1};
                end
            end    
            regression_loss = 0.5 / mini_batch_size * sum(sum((training_batch.target' - activities{num_layers}) .^ 2));     
            weight_decay_loss = sum(model_to_theta(model) .^ 2) / 2 * weight_decay;
            ret = regression_loss + weight_decay_loss;
        case 'sigmoid'
            for i = 1:num_layers
                if i == 1
                    activities{1} = training_batch.input';
                else
                    activities{i} = logistic(model{i-1}' * activities{i-1});
                end
            end
            cross_entropy_loss = -1 * training_batch.target' .* log(activities{num_layers}) - (1 - training_batch.target') .* log(1 - activities{num_layers});
            classification_loss = mean(sum(cross_entropy_loss, 1));
            weight_decay_loss = sum(model_to_theta(model) .^ 2) / 2 * weight_decay;
            ret = classification_loss + weight_decay_loss;
        case 'softmax'
            for i = 1:num_layers-1
                if i == 1
                    activities{1} = training_batch.input';
                else
                    activities{i} = logistic(model{i-1}' * activities{i-1});
                end
            end
            net_input = model{num_layers-1}' * activities{num_layers-1};
            output_normalizer = log_sum_exp_over_rows(net_input);

            log_output_prob = net_input - repmat(output_normalizer, [size(net_input, 1), 1]);
            output_prob = exp(log_output_prob); 

            classification_loss = -mean(sum(log_output_prob .* training_batch.target', 1));
            weight_decay_loss = sum(model_to_theta(model) .^ 2) / 2 * weight_decay; 
            ret = classification_loss + weight_decay_loss;
        otherwise
            assert(false, 'unit type not supported');
    end
end

% This function implements the finite difference gradient check procedure
function test_gradient(model, architecture, data, loss_type, weight_decay)
    base_theta = model_to_theta(model);
    h = 1e-2;
    correctness_threshold = 1e-5;
    switch loss_type
        case 'linear'
            activities = linear_fprop(model, data.input);
            analytic_gradient = linear_bprop(model, data, activities, weight_decay);
        case 'sigmoid'
            activities = sigmoid_fprop(model, data.input);
            analytic_gradient = sigmoid_bprop(model, data, activities, weight_decay);
        case 'softmax'
            activities = softmax_fprop(model, data.input);
            analytic_gradient = softmax_bprop(model, data, activities, weight_decay);
        otherwise
            error('loss type is not supported!');
    end

    % Test the gradient not for every element of theta, because that's a lot of work. Test for only a few elements.
    for i = 1:100
    test_index = mod(i * 1299721, size(base_theta, 2)) + 1; % 1299721 is prime and thus ensures a somewhat random-like selection of indices
    analytic_here = analytic_gradient(test_index);
    theta_step = base_theta * 0;
    theta_step(test_index) = h;
    % The following two lines of code seem strange at first sight but if you sum the numerators up using first order taylor expansion, you will see that it's just 1
    contribution_distances = [-4:-1, 1:4];
    contribution_weights = [1/280, -4/105, 1/5, -4/5, 4/5, -1/5, 4/105, -1/280];
    temp = 0;
    for contribution_index = 1:8,
    temp = temp + loss(loss_type, theta_to_model(base_theta + theta_step * contribution_distances(contribution_index), architecture), data, weight_decay) * contribution_weights(contribution_index);
    end

    fd_here = temp / h;
    diff = abs(analytic_here - fd_here);
    % fprintf('%d %e %e %e %e\n', test_index, base_theta(test_index), diff, fd_here, analytic_here);
    if diff < correctness_threshold, continue; end
    if diff / (abs(analytic_here) + abs(fd_here)) < correctness_threshold, continue; end
    error(sprintf('Theta element #%d, with value %e, has finite difference gradient %e but analytic gradient %e. That looks like an error.\n', test_index, base_theta(test_index), fd_here, analytic_here));
    end
    fprintf('Gradient test passed. That means that the gradient that your code computed is within 0.001%% of the gradient that the finite difference approximation computed, so the gradient calculation procedure is probably correct (not certainly, but probably).\n');
    end

function ret = logistic(input)
    ret = 1 ./ (1 + exp(-input));
end

% This functions computes the log partition fucntion in a numerically stable way
function ret = log_sum_exp_over_rows(net_input)
    maxs_small = max(net_input, [], 1);
    maxs_big = repmat(maxs_small, [size(net_input, 1), 1]);
    ret = log(sum(exp(net_input - maxs_big), 1)) + maxs_small;
end