# Problem Description and Ranking Method

*Update history:*

- *2024/07/15 - Added objective comparison rounding rules*
- *2024/06/25 - Added leaderboard update policy*
- *2024/06/21 - Added JSON format description*
- *2024/05/08 - Added source code plagiarism check policy*

## 0. Terminology

- Rider
    - A person who picks up food from a store and delivers it to a customer.
- Pickup
    - Handing off an order at the store.
- Delivery
    - Delivering the order to the customer location.
- Ready time (`readytime`)
    - The time when an order is ready = order time (OT) + preparation time at the store (RT).
- Deadline (`deadline`, DT)
    - The latest allowable delivery time. The rider must arrive and complete delivery by this time.
- Bundle delivery
    - Delivering multiple orders together by a single rider.

## 1. Problem setting

### 1.1. Orders

When you place a food order through a delivery app, order information is generated as shown below.

Assigning one rider per order is inefficient. Delivery platforms want to bundle multiple orders that occur around the same time to reduce the number of riders and lower delivery cost.

You are given a list of orders issued in a region.

However, bundling orders requires multiple constraints. First, consider the riders who will execute the deliveries.

# Constraints

### 1.2. Riders

There are three rider types.

![023-delivery-courier.png](delivery-courier.png)

Walk rider

![002-delivery-bike-1.png](delivery-bike.png)

Bike rider

![022-car.png](delivery-car.png)

Car rider

Each rider type differs in **capacity**, **speed**, **service time**, and **cost**. For example:

- Walk riders are slowest but cheapest.
- Bike riders are fastest but most expensive.
- Car riders have larger capacity but require more service time for parking and access.

The delivery cost is defined as follows.

**Delivery cost**

> **Bundle cost = fixed cost by rider type + variable cost by rider type (per distance)**

Fixed and variable costs differ by rider type.

> **Note:** Fixed cost is charged once per bundle, regardless of how many orders are bundled.

> **Note:** Variable cost is proportional to **distance**. Speed affects travel time but not distance, so the variable cost uses distance only.

From the customer's perspective, only the delivery fee and delivery deadline matter, not the rider type. But the platform's cost depends on the rider type. We cannot always use only the cheapest rider type because rider availability is limited. Bundling multiple orders can reduce the number of riders and cost, but additional constraints apply.

### 1.3. Bundle delivery constraints

To bundle orders, the following constraints must be satisfied.

> 💡 **Constraint 1.** The total volume of bundled orders must not exceed the rider capacity: **capacity constraint**

> 💡 **Constraint 2.** All orders must be delivered before their deadlines: **time constraint**

> 💡 **Constraint 3.** When bundling, all pickups must be completed before deliveries: **visit order constraint**

After forming bundles, assign them to riders. This introduces additional constraints on rider availability.

> 💡 **Constraint 4.** Every order must be delivered by some rider: **order fulfillment constraint**

> 💡 **Constraint 5.** Each rider can be assigned at most one bundle: **rider assignment constraint**

## 2. Example

Consider the following two orders.

![Example orders](example-orders-diagram.png)

The two orders have two pickup stores and two delivery locations. The distances are shown below.

![Numbers on arcs represent travel distances](distance-network-diagram.png)

Numbers on arcs represent travel distance.

To bundle the two orders, we must satisfy two constraints.

**Constraint 1. Capacity constraint**

The total volume is 90 (=40+50), so a walk rider cannot deliver. Bike and car riders satisfy the capacity constraint. Now check the time constraint.

**Constraint 2. Time constraint**

To satisfy the time constraint, the rider must:

1. Depart from a pickup location only after the order ready time.
2. Arrive at each delivery location by `deadline - service_time`.

Consider a bike rider following the route below.

![Arc numbers represent travel time for the bike](bike-time-network-diagram.png)

Arc numbers represent bike travel time.

Step-by-step:

1. Pickup for Order 1: The rider completes pickup at time 15 and departs. Here 15 is the ready time for Order 1, and we assume the rider arrived early enough to complete service time.

> 💡 **At the first pickup location in a bundle, the rider can depart right after ready time without adding service time.**

