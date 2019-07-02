from pybde import BDESolver
from pybde import BooleanTimeSeries
from numpy import genfromtxt
import matplotlib.pyplot as plt

# Read in the experiment data from CSV - first column is a, second column is b, third column is time
# Data goes to t=118 hours.
experiment_data = genfromtxt('neurospora_data.csv', delimiter=',')

num_plots = 3

# Plot experiment data

plt.plot(experiment_data[:,2], experiment_data[:,0], 'b-', label="m", )
plt.plot(experiment_data[:,2], experiment_data[:,1], 'r-', label="ft")
plt.legend()
plt.xlabel("time (hours)")
plt.ylabel("Expression levels (AU)")
plt.title("Experiment data")
plt.show()

# Turn experiment data into Boolean time series
m_bts = \
    BooleanTimeSeries.relative_threshold(experiment_data[:,2], experiment_data[:,0], 0.3)
ft_bts = \
    BooleanTimeSeries.relative_threshold(experiment_data[:,2], experiment_data[:,1], 0.3)

# Add labels and plot styles to the switch points objects
ft_bts.label = "ft"
m_bts.label = "m"
ft_bts.style = "r-"
m_bts.style = "b-"

# Plot the experiment data as Boolean time series
BooleanTimeSeries.plot_many([m_bts, ft_bts])
plt.xlabel("Time (hours)")
plt.show()


# Now plot the experiment data Boolean time series with the original data

plt.plot(experiment_data[:,2], experiment_data[:,0], 'b-', label="m", )
m_bts.plot(scale=150)
plt.xlabel("time (hours)")
plt.ylabel("Expression levels (AU)")
plt.title("m")
plt.show()


plt.plot(experiment_data[:,2], experiment_data[:,1], 'r-', label="ft")
ft_bts.plot(scale=300)
plt.xlabel("time (hours)")
plt.ylabel("Expression levels (AU)")
plt.title("ft")
plt.show()

# We wish to use the first 24 hours as our history

hist_ft = ft_bts.cut(0, 24)
hist_m = m_bts.cut(0, 24)

# Plot the history
BooleanTimeSeries.plot_many([hist_m, hist_ft])
plt.xlabel("Time (hours)")
plt.legend()
plt.show()

# The model uses a forcing input for light

light_t = [0] + list(range(6,120,12))
light_y = []
for t in light_t:
    light_y.append(6 <= t % 24 < 18)
light_bts = BooleanTimeSeries(light_t, light_y, 118)
light_bts.label = "light"
light_bts.style = "-g"

# Plot light
light_bts.plot()
plt.show()

# Plot light and the histories
BooleanTimeSeries.plot_many([hist_m, hist_ft, light_bts])
plt.show()

# Define the model equations

def neurospora_eqns(z, forced_inputs):
    m = 0
    ft = 1
    light = 0
    tau1 = 0
    tau2 = 1
    tau3 = 2

    return [ (not z[tau2][ft]) or forced_inputs[tau3][light], z[tau1][m] ]

# Run the simulator

tau1 = 5.0752
tau2 = 6.0211
tau3 = 14.5586
delays = [tau1, tau2, tau3]

solver = BDESolver(neurospora_eqns, delays, [hist_m, hist_ft], [light_bts])
[m_output, ft_output] = solver.solve(118)

# Plot output of the simulation

plt.title("Simulation output")
BooleanTimeSeries.plot_many([m_output , ft_output, light_bts])
plt.xlabel("Time (hours)")
plt.legend()
plt.show()

# Plot outputs over the original experiment data

plt.plot(experiment_data[:,2], experiment_data[:,0], 'b-', label="m", )
m_output.plot(scale=150)
plt.xlabel("time (hours)")
plt.ylabel("Expression levels (AU)")
plt.title("m")
plt.show()


plt.plot(experiment_data[:,2], experiment_data[:,1], 'r-', label="ft")
ft_output.plot(scale=300)
plt.xlabel("time (hours)")
plt.ylabel("Expression levels (AU)")
plt.title("ft")
plt.show()

# Plot simulated data alongside thresholded data

m_output.label = "m sim"
m_output.style = 'c-'
BooleanTimeSeries.plot_many([m_bts, m_output])
plt.xlabel("time (hours)")
plt.title("m")
plt.legend()
plt.show()

ft_output.label = "ft sim"
ft_output.style = 'c-'
BooleanTimeSeries.plot_many([ft_bts, ft_output])
plt.xlabel("time (hours)")
plt.title("ft")
plt.legend()
plt.show()

# Calculate Hamming distances

print("Hamming of m : {:.4f}".format(m_bts.hamming_distance(m_output)))
print("Hamming of ft : {:.4f}".format(ft_bts.hamming_distance(ft_output)))

print("Hamming of m as %age of simulated time: {:.2f}%".format(
    m_bts.hamming_distance(m_output)/0.96))
print("Hamming of ft as %age of simulated time : {:.2f}%".format(
    ft_bts.hamming_distance(ft_output)/0.96))
