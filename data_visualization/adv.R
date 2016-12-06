library(plotly)

setwd('~/Downloads/battleship/data_visualization')

# board size x runtime, for model 1, for 3 propagators (propagators scaling with board size)

plot = read.csv('../results/large_board_runtime_model.csv')
plot = na.omit(plot)

p = plot_ly(plot, x = ~board.size, y = ~bt.runtime1, name = 'model1 BT', type = 'scatter', mode = 'lines', line = list(color = '#3F51B5', width = 2))%>%
  add_trace(y = ~fc.runtime1, name = 'model1 FC', line = list(color = '#2196F3', width = 2)) %>%
  add_trace(y = ~gac.runtime1, name = 'model1 GAC', line = list(color = '#B3E5FC', width = 2)) %>%
  layout(title = "Propagators Scaling with Board Size",
         xaxis = list(title = "Board Size"),
         yaxis = list (title = "Runtime (sec)", type = "log"))

# board size x runtime, for model 1, for decreasing order, for 3 propagators (assignments/prunings with board size)

p = plot_ly(plot, x = ~board.size, y = ~bt.assignment1, name = 'model1 BT assignments', type = 'scatter', mode = 'lines', line = list(color = '#B71C1C', width = 2))%>%
  add_trace(y = ~fc.assignment1, name = 'model1 FC assignments', line = list(color = 'rgb(0,255,0)', width = 2)) %>%
  add_trace(y = ~fc.pruning1, name = 'model1 FC prunings', line = list(color = '#1B5E20', width = 2)) %>%
  add_trace(y = ~gac.assignment1, name = 'model1 GAC assignments', line = list(color = '#2196F3', width = 2)) %>%
  add_trace(y = ~gac.pruning1, name = 'model1 GAC prunings', line = list(color = '#1A237E', width = 2)) %>%
  layout(title = "Assignments/Prunings Scaling with Board Size",
         xaxis = list(title = "Board Size"),
         yaxis = list (title = "Assignments/Prunings", type = "log"))
