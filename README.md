
1
  
ECE 479/579 
Spring 2022 
 
 
Semester Project 
 
For the GUI: KIVY: https://kivy.org/doc/stable/gettingstarted/installation.html#install-pip
 
Due: April 27 (11pm), 2022 via D2L 
Documents to be submitted 
1. Brief summary of your design and instructions on how to run your system.  
2. Requirements document 
3. UML diagram of the system architecture 
4. Code (in python, matlab, or c/c++) in a zip file.  
 
 This semester project is intended to reinforce the theoretical concepts covered in class. It 
will provide you with flexibility and freedom to be creative and implement concepts in ways 
which the teams feel are most effective, and at the same time valid.  
   
The following problem will serve as the basis for it.  
  
Problem:   
 
Consider a task of designing an integrated, AI-based system for supporting the operation of 
an imaginary bottled water distribution company. In the description below, we focus only 
on some selected aspects of the system's operation but you are free to introduce your own 
constrains and design parameters as long the operational principles are consistent with 
the problem statement. (For instance, assume the existence of a dispatch center.) 
 
In each customer's home, the company installs the ThirstAId system which has:  
• a water column that consists of a water stand --- the water stand is either a regular 
stand or a chilled water stand --- and a bottle that could be a clear glass or a plastic 
bottle with a choice of two capacities (4 gallons or 6 gallons) for either type of bottle,  
• a robot (bottle changer) that can be either a mobile robot or a fixed location robot,   
• a vertical full-bottle shelf in which up to three bottles can be stacked up,  
• a vertical empty-bottle shelf in which up to two bottles can be stacked up, 
• a management unit that monitors and controls the system,  
• a transceiver that connects the system to the company's monitoring station,  
• system software.  
 
Overall Goal 
 
Design and implement a software-based model and simulate the operation of the system 
along the following steps. 
 
Step 0 
 
Based on the description below (please read to the end) define a set of requirements and 
constrains for this system (the minimal requirements are given in this description but you 
are free to introduce your own).  
 
Step 1  
 
So far, the company has five customers whose codes are A, B, C, D, E. To help the dispatcher 
optimize the distribution routes,  ThirstAID will be using the TSP and search for an optimal 
route based on distances between the customers.   
 
Task: 
  implement and test a module which allows you to enter distances between the 
customers and generates the optimal path using one of the search algorithms you have 
studied.   
  
Step 2 
 
Task 
  develop the system architecture using the UML notation.  This architecture must have 
attributes that characterize the components’ properties.  
 
Step 3 
 
One of the components of ThirstAId is an AI Production System (AIPS) that has the following 
specifications:  
 
  The AIPS monitors the system by checking state variables. It takes certain actions.   
  
   The AIPS issues the Replenish command if there is only one bottle left on the full-bottle 
shelf and the water level in the bottle on the water stand drops below 1/4 gallon.   
   The AIPS controls the water temperature by issuing on/off commands which are sent 
to the cooler (only if the stand is a chilled water stand). The proper operating temperature is to 
be 42F +/- 2F.             
   The AIPS issues the Replace Bottle command if the bottle on the water stand is empty.  
 
   The AIPS issues the Alarm command to the dispatch center if it detects a leak.   
  
Replenish command: results in two filled bottles being dropped off (by a technician) at the full-
bottle shelf. These bottles are placed on the floor next to this shelf. Empty bottles are collected 
(by the technician) from the empty-bottle shelf. At the same time, the robot (bottle changer) 
is directed to re-stack the full-bottle shelf --- all three full bottles must be in the vertical shelf, 
stacked on top of one another. 