1. Pickup for Order 2: Bike speed is 2, so travel time from Order 1 pickup to Order 2 pickup is 10. Arrival at time 25, service time 3, so store entry is time 28. But Order 2 ready time is 30 (= order time 10 + prep time 20), so the rider departs at 30 (2 units of waiting).

> 💡 **Ready time = order time + preparation time.**

1. Delivery for Order 1: Depart at 30, arrive at 70, and after service time 3, deliver at 73. This meets Order 1 deadline 80.
2. Delivery for Order 2: Depart at 73, arrive at 92, plus service time 3 gives 95, which meets Order 2 deadline 95.

**Constraint 3. Visit order constraint**

The only feasible bundling in this example is the bike rider route above. The rider visits both pickups first, then the deliveries. The rider cannot go from a pickup directly to a delivery before completing all pickups.

> **Note:** You may visit delivery locations only after completing all pickups.

**Constraint 4. Order fulfillment constraint**

Both orders are delivered successfully, so this constraint is satisfied.

**Therefore, to build a bundle, you must decide:**

1. **Rider type (walk, bike, or car)**
2. **A set of orders that satisfies the capacity constraint**
3. **A visit order that satisfies the time constraint**

### Another example

Suppose there are 10 orders (IDs 1-10). Assume each pair can be bundled by bike or car as follows:

- Orders 1 & 2: bike or car
- Orders 3 & 4: bike or car
- Orders 5 & 6: bike or car
- Orders 7 & 8: bike or car
- Orders 9 & 10: bike or car

Assume there are 3 bike riders and 10 car riders available.

If the visit order is the same for bike and car bundles, travel distance is the same, so bundle cost depends only on fixed and variable cost. Assume bikes are cheaper for every bundle. Then assigning all 5 bundles to bikes minimizes cost.

**Constraint 5. Rider assignment constraint**
However, **Constraint 5** limits bike assignments to at most 3 bundles. The remaining 2 bundles must be assigned to car riders.

Thus, when a bundle can be served by multiple rider types, you must consider rider availability. A rider cannot serve more than one bundle.

## 3. Objective

Once rider types and visit orders are set, costs can be computed from distances. Summing all bundle costs gives total cost; dividing by the number of orders yields average delivery cost.

> Objective = average delivery cost = total delivery cost / total number of orders

## 4. Problem data format

Each problem instance provides:

- A list of `K` orders
- Rider types and attributes
- A distance matrix

Each instance is a JSON file with the following fields.

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

- `name`: instance name
- `K`: number of orders
- `RIDERS`: rider information, e.g. `['BIKE', 5.291005291005291, 100, 80, 2200, 120, 5]`
    - type: `BIKE`, `WALK`, or `CAR`
    - speed: distance(m)/time(sec)
    - capacity
    - variable cost (per 100m)
    - fixed cost
    - service time (sec)
    - availability
    
    > **Note:** Car riders always have availability equal to the number of orders, so delivering each order separately by car is always feasible (but not cost efficient).
    
- `ORDERS`: order information, e.g. `[0, 7, 37.49493567, 127.03071274, 37.501853, 127.037541, 900, 40, 1980]`
    - order id
    - order time (sec)
    - pickup latitude
    - pickup longitude
    - delivery latitude
    - delivery longitude
    - preparation time (sec)
    - order volume
    - deadline (sec)
- `DIST`: distance matrix
    - size `2K * 2K`
    - units: meters (rounded to integers)
    - distance between pickup `i` and pickup `j`: `DIST[i,j]`
    - distance between pickup `i` and delivery `j`: `DIST[i,j+K]`
    - distance between delivery `i` and delivery `j`: `DIST[i+K,j+K]`
    
    > **Note:** Travel time is not given directly. Compute it from distance and rider speed. Round to seconds and add service time if desired.
    
    Python example:
    `rider.T = np.round(dist_mat/rider.speed + rider.service_time)`

## 5. Solution format

Your algorithm must return a list of bundles in the following format.

- A list of `[rider_type, pickup_order_sequence, delivery_order_sequence]`
- Visit order uses order IDs, e.g., `[1,3,2]`
- Example: `['BIKE', [1,3,2], [2,3,1]]`
    - Meaning: Assign orders 1, 2, 3 to a bike rider, visit pickups in 1,3,2 order, then deliveries in 2,3,1 order.

