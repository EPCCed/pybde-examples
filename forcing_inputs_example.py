from pybde import BDESolver, BooleanTimeSeries


def my_forcing_input_model(z, forcing_inputs):
    tau = 0
    x1 = 0
    return [ forcing_inputs[tau][x1] ]


def main():
    x2_history = BooleanTimeSeries([0], [True], 0.5)
    x2_history.label = 'x2'
    x2_history.style = '-r'

    x1_input = BooleanTimeSeries([0, 0.5, 1, 1.5, 2, 2.5, 3], [False], 3)
    x1_input.label = 'x1'
    x1_input.style = '-b'

    delay_parameters = [0.3]
    end_time = 3

    my_bde_solver = \
        BDESolver(my_forcing_input_model, delay_parameters, [x2_history], [x1_input])
    my_bde_solver.solve(end_time)

    my_bde_solver.show_result()


if __name__ == "__main__":
    main()