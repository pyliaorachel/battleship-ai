setwd('~/Downloads/battleship/data_visualization')

# model 1
basic_model1 = read.csv('../results/basic_test_model1.csv')
b_model1_BT = subset(basic_model1, `propagation.type` == 'BT')
b_model1_FC = subset(basic_model1, `propagation.type` == 'FC')
b_model1_GAC = subset(basic_model1, `propagation.type` == 'GAC')

b_model1_BT_aggr = aggregate(b_model1_BT[, 7:9], list(b_model1_BT$`board.size`), mean)
b_model1_FC_aggr = aggregate(b_model1_FC[, 7:9], list(b_model1_FC$`board.size`), mean)
b_model1_GAC_aggr = aggregate(b_model1_GAC[, 7:9], list(b_model1_GAC$`board.size`), mean)

b_model1_GAC_val_dec = subset(b_model1_GAC, `value.ordering.type` == 'val_decreasing_order')
b_model1_GAC_val_dec_aggr = aggregate(b_model1_GAC_val_dec[, 7:9], list(b_model1_GAC_val_dec$`board.size`), mean)
b_model1_GAC_val_inc = subset(b_model1_GAC, `value.ordering.type` == 'val_increasing_order')
b_model1_GAC_val_inc_aggr = aggregate(b_model1_GAC_val_inc[, 7:9], list(b_model1_GAC_val_inc$`board.size`), mean)
b_model1_GAC_val_dec_lcv = subset(b_model1_GAC, `value.ordering.type` == 'val_decrease_lcv')
b_model1_GAC_val_dec_lcv_aggr = aggregate(b_model1_GAC_val_dec_lcv[, 7:9], list(b_model1_GAC_val_dec_lcv$`board.size`), mean)

# model 2
basic_model2 = read.csv('../results/basic_test_model2.csv')
b_model2_BT = subset(basic_model2, `propagation.type` == 'BT')
b_model2_FC = subset(basic_model2, `propagation.type` == 'FC')
b_model2_GAC = subset(basic_model2, `propagation.type` == 'GAC')

b_model2_BT_aggr = aggregate(b_model2_BT[, 7:9], list(b_model2_BT$`board.size`), mean)
b_model2_FC_aggr = aggregate(b_model2_FC[, 7:9], list(b_model2_FC$`board.size`), mean)
b_model2_GAC_aggr = aggregate(b_model2_GAC[, 7:9], list(b_model2_GAC$`board.size`), mean)

# model 3
basic_model3 = read.csv('../results/basic_test_model3.csv')
b_model3_BT = subset(basic_model3, `propagation.type` == 'BT')
b_model3_FC = subset(basic_model3, `propagation.type` == 'FC')
b_model3_GAC = subset(basic_model3, `propagation.type` == 'GAC')

b_model3_BT_aggr = aggregate(b_model3_BT[, 7:9], list(b_model3_BT$`board.size`), mean)
b_model3_FC_aggr = aggregate(b_model3_FC[, 7:9], list(b_model3_FC$`board.size`), mean)
b_model3_GAC_aggr = aggregate(b_model3_GAC[, 7:9], list(b_model3_GAC$`board.size`), mean)

# data - board size x runtime, for 3 models, for 3 propagation types
data = cbind(b_model1_BT_aggr[1:2], 
             b_model2_BT_aggr[2], 
             b_model3_BT_aggr[2],
             b_model1_FC_aggr[2],
             b_model2_FC_aggr[2],
             b_model3_FC_aggr[2],
             b_model1_GAC_aggr[2],
             b_model2_GAC_aggr[2],
             b_model3_GAC_aggr[2])
colnames(data) = c('board.size', 
                   'bt.runtime1', 
                   'bt.runtime2', 
                   'bt.runtime3', 
                   'fc.runtime1', 
                   'fc.runtime2', 
                   'fc.runtime3', 
                   'gac.runtime1', 
                   'gac.runtime2', 
                   'gac.runtime3')

write.csv(data, file='../results/small_propagator_model.csv')

# data - board size x runtime/assignment/pruning, for 3 orderings, for 3 propagation types
colnames(b_model1_GAC_val_dec_aggr) = c('board.size', 
                                        'runtime_dec',
                                        'assignment_dec',
                                        'pruning_dec')
colnames(b_model1_GAC_val_inc_aggr) = c('board.size', 
                                        'runtime_inc',
                                        'assignment_inc',
                                        'pruning_inc')
colnames(b_model1_GAC_val_dec_lcv_aggr) = c('board.size', 
                                        'runtime_dec_lcv',
                                        'assignment_dec_lcv',
                                        'pruning_dec_lcv')
data = merge(b_model1_GAC_val_dec_aggr, b_model1_GAC_val_inc_aggr, by='board.size')
data = merge(data, b_model1_GAC_val_dec_lcv_aggr, by='board.size')

write.csv(data, file='../results/small_val_ord.csv')
