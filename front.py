import streamlit as st
import requests


api_url = 'http://127.0.0.1:8001/predict'

st.title('House')
GrLivArea = st.number_input('GrLivArea', min_value=0.0, step=0.1)
YearBuilt = st.number_input('YearBuilt', min_value=0.0, step=0.1)
GarageCars = st.number_input('GarageCars', min_value=0.0, step=0.1)
TotalBsmtSF = st.number_input('TotalBsmtSF', min_value=0.0, step=0.1)
FullBath = st.number_input('FullBath', min_value=0.0, step=0.1)
OverallQual = st.number_input('OverallQual', min_value=0.0, step=0.1)
Neighborhood = st.selectbox('Район', ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr' ,'Crawfor',
                     'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes',
                     'NPkVill', 'NWAmes', 'NoRidge', 'NridgHt', 'OldTown', 'SWISU',
                     'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker'])


house_dict = {
    'GrLivArea': GrLivArea,
    'YearBuilt': YearBuilt,
    'GarageCars': GarageCars,
    'TotalBsmtSF': TotalBsmtSF,
    'FullBath': FullBath,
    'OverallQual': OverallQual,
    "Neighborhood": Neighborhood,
}


if st.button('Predict'):
    try:
        answer = requests.post(api_url, json=house_dict, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f"predict price: {result.get('price')}")
        else:
            st.error(f'Ошибка: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error('Ошибка подключения к API')