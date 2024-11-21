import streamlit as st
from st_files_connection import FilesConnection
from streamlit.logger import get_logger

import pandas as pd
import matplotlib.pyplot as plt

LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="Wildwatch Dashboard",
    page_icon="🐾",
)

conn = st.connection('s3', type=FilesConnection)
conservation_actions_df = conn.read("wildwatchstorage/en_conservation_actions.csv", input_format="csv", ttl=600)
desc_ca_df = conn.read("wildwatchstorage/conservation_actions.csv", input_format="csv", ttl=600)


def run():
    st.write("# Welcome to Wildwatch Dashboard! 👋")
    st.subheader("Conservation actions")
    group = conservation_actions_df.groupby('group').size().reset_index(name='count')
    fig, ax = plt.subplots()
    ax.pie(x=group['count'], 
            labels=[desc_ca_df.loc[desc_ca_df['code'] == str(g), 'description'].values[0] for g in group['group']], 
            colors=['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462'],
            autopct='%1.0f%%', pctdistance=0.8, labeldistance=1.2)
    st.pyplot(fig)


if __name__ == "__main__":
    run()