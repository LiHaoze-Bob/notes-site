---
title: Ch10-Graph
---
Ch10 Graph

2024 年 5 月 21 日

> 本篇笔记主要介绍了图论的基本概念，包括图的定义、类型（如无向图、有向图、二分图等）、图的表示方法（邻接矩阵和关联矩阵）、图同构、连通性、经典图论问题（如欧拉路径、哈密顿路径、最短路径问题和平面图）以及图的染色与对偶图等内容。通过这些内容，读者可以深入理解图的结构及其在不同领域中的应用。<small>（由 gpt-4o-mini 生成摘要）</small>

## 1\. 图论术语 Graph Terminologies {#1-图论术语-graph-terminologies}

### 1.1. 基本术语 Basic Terminology {#11-基本术语-basic-terminology}

Definition: Graph

A **图(graph)** $G=(V,E)$ consists of $V$, a nonempty set of **顶点(vertex, node)** and $E$, a set of **边(edge)**. Each edge has either one or two vertices associated with it, called its **端点(endpoint)**. An edge is said to **连接(connect)** its endpoints.

在无向图中，定义点的**度(degree)** 与这一顶点**关联(incident)** 的边的数量。记号：$\text{deg}(v)$。

-   如果 $\text{deg}(v) = 0$，则称 $v$ 是**孤立的(isolated)**；
-   如果 $\text{deg}(v) = 1$，则称 $v$ 是**悬挂的(pendant)**。

### 1.2. 无向图和有向图 Undirected and Directed Graphs {#12-无向图和有向图-undirected-and-directed-graphs}

![](../../../assets/notes/f689a577d9bf496030d1.png)

**无向图(undirected graph)**：

-   **简单图(simple graph)**：没有重边和自环的无向图。
-   **多重图(multigraph)**：允许重边但不允许自环的无向图。
-   **伪图(pseudograph)**：允许自环和重边的无向图。

![Uy7IUPyq.png](../../../assets/notes/6a2c18cddf77fb133b34.png)

**有向图(directed graph = digraph)**：$E$ 是**有向边(directed edge, arc)** 的集合。

-   **简单有向图(simple directed graph)**：没有重边和自环的有向图。
-   **有向多重图(directed multigraph)**：有重边或自环的有向图。如果恰有一条 $(u,v)$ 的边和一条 $(v,u)$ 的边，这种情况不属于重边。

### 1.3. 一些特殊的简单图 Some Special Simple Graphs {#13-一些特殊的简单图-some-special-simple-graphs}

**完全图(complete graph)** - $K_n$：$n$ 个顶点有一条边的简单无向图。

![](../../../assets/notes/ef5769a06aadc7b3338d.png)

**环(cycle)** - $C_n\ (n>2)$：

![gMi8SdeB.png](../../../assets/notes/3d02587ba6ddf7dad184.png)

**轮(wheel)** - $W_n\ (n>2)$：在 $C_n$ 的基础上添加一个点，并于前 $n$ 个点相连。（注意 $W_n$ 有 $n+1$ 个点）

![lKNyixLm.png](../../../assets/notes/bff88b7b5eaf7eed449a.png)

n-Cubes - $Q_n (n>0)$：

![ONwVeFU2.png](../../../assets/notes/23a3659729e6fa093cc4.png)

### 1.4. 二分图 Bipartite Graph {#14-二分图-bipartite-graph}

Definition: **二分图(bipartite graph)**

一个简单图是**二分的(bipartite)** 当且仅当其点集 $V$ 可以被划分成两个子集 $V_1$ 和 $V_2$ 满足所有边都是连接 $V_1$ 和 $V_2$ 的（即 $V_1$ 和 $V_2$ 内部不连边）。

**完全二分图(complete bipartite graph)**：对于 $V_1$ 和 $V_2$ 的每个点之间都有连边的二分图。

Theorem

一个图是二分的当且仅当其可以被黑白染色。

### 1.5. 正则图 Regular Graph {#15-正则图-regular-graph}

Definition: Regular Graph

一个简单图是**正则的(regular)** 当且仅当其每个顶点都有相同的度。

一个**正则图(regular graph)** 被称为 $n$\-regular 的当且仅当每个顶点的度数均为 $n$。

## 2\. 图表示 Graph Representings {#2-图表示-graph-representings}

**邻接矩阵(adjacency matrix)**

一张 $n$ 个点 $(v_1,v_2,\cdots,v_n)$ 的简单图 $G=(V,E)$ 可以用邻接矩阵 $A$ 表示，其中：

$a_{i,j} = \begin{cases}  1 \quad\text{if }\{v_i,v_j\}\text{ is an edge of }G\\0\quad\text{otherwise.}\end{cases}$

**关联矩阵(incidence matrix)**

一张 $n$ 个点 $m$ 条边的简单图 $G=(V,E)$ 可以用邻接矩阵 $A_{n\times m}$ 表示，其中：

