
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

# see https://plotly.com/python/px-arguments/ for more options

##Lendo arquivo e estruturando data frame
df = pd.read_csv("dataset.csv")

df.loc[ df['Mês'] == 'Jan', 'Mês'] = 1
df.loc[ df['Mês'] == 'Fev', 'Mês'] = 2
df.loc[ df['Mês'] == 'Mar', 'Mês'] = 3
df.loc[ df['Mês'] == 'Abr', 'Mês'] = 4
df.loc[ df['Mês'] == 'Mai', 'Mês'] = 5
df.loc[ df['Mês'] == 'Jun', 'Mês'] = 6
df.loc[ df['Mês'] == 'Jul', 'Mês'] = 7
df.loc[ df['Mês'] == 'Ago', 'Mês'] = 8
df.loc[ df['Mês'] == 'Set', 'Mês'] = 9
df.loc[ df['Mês'] == 'Out', 'Mês'] = 10
df.loc[ df['Mês'] == 'Nov', 'Mês'] = 11
df.loc[ df['Mês'] == 'Dez', 'Mês'] = 12

df['Chamadas Realizadas'] = df['Chamadas Realizadas'].astype(int) #alterar tipo coluna chamada para numero
df['Dia'] = df['Dia'].astype(int)#alterar tipo coluna dia para numero
df['Mês'] = df['Mês'].astype(int)#alterar tipo coluna mes para numero

df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')#lstrip pega prefixo e retira
df['Valor Pago'] = df['Valor Pago'].astype(int)# altera para numero também

#altera uma categoria para binario, a fim de transformar coluna para numerico
df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0
#altera coluna para tipo numerico
df['Status de Pagamento'] = df['Status de Pagamento'].astype(int)


## criando os gráficos estático (Antes do mecanismo callback/dropdown)

#Chamadas médias por dia do mês


##Indicadores

#função para formar valores da ordem de milhares
def abrevMilhar (numero):
    n=str(int(numero))
    x=len(n)//3
    if x==1:
        forma=round(numero/1000**x,3)
        forma=str(forma)+'k'
    if x==2:
        forma=round(numero/1000**x,3)
        forma=str(forma)+'Mi'
    if x==3:
        forma=round(numero/1000**x,3)
        forma=str(forma)+'Bi'
    if x==4:
        forma=round(numero/1000**x,3)
        forma=str(forma)+'Tri'
    return forma
#Indicator Melhor consultor
df7 = df.groupby(['Consultor', 'Equipe'])['Valor Pago'].sum()
df7.sort_values(ascending=False, inplace=True)
df7 = df7.reset_index()

#Indicator - Melhor equipe
df8 = df.groupby('Equipe')['Valor Pago'].sum()
df8.sort_values(ascending=False, inplace=True)
df8 = df8.reset_index()

#indicator - total investido

#indicator - chamadas realizadas

#chamadas por mes do ano

# valor gasto meios de propaganda por mes

#valor total gasto por meio de propaganda

#consultor por valor pago

# status de pagamentoPropagandaEquipe


##listas para dropdown
Equipe=df['Equipe'].unique().tolist()
Propaganda=df['Meio de Propaganda'].unique().tolist()
Consultor=df['Consultor'].unique().tolist()


###Estrutura da pagina 

##styles CSS.
# Style graficos
colorx=['#ea4335','#4285f4','#fbbc05','#34a853','#00af97','#9e0000']
template=None
template2='plotly_white'
plotbgc=None
paperbgc='white'
axis=None
Fundocor='#e3e0f3'
cortitulo='#474a51'
cortitulofundo='rgba(255,255,255,0.7)'
margingraph=dict(l=25, r=25, t=50, b=40)
#Style Plano de fundo da pagina
stylepagina={"background":Fundocor}
#Style Cabeçario
styledivtitulo={'width': '1420px','height':'60px','display':'inline-block',
                 'margin':'0px 0px 25px 20px','padding': '0px',"background":cortitulofundo,
                 'border-radius':'0px 15px 15px 15px'}
styletitulo={'textAlign': 'center','fontFamily': 'Roboto',
             'margin': '0px 0px 15px 0px', 'color':cortitulo}
#Style Dropdown
styledropdiv={'width': '1420px','height':'90px',"background":paperbgc,
             'margin':'20px 20px 0px', 'padding': '0px',
             'border-radius':'15px 15px 15px 15px'}
styledrop={'width': '250px','display':'inline-block',
            'margin': '10px 0px 0px'}
styledroplabel={'margin': '20px 15px 0px 40px'}
#Style Paineis indicadores
styleindicator={'width': '300px','height':'200px','display':'inline-block','vertical-align':'top',
                'padding': '0px 0px 0px','border-radius':'0px 15px 0px 15px'}
