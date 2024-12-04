# solids-vis-1

## How to use package in development mode
1. create a virtual environment for this package if you do not already have one and activate it

    (windows)
    python -m venv .venv
    # run this step to make sure you can activate the virtual environment
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
    .venv\Scripts\activate.ps1 

    (mac/linux)
    python3 -m venv .venv
    . .\.venv\bin\activate (mac/linux)

2. link source code to your virtual environment or global environment

    pip install -e ./src/sv

3. use the package like you would any other package. any changes you make to the source code will be reflected. for example in a test file

    # add sphere test
    import sv

    if __name__=="__main__":
        bpy_conn = sv.conn.Conn()
        scene = sv.Scene.Scene(bpy_conn)
        obj = sv.AnimatedObject.AnimatedObject(
            bpy_conn,
            [[0,0,0]],
            "uv_sphere",
            "test_sphere",
        )

        scene.render("added sphere","tests", "JPEG")

## Short description
A python program that interfaces with blender to produce visualizations related to solid bodies and their motions or deformations.


## About

This project would develop a program in python as an interface with blender, a general-purpose 3D modeling tool. The program would produce visualizations related to solid bodies and their motions or deformations. In future versions the software could take advantage of colors or materials in the 3D modeling tool to repreesnt temperature, stress, or other states on the solid along with animating deformations and motions. The developed program would take output from well known, standard simulation tools or custom simulations, convert it to a standard input for the software, and create custom visualizations for it.

As an example case, simulations from this repository will be visualized in our software.

[example simulations](https://github.com/samco7/optimal-spacecraft-control)

Here is an example hand-made animation of what we plan to create programatically.

[video](https://youtu.be/4oE9WtqQrDE)

## Usage

This module is best used if blender is compiled as a python module `bpy`, but we also plan to make it work with standard blender installations.