$a_{i,j} = \begin{cases} 1\quad&\text{iff edge }e_j\text{ is incident with }v_i\\ 0\quad&\text{otherwise.} \end{cases}$

## 3\. 图同构 Graph Isomorphism {#3-图同构-graph-isomorphism}

同构

我们称两个图 $G_1=(V_1,E_1)$ 和 $G_2=(V_2,E_2)$ 是**同构(isomorphic)** 的当且仅当存在一个从 $V_1$ 到 $V_2$ 的双射函数满足 $(u,v) \in E_1$ 当且仅当 $(f(u),f(v)) \in E_2$。

判定两个图是否同构，重点可以考察一些**不变量(invariant)**，比如：

-   点数
-   边数
-   对应点的度数
-   如果一个是二分图，另一个也必须是二分图
-   如果一个是完全图，另一个也必须是完全图

等等。所以，如果我们要断言图是同构的，就给出一组映射关系；如果我们要断言图不是同构的，就找出一个改变的不变量。

## 4\. 连通性 Connectivity {#4-连通性-connectivity}

### 4.1. 无向图的连通性 Connectedness in Undirected Graphs {#41-无向图的连通性-connectedness-in-undirected-graphs}

一张无向图被称作**联通的(connected)** 当且仅当对于每一对图中的点对，都存在一条他们之间的路径。

无向图的极大连通子图被称为一个**联通块(connected component = component)**

-   在无向图中，如果删除一个点会产生更多的联通块，则将这个点称为**割点(cut vertex)**。
-   在无向图中，如果删除一条边会产生更多的联通块，则将这条边称为**割边(cut edge)** 或**桥(bridge)**。

### 4.2. 有向图的连通性 Connectedness in Directed Graphs {#42-有向图的连通性-connectedness-in-directed-graphs}

在一张有向图中，如果对于任意两个点 $a,b$ 都存在一条从 $a$ 到 $b$ 的有向路径，也存在一条 $b$ 到 $a$ 的有向路径，则称这个有向图是**强连通的(strongly connected)**。

对于一张有向图，所有有向边当做无向边，所得到的图是联通的，我们就称这个有向图是**弱联通的(weakly connected)**。

有向图的一个极大强连通子图被称为一个**强连通分量(strongly connected component = strong component)**。

## 5\. 图上的经典问题 Classic Problems on Graphs {#5-图上的经典问题-classic-problems-on-graphs}

### 5.1. 欧拉路径 Euler Paths {#51-欧拉路径-euler-paths}

-   **欧拉路径(euler path)**：经过图 $G$ 每条边恰好一次的简单路径。
-   **欧拉回路(euler circuit)**：过图 $G$ 的每条边恰好一次的简单回路。
-   **欧拉图(euler graph)**：包含欧拉回路的图。

Theorem 1

一张联通多重图存在欧拉回路当且仅当每个节点的度数都是偶数。

Proof

![](../../../assets/notes/657e270d5c9c4599bda1.png)

![](../../../assets/notes/c34ec6c0b118fb1ffbe2.png)

Theorem 2

一张联通多重图存在不是欧拉回路的欧拉路径当且仅当有恰好两个节点的度数为奇数。

Theorem 3

一张连通有向多重图存在欧拉回路当且仅当：1. 图是弱联通的 2. 每个点的入度和出度相等。

Theorem 4

一张连通有向多重图存在不是欧拉回路的欧拉路径当且仅当：1. 图是弱联通的 2. 每个点的入度和出度相等，但除了两个点，其中一个入度比出度多 $1$，另一个出度比入度多 $1$。

### 5.2. 哈密顿路径 Hamilton Paths {#52-哈密顿路径-hamilton-paths}

-   **哈密顿路径(hamilton path)**：经过图 $G$ 每个点恰好一次的简单路径。
-   **哈密顿回路(hamilton circuit)**：经过图 $G$ 每个点恰好一次，但除了第一个点的简单回路。
-   **哈密顿图(hamilton graph)**：包含哈密顿回路的图。

Dirac's Theorem

简单图 $G$ 存在哈密顿回路的一个充分条件是图的顶点数 $\ge 3$ 且每个点的度数 $\ge n/2$。

Ore's Theorem

简单图 $G$ 存在哈密顿回路的一个充分条件是图的顶点数 $\ge 3$，且对于对于所有不相邻的顶点 $u$ 和 $v$，他们的度数之和总是 $\ge n$。

Theorem

简单图 $G$ 存在哈密顿路径的必要条件有：

(1) $G$ 是连通的。

(2) 有至多两个点的度数小于 $2$。

简单图 $G$ 存在哈密顿回路的必要条件有：

(1) $G$ 是连通的。

(2) 每个点的度数都大于 $1$。

