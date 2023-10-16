import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title='Visualization', #strating command of streamlit
page_icon=":bar_chart:", layout='wide')

@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    df=pd.read_excel(io='supermarkt_sales.xlsx', #reading excel
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000
    )
    return df

df=get_data_from_excel() #caching the data so that we dont load it always

st.dataframe(df) #first st command of dataframe

# st.sidebar.header("Selection here?")

st.subheader(":bar_chart: Data Visualisations")#visualisation start
st.markdown("---")


left_column, middle_column, right_column=st.columns(3) #columns for placements

#visualisation 1
dfg=df.groupby(by='City').sum()[["Total"]] #how to automate this?
fig=px.bar(dfg,x='Total',y=dfg.index) #can be automated by writing different functions for different charts which would be called when buttons are pressed
fig.update_layout(autosize=True, width=400, height=400)


#visualisation 2
df['hour']=pd.to_datetime(df['Time'],format="%H:%M:%S").dt.hour
dfg1=df.groupby(by='hour').mean()[['gross income']]
fig1=px.line(dfg1,x=dfg1.index,y="gross income")
fig1.update_layout(xaxis=dict(tickmode='array',
            tickvals=np.array(dfg1.index),ticktext=df.hour),autosize=True, width=400, height=400)


sst=st.session_state
if "m" not in sst:
    sst.m=1
if "dic" not in st.session_state:
    sst.dic={}
if "diccol" not in st.session_state:
    sst.diccol={}
if "diccust" not in st.session_state:
    sst.diccust={}
if "dicform" not in st.session_state:
    sst.dicform={}
if "dicxaxis" not in st.session_state:
    sst.dicxaxis={}
if "dicyaxis" not in st.session_state:
    sst.dicyaxis={}
if "dicgraphtype" not in st.session_state:
    sst.dicgraphtype={}
if "submitted" not in st.session_state:
    sst.submitted={}
if "diccol1" not in st.session_state:
    sst.diccol1={}
def add_chart(k,graph,xaxis,yaxis):

    if graph=='button':
        retfig=px.bar(x=np.linspace(0,10,10),y=np.linspace(0,10,10),color_discrete_sequence=["#7f7f7f"]*10)
        sst.m+=1
    if graph=='Bar graph':
        dfg1=df.groupby(by=xaxis).mean()[[yaxis]]
        fig=px.bar(dfg1,x=yaxis,y=dfg1.index)
        retfig=fig
    if graph=='Pie Chart':
        dfg1=df.groupby(by=xaxis).mean()[[yaxis]]
        fig=px.pie(dfg1,names=dfg1.index,values=yaxis)
        retfig=fig
    if graph=='Line Chart':
        dfg1=df.groupby(by=xaxis).mean()[[yaxis]]
        fig=px.line(dfg1,x=dfg1.index,y=yaxis)
        retfig=fig
    sst.dic[k]=retfig

    
def del_dic():
    sst.dic={}
    sst.iter=0
    sst.m=1
    sst.diccol={}
    sst.diccust={}
    sst.submitted={}
butcol=st.columns([0.8,0.03,0.05,0.03,0.05])
but1=butcol[1].button("X",help='click to add chart',key='button1')
if but1:
    add_chart(sst.m,'button','na','na')
butcol[2].markdown('Add Chart')
but2=butcol[3].button("X",help='to clear the cache',key='button2')
if but2:
    del_dic()
butcol[4].markdown('Delete all')
st.markdown("---")
# st.markdown(f"@@@@@@@@@@@@@@@@@@@@{len(sst.dic)},{sst.dic}")
if len(sst.dic)>=1:
    b=0 #represents row number
    for x in range(1,len(sst.dic)+1):
        sst.diccol[b]=st.columns([1])
        # sst.diccust[b]=sst.diccol[b][1].multiselect("select city",key=b, options=df["City"].unique(),
        # default=df["City"].unique())
        with sst.diccol[b][0]:
            diccoll=st.columns([0.2,0.2])
            with diccoll[1]:
                sst.dicform[b]=st.form(key=str(b))
                ln=list(np.append(['select'],df.columns, axis=0))
                sst.dicxaxis[b]=sst.dicform[b].selectbox("xaxis",ln,index=0)
                sst.dicyaxis[b]=sst.dicform[b].selectbox("yaxis",np.append(['Select'],df.columns,axis=0),index=0)
                sst.dicgraphtype[b]=sst.dicform[b].selectbox("Graph_type",['Select graph type','Bar graph','Pie Chart','Line Chart'],index=0)
                sst.submitted[b]=sst.dicform[b].form_submit_button("Create chart")
                if sst.submitted[b]:
                    # st.markdown(sst.dicgraphtype[b])
                    add_chart(b+1,sst.dicgraphtype[b],sst.dicxaxis[b],sst.dicyaxis[b])
                # st.markdown(sst.dic)
                # st.markdown(sst.m)
                # st.markdown(sst.submitted)
            diccoll[0].plotly_chart(sst.dic[x],use_container_width=True)
        sst.diccol1[b]=st.columns([1])
        with sst.diccol1[b][0]:
            st.text_area('Description of the Chart>',key=b)
        b+=1
        st.markdown("---")
        
    # cn=len(sst.dic)/2
    # for i in range(0,cn):
    #     col=st.columns([0.5,0.5])
    #     for j in [0,1]:
    #         for x in 
    #         col[j].plotly_chart(sst.dic[x],use_container_width=True)
    #         x+=1

    # for i,row in enumerate(sst.dic):
    #     col=st.columns([0.5,0.5])
    #     for j,field in enumerate(dic[row]):
    #         if j==0:
    #             col[j].plotly_chart(sst.dic[row][j],use_container_width=True)
    #         elif j==1:
    #             col[j].markdown(f'{sst.dic[row][j]}')




# cols=st.beta_columns([0.3,0.3,0.3])
# cols[0].plotly_chart(fig,use_container_width=True)
# cols[1].plotly_chart(fig1,use_container_width=True)
if "iter" not in st.session_state:
    st.session_state.iter=0
if but1:
    st.session_state.iter+=1
