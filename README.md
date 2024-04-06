# Warehouse-Navigation-Application
The Warehouse Navigation Application aims to streamline the process of picking goods from shelves in a warehouse by employing efficient pathfinding algorithms. This application targets both human workers and robots, ensuring that orders are fulfilled swiftly and accurately while minimizing travel time.

## Features
- ### Multiple access points enable
  In real-world scenarios, goods on shelves may be obstructed by neighboring shelves, allowing access only from adjacent aisles. Our application accommodates this constraint, enabling users to find the shortest path considering access points.
    
  <img src="https://github.com/BearLand0713/Warehouse-Navigation-Application/blob/d0b8e8611431a0cda405a87c4e60a65209d01b68/image/MAP.png" width=60%>
    
  
- ### Optimized results
  Recognizing the complexity of the Traveling Salesman Problem (TSP), particularly in large warehouses with extensive order lists, our application employs three distinct algorithms (Branch and   Bound, Held–Karp, and Nearest Neighbor) simultaneously. This approach yields optimized results within predefined time constraints.
  ![Algos]
    
  
- ### Specific Navigation
   Designed for ease of use, our application not only generates warehouse maps based on user input but also provides detailed routes with maps and instructions. This intuitive interface enhances   user experience and facilitates efficient navigation within the warehouse.
    
  <img src="https://github.com/BearLand0713/Warehouse-Navigation-Application/blob/d0b8e8611431a0cda405a87c4e60a65209d01b68/image/GUI.png" width=60%>
    
  
## Getting Started
  - ### Install and compile
    Download the source code folder from this repository, and transfer the "Warehouse_Navigation_Application_V5.py" file into an execute file with [py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) or run it with Python compiler.
  - ### Data load and setting

  <img src="https://github.com/BearLand0713/Warehouse-Navigation-Application/blob/a994421493ca0ed1d707c2cb93c22787ea2174f3/image/Menu%20panel.png" width=60%>
  
    In the Menu panel, you can load the product info and order list from a text file with the following format.
    (Samples of both are in the source code folder)
    __product info__
    Product_Id    x-axis of the shelf     y-axis of the shelf
    1	            2	                      0
    45	          10                      14
    .             .                       .
    .             .                       .
    74	          10.2	                  8
      
    __order list__
    (Each row is a single order)
    order1:  108335, 391825, 340367, 286457, 661741
    order2:  219130, 365285, 364695
    .
    .
    .
    order99: 422465, 379019, 98888

    Also, you can set the warehouse size, start position, end position, etc. in the settings panel.
    After all settings are ready, come back to the menu panel and "Go Get Products"!




