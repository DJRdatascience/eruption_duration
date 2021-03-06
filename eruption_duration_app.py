import pandas as pd
import streamlit as st
import plotly.express as px
import joblib

#####################################################################################
# SETUP PAGE
#####################################################################################

st.set_page_config( page_title='Eruptive Active Duration',
                    page_icon=':volcano:',
                    layout='wide' )

#####################################################################################
# LOAD DATA
#####################################################################################

df_volcano = pd.read_feather( 'volc_data.feather' )

#####################################################################################
# SIDEBAR
#####################################################################################

st.sidebar.header('Select filters')


erupt_type = st.sidebar.selectbox(  'Eruptive activity type',
                                    options=['Event','Eruption'] )

if erupt_type == 'Event':
    columns = [ 'stratovolcano', 'dome', 'lava_cone', 'subduction', 'continental', 'elevation', 
                'avgrepose', 'intermediate', 'felsic', 'summit_crater', 'h_bw', 'ellip']
    df_volcano.dropna( subset=columns, how='any', axis=0, inplace=True )
else:
    columns = [ 'stratovolcano', 'caldera', 'dome', 'complex', 'lava_cone', 'compound', 'subduction', 'rift',
                'intraplate', 'continental', 'ctcrust1', 'elevation', 'volume', 'eruptionssince1960', 'avgrepose', 'mafic',
                'intermediate', 'felsic', 'summit_crater', 'h_bw', 'ellip' ]
    df_volcano.dropna( subset=columns, how='any', axis=0, inplace=True )

volc_list = df_volcano['volcanoname'].str.capitalize().values
volcano = st.sidebar.selectbox( 'Select a volcano',
                                options=volc_list ).lower()

if erupt_type == 'Event':
    explosive = st.sidebar.selectbox(   'Explosive?',
                                        options=['Yes','No'] )
    continuous = st.sidebar.selectbox(  'Continuous?',
                                        options=['Yes','No'] )
else:
    explosive = st.sidebar.selectbox(   'VEI',
                                        options=[ i for i in range(6) ] )
    #continuous = st.sidebar.text_input(  'Repose duration (days)', '10' )

gen_plot = st.sidebar.button('Generate plot')

#####################################################################################
# MAIN PAGE
#####################################################################################

st.markdown( '# <font color="#D62728">'+erupt_type+'</font> Duration', unsafe_allow_html=True )
st.markdown( '###' )

#------------------------------------------------------------------------------------
# Top section
#------------------------------------------------------------------------------------

st.markdown('---')

#------------------------------------------------------------------------------------
# Bar plots
#------------------------------------------------------------------------------------
model_select = { 'Event': 'event_gb.joblib', 'Eruption': 'eruption_gb.joblib' }
x_axis_title = { 'Event': 'Duration (hours)', 'Eruption': 'Duration (days)' }
x_axis_range = { 'Event': [-3,3], 'Eruption': [-0.5,4.5] }
factor = { 'Event': 1/(60*60), 'Eruption': 1 }
yes_no = {'No': 0, 'Yes': 1}

if gen_plot:
    model = joblib.load( model_select[erupt_type] )
    if erupt_type == 'Event':
        features = [ yes_no[explosive], yes_no[continuous] ]
    else:
        features = [ int(explosive) ]
    features += [ df_volcano[df_volcano.volcanoname == volcano][c].values[0] for c in columns ]
    surv_func = model.predict_survival_function( [features] )

    fig_sf = px.line(
        x = surv_func[0].x * factor[erupt_type],
        y = surv_func[0](surv_func[0].x),
        title='<b>Survivor function</b>',
        template='simple_white',
        log_x=True,
        
    )
    fig_sf.update_traces(line={"shape": 'hv'})
    fig_sf.update_layout(
        xaxis_range=x_axis_range[erupt_type],
        xaxis={'title_text': x_axis_title[erupt_type]},
        yaxis={'title_text': 'Exceedance probability'} )

    #~~~~~~~~~~
    # Plot figures
    #~~~~~~~~~~

    #left_column, middle_column, right_column = st.columns(3)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart( fig_sf, use_container_width=True )