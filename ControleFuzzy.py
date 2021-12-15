import pygad
from skfuzzy import control as ct
import skfuzzy as fuzzy
import numpy as np
import numpy

#Configurando os inputs (antecedentes) do controle
vazao = ct.Antecedent(np.arange(0, 101, 1),'vazao') 
temp = ct.Antecedent(np.arange(16, 56, 1),'temp')
#Configurando o output (consequência) 
pot = ct.Consequent(np.arange(0, 101, 1),'pot')

#Distribui automaticamente os valores das funções de pertinência da vazão e potência na faixa de 0% a 100%
vazao.automf(names=['VLow','VMediumLow','VMediumHigh','VHigh'])
pot.automf(names=['PLow','PMediumLow','PMediumHigh','PHigh'])  

#Configura manualmente as funções de pertinência, tendo como centro 36 graus, com variação de 20 graus positivos e negativos
temp['TLow'] =fuzzy.trapmf(temp.universe, [0, 16,26,31 ])
temp['TMediumLow'] =fuzzy.trimf(temp.universe, [26, 34, 41])
temp['TMediumHigh'] =fuzzy.trimf(temp.universe, [31, 39, 46])
temp['THigh'] =fuzzy.trapmf(temp.universe, [41, 46, 56,56])

#Configuração das regras de inferência
r1=  ct.Rule(temp['TLow'] ,pot['PLow'])
r2 = ct.Rule((temp['TLow']   & (vazao['VMediumHigh']|vazao['VHigh']))|(temp['TMediumLow'] & ~vazao['VHigh'])|(temp['TMediumHigh'] &  vazao['VLow']),pot['PMediumLow'])
r3=  ct.Rule((temp['TMediumLow']  &  vazao['VHigh'])|(temp['TMediumHigh'] & ~vazao['VLow'])|(temp['THigh']  & (vazao['VLow'] |vazao['VMediumLow'])),pot['PMediumHigh'])
r4=  ct.Rule((temp['THigh']  &(vazao['VMediumHigh']|vazao['VHigh'])),pot['PHigh'])    
r=[r1,r2,r3,r4]
fP_ctrl = ct.ControlSystem(r) 
fP = ct.ControlSystemSimulation(fP_ctrl) 
#Configuração do teste a ser feito
fP.input['vazao'] = 80
fP.input['temp'] = 38
fP.compute()
#Visualização dos resultados
pot.view(sim=fP)
output=fP.output['pot']

