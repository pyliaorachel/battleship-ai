setwd('~/Downloads/battleship/data_visualization')

# basic
basic_model1 = read.csv('../results/basic_test_model1.csv')
b_model1_BT = subset(basic_model1, `propagation.type` == 'BT')
b_model1_FC = subset(basic_model1, `propagation.type` == 'FC')
b_model1_GAC = subset(basic_model1, `propagation.type` == 'GAC')

b_model1_BT_aggr = aggregate(b_model1_BT[, 7:9], list(b_model1_BT$`board.size`), mean)
b_model1_FC_aggr = aggregate(b_model1_FC[, 7:9], list(b_model1_FC$`board.size`), mean)
b_model1_GAC_aggr = aggregate(b_model1_GAC[, 7:9], list(b_model1_GAC$`board.size`), mean)

# advanced 5x5 10x10
adv_model1 = read.csv('../results/advanced_test_model1_BT_FT_GAC.csv')
a_model1_BT = subset(adv_model1, `propagation.type` == 'BT')
a_model1_FC = subset(adv_model1, `propagation.type` == 'FC')

a_model1_BT_aggr = aggregate(a_model1_BT[, 7:9], list(a_model1_BT$`board.size`), mean)
a_model1_FC_aggr = aggregate(a_model1_FC[, 7:9], list(a_model1_FC$`board.size`), mean)

# advanced 5x5 ~ 10x10
adv_gac_model1 = read.csv('../results/advanced_test_model1_GAC_only.csv')
a_model1_GAC = subset(adv_gac_model1, `propagation.type` == 'GAC')

a_model1_GAC_aggr = aggregate(a_model1_GAC[, 7:9], list(a_model1_GAC$`board.size`), mean)
colnames(a_model1_GAC_aggr) = c('board.size',
                                'gac.runtime1',
                                'gac.assignment1',
                                'gac.pruning1')

# data - board size x runtime, for model 1, for 3 propagation types
basic = cbind(b_model1_BT_aggr, 
              b_model1_FC_aggr[2:4])
colnames(basic) = c('board.size',
                    'bt.runtime1',
                    'bt.assignment1',
                    'bt.pruning1',
                    'fc.runtime1',
                    'fc.assignment1',
                    'fc.pruning1')
advanced = cbind(a_model1_BT_aggr, 
                 a_model1_FC_aggr[2:4])
colnames(advanced) = c('board.size',
                       'bt.runtime1',
                       'bt.assignment1',
                       'bt.pruning1',
                       'fc.runtime1',
                       'fc.assignment1',
                       'fc.pruning1')
bt_fc = rbind(basic, advanced)

data = merge(bt_fc, a_model1_GAC_aggr, by='board.size', all.y=TRUE)

write.csv(data, file='../results/large_propagator_runtime_assignment_pruning.csv')

# data - board size x runtime/assignment/pruning, for 3 models, for 3 propagation types
basic = cbind(b_model1_BT_aggr[1:2], 
              b_model1_FC_aggr[2])
colnames(basic) = c('board.size',
                    'bt.runtime1',
                    'fc.runtime1')
advanced = cbind(a_model1_BT_aggr[1:2], 
                 a_model1_FC_aggr[2])
colnames(advanced) = c('board.size',
                       'bt.runtime1',
                       'fc.runtime1')
bt_fc = rbind(basic, advanced)

data = merge(bt_fc, a_model1_GAC_aggr[1:2], by='board.size', all.y=TRUE)

write.csv(data, file='../results/large_propagator_runtime.csv')



