# Warehouse-Navigation-Application
An App that generate shortest paths for store clerks so they can grab goods from accessible locations in a timely manner.

## Description

This project involves implementing the Canny Edge Decoder in a SystemC-based SoC architecture. The goal is to demonstrate proficiency in system-level design using high-level modeling languages. The final deliverable will be a working implementation of the decoder with simulation and valuation results.

## Project Outcomes

The final deliverable of this project is a working implementation of the Canny Edge Decoder, with simulation and verification results that demonstrate its performance and accuracy. The implementation includes a pipeline architecture that allows for efficient processing of large images, and a memory management system that minimizes memory usage and maximizes throughput.

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
