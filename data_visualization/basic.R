library(plotly)

setwd('~/Downloads/battleship/data_visualization')

# board size x runtime, for 3 models (models with board size)
plot = read.csv('../results/small_propagator_model.csv')
p = plot_ly(plot, x = ~board.size, y = ~bt.runtime1, name = 'model1 BT', type = 'scatter', mode = 'lines', line = list(color = 'rgb(255,0,0)', width = 2))%>%
    add_trace(y = ~bt.runtime2, name = 'model2 BT', line = list(color = 'rgb(0,255,0)', width = 2)) %>%
    add_trace(y = ~bt.runtime3, name = 'model3 BT', line = list(color = 'rgb(0,0,255)', width = 2)) %>%
    add_trace(y = ~fc.runtime1, name = 'model1 FC', line = list(color = 'rgba(255,0,0,0.6)', width = 2)) %>%
    add_trace(y = ~fc.runtime2, name = 'model2 FC', line = list(color = 'rgba(0,255,0,0.6)', width = 2)) %>%
    add_trace(y = ~fc.runtime3, name = 'model3 FC', line = list(color = 'rgba(0,0,255,0.6)', width = 2)) %>%
    add_trace(y = ~gac.runtime1, name = 'model1 GAC', line = list(color = 'rgba(255,0,0,0.2)', width = 2)) %>%
    add_trace(y = ~gac.runtime2, name = 'model2 GAC', line = list(color = 'rgba(0,255,0,0.2)', width = 2)) %>%
    add_trace(y = ~gac.runtime3, name = 'model3 GAC', line = list(color = 'rgba(0,0,255,0.2)', width = 2)) %>%
    layout(title = "Models Scaling with Board Size",
        xaxis = list(title = "Board Size"),
        yaxis = list (title = "Runtime (sec)", type = "log"))

# board size x runtime, for GAC, for 3 value orderings
plot = read.csv('../results/basic_board_runtime_val_ord.csv')
p = plot_ly(plot, x = ~board.size, y = ~runtime_dec, name = 'GAC val_decreasing', type = 'scatter', mode = 'lines', line = list(color = 'rgb(255,0,0)', width = 2))%>%
  add_trace(y = ~runtime_inc, name = 'GAC val_increasing', line = list(color = 'rgb(0,255,0)', width = 2)) %>%
  add_trace(y = ~runtime_dec_lcv, name = 'GAC val_decreasing_lcv', line = list(color = 'rgb(0,0,255)', width = 2)) %>%
  layout(title = "Models Scaling with Board Size",
         xaxis = list(title = "Board Size"),
         yaxis = list (title = "Runtime (sec)"))
