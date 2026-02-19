# Problem Description and Ranking Method

*Update history:*

- *2025/07/01 - Added problem description materials for the Spring Joint Academic Conference*
- *2025/05/12 - Added problem description podcast*
- *2025/05/07 - initial page created*


# 0. Terminology

- Loading
  - Means loading vehicles from a port onto the vessel.
- Unloading
  - Means unloading vehicles from the vessel to a port.
- Loading and unloading
  - Means either loading or unloading vehicles.
- Placement
  - Means placing a vehicle in a specific slot (node) inside the vessel.
- Deck graph (internal vessel structure)
  - Node
    - Each individual space that can hold one vehicle is represented as a node.
  - Edge
    - A line connecting two nodes; if two nodes are connected by an edge, a vehicle can move between them.
  - Gate node
    - The only passage through which vehicles can be loaded/unloaded at ports.
    - Represented as node 0, and there is only one gate on the vessel.
    - No vehicle can be placed at the gate.
- Relocation
  - Means moving a vehicle inside the vessel from one node to another.
- Temporary unloading
  - Means unloading a vehicle at an intermediate port that is not its destination.
- Reloading
  - Means loading a temporarily unloaded vehicle again and placing it on a node (possibly a different node).
- Rehandling
  - There are two major ways to change a vehicle’s position:
    - Relocation
    - Temporary unloading + reloading
- Vehicle transportation demand
  - Given as origin-destination pairs and the number of vehicles.
- Route
  - Defined as a list of nodes representing the movement sequence of a vehicle on the deck graph.
  - Loading, unloading, placement, reloading, and rehandling are all represented as routes on the deck graph.

# 1. Problem Setting