styleindicator1={'margin':'0px 10px 0px 90px',"background":colorx[0],}
styleindicator1.update(styleindicator)
styleindicator2={'margin':'0px 10px 0px',"background":colorx[1],}
styleindicator2.update(styleindicator)
styleindicator3={'margin':'0px 10px 0px',"background":colorx[2],}
styleindicator3.update(styleindicator)
styleindicator4={'margin':'0px 10px 0px',"background":colorx[3],}
styleindicator4.update(styleindicator)
indicatorobj={'height':'170px',
              'margin':'15px 10px 15px','padding':'0px 0px 0px'}
indicatortext={'color':'#ffffff'}
#Style graph padrão
graphpadrao={'width': '700px','height':'350px','display':'inline-block',
             'margin':'0px','padding':'15px 0px 0px 20px','border-radius':'15px'}
#Style graph pie
graphpie={'width': '340px','height':'350px','display':'inline-block',
         'margin':'0px','padding':'15px 0px 0px 20px','border-radius':'15px'}
styleimg={}

app.layout = html.Div([ #children da div inclui os Hs e outros dcc
    html.Div([
        html.H1(children='Dashboard de Planejamento de Marketing',style = styletitulo),
        html.H2(style ={}),

     ], id ="cabeçariodiv",style = styledivtitulo),       

    html.Div([ html.H1(children=f"{df7['Consultor'].iloc[0]} - Top Consultant",id="titulo",style =indicatortext),
             html.H2(children="Entre todas as equipes",id="subtitulo",style =indicatortext),
             html.H3(children=f"R${abrevMilhar(df7['Valor Pago'].iloc[0])}",id="valor",style =indicatortext),
             html.Img(src='assets/indicador1.png', id='img', style=styleimg)
            ], className='indicator', style = styleindicator1),
    html.Div([ html.H1(children=f"{df8['Equipe'].iloc[0]} - Top Team",id="titulo",style =indicatortext),
             html.H2(children="Em vendas",id="subtitulo",style =indicatortext),
             html.H3(children=f"R${abrevMilhar(df8['Valor Pago'].iloc[0])}",id="valor",style =indicatortext),
             html.Img(src='assets/indicador2.png', id='img', style=styleimg)
            ], className='indicator', style = styleindicator2),
    html.Div([ html.H1(children="Valor total de Vendas",id="titulo",style =indicatortext),
             html.H2(children=" ",id="subtitulo",style =indicatortext),
             html.H3(children=f"R${abrevMilhar(df['Valor Pago'].sum())}",id="valor",style =indicatortext),
             html.Img(src='assets/indicador3.png', id='img', style=styleimg)
            ], className='indicator', style = styleindicator3),
    html.Div([ html.H1(children=f"Chamadas Realizadas",id="titulo",style =indicatortext),
             html.H2(children="",id="subtitulo",style =indicatortext),
             html.H3(children=f"{len(df[df['Status de Pagamento'] == 1])}",id="valor",style =indicatortext),
             html.Img(src='assets/indicador4.png', id='img', style=styleimg)
             ], className='indicator', style = styleindicator4),
    html.Div([
    html.Div([
        html.Label('Selecione equipe:',style=styledroplabel),
        dcc.Dropdown(options=Equipe, multi=True, placeholder='Filtre Equipe', value=[],
                     id='dropequipes',style=styledrop),
        html.Label('Selecione Meio de Propaganda:',style=styledroplabel),
        dcc.Dropdown(options=Propaganda, multi=True, placeholder='Filtre Meio de Propaganda', value=[],
                     id='droppropaganda',style=styledrop),
        html.Label('Selecione Consultor:',style=styledroplabel),
        dcc.Dropdown(options=Consultor, multi=True, placeholder='Filtre Consultor', value=[],
                     id='dropconsultor',style=styledrop)
        ], id= 'dropdowndiv',style=styledropdiv),
        
        dcc.Graph(className='grafico',id='Valor_gasto_por_equipe',style = graphpadrao),
        dcc.Graph(className='grafico',id='Status_de_pagamento', style=graphpie),
        dcc.Graph(className='grafico',id='valor_total_gasto_meios_de_propaganda', style=graphpie),
        dcc.Graph(className='grafico',id='Chamadas_médias_por_dia', style=graphpadrao),
        dcc.Graph(className='grafico',id='Chamadas_médias_por_mes', style=graphpadrao),
        dcc.Graph(className='grafico',id='valor_gasto_meios_de_propaganda_por_mes', style=graphpadrao),
        dcc.Graph(className='grafico',id='topconsultor',style = graphpadrao),
        html.H2(id='teste', style={'color':'white'})
    ]  )
], style=stylepagina)   


