from django.shortcuts import render
from io import BytesIO
import numpy as np
import math
import base64
import matplotlib.pyplot as plt


def plotter(request):
    
    # name = "Veekode"
    if request.method == "POST":
        eqn = request.POST["eqn"]
        range_x = request.POST["range_1"].split()
        range_t = request.POST["range_2"].split()
        n_points = request.POST["n_points"]
        
        # range_1 = range(int(range_1[0]), int(range_1[1]))
        # range_2 = range(int(range_2[0]), int(range_2[1]))

        range_x = np.linspace(int(range_x[0]), int(range_x[1]), int(n_points))
        range_t = np.linspace(int(range_t[0]), int(range_t[1]), int(n_points))
        
        eqn = "math.sin(x - t)"
        # print(type(eqn))
        y = [ eval(eqn) for x, t in zip(range_x, range_t) ]
        
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot the line
        ax.plot(range_x, y, "o:r", label="f(x, t)", linewidth=2)

        # Set labels and title
        ax.set_xlabel("x(m)")
        ax.set_ylabel("f(x, t)")
        ax.set_title(f"y = {eqn}")

        # Add legend
        ax.legend()

        # Save the plot as an image
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        image_src = f"data:image/png;base64,{image_base64}"

        return render(request, "plotter_app/index.html", {"image_src": image_src})
    return render(request, "plotter_app/index.html")