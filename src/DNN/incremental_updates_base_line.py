'''
Created on Mar 15, 2019

'''
import torch

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/data_IO')
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/Interpolation')


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from data_IO.Load_data import *
# from sensitivity_analysis.logistic_regression.Logistic_regression import test_X
    from utils import *
#     from sensitivity_analysis.linear_regression.evaluating_test_samples import *
    from DNN import *

except ImportError:
    from Load_data import *
# from sensitivity_analysis.logistic_regression.Logistic_regression import test_X
    from utils import *
#     from evaluating_test_samples import *
    from DNN import *






if __name__ == '__main__':
    
    
    configs = load_config_data(config_file)
    
    git_ignore_folder = configs['git_ignore_folder']
    
    sys_args = sys.argv

    origin_model = torch.load(git_ignore_folder + 'model_without_noise')
        
    alpha = torch.load(git_ignore_folder + 'alpha')
    
    beta = torch.load(git_ignore_folder + 'beta')
    
    
    init_para_list = list(torch.load(git_ignore_folder + 'init_para'))
    
    random_ids_multi_super_iterations = torch.load(git_ignore_folder + 'random_ids_multi_super_iterations')
    
    learning_rate_all_epochs = torch.load(git_ignore_folder + 'learning_rate_all_epochs')
    
    
#     delta_gradient_all_epochs = torch.load(git_ignore_folder + 'delta_gradient_all_epochs')
    
#     beta = torch.load(git_ignore_folder + 'beta')
    
#     hessian_matrix = torch.load(git_ignore_folder + 'hessian_matrix')
    
#     gradient_list = torch.load(git_ignore_folder + 'gradient_list')
    
    max_epoch = torch.load(git_ignore_folder+'epoch')
    
    print("max_epoch::", max_epoch)
    
    X = torch.load(git_ignore_folder+'noise_X')
    
    Y = torch.load(git_ignore_folder+'noise_Y')
    
    
    delta_data_ids = torch.load(git_ignore_folder + 'noise_data_ids')
    dim = X.shape

#     delta_size = int(dim[0]*0.1)
#     
#     print("delta_size::", delta_size)

    print("delta_size::", delta_data_ids.shape[0])
    
    
#     delta_data_ids = random_generate_subset_ids(dim, delta_size)
    
    update_X, update_Y, selected_rows = get_subset_training_data(X, Y, dim, delta_data_ids)

    torch.save(delta_data_ids, git_ignore_folder + 'delta_data_ids')
    
    
    
#     update_X, update_Y, selected_rows = get_subset_training_data(X, Y, X.shape, delta_data_ids)
    
    test_X = torch.load(git_ignore_folder + 'test_X')
    
    test_Y = torch.load(git_ignore_folder + 'test_Y')
    
    hidden_dim = torch.load(git_ignore_folder + 'hidden_dims')
    
#     delta_gradient_all_epochs = torch.load(git_ignore_folder + 'delta_gradient_all_epochs')
    
#     delta_all_epochs = torch.load(git_ignore_folder + 'delta_all_epochs')
    
#     old_para_list_all_epochs = torch.load(git_ignore_folder + "old_para_list")
    
    
    
    input_dim = X.shape[1]
    
    num_class = torch.unique(Y).shape[0]
    
    output_dim = num_class
    
    model = DNNModel(input_dim, hidden_dim, output_dim)
    
    init_model(model,init_para_list)
    
#     init_model(model, list(origin_model.parameters()))

#     hessian_para_list = torch.load(git_ignore_folder + 'hessian_para_list')
    
#     init_model(model, hessian_para_list)
    
    error = nn.CrossEntropyLoss()
# 
# 
#     learning_rate = 0.1
#     optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    
    print("learning rate::", alpha)
    
    print("max_epoch::", max_epoch)
    
    batch_size = torch.load(git_ignore_folder + 'batch_size')
    
    
    
#     model, gradient_list, res_list, count = model_training(max_epoch, update_X, update_Y, test_X, test_Y, alpha, error, model)
    
    
    
#     max_epoch = 150
    
#     model, count = model_update_standard_lib_stochastic(batch_size, max_epoch, update_X, update_Y, alpha, error, model)
    t1 = time.time()
    model, count, para_list_all_epochs, gradient_list_all_epochs = model_update_standard_lib(max_epoch, X, Y, error, model, beta, random_ids_multi_super_iterations, selected_rows, batch_size, learning_rate_all_epochs)

    t2 = time.time()
    
    print('time_baseline::', t2 - t1)
    cut_off_epoch = max_epoch

    

