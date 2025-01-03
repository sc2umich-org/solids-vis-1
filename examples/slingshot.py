from scipy.optimize import minimize 
from scipy.integrate import solve_ivp
import numpy as np
import sys
sys.path.append('.')
from solid_vis import conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject

def gravity_acceleration(t, x, m1=1, m2=1):
    """

    Parameters:
        x (ndarray, length 18) xyz coordinates of 3 bodies, followed by their velocities
    """
    # Extract coordinates
    v = x[9:]
    x1, x2, x3 = x[:3], x[3:6], x[6:9]

    # Get body distances
    sqdist12 = np.sum(np.square(x2-x1))
    sqdist13 = np.sum(np.square(x3-x1))
    sqdist23 = np.sum(np.square(x3-x2))

    # Construct the acceleration due to gravity
    a = np.zeros(9)

    a[:3] = m2*(x2-x1)/np.power(sqdist12, 1.5)
    a[3:6] = m1*(x1-x2)/np.power(sqdist12, 1.5)
    a[6:9] = m2*(x2-x3)/np.power(sqdist23, 1.5) + m1*(x1-x3)/np.power(sqdist13, 1.5)

    # Return the result
    return np.concatenate((v,a))

def gravity_acceleration_general(x, m):
    """

    Parameters:
        x (ndarray, length 6*n) xyz coordinates of 3 bodies (first 3*n entries), followed by their velocities (last 3*n entries)
        m (iterable, length n) masses of bodies.

    Returns:
        a (ndarray, length 6*n) derivative of x (velocities, followed by acceleration)
    """
    assert len(x)%6 == 0
    n = len(x) // 6

    # Extract velocities
    v = x[3*n:]

    # Extract positions
    x = [ x[3*i:3*(i+1)] for i in range(n) ]

    # Construct acceleration due to gravity
    a = np.concatenate(tuple([sum( m[j] * (x[j] - x[i])/np.power(np.sum((x[j]-x[i])**2), 1.5) for j in range(n) if j != i) for i in range(n)]))

    # Return the result
    return np.concatenate((v,a))

def simulate_mechanics_general(ic, t_span, t_eval, m):
    """
    Uses solve_ivp to simulate the time evolution of the system with given
    initial conditions under gravity.

    Parameters:
        ic (ndarray, (6*n,)): initial conditions
        t_span (tuple, 2): start and end of time interval
        t_eval (ndarray): evaluation times for solution
        m (iterable): list of masses

    Returns:
        sol (ndarray, (6*n, L)): an array where each column is the state of the
            system at the given time step
    """
    # Construct a function for use in solve_ivp
    f = lambda t, y: gravity_acceleration_general(y, m=m)

    # Numerically simulate
    sol = solve_ivp(fun=f, t_span=t_span, y0=ic, t_eval=t_eval)

    # Return the solution
    return sol.y

def pass_through(goal, init):
    v3 = np.copy(init[-3:-1])
    def to_minimize(v3):
        y0 = np.copy(init)
        y0[-3:-1] = v3
        sol = simulate_mechanics_general(y0, (t0, tf), t_eval=np.linspace(t0, tf, 1000), m = np.array([1, .09, .0001])*100**4)
        index = np.argmin(np.linalg.norm(sol[6:9, :].T - goal, axis=1, ord=2))
        sol = sol[:, index]
        return np.linalg.norm(goal - sol[6:9], ord=2)
    v = minimize(to_minimize, v3, tol=1e-10, options={'maxiter':500}).x
    init[-3:-1] = v
    return init

# Set up initial conditions and parameters
t0 = 0
tf = 5

init = np.array([-.09, 0, 0, # Position 1 planet
                 1, 0, 0, # Position 2 moon
                 .5, -.25, 0, # Position 3 spaceship
                 0, -.09, 0, # Velocity/Momentum 1
                 0, 1, 0, # Velocity/Momentum 2
                 2.5, 2, 0])*100 # Velocity 3 

init = pass_through(np.array([2, 4, 0])*100, init) 

# Solve the system
sol = simulate_mechanics_general(init, (t0, tf), t_eval=np.linspace(t0, tf, 1000), m = np.array([1, .09, .0001])*100**3)

bpy_conn = conn.Conn()

frames = list(range(1000))
scale = 0.1
pos_1 = np.transpose(sol[0:3,:])
pos_2 = np.transpose(sol[3:6,:])
pos_3 = np.transpose(sol[6:9,:])
vel_3 = np.transpose(sol[15:18,:])
positions = [pos_3_i-vel_3_i*.005 for pos_3_i,vel_3_i in zip(pos_3,vel_3)]

scene = Scene(bpy_conn)

planet = AnimatedObject(
        bpy_conn,
        pos_1,
        "uv_sphere",
        "planet",
        radius = 1/scale
    )
moon = AnimatedObject(
        bpy_conn,
        pos_2,
        "uv_sphere",
        "moon",
        radius = 0.09/scale
    )
ship = AnimatedObject(
        bpy_conn,
        pos_3,
        "uv_sphere",
        "ship",
        radius=0.001/scale
        
    )

scene.animate_camera(frames,pos=positions,track_object=ship)
bpy_conn.save_blend("examples/blend/slingshot.blend")