The evaluation system checks objectives and constraints. Each bundle must satisfy **Constraints 1, 2, and 3**, and the full solution must satisfy **Constraints 4 and 5**.

## 6. Algorithm submission and evaluation

Teams implement algorithms for each stage (preliminary, main, final) based on the public instances. Submitted code is run on hidden instances for evaluation. Server specs:

- AWS EC2 instance (c5.2xlarge)
- 8 cores, 16 GB memory, 32 GB storage
- OS: Ubuntu 22.04 LTS

Each stage enforces time limits. Preliminary: 1 minute per instance. Main and final time limits are announced at stage start.

> 💡 **Preliminary time limit is 1 minute per instance.**

Since your local PC differs from the evaluation server, your algorithm must measure elapsed time and terminate within the limit.

Additional restrictions:

- No external internet access during execution
- Maximum 4 CPU cores (up to 400% CPU usage)

Violations may lead to disqualification.

> 💡 Internet access and CPU limits are enforced with `firejail` and `cpulimit`. Your algorithm must not conflict with these tools.

Each team can submit **once per day**. A day is defined as 00:00-23:59 KST. Only one submission per calendar day is allowed.

> 💡 **Only one submission per day is allowed.**

Submitted algorithms are run on hidden instances, and results are collected at a fixed time (announced later). The leaderboard is updated accordingly.

> 💡 **The leaderboard updates once per day at a fixed time.**

The most recent submission before evaluation time is used. Therefore, before a stage ends, re-submit your best algorithm to ensure it is evaluated.

Hidden instances are similar to the public ones. Each stage has a different number of hidden instances. Suppose 5 teams submit and there are 3 hidden instances, with results:

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

The evaluation system computes the following for each instance $p$:

$$
nb_p = |\{\text{teams that found a better objective for problem $p$}\}|
$$

In other words, $nb_p$ is smaller for better solutions. Infeasible or crashed runs are treated as the worst objective.

Points for each instance are computed as:

$$
p_p = \begin{cases} \max \{0, R-nb_p\} &\text{ if solution is feasible}\\ -1 &\text{otherwise} \end{cases}
$$

> 💡 **If the solution is infeasible, exceeds the time limit, or crashes, the instance receives a penalty score of -1.**

Here $R$ is the number of teams. Total points across instances determine ranking. Example leaderboard:

```
  team  nb_prob1  p_prob1  nb_prob3  p_prob3  nb_prob2  p_prob2  total_score  **ranking**
TEAM00         0        5         1        4         0        5           14        1
TEAM02         2        3         3        2         1        4            9        2
TEAM05         3        2         0        5         3        2            9        2
TEAM03         1        4         4        1         2        3            8        4
TEAM01         5       -1         2        3         4        1            3        5
```

### Leaderboard update policy

**The leaderboard is updated daily at 13:00.** The update reflects algorithms executed up to 00:00 (midnight) of that day. For example, if a team submitted at 23:00 yesterday and again at 09:00 today, the leaderboard at 13:00 will use the submission from yesterday. In other words, the latest submission before 00:00 is evaluated.

### Numerical error in objective comparison (updated 2024-07-15)

Objective values are compared after rounding to the second decimal place. For example, 100.122999997 and 100.123 both round to 100.12 and are treated as equal. This accounts for numerical error in objective computation. *(The evaluation server uses this rule from 2024-07-15, so leaderboard results after that date may differ slightly from earlier results.)*

### Final presentation evaluation

For finalists, presentation evaluation scores are computed from judges' scores. The final ranking combines the final leaderboard score and presentation score with a fixed ratio.

> 💡 **Final ranking combines the final leaderboard score and the presentation score by a fixed ratio. The number of hidden instances is announced at the start of each stage.**

### Source code plagiarism check

Submitted algorithms must include meaningful contributions from the team. For example, submitting nearly identical algorithms under multiple team names is not allowed. As described in the [algorithm submission guide](https://www.notion.so/df33194981c94768bd1c05f6157a8b9c?pvs=21), source code is submitted and may be used later to check for plagiarism. Determining originality is difficult, so the competition assumes honorable conduct. Teams that violate this principle may be restricted at the committee's discretion.

All icons from Flaticon designed by Smashicons, iconixar, Freepik, Paul J., and kliwir art.
