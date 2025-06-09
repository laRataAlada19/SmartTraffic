export default [
    { name: 'Gráfico de Linhas', type: 'line', component: 'LineChart' , description: 'Gráfico de linhas para mostrar tendências ao longo do tempo.' },
    { name: 'Gráfico de Barras', type: 'bar', component: 'BarChart' , description: 'Gráfico de barras para comparar categorias.' },
    { name: 'Gráfico de Pizza', type: 'pie', component: 'PieChart' , description: 'Gráfico de pizza para mostrar proporções.' },
    { name: 'Gráfico tipos de veiculos' , type: 'bar', component: 'TypeVei' , description: 'Gráfico de barras para mostrar a distribuição dos tipos de veículos.' },
    { name: 'Gráfico direção de veiculos' , type: 'bar', component: 'Direction' , description: 'Gráfico de barras para mostrar a direção dos veículos.' },
    { name: 'Grafico heatmap', type: 'heatmap', component: 'HeatMap' , description: 'Gráfico de calor para mostrar a densidade de dados em uma área.' },
    { name: 'Grafico mapa', type: 'choropleth', component: 'Geografic' , description: 'Gráfico geográfico para mostrar dados em um mapa.' },
    { bane: 'Grafico pico de horas', type: 'bar', component: 'HourPic' , description: 'Gráfico de barras para mostrar os picos de tráfego por hora.' },
    { bane: 'Grafico comparar peridos', type: 'bar', component: 'ComparePeriods' , description: 'Gráfico de barras para comparar diferentes períodos.' },
    { bane: 'Grafico crescimento', type: 'bar', component: 'GrowthRate' , description: 'Gráfico de barras para mostrar a taxa de crescimento ao longo do tempo.' },
    { bane: 'Grafico densidade trafego', type: 'line', component: 'TrafficDensity' , description: 'Gráfico de linhas para mostrar a densidade de tráfego.' },
    { bane: 'Grafico tendencia diara', type: 'line', component: 'Trend' , description: 'Gráfico de linhas para mostrar tendências diárias.' },
    { bane: 'Grafico direçao radar', type: 'radar', component: 'DirectionRadar' , description: 'Gráfico radar para mostrar a direção dos veículos em diferentes categorias.' },
    { bane: 'Grafico picos', type: 'line', component: 'Anomalies' , description: 'Gráfico de linhas para identificar picos e anomalias nos dados.' },
    { bane: 'Mapa com evolução temporal', type: 'radar', component: 'TimeMap' , description: 'Mapa que mostra a evolução dos dados ao longo do tempo.' },
    { bane: 'Matriz de Origem-Destino', type: 'line', component: 'ODMatrix' , description: 'Matriz que mostra a origem e destino dos veículos.' },
  ]
  