import do_mpc
from casadi import *
import numpy as np

def model():
    # Obtain an instance of the do-mpc model class
    # and select time discretization:
    model_type = 'discrete' # either 'discrete' or 'continuous'
    model = do_mpc.model.Model(model_type)

    # Introduce new states, inputs and other variables to the model, e.g.:
    p_x_1 = model.set_variable(var_type='_x', var_name='p_x_1', shape=(1,1))
    p_y_1 = model.set_variable(var_type='_x', var_name='p_y_1', shape=(1,1))

    p_x_2 = model.set_variable(var_type='_x', var_name='p_x_2', shape=(1,1))
    p_y_2 = model.set_variable(var_type='_x', var_name='p_y_2', shape=(1,1))

    p_x_3 = model.set_variable(var_type='_x', var_name='p_x_3', shape=(1,1))
    p_y_3 = model.set_variable(var_type='_x', var_name='p_y_3', shape=(1,1))


    v_x_1 = model.set_variable(var_type='_x', var_name='v_x_1', shape=(1,1))
    v_y_1 = model.set_variable(var_type='_x', var_name='v_y_1', shape=(1,1))

    v_x_2 = model.set_variable(var_type='_x', var_name='v_x_2', shape=(1,1))
    v_y_2 = model.set_variable(var_type='_x', var_name='v_y_2', shape=(1,1))

    v_x_3 = model.set_variable(var_type='_x', var_name='v_x_3', shape=(1,1))
    v_y_3 = model.set_variable(var_type='_x', var_name='v_y_3', shape=(1,1))

    s = model.set_variable(var_type='_x', var_name='s', shape=(1,1))

    a_x_1 = model.set_variable(var_type='_u', var_name='a_x_1', shape=(1,1))
    a_y_1 = model.set_variable(var_type='_u', var_name='a_y_1', shape=(1,1))


    # Set right-hand-side of ODE for all introduced states (_x).
    # Names are inherited from the state definition.
    model.set_rhs('p_x_1', p_x_1 + v_x_1)
    model.set_rhs('p_y_1', p_y_1 + v_y_1)

    model.set_rhs('p_x_2', p_x_2 + v_x_2)
    model.set_rhs('p_y_2', p_y_2 + v_y_2)

    model.set_rhs('p_x_3', p_x_3 + v_x_3)
    model.set_rhs('p_y_3', p_y_3 + v_y_3)

    model.set_rhs('v_x_1', v_x_1 + a_x_1)
    model.set_rhs('v_y_1', v_y_1 + a_y_1)

    model.set_rhs('v_x_2', v_x_2)
    model.set_rhs('v_y_2', v_y_2)

    model.set_rhs('v_x_3', v_x_3)
    model.set_rhs('v_y_3', v_y_3)


    model.set_rhs('s', s)

    # Setup model:
    model.setup()

    return model