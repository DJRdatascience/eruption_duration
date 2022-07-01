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
    df_volcano = df_volcano[ columns ].dropna(axis=0)

volcano = st.sidebar.selectbox( 'Select a volcano',
                                options=df_volcano.volcanoname )

if erupt_type == 'Event':
    explosive = st.sidebar.selectbox(   'Explosive?',
                                        options=['Yes','No'] )
    continuous = st.sidebar.selectbox(  'Continuous?',
                                        options=['Yes','No'] )
else:
    TFC = [0,1]


gen_plot = st.button('Generate plot')

#####################################################################################
# MAIN PAGE
#####################################################################################

st.markdown( '# <font color="#D62728">'+erupt_type+'</font> Duration', unsafe_allow_html=True )
st.markdown( '###' )

#------------------------------------------------------------------------------------
# Top section
#------------------------------------------------------------------------------------

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Open Rate')
    #st.markdown( '### <font color="#D62728">'+str(round(open_rate, 1))+' %</font> ('+str(round(open_rate_total, 1))+' % avg)', unsafe_allow_html=True )
with middle_column:
    st.subheader('Click Per Open Rate')
    #st.markdown( '### <font color="#D62728">'+str(round(click_rate, 2))+' %</font> ('+str(round(click_rate_total, 2))+' % avg)', unsafe_allow_html=True )
with right_column:
    st.subheader('Donations')
    #st.markdown( '### <font color="#D62728">\$'+str(round(raised))+' </font> of $'+str(round(raised_total))+' (total)', unsafe_allow_html=True )

st.markdown('---')

#------------------------------------------------------------------------------------
# Bar plots
#------------------------------------------------------------------------------------

if gen_plot:
    model_select = { 'Event': 'event_gb.joblib', 'Eruption': 'eruption_gb.joblib' }
    yes_no = {'No': 0, 'Yes': 1}
    model = joblib.load( model_select[erupt_type] )
    if erupt_type == 'Event':
        
        volc_features = [ df_volcano[df_volcano.volcanoname == volcano][c].value for c in columns[2:] ]
        features = [ yes_no[explosive], yes_no[continuous] ] + volc_features
    surv_func = model.predict_survival_function(features)

    fig_sf = px.line(
        x = surv_func[0].x/(60*60),
        y = surv_func[0](surv_func[0].x),
        title='<b>Survivor function</b>',
        template='simple_white',
        color='tab:red',
        labels={'xaxis_title': 'Duration (days)', 'yaxis_title': 'Exceedance probability'}
    )

'''
df_grp_select = df_select.groupby('Email').mean().sort_values('Opened',ascending=False)
df_grp_select['Opened'] *= 100

#default_color = '#1F77B4'
#colors = {email: '#D62728'}
color_discrete_map = {
    c: colors.get(c, default_color) 
    for c in df_grp_select.index.unique() }

#~~~~~~~~~~
# Open rate
#~~~~~~~~~~

fig_open_rate = px.bar(
    df_grp_select,
    x = 'Opened',
    y = df_grp_select.index,
    orientation='h',
    title='<b>Open Rates (percent)</b>',
    template='simple_white',
    color=df_grp_select.index,
    color_discrete_map=color_discrete_map
)
fig_open_rate.add_vline(x=open_rate_total,line_color='white',line_width=3)
fig_open_rate.update_traces(showlegend=False)

fig_open_rate.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis={'title_text': None},
    yaxis={'title_text': None},
)

#~~~~~~~~~~
# Click per open rate
#~~~~~~~~~~

df_grp_select = df_select.groupby('Email').sum() #.sort_values('Opened',ascending=False)
df_grp_select['Click Per Open'] = 100 * df_grp_select['Clicked'] / df_grp_select['Opened']
df_grp_select.sort_values('Click Per Open', ascending=False,inplace=True)

fig_click_rate = px.bar(
    df_grp_select,
    x = 'Click Per Open',
    y = df_grp_select.index,
    orientation='h',
    title='<b>Click Per Open Rates (percent)</b>',
    template='simple_white',
    color=df_grp_select.index,
    color_discrete_map=color_discrete_map
)
fig_click_rate.add_vline(x=click_rate_total,line_color='white',line_width=3)
fig_click_rate.update_traces(showlegend=False)

fig_click_rate.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis={'title_text': None},
    yaxis={'title_text': None}
)

#~~~~~~~~~~
# Donations
#~~~~~~~~~~

df_grp_donations_select = df_donations_select.groupby('Reference Code').sum() #.sort_values('Opened',ascending=False)
df_grp_donations_select.sort_values('Amount', ascending=False,inplace=True)

default_color = '#1F77B4'
colors = {email: '#D62728'}
color_discrete_map = {
    c: colors.get(c, default_color)
    for c in df_grp_donations_select.index.unique() }

fig_donations = px.bar(
    df_grp_donations_select,
    x = 'Amount',
    y = df_grp_donations_select.index,
    orientation='h',
    title='<b>Total donations ($)</b>',
    template='simple_white',
    color=df_grp_donations_select.index,
    color_discrete_map=color_discrete_map
)
#fig_donations.add_vline(x=df_donations_select.Amount.mean(),line_color='white',line_width=3)
fig_donations.update_traces(showlegend=False)

fig_donations.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis={'title_text': None},
    yaxis={'title_text': None}
)
'''
#~~~~~~~~~~
# Plot figures
#~~~~~~~~~~

#left_column, middle_column, right_column = st.columns(3)

middle_column = st.columns(1)
middle_column.plotly_chart( fig_sf, use_container_width=True )
