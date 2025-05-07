import streamlit as st
from ProductSearcher import ProductSearcher

if "productSearcher" not in st.session_state:
    st.session_state.productSearcher = ProductSearcher()

st.title("Product Recommender")
category = st.text_input(label="Category")
useCase = st.text_input(label="Use Case")

if st.button("Submit"):
    res = st.session_state.productSearcher.searchProduct(category, useCase)
    for i in res:
        st.text(i)
