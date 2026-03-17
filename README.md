This project builds a smart ambulance decision and routing system for Kolkata.
It uses two artificial intelligence search algorithms:

AO* → decides which hospital is the best choice for the patient

A* → finds the fastest or safest road route for the ambulance

The system uses real road network data from OpenStreetMap and visualizes the route on an interactive map.

Problem

During emergencies, an ambulance must quickly decide:

Which hospital should the patient go to?

What is the fastest or safest route to reach the hospital?

A normal navigation system only finds the shortest path.
But emergency systems must also consider traffic, distance, and hospital availability.

A*
Step 1
Load the Kolkata road network from OpenStreetMap.

Step 2
Convert roads into a graph structure.

Nodes → road intersections

Edges → roads

Step 3
Choose a starting location for the ambulance.

Example:

Park Street, Kolkata

Step 4
Choose a hospital destination.

Example:

AMRI Hospital

Step 5
Apply the A* algorithm to compute the optimal route.

Step 6
Calculate:

route distance

estimated travel time

Step 7
Visualize the route using an interactive map.

AO*
Step 1
Load the Kolkata road network from OpenStreetMap.

Step 2
Use AO* to compare hospital options.

Step 3
Select the best hospital based on total cost.

Step 4
Run A* to compute routes to hospitals.

Step 5
Calculate distance and travel time.

Step 6
Display routes and results on an interactive map.
