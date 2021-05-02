import streamlit as st
st.title('My first app')
st.write('### Hello World')

st.sidebar.checkbox('hello')

st.sidebar.selectbox('hello', [1,2])

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

left_column, right_column = st.beta_columns(2)
left_column.button('Press me!')
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

with st.form(key='my_form'):
    text_input = st.text_input(label='Enter your name')
    x = st.slider('x')
    submit_button = st.form_submit_button(label='Submit')

# st.form_submit_button returns True upon form submit
if submit_button:
    st.write('hello', text_input)
    st.write(x, 'squared is', x * x)