![Source: [https://www.news1.kr/economy/trend/5312046](https://www.news1.kr/economy/trend/5312046) ⓒ News1 reporter Yoon Il-ji](roroship.png)

[https://youtu.be/Ug3SQBoDS1E?si=EIXZDQ7QhR1braZE](https://youtu.be/Ug3SQBoDS1E?si=EIXZDQ7QhR1braZE)

Finished vehicles are typically shipped by vessel to major overseas markets such as the U.S. and Europe. A vessel visits multiple ports and repeatedly performs loading and unloading, so efficient stowage inside the vessel is critical.

In particular, to unload a vehicle placed deep inside the vessel, other vehicles on its path may need to be moved within the vessel, or temporarily unloaded at the port and then reloaded.

Such unnecessary rehandling operations cause significant costs, so vehicles should be placed to minimize them.

The detailed setting is as follows:

- Each vehicle has an origin port (O), where it must be loaded, and a destination port (D), where it must be unloaded. There are multiple (O, D) pairs, and each pair has an assigned quantity. This is called transportation demand.
- The vessel route (port visit order) is given, and the vessel performs loading/unloading at each visited port.
- Space inside the vessel is limited, and due to the deck structure, vehicles loaded earlier may block routes needed for unloading later vehicles. In such cases, vehicles must be relocated or temporarily unloaded and reloaded.
  - A temporarily unloaded vehicle may be reloaded to a different node.
  - Every rehandling operation incurs a cost.
  - Assume no limit on the number of vehicles that can be temporarily unloaded at each port.
  - You cannot avoid rehandling by skipping required loading or unloading. In other words, all given transportation demand must be satisfied.

> You must design an optimization algorithm that **minimizes the total cost of loading/unloading all required vehicles, including rehandling**.

## Vessel Structure

- The vessel has individual spaces (nodes) for vehicle placement.
- Each node can hold at most one vehicle.
- The vessel structure is represented as edges connecting nodes (example in Figure 1).
- All edges are undirected, i.e., movement is possible in both directions.
- Nodes represent possible placement spaces, and edges represent possible movement. These edges form the movement routes for loading/unloading/relocation.
- The internal structure (deck graph) is defined by the given nodes and edges.

![Figure 1. Example vessel structure](graph1.png)

- Various vessel structures will be provided as shown below.

![Figure 2. Examples of diverse vessel structures](graph2.png)

> There is no structural restriction on the deck graph. It may be non-tree (e.g., the fourth example above) and non-planar.

## Routes

- Since the gate (node 0) is fixed, all loading/unloading must be performed through that node.
  - For example, in Figure 1, to place a vehicle at node 5, it must pass 0 → 1 → 2 → 4 → 5. To unload, the reverse route is used: 5 → 4 → 2 → 1 → 0.
- **If another vehicle exists on a route, that vehicle must be relocated or temporarily unloaded and reloaded.**
- For example, suppose a vehicle at node 5 must be unloaded, but node 2 is occupied. Two rehandling options exist:
  - Temporarily unload the vehicle at node 2 through gate 0 (2 → 1 → 0), unload the vehicle at node 5, then reload the temporarily unloaded vehicle to an empty node. (temporary unload + reload)
  - Relocate the vehicle at node 2 to node 3 (2 → 3), then unload the vehicle at node 5. (relocation)

💡

> A route that satisfies all constraints is called a **feasible route**. For a route to be feasible, all constraints below must hold:
>
> - A route is given as a list of nodes, and all nodes must exist in the deck graph.
> - Every edge formed by consecutive nodes in the route must exist in the deck graph.
> - No duplicate node is allowed in a route (simple-route constraint).
> - A loading route must always start at node 0, and at execution time all nodes on the route (including the last node) must be empty.
> - An unloading route must always end at node 0, and at execution time the first node must contain the vehicle to unload while all other route nodes must be empty.
> - A rehandling route can be either **relocation** or **temporary unload + reload**:
>   - Relocation route: at execution time, the first node must contain the vehicle to move and all remaining route nodes must be empty (the last node becomes the new position).
>   - Temporary unload + reload: **two separate routes** are generated, each satisfying unloading-route and loading-route constraints, respectively.

# 2. Objective – Minimize Total Cost

## Route Cost

Route cost is computed as:

> **Movement cost = fixed cost + distance-based variable cost**

- The fixed cost is charged once per route.
- The variable cost is proportional to route length, where length is the number of traversed edges.

> **Note:** If temporary unloading + reloading is used for rehandling, two routes are created, so fixed cost is charged twice.

### Route-Cost Example

- Distance between two adjacent nodes (or between a node and gate via adjacent edges) is counted as 1 per traversed edge.
- Assume fixed cost is 10.
- In Figure 1, if two loaded vehicles are placed at nodes 3 and 2, the total loading distance from gate is 5 (=3+2). If those vehicles are unloaded in order node 2 then node 3, unloading distance is also 5 (=2+3), so total movement distance is 10. There are 4 routes (2 loading + 2 unloading), so total cost is $4 \times 10 + 10 = 50$.
  - If the vehicle at node 3 must be unloaded before the one at node 2, the vehicle at node 2 must be rehandled. If it is temporarily unloaded and then reloaded, additional distance is 4 (2 for unloading + 2 for reloading). Since two rehandling routes are created, added rehandling cost is $2 \times 10 + 4 = 24$.

💡

> As in this example, the **execution order** of loading/unloading routes is important.
>
> Depending on route order, rehandling may be avoidable, or rehandling cost may increase.
>
> **You must decide the execution order of routes.**
>
> As long as all routes are feasible, there is no restriction on execution order among loading, unloading, and rehandling routes. In temporary unload + reload, reloading may be delayed until after other routes.

## Solution

For each problem, your solution should specify:

- For each port:
  - A route list of (route, moved-demand) pairs.

Operations are executed in the listed order. After each route execution, vessel state changes. Therefore, whether a route is valid depends on vessel state **at that exact execution time**.

A solution is **feasible** if all routes in the solution are feasible and all required demand is delivered from origins to destinations.

## Objective Function

The objective function is defined only for feasible solutions:

- **(sum of all route costs) - (total cost lower bound, LB)**

> The total cost lower bound is computed as follows:
>
> - $P$: set of ports
> - $F$: route fixed cost
> - $Load_p$: total number of vehicles to load at port $p$ (demands with origin $p$)
> - $Unload_p$: total number of vehicles to unload at port $p$ (demands with destination $p$)
> - $N_m$: the set of $m$ nodes (excluding gate) closest to gate
> - $d_i$: shortest distance from gate to node $i$
>
> $$
> \text{LB} := \sum_{p \in P} \left[ F \times (Load_p + Unload_p) + \sum_{i \in N_{Load_p}} d_i + \sum_{i \in N_{Unload_p}} d_i \right]
> $$
>
> LB is the optimal total cost under a relaxed setting where every non-gate node has an additional direct edge to gate whose cost equals shortest-path distance, i.e., ignoring blocking by other vehicles.
>
> ***Note: LB is provided with each problem; you do not need to compute it.***
>
> Since objective value is (total route cost) - LB, minimizing objective means:
>
> 1. reducing loading/unloading route lengths (beyond shortest-distance baseline), and
> 2. reducing rehandling cost.

## Example Problem

- Vessel route:
  - Port A → Port B → Port C → Port D → Port E
- Demand:

| **Demand** | Origin | Destination | Quantity |
| ---------- | ------ | ----------- | -------- |
| Demand 0   | A      | C           | 2 (navy, gray) |
| Demand 1   | B      | E           | 1 (orange) |
| Demand 2   | C      | D           | 1 (red) |
| Demand 3   | B      | D           | 1 (green) |
| Demand 4   | D      | E           | 1 (pink) |

- Deck graph:
  - As shown in Figure 3 below.

![Figure 3. Vessel structure in the example](graph3.png)

💡

> For readability in this example, route types are annotated as below. (You do not need to distinguish route types when submitting.)
>
> - [...], demand X: loading route
> - [...], demand X: unloading route
> - [...], demand X: rehandling route

- Example solution
  - Port A: total cost = (10 + 4) + (10 + 3) = 27
    - [node 0, node 1, node 2, node 3, node 4], demand 0
    - [node 0, node 1, node 2, node 3], demand 0
  - Port B: total cost = (10 + 2) + (10 + 1) = 23
    - [node 0, node 1, node 2], demand 1
    - [node 0, node 1], demand 3
  - Port C: total cost = (10 + 1) + (10 + 2) + (10 + 3) + (10 + 4) + (10 + 3) + (10 + 2) + (10 + 1) = 86
    - [node 1, node 0], demand 3
    - [node 2, node 1, node 0], demand 1
    - [node 3, node 2, node 1, node 0], demand 0
    - [node 4, node 3, node 2, node 1, node 0], demand 0
    - [node 0, node 1, node 2, node 3], demand 1
    - [node 0, node 1, node 2], demand 2
    - [node 0, node 1], demand 3
  - Port D: total cost = (10 + 1) + (10 + 2) + (10 + 1) = 34
    - [node 1, node 0], demand 3
    - [node 2, node 1, node 0], demand 2
    - [node 0, node 1], demand 4
  - Port E: total cost = (10 + 1) + (10 + 3) = 24
    - [node 1, node 0], demand 4
    - [node 3, node 2, node 1, node 0], demand 1
- Objective value of this solution:
  - Sum of route costs = 27 + 23 + 86 + 34 + 24 = 194
  - LB = (10*(2+0)+(1+2)+(0)) + (10*(2+0)+(1+2)+(0)) + (10*(1+2)+(1)+(1+2)) + (10*(1+2)+(1)+(1+2)) + (10*(0+2)+(0)+(1+2)) = 23 + 23 + 34 + 34 + 23 = 137
  - Objective = 194 - 137 = 57

![Figure 4. Example solution](graph4.png)

💡

> In this example, only rehandling via temporary unload + reload was used.
> Depending on deck graph structure, relocation-based rehandling may reduce cost further.
> You must decide which rehandling strategy to use.

# 3. Problem Data Definition

Each problem provides:

- `N`: number of nodes (integer). `0` is gate, `1,...,N-1` are vehicle-placeable nodes.
- `E`: edge list (list of edge pairs).
- `P`: number of ports (integer). Ports are visited in order `0,1,...,P-1`.
- `K`: demand list (list of `((O,D), quantity)`).
- `F`: route fixed cost.
- `LB`: lower bound of total cost.
- `grid_graph`: additional data for visualization (optional, not required for solving).

Problems are given in JSON format as follows:

```json
{
  "N": 49,
  "E": [
    [0, 1],
    [1, 2],
    [2, 3],
    [2, 4],

    ...

  ],
  "P": 10,
  "K": [
    [
      [0, 1], 4
    ],
    [
      [0, 2], 3
    ],
    [
      [0, 3], 2
    ],

    ...

  ],
  "F": 100,
  "LB": 13259,
  "grid_graph": ...

}
```

Notes:

- `E` is undirected and each edge appears only once in arbitrary direction. For example, `[0,1]` means both `0→1` and `1→0` exist.
- `K` contains origin, destination, and quantity for each demand. For example, `[0,1],4` means 4 vehicles must be transported from port 0 to port 1.
  - List order is demand index. In the example above, `[0,1],4` is demand 0 and `[0,3],2` is demand 2.
  - Vehicles under the same OD pair demand are assumed identical. So when returning a solution, specifying the demand index is sufficient; individual vehicle IDs are unnecessary.

# 4. Algorithm Submission and Evaluation

Teams develop algorithms for stage-specific public problems (preliminary/main/final). Submitted algorithm code is executed on hidden problems for evaluation. The evaluation server specification is:

- AWS EC2 instance (c5.4xlarge)
- 16 cores, 32 GB memory, 32 GB storage
- OS: Ubuntu 24.04 LTS

Algorithms are subject to a time limit, which can differ by problem. Practice problems and their time limits are disclosed for each stage. **Time limits of hidden evaluation problems are not disclosed.**

Because team PC specs differ from server specs, algorithms should monitor elapsed time internally and avoid exceeding limits.

Submitted algorithms are also subject to these constraints:

- No external internet access during execution
- No access to parent directories above execution folder
- At most 4 CPU cores (~400% CPU usage)

Violating these constraints may lead to disqualification.

> **Internet blocking and CPU-core limits are enforced using `firejail` and `cpulimit` at evaluation runtime. Your algorithm must not conflict with these tools.**

Each team may submit at most twice per day:

- once between 00:00:00 and 11:59:59 (KST),
- once between 12:00:00 and 23:59:59 (KST).

> **Maximum 2 submissions/day: once before noon and once before midnight.**

Submitted algorithms are run on hidden problems, and results are aggregated hourly. At each aggregation point, a leaderboard is generated from algorithms that produced results on all problems and then published on the website.

> **Leaderboard updates every hour.**

All evaluation is based on each team’s **most recently submitted algorithm**.

> **At each evaluation time, your latest submission is the one that counts.**

Therefore, just before a stage ends, resubmit your best algorithm; otherwise ranking is determined by your last submitted version.

Hidden evaluation problems have characteristics similar to public ones. The number of hidden problems depends on stage.

Suppose 5 teams submit and there are 3 hidden problems, with outcomes:

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

For each problem $p$, compute:

$$
nb_p = |\{\text{teams that found a better objective for problem } p\}|
$$

So better algorithms on problem $p$ get smaller $nb_p$. If a solution is infeasible or execution crashes, it is treated as the worst objective.

Per-problem point is:

$$
p_p = \begin{cases} \max \{0, R-nb_p\} &\text{if solution is feasible}\\ -1 &\text{otherwise} \end{cases}
$$

> **If a solution is infeasible, time-limited, or crashes, the team receives a penalty score (-1) for that problem.**

Here, $R$ is the number of evaluated teams. Rankings are determined by total points over all problems. The table below shows the example leaderboard:

```

  team  nb_prob1  p_prob1  nb_prob3  p_prob3  nb_prob2  p_prob2  total_score  **ranking**
TEAM00         0        5         1        4         0        5           14        1
TEAM02         2        3         3        2         1        4            9        2
TEAM05         3        2         0        5         3        2            9        2
TEAM03         1        4         4        1         2        3            8        4
TEAM01         5       -1         2        3         4        1            3        5
```

## Final Stage Evaluation Method

💡

> **During the final stage, no new algorithm submissions are accepted. Hidden-problem results are updated daily using the algorithm most recently submitted in the main stage.**

Final-stage teams also undergo presentation evaluation. Judges’ scores are aggregated into a presentation score. Final ranking is determined by a weighted combination of final leaderboard score and presentation score.

> **Final ranking = weighted sum of final leaderboard score and presentation score.**

## Source Code Plagiarism Check

Submitted algorithms must include sufficient original contribution by each team. For example, multiple teams submitting nearly identical algorithms by the same members is not allowed. As described in **Algorithm Development Method**, source code must be submitted with algorithms. Submitted source may later be used for plagiarism checks across teams.

Algorithm originality can be difficult to assess perfectly. This competition assumes teams participate honorably and with common-sense fairness. Teams violating this assumption may have participation restricted by the organizing committee.