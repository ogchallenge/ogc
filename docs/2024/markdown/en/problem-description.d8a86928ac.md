# Problem Description and Ranking Method

*Update history:*

- *2024/07/15 - Added objective function comparison criteria for ranking calculation*
- *2024/06/25 - Added leaderboard update schedule explanation*
- *2024/06/21 - Added problem JSON format description*
- *2024/05/08 - Added algorithm source code plagiarism check information*

## 0. Terminology

- Rider
    - A person who picks up food from a restaurant and delivers it to the ordering customer.
- Pickup
    - Receiving a customer's order from a restaurant.
- Delivery
    - Delivering the customer's order received from the restaurant to the requested location.
- Ready time
    - Time when a customer's order is ready = Order time (OT) + Preparation time at restaurant (RT)
- Deadline (DT)
    - The deadline by which the order must be delivered. The rider must arrive at the customer and complete the delivery before this time.
- Bundle delivery
    - Delivering multiple orders together by a single rider.

## 1. Problem Situation

### 1.1. Orders

Have you ordered food delivery? When you order food through a delivery app, the following order information is generated.

Having one rider deliver one order is not cost-efficient. 
Delivery companies want to reduce the number of required riders by bundling multiple orders that occur at similar times, thereby reducing delivery costs.

You are given a list of orders that occurred in a specific area.

However, to bundle orders for delivery, various constraints must be considered. 
Let's first consider the riders who will fulfill the orders!

# Constraints

### 1.2. Riders

There are three types of riders.

![Walk Rider|100](delivery-courier.png) 
![Bike Rider|100](delivery-bike.png)
![Car Rider|100](delivery-car.png)




Each rider type has different **capacity**, **speed**, **service time**, and **cost**. For example:

- Walk riders are the slowest but the delivery company pays the lowest cost.
- Bike riders are the fastest but cost more,
- Cars have larger delivery capacity compared to other riders but require more time for parking (i.e., service time).

The cost paid to riders is determined as follows:

**Delivery Cost**

> **Bundle delivery cost = Fixed cost by rider type + Variable cost by rider type (cost per distance)**


Fixed and variable costs are given differently for each rider type.

> **Note!** The fixed cost for a rider type is charged only once, regardless of how many orders are bundled.


> **Note!** Variable cost is proportional to **distance**! Although travel time may differ because each rider type has different speeds, the variable cost is calculated based on distance for the same distance traveled.


From the customers' perspective, the delivery fee is predetermined when ordering, and as long as delivery occurs before the deadline, they don't care which type of rider delivers. However, the delivery company's costs vary by rider type.  
But it's difficult to use only the cheapest riders. There's a limit to the number of available riders. 
What if we bundle multiple orders for delivery together to reduce the number of required riders? Costs will naturally decrease! However, there are considerations for performing bundle deliveries.

### 1.3. Bundle Delivery Constraints

To bundle orders for delivery, the following constraints must be satisfied:


💡 **Constraint 1.** *Sum of bundled order volumes must not exceed the rider's capacity: **Capacity Constraint***


💡 **Constraint 2.** *All orders must be delivered before their deadline: **Time Constraint***


💡 **Constraint 3.** *When bundling deliveries, all pickups must be completed before deliveries: **Visit Order Constraint***



Bundles created satisfying the above conditions are assigned to riders. 
Therefore, the following condition regarding available riders must additionally be satisfied:

💡 **Constraint 4.** *All orders must be delivered by riders without exception: **Order Fulfillment Constraint***

💡 **Constraint 5.** *Maximum 1 bundle delivery is assigned per rider: **Rider Assignment Constraint***


## 2. Example

Let's consider the case where two orders are given as follows:

![Order Example](example-orders-diagram.png)

In this example with two orders, there are two pickup restaurants and two delivery points. 
The distances between pickup locations and delivery locations are as follows:

![Arc numbers represent travel distance](distance-network-diagram.png)


To bundle the two orders, two constraints must be satisfied.

**Constraint 1. Capacity Constraint**

For the capacity constraint, since the sum of the two orders' volumes is 90 (=40+50), walk riders cannot make the delivery. 
Both bike and car riders satisfy the capacity constraint! 
Let's now check if the time constraint is satisfied.

