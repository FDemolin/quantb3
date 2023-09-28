import streamlit as st


st.markdown('## Calendário Econômico')

calendar_html = ''' <iframe src="https://sslecal2.investing.com?
columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=2,3
&features=datepicker,timezone&countries=17,32,37,5,35,4,72
&calType=week&timeZone=12&lang=12" width="800" height="700" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0">
</iframe>'''

st.markdown(calendar_html, unsafe_allow_html=True)