##FUNCIONALIDADES DOS FILTROS

#primeiro grafico de barras horizontais
@app.callback(Output('Valor_gasto_por_equipe','figure'),
             Input('dropequipes','value'),
             Input('droppropaganda','value'),
             Input('dropconsultor','value'),
)
def equipes_valorpago(dropequipes,droppropaganda,dropconsultor):

    #Nenhum drop  foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor == []:
        df1 = df.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)
        data =go.Bar(  # gera barras dentro da figura do Graf obj
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
    #apenas drop Equipes foi escolhido
    if dropequipes != [] and droppropaganda == [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            data=df.loc[(df['Equipe']==i)]#&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
    if dropequipes == [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for j in droppropaganda:
            data=df.loc[(df['Meio de Propaganda']==j)]#&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
    #apenas drop Consultor foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for k in dropconsultor:
            data=df.loc[(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
    # Todos os drops selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:
                for k in dropconsultor:
                    data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                    Filtro.append(data)
                    Filtrodf=pd.concat(Filtro)
                    Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)

    # Drop 1 e 2 selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:         
                data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
     # Drop 3 e 2 selecionados
    if dropequipes == [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for j in droppropaganda:
            for k in dropconsultor:         
                data=df.loc[(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:,s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
    if dropequipes != [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for k in dropconsultor:
                data=df.loc[(df['Equipe']==i)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df1 = Filtrodf.groupby('Equipe')['Valor Pago'].sum().reset_index().sort_values(by="Valor Pago", ascending=False)   
        data =go.Bar( 
                x=df1['Valor Pago'],  
                y=df1['Equipe'],
                orientation='h',   
                textposition='auto',
                text=df1['Valor Pago'],
                texttemplate='%{text:.2s}',
                insidetextfont=dict(family='Times', size=12,),
                marker=dict(color = colorx)
        ),
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig1 = go.Figure(data=data, layout=layout)
    return fig1           
   

###tem que ser refeitoooooo!!

#Grafico do meio de propaganda e valor gasto
@app.callback(Output('valor_gasto_meios_de_propaganda_por_mes','figure'),
             Input('dropequipes','value'),
             Input('droppropaganda','value'),
             Input('dropconsultor','value'),
)
def MeioPropaganda_valorpago(dropequipes,droppropaganda,dropconsultor):
    #Nenhum drop  foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor == []:
        df3 = df.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    if dropequipes != [] and droppropaganda == [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            data=df.loc[(df['Equipe']==i)]#&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    #apenas drop Propaganda foi escolhido
    if dropequipes == [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for j in droppropaganda:
            data=df.loc[(df['Meio de Propaganda']==j)]#&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    #apenas drop Consultor foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for k in dropconsultor:
            data=df.loc[(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    # Todos os drops selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:
                for k in dropconsultor:
                    data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                    Filtro.append(data)
                    Filtrodf=pd.concat(Filtro)
                    Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    # Drop 1 e 2 selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:         
                data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
     # Drop 3 e 2 selecionados
    if dropequipes == [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for j in droppropaganda:
            for k in dropconsultor:         
                data=df.loc[(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    if dropequipes != [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for k in dropconsultor:
                data=df.loc[(df['Equipe']==i)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df3 = Filtrodf.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
        fig3=px.line(df3, y="Valor Pago", x="Mês", color="Meio de Propaganda", color_discrete_sequence = colorx,template=template)
    return fig3           
   



# grafico chamada media por dia
@app.callback(Output('Chamadas_médias_por_dia','figure'),
             Input('dropequipes','value'),
             Input('droppropaganda','value'),
             Input('dropconsultor','value'),
)
def chamada_media_pordia(dropequipes,droppropaganda,dropconsultor):

    #Nenhum drop  foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor == []:
        df2 = df.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    #apenas drop Equipes foi escolhido
    if dropequipes != [] and droppropaganda == [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            data=df.loc[(df['Equipe']==i)]#&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    #apenas drop Propaganda foi escolhido
    if dropequipes == [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for j in droppropaganda:
            data=df.loc[(df['Meio de Propaganda']==j)]#&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    #apenas drop Consultor foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for k in dropconsultor:
            data=df.loc[(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    # Todos os drops selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:
                for k in dropconsultor:
                    data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                    Filtro.append(data)
                    Filtrodf=pd.concat(Filtro)
                    Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    # Drop 1 e 2 selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:         
                data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
     # Drop 3 e 2 selecionados
    if dropequipes == [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for j in droppropaganda:
            for k in dropconsultor:         
                data=df.loc[(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    if dropequipes != [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for k in dropconsultor:
                data=df.loc[(df['Equipe']==i)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df2 = Filtrodf.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[0]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig2 = go.Figure(data=data, layout=layout)
    return fig2           


# grafico chamada media por mes
@app.callback(Output('Chamadas_médias_por_mes','figure'),
             Input('dropequipes','value'),
             Input('droppropaganda','value'),
             Input('dropconsultor','value'),
)
def chamada_media_pormes(dropequipes,droppropaganda,dropconsultor):

    #Nenhum drop  foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor == []:
        df4 = df.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    #apenas drop Equipes foi escolhido
    if dropequipes != [] and droppropaganda == [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            data=df.loc[(df['Equipe']==i)]#&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    #apenas drop Propaganda foi escolhido
    if dropequipes == [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for j in droppropaganda:
            data=df.loc[(df['Meio de Propaganda']==j)]#&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    #apenas drop Consultor foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for k in dropconsultor:
            data=df.loc[(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    # Todos os drops selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:
                for k in dropconsultor:
                    data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                    Filtro.append(data)
                    Filtrodf=pd.concat(Filtro)
                    Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    # Drop 1 e 4 selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:         
                data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
     # Drop 3 e 4 selecionados
    if dropequipes == [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for j in droppropaganda:
            for k in dropconsultor:         
                data=df.loc[(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    if dropequipes != [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for k in dropconsultor:
                data=df.loc[(df['Equipe']==i)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df4 = Filtrodf.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
        data = go.Scatter(
        x=df4['Mês'], y=df4['Chamadas Realizadas'], mode='lines', fill='tonexty',marker=dict(color=colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template2)
        fig4 = go.Figure(data=data, layout=layout)
    return fig4 

##Controles dos Drops afetados por apenas 2 drops

#Pago nao pago
@app.callback(Output('Status_de_pagamento','figure'),
             Input('dropequipes','value'),
             Input('droppropaganda','value'),
             Input('dropconsultor','value'),
)
def statuspagamento(dropequipes,droppropaganda,dropconsultor):
 
    #Nenhum drop  foi escolhido
    if dropequipes == [] and droppropaganda == [] and dropconsultor == []:
        df6 = df.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)
    #apenas drop Equipes foi escolhido
    if dropequipes != [] and droppropaganda == [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            data=df.loc[(df['Equipe']==i)]#&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)
    if dropequipes == [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for j in droppropaganda:
            data=df.loc[(df['Meio de Propaganda']==j)]#&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)
    if dropequipes == [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for k in dropconsultor:
            data=df.loc[(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)    # Todos os drops selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:
                for k in dropconsultor:
                    data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                    Filtro.append(data)
                    Filtrodf=pd.concat(Filtro)
                    Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)    # Drop 1 e 2 selecionados
    if dropequipes != [] and droppropaganda != [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            for j in droppropaganda:         
                data=df.loc[(df['Equipe']==i)&(df['Meio de Propaganda']==j)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)     # Drop 3 e 2 selecionados
    if dropequipes == [] and droppropaganda != [] and dropconsultor != []:
        Filtro=[]
        for j in droppropaganda:
            for k in dropconsultor:         
                data=df.loc[(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)
    if dropequipes !=   [] and droppropaganda == [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for k in dropconsultor:
                data=df.loc[(df['Equipe']==i)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df6 = Filtrodf.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()        
        data=go.Pie(labels=['Não Pago', 'Pago'], values=df6, hole=.6,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig6 = go.Figure(data=data, layout=layout)  
    return fig6           
   

#Grafico Pie meios de propaganda (usando filtro com só dois drops)
@app.callback(Output('valor_total_gasto_meios_de_propaganda','figure'),
             Input('dropequipes','value'),
             Input('dropconsultor','value'),
)
def MeioPropaganda_valorpago(dropequipes,dropconsultor):
 
    #Nenhum drop  foi escolhido
    if dropequipes == [] and dropconsultor == []:
        df11 = df.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
        data=go.Pie(labels=df11['Meio de Propaganda'], values=df11['Valor Pago'], hole=.7, marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig11 = go.Figure(data=data, layout=layout)  
    if dropequipes != [] and dropconsultor == []:
        Filtro=[]
        for i in dropequipes:
            data=df.loc[(df['Equipe']==i)]#&(df['Meio de Propaganda']==j)&(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df11 = Filtrodf.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
        data=go.Pie(labels=df11['Meio de Propaganda'], values=df11['Valor Pago'], hole=.7,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig11 = go.Figure(data=data, layout=layout)   
        #apenas drop Consultor foi escolhido
    if dropequipes == [] and dropconsultor != []:
        Filtro=[]
        for k in dropconsultor:
            data=df.loc[(df['Consultor']==k)]
            Filtro.append(data)
            Filtrodf=pd.concat(Filtro)
            Filtrodf=Filtrodf
        df11 = Filtrodf.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
        data=go.Pie(labels=df11['Meio de Propaganda'], values=df11['Valor Pago'], hole=.7,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig11 = go.Figure(data=data, layout=layout)
        # Todos os drops (1 e 2) selecionados
    if dropequipes != [] and dropconsultor != []:
        Filtro=[]
        for i in dropequipes:
            for k in dropconsultor:
                data=df.loc[(df['Equipe']==i)&(df['Consultor']==k)]
                Filtro.append(data)
                Filtrodf=pd.concat(Filtro)
                Filtrodf=Filtrodf
        df11 = Filtrodf.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
        data=go.Pie(labels=df11['Meio de Propaganda'], values=df11['Valor Pago'], hole=.7,marker=dict(colors=colorx))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig11 = go.Figure(data=data, layout=layout)
    return fig11  


#Grafico barras Top consultores (usando filtro com só um drops)
@app.callback(Output('topconsultor','figure'),
             Input('dropequipes','value'),
)
def valorpagoTopconsultores(dropequipes):
    filtro=df['Equipe'].isin(dropequipes)
    df13 = df[filtro].groupby(['Equipe', 'Consultor'])['Valor Pago'].sum()
    df13 = df13.sort_values(ascending=False)
    #Nenhuma Equipe  foi escolhida
    if len(dropequipes) == 0 or len(dropequipes) == 4: 
        df13 = df.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum()
        df13 = df13.sort_values(ascending=False)
        df13 = df13.groupby('Equipe').head(1).reset_index()
        data=go.Bar(y=df13['Consultor']+'<br>'+df13['Equipe'], x=df13['Valor Pago'], orientation='h',
                                textposition='auto', text=df13['Valor Pago'], texttemplate='%{text:.2s}',
                                insidetextfont=dict(family='Times', size=12), marker=dict(color = colorx[1]))
        layout= go.Layout(yaxis = axis, xaxis = axis, margin=margingraph,
                            plot_bgcolor=plotbgc, paper_bgcolor=paperbgc, template=template)
        fig13 = go.Figure(data=data, layout=layout) 
        #apenas drop Equipe foi escolhido 1
    if len(dropequipes) == 1:
        df13=df13.groupby('Equipe').head(4).reset_index()
        data=go.Bar(y=df13['Consultor']+'<br>'+df13['Equipe'], x=df13['Valor Pago'], orientation='h',
                                textposition='auto', text=df13['Valor Pago'], texttemplate='%{text:.2s}',
                                insidetextfont=dict(family='Times', size=12), marker=dict(color = colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig13 = go.Figure(data=data, layout=layout)   
    #apenas drop Equipe foi escolhido 2
    if len(dropequipes) == 2:
        df13=df13.groupby('Equipe').head(2).reset_index()
        data=go.Bar(y=df13['Consultor']+'<br>'+df13['Equipe'], x=df13['Valor Pago'], orientation='h',
                                textposition='auto', text=df13['Valor Pago'], texttemplate='%{text:.2s}',
                                insidetextfont=dict(family='Times', size=12), marker=dict(color = colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig13 = go.Figure(data=data, layout=layout)         
    #apenas drop Equipe foi escolhido 3
    if len(dropequipes) == 3:
        df13=df13.groupby('Equipe').head(1).reset_index()
        data=go.Bar(y=df13['Consultor']+'<br>'+df13['Equipe'], x=df13['Valor Pago'], orientation='h',
                                textposition='auto', text=df13['Valor Pago'], texttemplate='%{text:.2s}',
                                insidetextfont=dict(family='Times', size=12), marker=dict(color = colorx[1]))
        layout=go.Layout(yaxis = axis,xaxis = axis, plot_bgcolor=plotbgc, 
                         margin=margingraph, paper_bgcolor=paperbgc, template=template)
        fig13 = go.Figure(data=data, layout=layout)
    return fig13  



##teste fim da pagina
@app.callback(Output('teste','children'),
             Input('dropequipes','value'),
             Input('droppropaganda','value'),
             Input('dropconsultor','value'),       
             )
def update_output_div(dropequipes,droppropaganda,dropconsultor):
    return f'Output: {dropequipes}/{droppropaganda}/{dropconsultor}/'

if __name__ == '__main__':
    app.run(debug=False, port="8050")