**Constraint 2. Time Constraint**

To satisfy the time constraint, the rider must:

1. When picking up, depart for the next location after the ready time
2. When delivering, arrive before deadline - service time

Let's consider the case of delivering in the following order using a bike:

![Arc numbers represent bike travel time](bike-time-network-diagram.png)


Explaining in detail according to the delivery order:

1. Order 1 pickup location: Complete pickup at time 15 and depart for the next location. 
Here, 15 is order 1's ready time, and we assume this rider arrived sufficiently early and has already completed access.


> 💡 **At the first location of a bundle delivery, service time is not considered and departure is possible after ready time!**



2. Order 2 pickup location: Since the bike's speed is 2, it takes 10 time units to travel from order 1's pickup location to order 2's pickup location. That is, arrive at time 25, and with 3 service time units needed, reach the restaurant at time 28. However, since order 2's ready time is 30 (= order occurrence time 10 + order preparation time 20), depart after 30. (2 time units of waiting occur)


> 💡 **Ready time is calculated as order occurrence time + order preparation time!**


3. Order 1 delivery location: Depart at time 30, arrive at order 1's delivery location at 70, and delivery occurs at 73 after 3 service time units. This is less than or equal to order 1's deadline of 80, so order 1 delivery is successful!
4. Order 2 delivery location: Depart at 73, arrive at 92, and delivery is possible at 95 after adding 3 service time units, which is less than or equal to order 2's delivery deadline of 95, so order 2 delivery is successful!

**Constraint 3. Visit Order Constraint**

Also, we can see that the only way to bundle the two orders in the above example is when a bike rider delivers in the above visit order. Looking closely at the visit order in the above example, all two orders' pickup locations are visited before performing the two deliveries. 
In other words, from order 1's pickup location, order 1 or order 2's delivery location cannot be visited directly.

> **Note! After completing all pickups, delivery locations can be visited.**
> 

**Constraint 4. Order Fulfillment Constraint**

Since both order 1 and order 2 have been delivered, we can see that the order fulfillment constraint is satisfied.

**In other words, to create one bundle delivery, the following must be determined:**

1. **Rider type (one of walk, bike, car)**
2. **Set of orders to bundle satisfying capacity constraint**
3. **Visit order complying with time constraint**

### Another Example

Let's look at a different example. 10 orders are given (order number 1 to order number 10). 
After checking the constraints, assume that each pair of two orders can be bundled with bike or car delivery.

- Orders 1 & 2: Bike or car bundle delivery possible
- Orders 3 & 4: Bike or car bundle delivery possible
- Orders 5 & 6: Bike or car bundle delivery possible
- Orders 7 & 8: Bike or car bundle delivery possible
- Orders 9 & 10: Bike or car bundle delivery possible

And assume 3 bike riders and 10 car riders are available.

If the visit order is the same for bike or car for all bundle deliveries, the travel distance is the same for each bundle delivery. That is, the cost of each bundle delivery is determined by the fixed and variable costs of bike and car. 
To simplify the example, let's assume bike is cheaper in all bundle delivery cases. 
If we assign all 5 bundle deliveries to bike riders, the lowest cost would occur!

**Constraint 5. Rider Assignment Constraint**
However, to satisfy **Constraint 5**, at most 3 of the five bundle deliveries can be assigned to bike riders. The remaining 2 bundle deliveries must be assigned to car riders.
In other words, if a bundle delivery can use multiple rider types, which type of rider to assign to must consider the number of available riders. And a rider cannot perform one bundle delivery and then perform another bundle delivery.

## 3. Objective Function

Once the rider type and visit order are determined for each bundle delivery, the cost can be calculated through distance. Adding up the costs of all bundle deliveries gives the total cost, and dividing it by the number of orders gives the average delivery cost.

> Objective function = Average delivery cost = Total delivery cost / Total number of orders


## 4. Problem Data Definition

The following data is provided for one problem:

- List of `K` orders
- Rider types and characteristics
- Distance matrix

Problems are provided in JSON format with the following items:

