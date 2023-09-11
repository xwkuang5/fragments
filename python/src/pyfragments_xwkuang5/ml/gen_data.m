function data = gen_data(problem, num_dim, num_output, num_case)
    switch problem
        case 'XOR'
            switch num_output
                case 1
                    data.training_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.training_target = [1; 0; 0; 1];
                    data.validation_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.validation_target = [1; 0; 0; 1];
                    data.test_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.test_target = [1; 0; 0; 1];
                case 2
                    data.training_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.training_target = [[1, 0]; [0, 1]; [0, 1]; [1, 0]];
                    data.validation_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.validation_target = [[1, 0]; [0, 1]; [0, 1]; [1, 0]];
                    data.test_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.test_target = [[1, 0]; [0, 1]; [0, 1]; [1, 0]];
                otherwise
                    error('Either one or two output is possible for XOR');
            end
        case 'AND'
            switch num_output
                case 1
                    data.training_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.training_target = [0; 0; 0; 1];
                    data.validation_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.validation_target = [0; 0; 0; 1];
                    data.test_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.test_target = [0; 0; 0; 1];
                case 2
                    data.training_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.training_target = [[0, 1]; [0, 1]; [0, 1]; [1, 0]];
                    data.validation_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.validation_target = [[0, 1]; [0, 1]; [0, 1]; [1, 0]];
                    data.test_input = [[0,0]; [0, 1]; [1, 0]; [1, 1]];
                    data.test_target = [[0, 1]; [0, 1]; [0, 1]; [1, 0]];
                otherwise
                    error('Either one or two output is possible for AND');
            end
        case 'parity'
            case_per_dataset = num_case / 3;
            data.training_input = gen_random_parity(case_per_dataset, num_dim);
            data.training_target = count_parity(data.training_input, num_output);
            data.validation_input = gen_random_parity(case_per_dataset, num_dim);
            data.validation_target = count_parity(data.training_input, num_output);
            data.test_input = gen_random_parity(case_per_dataset, num_dim);
            data.test_target = count_parity(data.training_input, num_output);
        otherwise
            error('Problem not supported!');
    end
end

function ret = gen_random_parity(num_case, num_dim)
    ret = [];
    for i = 1:num_case
        ret = [ret; random_parity(num_dim)];
    end
end

% How to let count_parity become a function on matrix directly
function ret = count_parity(input, num_output)
    parity = mod(sum(input), 2);
    if parity == 0
        if num_output == 1
            ret = [0];
        else
            ret = [0,1];
        end
    else
        if num_output == 1
            ret = [1];
        else
            ret = [1, 0];
        end
    end
end

function ret = random_parity(num_dim)
    ret = binary_threshold(randn(1, num_dim), 0.0);
end

function ret = binary_threshold(input, thres)
    if input >= thres
        ret = 1;
    else
        ret = 0;
    end
end
