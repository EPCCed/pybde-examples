from pybde import BDESolver, BooleanTimeSeries

def my_two_variable_model(z):
    x1 = 0
    x2 = 1
    tau1 = 0
    tau2 = 1
    return [z[tau1][x2], not z[tau2][x1]]


def main():
    x1_history = BooleanTimeSeries([0, 1.5], [True, False], 2)
    x2_history = BooleanTimeSeries([0, 1], [True, False], 2)

    x1_history.label = "x1"
    x1_history.style = "-r"
    x2_history.label = "x2"
    x2_history.style = "-b"

    delay_parameters = [1, 0.5]

    end_time = 6

    my_bde_solver = BDESolver(my_two_variable_model, delay_parameters,[x1_history, x2_history])
    my_bde_solver.solve(end_time)
    my_bde_solver.show_result()

    my_bde_solver.print_result()

if __name__ == "__main__":
    main()