```json
{
 "name": "TEST_K50_1",
 "K": 50,
 "RIDERS": [["BIKE", 5.291005291005291, 100, 80, 2200, 120, 5],
            ["WALK", 1.3227513227513228, 70, 50, 2200, 120, 10],
            ["CAR", 4.2328042328042335, 200, 60, 2200, 150, 50]],
 "ORDERS": [[0, 7, 37.49493567, 127.03071274, 37.501853, 127.037541, 900, 40,
             1980],
            [1, 53, 37.49246391, 127.04021194, 37.491006, 127.023683, 1200, 42,
             2489],
            [2, 95, 37.5030462, 127.05048848, 37.503553, 127.053148, 600, 28,
             1525],
            [3, 142, 37.50457363, 127.04140593, 37.507767, 127.025053, 900, 19,
             2284],
            [4, 221, 37.48549201, 127.01352012, 37.48385, 127.015403, 1800, 40,
             2853],
            [5, 391, 37.50960069, 127.0335454, 37.494084, 127.028143, 900, 20,
             2634],
            [6, 597, 37.5001711, 127.0522837, 37.499698, 127.069605, 900, 47,
            ...
            
            
 "DIST": [[0, 1236, 2753, 2001, 2586, 2312, 2789, 1809, 3978, 2126, 1551, 2312,
           3807, 2483, 1067, 1453, 4188, 1479, 2364, 10027, 3689, 1859, 7330,
           3495, 3046, 460, 3150, 1552, 2548, 3351, 5412, 3020, 2534, 3122,
           2839, 1484, 1722, 3092, 3046, 2534, 2736, 2685, 522, 3483, 4065,
           3340, 3631, 2504, 1739, 2016, 1369, 1063, 3082, 2119, 2563, 344,
           4866, 1392, 3266, 1390, 1099, 2370, 3919, 537, 4834, 2318, 5043,
           2569, 1205, 9609, 2283, 2153, 5245, 5640, 3381, 1836, 2976, 1035,
           766, 2211, 3830, 3174, 4051, 3838, 4587, 1753, 1771, 2588, 2244,
           2176, 213, 3015, 2257, 2138, 3673, 3806, 1023, 3278, 4554, 1559],
          [1236, 0, 2082, 1893, 3475, 2795, 1916, 2916, 2933, 2903, 1802, 2795,
           4676, 2654, 1264, 1693, 3627, 2660, 3542, 8791, 2502, 1572, 8409,
           4673, 1999, 1577, 4307, 445, 2105, 4261, 5164, 4021, 2884, 2078,
           4008, 1651, 1716, 3607, 1999, 2884, 1900, 1795, 1174, 3641, 5288,
           2621, 2822, 3446, 2725, 2872, 1500, 2056, 2355, 3033, 3349, 1514,
           3805, 683, 2743, 1865, 1317, 3032, 4883, 1487, 4664, 2814, 4034,
           3662, 954, 8375, 1053, 2744, 6362, 6238, 2967, 2902, 4175, 225, 954,
           1961, 3661, 3880, 3910, 3844, 5370, 2860, 2826, 2991, 1009, 3203,
           1024, 2295, 1798, 2543, 4908, 4641, 2157, 3803, 5788, 2314],
           ...
  }
```

- `name`: Problem name
- `K`: Number of orders in the problem
- `RIDERS`: Rider information e.g. `["BIKE", 5.291005291005291, 100, 80, 2200, 120, 5]`
    - Type: `BIKE`, `WALK`, or `CAR`  → `"BIKE"`
    - Speed: distance(m)/time(sec) unit → `5.291005291005291`
    - Capacity → `100`
    - Variable cost (per 100m)  → `80`
    - Fixed cost → `2200`
    - Service time(sec) → `120`
    - Rider availability → `5`
    
    > **Note!** Car riders are always given availability equal to the number of orders. That is, delivering all orders one by one with cars without bundling is always possible! Of course, it's not good cost-wise!
    > 
- `ORDERS`: Order information e.g. `[0, 7, 37.49493567, 127.03071274, 37.501853, 127.037541, 900, 40, 1980]`
    - Order ID → `0`
    - Order occurrence time(sec)  → `7`
    - Pickup location latitude coordinate  → `37.49493567`
    - Pickup location longitude coordinate → `127.03071274`
    - Delivery location latitude coordinate → `37.501853`
    - Delivery location longitude coordinate → `127.037541`
    - Order preparation time(sec): *Adding cooking preparation time to order occurrence time gives pickup ready time* → `900`
    - Order volume → `40`
    - Delivery deadline(sec) → `1980`
