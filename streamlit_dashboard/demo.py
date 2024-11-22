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
try:
    conn = st.connection('s3', type=FilesConnection)

    conservation_actions_df = conn.read("wildwatchstorage/en_conservation_actions.csv", input_format="csv", ttl=600)
    desc_ca_df = conn.read("wildwatchstorage/conservation_actions.csv", input_format="csv", ttl=600)

    habitats_df = conn.read("wildwatchstorage/en_habitats.csv", input_format="csv", ttl=600)
    desc_habitats_df = conn.read("wildwatchstorage/habitats.csv", input_format="csv", ttl=600)

    locations_df = conn.read("wildwatchstorage/en_locations.csv", input_format="csv", ttl=600)
    
    threats_df = conn.read("wildwatchstorage/en_threats.csv", input_format="csv", ttl=600)
    desc_threats_df = conn.read("wildwatchstorage/threats.csv", input_format="csv", ttl=600)
except Exception as e:
    print(e)
    print('Connection error with AWS S3')

def conservation_action():
    st.subheader("Conservation actions for Endangered species")
    group = conservation_actions_df.groupby('group').size().reset_index(name='count')
    fig, ax = plt.subplots()
    ax.pie(x=group['count'], 
            labels=[desc_ca_df.loc[desc_ca_df['code'] == str(g), 'description'].values[0] for g in group['group']], 
            colors=['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462'],
            autopct='%1.0f%%', pctdistance=0.8, labeldistance=1.2)
    st.pyplot(fig)

def habitats():
    st.subheader("Habitats for Endangered species")
    group = habitats_df.groupby('group').size().reset_index(name='count')
    fig, ax = plt.subplots()
    ax.pie(x=group['count'], 
            labels=[desc_habitats_df.loc[desc_habitats_df['code'] == str(g), 'description'].values[0] for g in group['group']],
            colors=['#ccebc5','#fbb4ae','#b3cde3','#decbe4','#fed9a6','#ffffcc','#e5d8bd'],
            autopct='%1.0f%%', pctdistance=0.8, labeldistance=1.2)
    st.pyplot(fig)


def threats():
    st.subheader("Threats for Endangered species")
    group = threats_df.groupby('group').size().reset_index(name='count')
    fig, ax = plt.subplots()
    ax.pie(x=group['count'], 
            labels=[desc_threats_df.loc[desc_threats_df['code'] == str(g), 'description'].values[0] for g in group['group']],
            colors=['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6'],
            autopct='%1.0f%%', pctdistance=0.8, labeldistance=1.2)
    st.pyplot(fig)

def top_k_countries(k=20):
    st.subheader(f'Top {k} countries with Endangered species')
    group = locations_df.groupby('description').size().reset_index(name='count')
    group = group.sort_values(['count'], ascending=False)
    fig, ax = plt.subplots(figsize=(32, 8))
    ax.bar(x=range(k), height=group['count'][:k], color='#b2df8a')
    ax.set_xticks(range(20))
    ax.set_xticklabels(group['description'][:k], rotation=-45, ha="left", rotation_mode="anchor")
    ax.set_xlim(left=-1)
    ax.set_ylabel('Species counts')
    st.pyplot(fig)


def run():
    st.write("# Welcome to Wildwatch Dashboard! 👋")
    habitats()
    threats()
    conservation_action()
    top_k_countries()


if __name__ == "__main__":
    run()