#     model, gradient_list_all_epochs, output_list_all_epochs, para_list_all_epochs, epoch = model_training(max_epoch, update_X, update_Y, test_X, test_Y, alpha, beta, error, model, True, batch_size, dim)

#     compute_model_parameter_iteration(max_epoch, model, update_X, update_Y, alpha, error, update_X.shape, num_class, input_dim, hidden_dim, output_dim, old_para_list_all_epochs, delta_gradient_all_epochs, delta_all_epochs)
    
#     print_model_para(model)
    
    
    compute_model_para_diff(list(origin_model.parameters()), list(model.parameters()))
    
    
    torch.save(model, git_ignore_folder + 'model_base_line')    
    
#     compute_derivative_one_more_step(model, error, X, Y)
     
#     origin_gradient_list = torch.load(git_ignore_folder + 'gradient_list')
    
    
#     loss = torch.load(git_ignore_folder + 'loss')
    
    
    torch.save(gradient_list_all_epochs, git_ignore_folder + 'expected_gradient_list_all_epochs')
      
    torch.save(para_list_all_epochs, git_ignore_folder + 'expected_para_list_all_epochs')
    
#     torch.save(max_epoch, git_ignore_folder + 'update_max_epochs')
    
    
#     torch.save(batch_size, git_ignore_folder + 'batch_size')
    
#     batch_num = update_X.shape[0]/batch_size
    
#     torch.save(batch_num, git_ignore_folder + 'batch_num')
    
    compute_test_acc(model, test_X, test_Y)
    
#     compute_derivative_one_more_step(model, error, X, Y)
#     
#     gradient_list2, para_list2 = compute_gradient_iteration(model, input_dim, hidden_dim, output_dim, X, Y)
#     
#     
#     
#     hessian_para_list = torch.load(git_ignore_folder + 'hessian_para_list')
#     
#     hessian_gradient_list = torch.load(git_ignore_folder + 'hessian_gradient_list')
#     
#     
#     
#     updated_gradient = torch.mm(get_all_vectorized_parameters(para_list2) - get_all_vectorized_parameters(hessian_para_list), hessian_matrix) + get_all_vectorized_parameters(hessian_gradient_list)
#     
#     print(torch.norm((updated_gradient - get_all_vectorized_parameters(gradient_list2))/X.shape[0]))
    
    
    
    
    
#     num_of_output = Y.shape[1]
#     
#     dim = X.shape
#     
#     print(X.shape)
#     
#     Y = Y.type(torch.DoubleTensor)
#     
#     sys_args = sys.argv
# 
#     
#     delta_num = int(10000)
# 
#     
#      
# #     delta_data_ids = random_generate_subset_ids(X.shape, delta_num)     
# #     torch.save(delta_data_ids, git_ignore_folder+'delta_data_ids')
# 
#     delta_data_ids = torch.load(git_ignore_folder + 'noise_data_ids')
#     
#     print(delta_data_ids.shape[0])
#     
#     max_epoch = torch.load(git_ignore_folder+'epoch')
#     
#     print(max_epoch)
# #     num_class = torch.unique(Y).shape[0]
#     
# #     delta_data_ids = torch.load(git_ignore_folder+'delta_data_ids')
#     
#     update_X, selected_rows = get_subset_training_data(X, X.shape, delta_data_ids)
#     
#     print(selected_rows.shape)
#     
#     update_Y, s_rows = get_subset_training_data(Y, Y.shape, delta_data_ids)
#     
#     #     res1 = update_model_parameters_from_the_scratch(update_X, update_Y)
#     
#     t1 = time.time()
#     
#     lr = initialize(update_X.shape, num_of_output)
# #     update_x_sum_by_class = compute_x_sum_by_class(update_X, update_Y, num_class, update_X.shape)
#     #     update_X_Y_mult = update_X.mul(update_Y)
#     #     res1 = update_model_parameters_from_the_scratch(update_X, update_Y)dim, theta,  X, Y, X_sum_by_class, num_class
#     res2 = linear_regression_standard_library(update_X, update_Y, lr, update_X.shape, max_epoch, alpha, beta)
# 
#     
#     t2 = time.time()
#     
#     
#     torch.save(res2, git_ignore_folder+'model_standard_lib')
#     
#     
#     test_X = torch.load(git_ignore_folder + 'test_X')
#     
#     test_Y = torch.load(git_ignore_folder + 'test_Y')
#     
#     print('training_accuracy::', compute_accuracy2(update_X, update_Y, res2))
#     
#     print('test_accuracy::', compute_accuracy2(test_X, test_Y, res2))
#     
#     print('training_time_standard_lib::', t2 - t1)
#     
#     print(res2)
    
    
    
    
    
    