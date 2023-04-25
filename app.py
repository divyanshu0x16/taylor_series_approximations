import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

st.set_page_config(page_title='Taylor Series Approximations', layout="wide")
st.title('Taylor Series Approximations')

x = sp.symbols('x')

sin_func = sp.sin(x)
cos_func = sp.cos(x)
ex_func = sp.exp(x)

with st.sidebar:
    function = st.selectbox('Select a function to approximate', ('sin(x)', 'cos(x)', 'e^x'))
    order = st.slider('Order of approximation', min_value=1, max_value=10, value=1)

def taylor_series(func, order):
    return sp.series(func, x, x0=0, n=order+1).removeO()

def app():
    x_range = np.linspace(-10, 10, 200)

    if function == 'sin(x)':
        taylor = taylor_series(sin_func, order)
        true_vals = np.sin(x_range)
        label = 'sin(x)'

    elif function == 'cos(x)':
        taylor = taylor_series(cos_func, order)
        true_vals = np.cos(x_range)
        label = 'cos(x)'

    elif function == 'e^x':
        taylor = taylor_series(ex_func, order)
        true_vals = np.exp(x_range)
        label = 'e^x'

    taylor_func = sp.lambdify(x, taylor, 'numpy')
    taylor_vals = taylor_func(x_range)
    
    #For cos(x) = 1
    if(type(taylor_vals)==int):
        taylor_vals=np.ones(200)

    rmse_arr = []
    for i in range(1,11):

        if(function == 'sin(x)'):
            rmse_func = sp.lambdify(x, taylor_series(sin_func, i), 'numpy')

        elif (function == 'cos(x)'):
            rmse_func = sp.lambdify(x, taylor_series(cos_func, i), 'numpy')

        elif (function == 'e^x'):
            rmse_func =  sp.lambdify(x, taylor_series(ex_func, i), 'numpy')
        
        curr_taylor_vals = rmse_func(x_range)
        if(type(curr_taylor_vals)==int):
            curr_taylor_vals=np.ones(200)

        rmse_arr.append(np.sqrt(np.mean(np.sum((curr_taylor_vals[60:140]-true_vals[60:140])**2)))) #Plotted only for values between -4 and 4

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))
    ax1.plot(x_range, true_vals, label=label)
    ax1.plot(x_range, taylor_vals, label=f'Taylor series approx. (order {order})')
    ax1.legend()
    ax1.set_xlim([-7, 7])
    ax1.set_ylim([-10, 10])
    ax1.grid(True)
    ax1.axhline(y=0, color='black', linestyle='--')
    ax1.axvline(x=0, color='black', linestyle='--')

    fig.subplots_adjust(wspace=0.25, hspace=None)

    ax2.plot(rmse_arr)
    ax2.set_xlabel('Order')
    ax2.set_ylabel('RMSE')
    ax2.grid(True)
    st.pyplot(fig)

app()