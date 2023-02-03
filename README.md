# Stabilizing Inverted Pendulum Using System Identification and Reinforcement Learning
<img src="inverted_pendulum.jpg" alt="Block diagram of circuit" title="" width=50%>

This project aims to solve two problems. The problem with traditional control system that fails to adapt as the system changes. The problem with reinforcement learning that needs training on a real model for a long time that might not be possible on some cases. We try to balance inverted pendulum virtually by using the system equation given by system identification and directly balance the real model.

The circuit diagram is
<img src="block_circuit.jpg" alt="Block diagram of circuit" title="">
The process is shown in the diagram
<img src="flowchart.jpg" alt="process" title="Optional title">
The ARX equation describing the actual system
<img src="system_identification.jpg" alt="system equation" title="Optional title">

The cost function used to train the system
<img src="cost_function.jpg" alt="cost_eqn" title="" width=60%>

The softwares used are
1. OpenAI Gym
2. Arduino IDE
3. System Identification Toolbox in MatLab
4. Python and Tensorflow

Proximal Policy Optimization(PPO) algorithm was used to train the system.

The final testing concluded the system to be balanced in the range of 10 degrees.