- `DIST`: Distance matrix
    - `2K * 2K` matrix
    - In meters (rounded to integer)
    - E.g.) Distance between order `i`'s pickup location and order `j`'s pickup location = `DIST[i,j]`
    - E.g.) Distance between order `i`'s pickup location and order `j`'s delivery location = `DIST[i,j+K]`
    - E.g.) Distance between order `i`'s delivery location and order `j`'s delivery location = `DIST[i+K,j+K]`
    
    > **Note!** Travel time is not provided separately and is obtained using rider speed and distance.
    Use integer value rounded in seconds! Service time can be added to travel time at this time.
    
    Python travel time conversion example) 
    `rider.T = np.round(*dist_mat*/rider.speed + rider.service_time)`
    > 

## 5. Algorithm Solution

The algorithm must return a solution for the given problem data as follows:

- The algorithm returns a list of `[rider type, restaurant visit order, customer visit order]` for the given problem
- Visit order is defined by order of order IDs like `[1,3,2]`
- E.g.) `["BIKE", [1,3,2], [2,3,1]]`
    - Meaning: Bundle orders 1,2,3 and assign to a bike rider, visit pickup locations in order 1,3,2 and visit delivery locations in order 2,3,1
    - Bike: P1 → P3 → P2 → D2 → D3 → D1

Objective function and constraint satisfaction are performed by the scoring system. 
That is, the solution submitted by the participating team must satisfy **Constraints 1, 2, 3** for each bundle delivery, and all bundle deliveries must satisfy **Constraints 4, 5**.

## 6. Algorithm Submission and Evaluation

Participating teams write algorithms for problems given per stage (preliminary, main, final) (public problems). When algorithm code is submitted to the competition system, it is evaluated by running the submitted algorithm on hidden problems. Algorithm evaluation server specifications are as follows:

- AWS EC2 instance (c5.2xlarge)
- 8 Core, 16 GB memory, 32GB storage
- OS: Ubuntu 22.04 LTS

Algorithms are given a time limit. For example, the preliminary round has a time limit of 1 minute per problem, and the main and final rounds will be given specific time limits when they start.


> 💡 **Preliminary algorithm time limit is 1 minute per problem!**


Since participating teams' PC specifications may differ from the evaluation server's specifications, participating teams' algorithms must check elapsed time during algorithm execution and not exceed the time limit.

Also, algorithms submitted by participating teams have the following constraints:

- Cannot access external internet during algorithm execution
- Can use up to 4 CPU cores (~ 400% CPU usage)

Algorithms that violate the above constraints may be disqualified.

> 💡 **Algorithm external internet usage and number of CPU cores are enforced through `firejail` and `cpulimit` when running algorithms on the evaluation server. Participants' algorithms must not conflict with these two programs**


Participating teams can submit algorithms once per day. The daily basis is from 0:00 AM to 11:59 PM Korea Standard Time. That is, based on the submission moment's date, a maximum of one submission is possible on the same date.

> 💡 **Algorithm submission is possible at most once per day!**


Submitted algorithms are executed on hidden problems on the evaluation server, and results are collected at a designated time (exact time to be announced later). Collected results are reflected in the leaderboard on the competition homepage.

> 💡 **Leaderboard is updated once per day at a designated time!**

All evaluations are based on the most recently submitted algorithm among those submitted by the participating team.

> 💡 **The most recently submitted algorithm as of evaluation time is the basis for all evaluations!**

In other words, right before the stage end date, be sure to resubmit your best algorithm! Otherwise, ranking will be determined based on the last submitted algorithm.

Hidden evaluation problems consist of problems with similar characteristics to the public problems. The number of evaluation problems varies by stage. For example, assume 5 teams submitted algorithms and there are 3 hidden evaluation problems when the results of solving the hidden problems are as follows:

- `TEAM00`
    - `prob1: obj=60, feasible`
    - `prob2: obj=121, feasible`
    - `prob3: obj=82, feasible`
