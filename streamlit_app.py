# Importar paquetes de Python
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Escribir directamente en la aplicación
st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')
st.write(
    """
    ***Choose the fruits you want in your custom Smoothie!***
    """
)

# Establecer conexión con Snowflake
cnx = st.connection("snowflake")
# Establecer una sesión
session = cnx.session()


# Entrada de texto para el nombre del cliente
name_on_order = st.text_input('Enter your name for the order:', '')

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")

# Extraer solo los nombres de las frutas
fruit_names = my_dataframe.select("FRUIT_NAME").collect()
fruit_names_list = [row["FRUIT_NAME"] for row in fruit_names]  # Convertir a una lista de nombres


# Selección múltiple de ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names_list,  # Pasar solo los nombres
    max_selections=5
)

if ingredients_list and name_on_order:
    ingredients_string = ' '.join(ingredients_list)  # Combinar ingredientes en una cadena

    # Crear una consulta SQL para la inserción
    insert_query = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    # Ejecutar la consulta en Snowflake
    session.sql(insert_query).collect()  # Ejecutar y confirmar la inserción

    st.success("Your Smoothie has been ordered successfully!", icon="✅")





'''
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(':cup_with_straw: Pending Smoothie Orders! :cup_with_straw:')
st.write(
    """
    ***Orders that need to be filled.***
    """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("name_on_order").is_null())
editable_df = st.data_editor(my_dataframe)


submitted = st.button('Submit')

if submitted:
    st.success("Someone clicked the button.", icon="👍")

'''
