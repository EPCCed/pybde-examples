from pybde import BDESolver, BooleanTimeSeries
import matplotlib.pyplot as plt


def my_model(z):
    return [not z[0][0]]


def main():
    history = BooleanTimeSeries([0], [True], 1)
    delay_parameters = [1]
    end_time = 5

    my_bde_solver = BDESolver(my_model, delay_parameters, [history])
    my_bde_solver.solve(end_time)

    plt.figure(figsize=(5, 2))
    my_bde_solver.plot_result()
    plt.savefig("C:\\Users\\ahume\\Documents\\MultiObjectiveOptimisation\\BDE\\wiki\\pybde.wiki\\images\\v1.0\\single_variable_output.png")


if __name__ == "__main__":
    main()
