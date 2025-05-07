import streamlit as st
from ProductSearcher import ProductSearcher

if "productSearcher" not in st.session_state:
    st.session_state.productSearcher = ProductSearcher()


st.title("Product Recommender")

st.header("Find products")
category = st.text_input(label="Category")
useCase = st.text_input(label="Use Case")

col1, col2 = st.columns(2)    
productList = []
if st.button("Find"):
    productList = st.session_state.productSearcher.searchProduct(category, useCase)
    with col1:
        for product in productList:
            st.text(product)

with col2:
    for product in productList:
        url = st.session_state.productSearcher.getLinks(product)
        st.text(url)

st.header("Get Pros and Cons")  
product = st.text_input("Product", placeholder="Enter the product name")    
if st.button("Submit"):
    reviews = st.session_state.productSearcher.getReviews(product)
    st.text(reviews)
