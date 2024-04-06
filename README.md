# Warehouse-Navigation-Application
The Warehouse Navigation Application aims to streamline the process of picking goods from shelves in a warehouse by employing efficient pathfinding algorithms. This application targets both human workers and robots, ensuring that orders are fulfilled swiftly and accurately while minimizing travel time.

## Features
- ### Multiple access points enable
  Unlike traditional TSP problems, we assume that in the real world, goods on shelves may be blocked by neighboring shelves and thus can only be grabbed from aisles next to the shelves, which we      call access points. Our application enables users to find the shortest path under the constraint of access points.
- ### Optimized results
  Recognizing the complexity of the Traveling Salesman Problem (TSP), particularly in large warehouses with extensive order lists, our application employs three distinct algorithms (Branch and   Bound, Held–Karp, and Nearest Neighbor) simultaneously. This approach yields optimized results within predefined time constraints
- ### Specific Navigation
   Designed for ease of use, our application not only generates warehouse maps based on user input but also provides detailed routes with maps and instructions. This intuitive interface enhances   user experience and facilitates efficient navigation within the warehouse.
## How it Works



## Project Outcomes

The final deliverable of this project is a working implementation of the Canny Edge Decoder, with simulation and verification results that demonstrate its performance and accuracy. The implementation includes a pipeline architecture that allows for efficient processing of large images, and a memory management system that minimizes memory usage and maximizes throughput.

## Getting Started

## Code Attribution

This project includes code from the following sources:
<br>http://www.eng.usf.edu/cvprg/edge/edge_detection.html
Original Canny Edge Decoder implementation by Heath, M., Sarkar, S., Sanocki, T., and Bowyer, K., licensed under the USF license.

## Dependencies

Before installing and running this program, you will need to have the following dependencies installed:
* SystemC 2.3.1

You can download and install SystemC from the official website at http://www.accellera.org/downloads/standards/systemc. Once you have installed SystemC, make sure that the SYSTEMC_HOME environment variable is set to the installation directory.

This program has been tested and verified to work on the following operating systems:
* Ubuntu 20.04 LTS
* Windows 10


## Results

**Photo Result** 
* Original Photo
![orig](/Image/EngPlaza001.pgm.png)
* Canny Edge Result
![canny](/Image/EngPlaza001_edges.pgm.png)


**Throughput Optimization**
![canny](/Image/throughput_optimization.png)