所以我们在构建哈密顿回路的过程中，有一些性质可以被利用：

-   如果有一个点的度数恰好为 $2$，那么其两条边都一定在哈密顿回路上。
-   如果在构建哈密顿回路的过程中，某个点的两条边已经被确认在哈密顿回路上，他们它剩下的边可以被删去。

Erdős–Stone Theorem

对于一个图 $G=(V,E)$，其存在哈密顿回路的必要条件是：对于 $V$ 的子集 $S$，图 $G - S$ 中的连通分量数量 $\leq |S|$。其中 $G-S$ 是指从图 $G$ 中删除点集 $S$ 和其相连的边后得到的子图。

-   **证明思路**：考虑一个 $n$ 个点的环，拿掉其中 $m$ 个点后至多有 $m$ 个联通快。

**旅行商问题(traveling salesman problem)**：求解在给定的图中，找出一条路径，使得旅行商从一个城市出发，经过其他所有城市一次且仅一次后，返回出发城市且总费用最小。

### 5.3. 最短路问题 Shortest Path Problems {#53-最短路问题-shortest-path-problems}

**带权图(weighted graph)**：$G = (V,E,W)$，每条边有一个边权。

**最短路问题(shortest path problem)**：在带权图 $G=(V,E,W)$ 中，对于给定的两点 $a,z \in V$，找到一条 $a$ 到 $z$ 的路径使其长度（即所经过边的边权和）最短。

关于 Dijkstra 算法的讲解略去。

### 5.4. 平面图 Planar Graphs {#54-平面图-planar-graphs}

Definition: **平面图(planar graph)**

如果一张图可以被画到一个平面上且没有任何边在非定点处交叉，则称这张图是 planar 的。

这样的画法被称为一个图的**平面表示(planar representation)**。

**区域(region)**：在平面表示中，与平面的其他部分通过平面图的边分割开来的一部分，称为区域。区域分为**有界区域(bounded region)** 和**无界区域(unbounded region)** 两种。（注意对于一个封闭图形，则封闭图形外面的区域也称一块区域）

**区域的度(degree of the region)**：在区域 $R$ 的边界上的边的数量，记为 $\operatorname{Deg}(R)$，这一定义对于有界区域和无界区域都相同。

**欧拉公式(Euler's formula)** ★

设 $G$ 是有 $v$ 个点和 $e$ 条边的简单连通平面图，设 $r$ 为其平面表示中的区域数量，则满足

$r=e-v+2$

注意到需要将一个区域划分出来，至少需要三条边；而每条边恰会属于两个区域的边界，即 $r\le \dfrac{2}{3} e$。将这一结论代入欧拉公式，可以得到如下推论：

Corollary 1 ★

如果 $G$ 是有 $v$ 个点和 $e$ 条边的简单连通平面图且 $v\ge 3$，则必定满足 $e\le 3v-6$。

-   当每个区域的度都恰好为 $3$ 时取等号。
-   如果进一步要求每个区域的度数至少为 $k$ 时，可以得到通式 $e \le \dfrac{(v-2)k}{k-2}$。

Corollary 2 ★

如果 $G$ 是简单连通平面图，则 $G$ 存在一个度数不超过 $5$ 的节点。

**基本细分(elementary subdivision)**：在原来的一条边中插入一个节点，将一条边分为两条边。

**同胚(homeomorphic)**：如果图 $G_1$ 和 $G_2$ 可以分别作一系列基本细分操作，得到一张相同的图，则称 $G_1$ 和 $G_2$ 是同胚的。

![fHHobbG5.png](../../../assets/notes/422f2c9d6b339c79317c.png)

Kuratowski's Theorem ★

一个无向图 $G$ 是平面的当且仅当其没有一个子图与 $K_5$ 或 $K_{3,3}$ 同胚。

### 5.5. 图染色与对偶图 Graph Coloring and Dual Graphs {#55-图染色与对偶图-graph-coloring-and-dual-graphs}

**对偶图(dual graph)**：任何一张平面图可以转化为其对偶图，通过如下步骤：

-   将原图的每一个区域用一个顶点表示。
-   对于所有仅相隔一条边（只有定点相邻的不算）的两个相邻的区域，在他们对应的顶点直接添加一条边。

![ubH4EMQH.png](../../../assets/notes/2fccd259a700719dac8a.png)

对于平面图染色的问题的研究，可以转化到其对应的对偶图上。

**四色定理(the four color theorem)**

-   **染色(coloring)**：对每个顶点分配一个颜色，满足相邻两节点的颜色不同。
-   **染色数(the chromatic number)**：至少需要多少种不同的颜色，才能将给定图 $G$ 染色。记为 $x(G)$。

四色定理指出，任意平面图的染色数不超过 $4$。

Theorem

-   染色数为 $2$ 的简单图一定是二分图。

-   连通二分图的染色数一定为 $2$。
