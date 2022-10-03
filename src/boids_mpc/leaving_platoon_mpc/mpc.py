import do_mpc
import numpy as np
from casadi import *
import math

def mpc(model):
    ego_max_speed = 4
    platoon_max_speed = 2

    # Obtain an instance of the do-mpc MPC class
    # and initiate it with the model:
    mpc = do_mpc.controller.MPC(model)

    # Set parameters:
    setup_mpc = {
        'n_horizon': 20,
        't_step': 0.1,
        'store_full_solution': True,
    }
    mpc.set_param(**setup_mpc)

    # Configure objective function:

    mterm = - model.x['p_y_1']
    lterm = if_else(model.x['s']==1, model.x['p_y_3'], -model.x['p_y_3']) + if_else(model.x['s']==2, -model.x['v_x_1'], model.x['v_x_1']**2) + if_else(model.x['s']==3, model.x['p_y_2'] + model.x['p_y_4'], - model.x['p_y_2'] - model.x['p_y_4']) + if_else(logic_or(model.x['s']==3, model.x['s']==4), -model.x['p_y_1'], model.x['p_y_1'])

    mpc.set_objective(mterm=mterm, lterm=lterm)

    mpc.set_rterm(
        a_x_1=1e+3,
        a_y_1=1e+3,
        a_x_2=1e+3,
        a_y_2=1e+3,
        a_x_3=1e+3,
        a_y_3=1e+3,
        a_x_4=1e+3,
        a_y_4=1e+3
    )
    
    # Lower bounds on states:

    mpc.bounds['lower', '_x', 'p_y_1'] = 0
    mpc.bounds['upper', '_x', 'p_y_1'] = 1000

    mpc.bounds['lower', '_x', 'p_y_2'] = 0
    mpc.bounds['upper', '_x', 'p_y_2'] = 1000

    mpc.bounds['lower', '_x', 'p_y_3'] = 0
    mpc.bounds['upper', '_x', 'p_y_3'] = 1000

    mpc.bounds['lower', '_x', 'p_y_4'] = 0
    mpc.bounds['upper', '_x', 'p_y_4'] = 1000

    mpc.bounds['lower', '_x', 'p_x_1'] = 0
    mpc.bounds['upper', '_x', 'p_x_1'] = 1000

    mpc.bounds['lower', '_x', 'p_x_2'] = 0
    mpc.bounds['upper', '_x', 'p_x_2'] = 1000

    mpc.bounds['lower', '_x', 'p_x_3'] = 0
    mpc.bounds['upper', '_x', 'p_x_3'] = 1000

    mpc.bounds['lower', '_x', 'p_x_4'] = 0
    mpc.bounds['upper', '_x', 'p_x_4'] = 1000

    mpc.bounds['lower', '_x', 'v_y_1'] = ego_max_speed / 2
    mpc.bounds['upper', '_x', 'v_y_1'] = ego_max_speed

    mpc.bounds['lower', '_x', 'v_x_1'] = -ego_max_speed
    mpc.bounds['upper', '_x', 'v_x_1'] = ego_max_speed

    mpc.bounds['lower', '_x', 'v_y_2'] = platoon_max_speed / 2
    mpc.bounds['upper', '_x', 'v_y_2'] = platoon_max_speed

    mpc.bounds['lower', '_x', 'v_x_2'] = -platoon_max_speed
    mpc.bounds['upper', '_x', 'v_x_2'] = platoon_max_speed
    
    mpc.bounds['lower', '_x', 'v_y_3'] = platoon_max_speed / 2
    mpc.bounds['upper', '_x', 'v_y_3'] = platoon_max_speed

    mpc.bounds['lower', '_x', 'v_x_3'] = -platoon_max_speed
    mpc.bounds['upper', '_x', 'v_x_3'] = platoon_max_speed

    mpc.bounds['lower', '_x', 'v_y_4'] = platoon_max_speed / 2
    mpc.bounds['upper', '_x', 'v_y_4'] = platoon_max_speed

    mpc.bounds['lower', '_x', 'v_x_4'] = -platoon_max_speed
    mpc.bounds['upper', '_x', 'v_x_4'] = platoon_max_speed

    mpc.bounds['lower', '_u', 'a_y_1'] = -0.5
    mpc.bounds['upper', '_u', 'a_y_1'] = 0.5

    mpc.bounds['lower', '_u', 'a_x_1'] = -0.5
    mpc.bounds['upper', '_u', 'a_x_1'] = 0.5

    mpc.bounds['lower', '_u', 'a_y_2'] = -0.5
    mpc.bounds['upper', '_u', 'a_y_2'] = 0.5

    mpc.bounds['lower', '_u', 'a_x_2'] = -0.5
    mpc.bounds['upper', '_u', 'a_x_2'] = 0.5

    mpc.bounds['lower', '_u', 'a_y_3'] = -0.5
    mpc.bounds['upper', '_u', 'a_y_3'] = 0.5

    mpc.bounds['lower', '_u', 'a_x_3'] = -0.5
    mpc.bounds['upper', '_u', 'a_x_3'] = 0.5

    mpc.bounds['lower', '_u', 'a_y_4'] = -0.5
    mpc.bounds['upper', '_u', 'a_y_4'] = 0.5

    mpc.bounds['lower', '_u', 'a_x_4'] = -0.5
    mpc.bounds['upper', '_u', 'a_x_4'] = 0.5


    mpc.setup()

    return mpc

