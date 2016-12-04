from util import binning, sparsematrix

class Mandelbrot:
    def __init__(self, x_bounds = (-2, 2), y_bounds = (-2, 2),
                 x_steps = 256, y_steps = 256):
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.x_steps = x_steps
        self.y_steps = y_steps

        self.matrix = sparsematrix.SparseMatrix(self.y_steps, self.x_steps)

    def calculate_point(self, point: complex, iterations):
        current_point = complex(0, 0)

        # The range limit is iterations + 1 so that if a point does not
        # excape, the function returns iteration == iterations
        for iteration in range(iterations + 1):
            current_point = pow(current_point, 2) + point
            if abs(current_point) > 2:
                break

        return iteration

    def calculate(self, iterations):
        for x_step in range(self.x_steps):
            for y_step in range(self.y_steps):
                x = binning.center_for_bin(*self.x_bounds, x_step, self.x_steps)
                y = binning.center_for_bin(*self.y_bounds, y_step, self.y_steps)
                point = complex(x,y)
                value =  self.calculate_point(point, iterations)
                self.matrix[y_step, x_step] = value