- `TEAM01`
    - `prob1: obj=104, infeasible`
    - `prob2: obj=223, feasible`
    - `prob3: obj=95, feasible`
- `TEAM02`
    - `prob1: obj=141, feasible`
    - `prob2: obj=125, feasible`
    - `prob3: obj=102, feasible`
- `TEAM03`
    - `prob1: obj=80, feasible`
    - `prob2: obj=136, feasible`
    - `prob3: obj=129, feasible`
- `TEAM04`
    - `prob1: obj=183, feasible`
    - `prob2: obj=210, feasible`
    - `prob3: obj=54, feasible`

The above results are from the evaluation system solving the submitted algorithms on hidden problems. Infeasibility is also judged per problem. Then for problem $p$, the following value can be calculated:

$$
nb_p = |\{\text{teams that found a better objective function for problem $p$}\}|
$$

That is, $nb_p$ has a smaller value for algorithms that find better solutions for problem $p$. Also at this time, if the found solution is infeasible or a crash occurs during algorithm execution, it is treated as the worst objective function.

With the calculated $nb_p$ value, the score (point) for each problem is calculated as follows:

$$
p_p = \begin{cases} \max \{0, R-nb_p\} &\text{ if solution is feasible}\\ -1 &\text{otherwise} \end{cases}
$$

> 💡 **If the algorithm's solution is infeasible or exceeds the time limit, cannot execute (crash), etc., a penalty score (-1) is obtained for that problem!**


Here $R$ is the number of teams being evaluated. Points are calculated for all problems and ranking is determined based on the total sum of points. The table below shows the leaderboard for the above example:

```

  team  nb_prob1  p_prob1  nb_prob3  p_prob3  nb_prob2  p_prob2  total_score  ranking
TEAM00         0        5         1        4         0        5           14        1
TEAM02         2        3         3        2         1        4            9        2
TEAM05         3        2         0        5         3        2            9        2
TEAM03         1        4         4        1         2        3            8        4
TEAM01         5       -1         2        3         4        1            3        5
```

### Leaderboard Update

**The leaderboard is updated daily at 1:00 PM (13:00). The leaderboard results are based on algorithms executed by 0:00 AM of the day (midnight of the previous day).** That is, if a team submitted an algorithm yesterday at 11 PM and submitted a new algorithm today at 9 AM, the leaderboard updated today at 13:00 will calculate scores based on the algorithm submitted yesterday. In other words, the most recent algorithm executed before 0:00 AM of the day is the evaluation target.

### Numerical Error in Objective Function Comparison (updated on 2024-07-15)

When comparing objective functions, they are rounded at the third decimal place. For example, if two objective function values are 100.122999997 and 100.123, when rounded they become 100.12 and 100.12. Therefore, they are recognized as the same objective function. The reason for doing this is to consider calculation errors that may occur when calculating the objective function value of the solution returned by the algorithm. (*The evaluation server will be updated to use these criteria as of 2024-07-15. Therefore, leaderboard scores after 2024-07-15 may be slightly different from before.)*

### Final Presentation Evaluation Method

Presentation evaluation is conducted for participating teams that advance to the finals, and presentation evaluation scores are calculated by summing judges' evaluation scores. The final ranking is determined by combining final leaderboard scores and presentation evaluation scores at a certain ratio.


> 💡 **Final ranking is determined by combining final leaderboard scores and presentation evaluation scores at a certain ratio. The number of hidden evaluation problems per stage is announced when each stage begins!**

### Algorithm Source Code Plagiarism Check

Algorithms submitted by participating teams must include sufficient contributions from the participating team. For example, it is not allowed for members who were originally on the same team to submit nearly identical algorithms under multiple team names. As detailed in [Algorithm Submission Method](#baseline-algorithm), when submitting an algorithm, the algorithm source is also submitted. The submitted source may be used later to check for plagiarism between participating teams. Algorithm uniqueness is admittedly difficult to judge clearly. This competition assumes that participating teams participate in the competition in an honorable manner at a common-sense level. Participating teams whose actions violate this assumption may have their participation restricted according to the organizing committee's decision.

All icons from Flaticon designed by Smashicons, iconixar, Freepik, Paul J., and kliwir art.
