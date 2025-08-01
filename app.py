import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="IQSSA - Queuing Simulator", layout="centered")

# App Title
st.title("📊 IQSSA – Queuing System Simulator and Analyzer")
st.markdown("""
Welcome to **IQSSA**, an interactive tool to simulate and evaluate the performance of a basic queuing system (**M/M/1** model).  
Use the sliders below to configure your system parameters, and click **Run Simulation** to see real-time results!
""")

# Sidebar - Parameters
st.sidebar.header("🔧 Configure Simulation")
arrival_rate = st.sidebar.slider("Arrival Rate (λ)", 0.1, 10.0, 2.0, step=0.1)
service_rate = st.sidebar.slider("Service Rate (μ)", 0.1, 10.0, 3.0, step=0.1)
num_customers = st.sidebar.slider("Number of Customers", 100, 2000, 1000, step=100)
random_seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=9999, value=42)

# Run simulation button
if st.button("▶️ Run Simulation"):

    # Set random seed for reproducibility
    np.random.seed(random_seed)

    # Generate inter-arrival and service times
    inter_arrival_times = np.random.exponential(1/arrival_rate, num_customers)
    service_times = np.random.exponential(1/service_rate, num_customers)

    # Calculate arrival times
    arrival_times = np.cumsum(inter_arrival_times)

    # Initialize tracking arrays
    start_times = np.zeros(num_customers)
    end_times = np.zeros(num_customers)
    wait_times = np.zeros(num_customers)
    turnaround_times = np.zeros(num_customers)

    # Simulate queue
    for i in range(1, num_customers):
        start_times[i] = max(arrival_times[i], end_times[i - 1])
        end_times[i] = start_times[i] + service_times[i]
        wait_times[i] = start_times[i] - arrival_times[i]
        turnaround_times[i] = end_times[i] - arrival_times[i]

    # Performance Metrics
    avg_wait = np.mean(wait_times)
    avg_turnaround = np.mean(turnaround_times)
    utilization = np.sum(service_times) / end_times[-1]
    throughput = num_customers / end_times[-1]

    # Display metrics
    st.subheader("📈 Performance Metrics")
    st.write(f"**Average Waiting Time:** {avg_wait:.4f} units")
    st.write(f"**Average Turnaround Time:** {avg_turnaround:.4f} units")
    st.write(f"**System Utilization (ρ):** {utilization:.4f}")
    st.write(f"**Throughput:** {throughput:.4f} jobs/unit time")

    # Gantt Chart
    st.subheader("📊 Gantt Chart (First 100 Customers)")
    fig, ax = plt.subplots(figsize=(10, 4))
    for i in range(min(100, num_customers)):
        ax.plot([start_times[i], end_times[i]], [i, i], color='blue')
        ax.scatter(arrival_times[i], i, color='red', marker='|')  # arrival
    ax.set_xlabel("Time")
    ax.set_ylabel("Customer Index")
    ax.set_title("Service Timeline (Blue = Service, Red = Arrival)")
    ax.grid(True)
    st.pyplot(fig)

    # Histogram of Waiting Times
    st.subheader("⏱️ Histogram of Waiting Times")
    fig2, ax2 = plt.subplots()
    ax2.hist(wait_times, bins=30, color='orange', edgecolor='black')
    ax2.set_xlabel("Waiting Time")
    ax2.set_ylabel("Number of Customers")
    ax2.set_title("Distribution of Waiting Times")
    st.pyplot(fig2)

else:
    st.info("Adjust parameters and click **Run Simulation** to begin.")
