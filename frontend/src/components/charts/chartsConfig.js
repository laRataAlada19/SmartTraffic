export default [
  {
    name: 'Evolução Temporal do Tráfego',
    type: 'line',
    component: 'LineChart',
    description: 'Mostra a variação do total de veículos ao longo do tempo (por dia, semana ou mês), permitindo análises de tendência em diferentes localidades.'
  },
  { name: 'Distribuição de Veículos por Localização', type: 'bar', component: 'BarChart', description: 'Mostra a quantidade de veículos detectados em diferentes locais, permitindo comparar a intensidade do tráfego entre zonas.' },
  {
    name: 'Distribuição de Veículos por Tipo',
    type: 'pie',
    component: 'VehiclePieChart',
    description: 'Mostra a proporção de cada tipo de veículo (ligeiros, motociclos, bicicletas, camiões, autocarros) no total de tráfego registado, com possibilidade de filtragem por localidade e período.'
  },
  {
    name: 'Evolução de Tipos de Veículos',
    type: 'bar',
    component: 'TypeVei',
    description: 'Mostra como diferentes tipos de veículos variam ao longo do tempo, com possibilidade de filtrar por localização e intervalo temporal.'
  },
  
  { name: 'Fluxo de Tráfego por Direção', type: 'bar', component: 'Directions', description: 'Exibe o volume de tráfego dividido pelas direções cardinais (norte, sul, leste, oeste), com filtros por localidade e intervalo de tempo.' },
  {
    name: 'Heatmap de Tráfego por Hora e Tipo de Veículo',
    type: 'heatmap',
    component: 'Heatmap',
    description: 'Representa a densidade de tráfego ao longo do dia por tipo de veículo, utilizando cores para indicar a intensidade em cada hora.'
  },
  { name: 'Mapa Geográfico de Tráfego', type: 'choropleth', component: 'Geografic', description: 'Visualiza a intensidade de tráfego por distrito em Portugal, com escala de cores indicando os valores relativos.' },
  {
    name: 'Distribuição de Tráfego por Hora do Dia',
    type: 'bar',
    component: 'HourPic',
    description: 'Apresenta a quantidade total de veículos por hora, permitindo identificar os períodos de maior movimento (horas de pico).'
  },
  { name: 'Comparação de Tráfego entre Períodos', type: 'bar', component: 'ComparePeriods', description: 'Compara os volumes de diferentes tipos de veículos entre dois dias distintos para analisar variações de tráfego.' },
  {
    name: 'Taxa de Crescimento Diário do Tráfego',
    type: 'indicador',
    component: 'GrowthRate',
    description: 'Exibe a variação percentual no total de tráfego entre dois dias consecutivos, destacando aumentos ou quedas no fluxo de veículos.'
  },
  {
    name: 'Densidade de Tráfego por Minuto',
    type: 'line',
    component: 'TrafficDensity',
    description: 'Representa o fluxo de veículos ao longo dos minutos de um dia específico, útil para identificar picos de tráfego.'
  },  
  {
    name: 'Tendência Diária de Tráfego',
    type: 'line',
    component: 'Trend',
    description: 'Apresenta a variação do volume total de veículos ao longo dos dias, facilitando a análise de padrões de tráfego.'
  },  
  { name: 'Radar de Direções de Tráfego', type: 'radar', component: 'DirectionsRadar', description: 'Mostra a intensidade acumulada do tráfego em cada uma das 8 direções (N, NE, E, SE, S, SW, W, NW) em formato radar.' },
  {
    name: 'Mapa Horário de Tráfego',
    type: 'mapa-temporal',
    component: 'TimeMap',
    description: 'Visualiza a distribuição geográfica do tráfego num determinado horário, com marcadores interativos que mostram o volume total por ponto de medição.'
  },
  { bane: 'Mapa com evolução temporal', type: 'radar', component: 'TimeMap', description: 'Mapa que mostra a evolução dos dados ao longo do tempo.' },
  {
    name: 'Matriz Origem-Destino de Veículos',
    type: 'matrix',
    component: 'ODMatrix',
    description: 'Representa os fluxos de tráfego entre localidades, com a intensidade das ligações exibida por uma escala de cor, facilitando a identificação de trajetos mais frequentes.'
  },
]
