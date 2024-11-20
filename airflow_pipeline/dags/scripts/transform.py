import pandas as pd
import ast

def transform_en_species_data():
    df = pd.read_csv('/opt/airflow/raw_data/EN.csv')

    def create_relationship_table(table, column, is_tuple=False, tuples=[]):
        table = df[['id', column]].copy()
        table[column] = table[column].apply(ast.literal_eval)
        table = table.explode(column).dropna().reset_index(drop=True)
        if is_tuple:
            table[tuples] = pd.DataFrame(table[column].tolist(), index=table.index)
        return table
    
    en_conservation_actions_df = create_relationship_table('en_conservation_actions_df', 'conservation_actions')
    en_conservation_actions_df['group'] = en_conservation_actions_df['conservation_actions'].apply(lambda x: x[0])
    
    en_habitats_df = create_relationship_table('en_habitats_df', 'habitats', is_tuple=True, tuples=['code', 'majorImportance', 'season']).drop('habitats', axis=1)
    en_habitats_df['group'] = en_habitats_df['code'].apply(lambda x: x[0])
    
    en_locations_df = create_relationship_table('en_locations_df', 'locations', is_tuple=True, tuples=['origin', 'code', 'description']).drop('locations', axis=1)

    en_threats_df = create_relationship_table('en_threats_df', 'threats', is_tuple=True, tuples=['code', 'timing', 'scope', 'score', 'severity']).drop('threats', axis=1)
    en_threats_df['group'] = en_threats_df['code'].apply(lambda x: x[0])
    
    en_main_df = df.drop(['conservation_actions', 'locations', 'habitats', 'threats'], axis=1)

    en_conservation_actions_df.to_csv('/opt/airflow/processed_data/en_conservation_actions.csv', header=True, index=False)
    en_habitats_df.to_csv('/opt/airflow/processed_data/en_habitats.csv', header=True, index=False)
    en_locations_df.to_csv('/opt/airflow/processed_data/en_locations.csv', header=True, index=False)
    en_threats_df.to_csv('/opt/airflow/processed_data/en_threats.csv', header=True, index=False)
    en_main_df.to_csv('/opt/airflow/processed_data/en_main.csv', header=True, index=False)