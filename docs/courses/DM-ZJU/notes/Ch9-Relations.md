---
tags:
- relation
title: Ch9-Relations
---
!!! quote
    ***Logic demands you face yourself before you can ever fairly face another.***

    [!abstract] 
    本篇笔记主要介绍了二元关系的定义、表示方法及其特殊性质，包括自反性、对称性、传递性等。还介绍了关系的组合、复合、逆关系及其闭包，最后探讨了等价关系和偏序关系的概念及其相关定理。通过这些内容，读者可以深入理解关系在集合论中的重要性及其应用。<small>（由 gpt-4o-mini 生成摘要）</small>


## 1\. 二元关系 Binary Relations {#1-二元关系-binary-relations}


!!! def
    A **二元关系(binary relation)** $R$ from a set $A$ to a set $B$ is a subset of $A\times B$.

    -   关系是集合：“A binary relation $R$” is a set.
    -   $R\subseteq A\times B$
    -   $R=\{(a,b)\mid a\in A, b\in B, a\;R\;b\}$.
    -   “A relation on set $A$” means a relation from set $A$ to itself.


Question: How many binary relations are there on a set $A$ with $n$ elements?

$2^{n^2}$

关系的证明题的解题思路

-   利用定义。
-   利用数学归纳法。


!!! lemma
    - The graph of function $f$ from set $A$ to set $B$ is a relation from $A$ to $B$.
    - 一个关系 $R \subseteq A \times B$ 要成为函数 $f: A \to B$ 的图像，必须满足：对于 $A$ 中的每个元素 $a$，在 $R$ 中**恰好有且仅有一个**有序对 $(a, b)$。


### 1.1. 表示方法 Represent Methods {#11-表示方法-represent-methods}

- 基础的表示方法：列出所有序偶、谓词描述

#### 1.1.1. 关系表 2D Table {#111-关系表-2d-table}

举个例子，$R$ 是一个二元关系，表示两个集合中按位或不为零的对：

$\begin{aligned} A  =\{2,&3,4\},B=\{2,3,4,5,6\} \quad R = \{(x,y) \mid x \in A,\ y \in B,\ x \mid y\} \\ &\implies R =\{(2,2),(2,4),(2,6),(3,3),(3,6),(4,4)\} \end{aligned}$


!!! tip
     **$a \mid b$** 表示 **“$a$ 整除 $b$”** 




    $$b = a \cdot k$$


    也就是说，$b$ 除以 $a$ 的余数为 $0$


可以 表示二元关系：

![jHqiS9Pb.png](../../../assets/notes/f768a7f9fa79281e6644.png)

#### 1.1.2. 有向图 Directed Graph {#112-有向图-directed-graph}

关系 $(V,E)$ 对应的**有向图(directed graph = digraph)** 是将 $V$ 作为点集，$E$ 作为边集的图。

对于一条边 (edges or arcs)$(a,b)$，$a$ 被叫作其**起始节点(initial vertice)**，$b$ 被叫作其**终止节点(terminal vertice)**。

#### 1.1.3 关系矩阵 / 0-1矩阵 (Connection matrix / Zero-one matrix) {#113-关系矩阵-0-1矩阵-connection-matrix-zero-one-matrix}
这是二维表格的数学化表示。如果元素 $a_i$ 与 $b_j$ 有关系，则矩阵对应位置记为 **1**；否则记为 **0**。
*   **示例**：


    $$M_R = \begin{bmatrix} 1 & 1 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$$



!!! hint
    若$A$和$B$中不是整数 $\rightarrow$将其中的元素映射成矩阵位置

### 1.2. 二元关系的特殊性质 Special Properties of Binary Relations {#12-二元关系的特殊性质-special-properties-of-binary-relations}

| 性质                      | 条件                                                                                   | 备注                       | 举例                  |
| ----------------------- | ------------------------------------------------------------------------------------ | ------------------------ | ------------------- |
| **自反性(reflexive)**      | $\forall x (x\in A\rightarrow (x,x)\in R)$                                           | $(\mathbb Z, =)$         |                     |
| **非自反性(irreflexive)**   | $\forall x (x\in A\rightarrow (x,x)\not\in R)$                                       | $(\mathbb Z, \neq)$      |                     |
| **对称性(symmetric)**      | $\forall x\forall y((x,y)\in R\rightarrow (y,x)\in R)$                               | $(\mathbb Z_+, \perp)$   |                     |
| **反对称性(antisymmetric)** | $\forall x \forall y((x,y)\in R \land (y,x)\in R\rightarrow x = y)$                  | 与非对称性的差别在于允许有自环。         | $(\mathbb Z, \leq)$ |
| **非对称性(asymmetric)**    | $\forall x \forall y ((x,y) \in R \rightarrow \lnot ((y,x)\in R))$                   | 与反对称性的差别在于不允许有自环，是更强的条件。 | $(\mathbb Z, <)$    |
| **传递性(transitive)**     | $\forall x \forall y \forall z ((x,y)\in R \land (y,z)\in R \rightarrow (x,z)\in R)$ | $x\rightarrow y$         | $(\mathbb Z, \leq)$ |


!!! important "二元关系的矩阵性质"
    ###### Reflexive
    主对角线全1，$\forall i, m_{ii} = 1$
    ###### Irreflexive
    主对角线全0，$\forall i, m_{ii} = 0$
    ###### Symmetric
    矩阵是对称矩阵 $M = M^T$，即 $m_{ij} = 1$ 则 $m_{ji} = 1$
    ###### Antisymmetric
    除了对角线，没有两个对称的1   
    $M \land M^T \leq I$
    ###### Asymmmetric
    主对角线全0，而且没有对称的1
    $M \land M^T = \mathbf{0}$
    ###### Transitive
    $M \odot M \leq M$
    ==原理：实际上，$M$的平方即是在寻找路径长度为2的关系==

    [!caution]

    Is a relation $R$ is reflexive if it is symmetric and transitive?

    Yet a wrong proof

    $(a,b) \in R$ and $R$ is symmetric implys $(b,a) \in R$.

    $(a,b) \in R$, $(b,a)\in R$ and $R$ is transitive $(a,a) \in R$.

    Which means that $R$ is reflexive.

    ==Incorrect==. Because **it cannot be guaranteed that for all $a \in S$, there exists a $b$ such that $(a,b)\in R$**. Therefore, there might exist such an $a\in R$ for which there is no relation concerning $a$."

    [!question] 传递关系序列


    $$T_n = \sum_{k=1}^n S(n, k) \cdot P(k)$$



    其中：
    *   **$S(n, k)$** 是**第二类斯特林数，它代表将 $n$ 个有标签元素放入 $k$ 个无标签非空子集（即“划分”）的方法数。
    *   **$P(k)$** 是 $k$ 个元素上的偏序关系数。
    它没有简单的闭项公式，具体数列可以参考[oeis——一个数列百科](https://oeis.org/A000798)


## 2\. 组合关系 Combining Relations {#2-组合关系-combining-relations}

因为定义在集合 $A, B$ 上的任意关系 $R$ 是 $A\times B$ 的子集，我们可以对关系定义任意组合运算。
==本质：将关系代数化处理。集合运算代表逻辑运算，而后两者是因为关系实质是上多个集合的运算才出现的==

### 2.1. 集合运算 Set Operations {#21-集合运算-set-operations}

定义在关系上的集合运算可以直接类比集合上的集合运算，然后再将集合运算转化为逻辑运算。

Let $A=\{a_1,a_2,\cdots,a_n\}$, $B=\{b_1,b_2,\cdots,b_n\}$, $M_{R_1} = [c_{ij}]$, $M_{R_2}=[d_{i,j}]$, the set operations of two relations are defined by

$\begin{aligned} M_{R_1 \cup R_2} &= [c_{ij} \lor d_{ij}] = M_{R_1} \lor M_{R_2} \\ M_{R_1 \cap R_2} &= [c_{ij} \land d_{ij}] = M_{R_1} \land M_{R_2}\\ M_{\overline{R_1}}&=[\overline{c_{ij}}]\\ M_{R_1-R_2} &= M_{R_1\cap \overline{R_2}} = [c_{ij} \land \overline{d_{ij}}]\\ \end{aligned}$

### 2.2. 关系的复合 Composition of Relations {#22-关系的复合-composition-of-relations}

对于关系 $R=\{(a,b)\mid a\in A,b\in B,aRb\}$ 和关系 $S=\{(b,c)\mid b\in B, c\in C, bSc\}$，定义 **$S$ 与 $R$ 的复合(the composite of $R$ and $S$)** 为：

$S \circ R =\{(a,c)\mid a\in A \land c\in C \land \exists b(b\in B\land aRb \land bSc)\}$

-   关系合成运算满足结合律：$(R\circ Q)\circ S = R \circ (Q \circ S)$。
- 注意$S$和$R$的先后，复合运算不满足交换律

- 

$$M_{S \circ R} = M_R \odot M_S$$


- 因为有中间集合的存在，所以一定合法

于此我们还可以递归定义**关系的幂(the power of relation)**：

$R^1=R,\text{ and }R^{n+1}=R^n\circ R$


!!! theorem
    The relation $R$ on a set $A$ is transitive if and only if $R^n \subseteq R,\, n=1,2,3,\ldots$.

    Proof

    (1) $\forall n (R^n\subseteq R) \Rightarrow R \text{ is transitive}$

    $(a,b)\in R$，$(b,c)\in R$，故 $(a,b)\in R^2$；由于 $R^2\subseteq R$，可以得到 $(a,c)\in R$，故 $R\text{ is transitive}$。

    (2) $R\text{ is transitive} \Rightarrow \forall n (R^n \subseteq R)$

    使用数学归纳法，对于所有 $(a,b)\in R^{n+1}=R^n\circ R$，那么 $(a,x)\in R^n\subseteq R,\ (x,b)\in R$ 且 $R$ 有传递性可以推出 $(a,b)\in R$。


### 2.3. 逆关系 Inverse Relations {#23-逆关系-inverse-relations}

对于定义在集合 $A$ 到 $B$ 上的关系 $R=\{(a,b)\mid a\in A,b\in B,aRb\}$，我们可以定义 $B$ 到 $A$ 的**逆关系(inverse relation)**：

$R^{-1} = \{(b,a) \mid (a,b)\in R ,a\in A,b\in B\}$


!!! note "和线性代数的联系"
    在关系矩阵中，逆关系矩阵即是原关系矩阵的转置


$$M_{R^{-1}} = (M_R)^T$$


> 在线性代数中，定义如下，此时的矩阵的逆是为了在多元空间中实现除法

$$M \cdot M^{-1} = I \quad (\text{单位矩阵})$$


> 当这个关系是一个“双射函数”（一一对应）时，此时的关系矩阵是一个置换矩阵（Permutation Matrix），在置换矩阵中，每一行和每一列都恰好只有一个 $1$


一些关于逆关系的恒等式（利用集合的证明思路即可）

设 $R,S$ 是从集合 $A$ 到集合 $B$ 上的关系，$T$ 是从集合 $B$ 到集合 $C$ 的关系，$P$ 是从集合 $C$ 到集合 $D$ 的关系。

-   $(R \cup S)^{-1} = R^{-1} \cup S^{-1}$
-   $(R\cap S)^{-1} = R^{-1} \cap S^{-1}$
-   $(\overline R)^{-1} = \overline{R^{-1}}$
-   $(R-S)^{-1} = R^{-1} - S^{-1}$
-   $(A\times B)^{-1} = B \times A$：

-   $\overline R= A \times B - R$
-   $(S \circ T)^{-1} = T^{-1} \circ S^{-1}$
-   $(R \circ T) \circ P = R \circ (T \circ P)$
-   $(R \cup S) \circ T = R \circ T \cup S \circ T$

## 3\. 关系的闭包 Closures of Relations {#3-关系的闭包-closures-of-relations}


!!! def "关系的闭包"

    The **闭包(closure)** of a relation $R$ with respect to property $P$ is the relation $S$ with property if and only if

    (1) $S$ contains $R$;

    (2) $S$ is a subset of every relation **that contains $R$** with property $P$.

    (3) $S$ is the smallest relation satisfying (1) and (2).




$$\forall T \quad \Big( \big( T \supseteq R \land P(T) \big) \implies S \subseteq T \Big)$$

 or 

$$S = \bigcap \{ T \mid T \supseteq R \land P(T) \}$$



### 3.1. 自反闭包 Reflexive Closure {#31-自反闭包-reflexive-closure}

给定关系 $R$，其**自反闭包(reflexive closure)** 是在 $R$ 上添加元素，使得对于每一个元素 $a$，都有 $(a, a)$ 在 R 中。


!!! theorem

    关系 $R$ 的自反闭包用 $r(R)$ 表示，且满足 $r(R) = R \cup I_A$。

    -   这里 $I_A$ 表示集合 $A$ 上的对角线关系，即 $I_A = \{(x,x) \mid x \in A\}$。

    Proof

    ![](../../../assets/notes/4e7be36dbd399ef5d996.png)

    [! Corollary]

    $R = R \cup I_A$ 当且仅当 $R$ 是自反关系。

    Proof


![](../../../assets/notes/7e44e0c7c37850117fa5.png)

### 3.2. 对称闭包 Symmetric Closure {#32-对称闭包-symmetric-closure}

给定关系 $R$，其**对称闭包(symmetric closure)** 是在 $R$ 上添加元素，使得对于每一对元素 $(a, b)$，如果 $(a, b)$ 在 R 中，那么 $(b, a)$ 也在 $R$ 中。


!!! theorem

    关系 $R$ 的对称闭包用 $s(R)$ 表示，且满足 $s(R) = R \cup R^{-1}$。

    Proof

    ![](../../../assets/notes/aaad989e928996af9d2d.png)

    ![](../../../assets/notes/390011c95c1baea7d43a.png)

    [!corollary]

    $R = R \cup R^{-1}$ 当且仅当 $R$ 是对称关系。


### 3.3. 传递闭包 Transitive Closure {#33-传递闭包-transitive-closure}

给定关系 $R$，其**传递闭包(transitive closure)** 是在 $R$ 上添加元素，使得对于每一对元素 $(a, b)$ 和 $(b, c)$，如果 $(a, b)$ 和 $(b, c)$ 在 $R$ 中，那么 $(a, c)$ 也在 $R$ 中。


!!! theorem

    设 $R$ 是定义在 $A$ 上的关系，则有一条从 $a$ 到 $b$ 的长度为 $n$ 的路径当且仅当 $(a,b) \in R^n$。

    一些来自下一章的概念：

    -   A **路径(path)** of length $n$ in a digraph $G$: A sequence of edges $(x_0,x_1),(x_1,x_2),\ldots,(x_{n-1},x_n)$.
    -   **环(cycle)**: A path of length $n$ with $x_0=x_n (n\ge 1)$.

    Proof (by induction)

    ![](../../../assets/notes/20ddae621e3ba084d548.png)

    [!Theorem]

    The **传递闭包(transitive closure)** of a relation $R$ is $t(R) = R^\ast$.

    Definition: 连通关系

    **连通关系(connectivity relation)** 是所有可通过 $R$ 上的边连通的有序对的集合，即：

    $R^\ast = \displaystyle{\bigcup_{i=1}^\infty R^i}$

    Proof

    证明 $R^\ast$ 是 $R$ 的传递闭包：

    (1) $R \subseteq R^\ast$。

    (2) $R^\ast$ is transitive：对于任意 $(a,b) \in R^\ast \land (b,c) \in R^\ast$，有一条从 $a$ 到 $b$ 的路径和一条从 $b$ 到 $c$ 的路径，那自然也有一条从 $a$ 到 $c$ 的路径，故 $(a,c) \in R^\ast$。

    (3) $R^\ast$ is the smallest：对于任意 $S$ 满足 $S$ 具有传递性且 $R\subseteq S$。我们有 $R^\ast \subseteq S^\ast = S$，故 $R^\ast \subseteq S$，得证。

    实际上，通过 $R^\ast = \displaystyle{\bigcup_{i=1}^n R^i}$ 即可计算，因为根据鸽笼原理可以证明，长度 $>n$ 的环至少有一个环。

    [!algorithm]

    ##### Floyd-Warshall 算法
    ![](../../../assets/notes/89c189d210ac45a77db3.png)
    k控制：允许经过中间节点的最大编号
    $O(n^3)$ 
    ##### bitset优化的Warshall算法


## 4\. 等价关系 Equivalence Relations {#4-等价关系-equivalence-relations}

Definition: Equivalence relation

A relation $R$ on a set $A$ is an **等价关系(equivalence relation)** if $R$ is (1) reflexive; (2) symmetric; (3) transitive.

We call $a$ and $b$ is **等价的(equivalent)** if $(a,b) \in R$, denoted as $a\sim b$.

如果我们想要证明一个关系是等价关系，通常可以通过证明这一关系满足以上三个性质。

### 4.1. 等价类 Equivalence Classes {#41-等价类-equivalence-classes}

Definition: Equivalence class

The **等价类(equivalence class)** of $x$: the set of all elements that is equivalent to $x$, denoted as $[x]_R$ or $[x]$.

Theorem

如果 $R$ 是集合 $A$ 上的等价关系，则以下三个命题等价：

(1) $aRb$

(2) $[a]=[b]$

(3) $[a]\cap[b] \neq \emptyset$

Note

(2) 和 (3) 的区别在于我们需要说明 $[a]$ 和 $[b]$ 不是空集。

Proof

![](../../../assets/notes/0cc4f3614a6b1e239d94.png)

![](../../../assets/notes/fd2a72ba856da4cae5ac.png)

Theorem 1

设 $R_1,R_2$ 是集合 $A$ 上的等价关系，则 $R_1 \cap R_2$ 也是集合 $A$ 上的等价关系。

Theorem 2

设 $R_1,R_2$ 是集合 $A$ 上的等价关系，则 $R_1 \cup R_2$ 具有自反性和对称性。进一步的，$(R_1\cup R_2)^\ast$ 是集合 $A$ 上的等价关系。

### 4.2. 划分 Partitions {#42-划分-partitions}

Definition: Partition

A **划分(partition)** of set $A$ is a collection of disjoint nonempty subsets of $A$ that have $A$ as their union, denoted as $pr(A) = \{A_1,A_2,\cdots A_n\}$.（两两不交，并为全集）

Theorem

Let $R$ be an equivalence relation on a set $A$. Then the equivalence classes of $R$ form a partition of $A$.

Conversely, given a partition $\{A_i\mid i \in I\}$ of the set $A$, there is an equivalence relation $R$ that has the sets $A_i,i\in I$, as its equivalence classes.

集合 $A$ 的所有等价类是原集合的一个划分；任给一个划分存在一个关系 $R$ 使得划分出的每个子集都是等价类。

## 5\. 偏序关系 Partial Orderings {#5-偏序关系-partial-orderings}

### 5.1. 偏序集 Poset {#51-偏序集-poset}

Definition: Partial ordering

A relation $R$ on a set $A$ is an **偏序关系(partial ordering)** if $R$ is (1) reflexive; (2) antisymmetric; (3) transitive.

Notation:

-   $(S,R)$: partially ordered set or **偏序集(poset)**.
-   $a\preccurlyeq b$: $(S,R)$ is a poset and $(a,b) \in R$.

如 $(\mathbb Z, \leq)$ 对应的关系为 $R=\{(a,b)\mid a,b\in \mathbb Z\land a\le b\}$。

### 5.2. 字典序 Lexicographic Order {#52-字典序-lexicographic-order}

Definition: **字典序(lexicographic order)**

Given two posets $(A_1,\preccurlyeq_1)$ and $(A_2,\preccurlyeq_2)$, the lexicographic ordering on $A_1\times A_2$ is defined by specifying that $(a_1,a_2)$ is less than $(b_1,b_2)$, that is, $(a_1, a_2)\prec (b_1,b_2)$, either if $a_1 \prec_1 b_1$ or if $a_1 =_1 b_1$ and $a_2 \prec_2 b_2$.

相当于就是从高位到低位依次比较大小。这是定义在两个偏序集的笛卡尔积上，可以通过此定义递推得到多个偏序集的笛卡尔积的字典序的定义。

Theorem

由多个偏序集的笛卡尔积得到的字典序是一个偏序关系。

### 5.3. 哈斯图 Hasse Diagrams {#53-哈斯图-hasse-diagrams}

**Hasse 图(Hasse diagram)** 是一种表示偏序集或者格的图形工具。构架 Hasse 图的步骤如下：

1.  根据偏序集 $(A,R)$ 构造有向图，并使所有边都指向上方。（一般来说 Hasse 图是上大下小的）
2.  消除所有的自环。
3.  消除所有可由偏序集的传递性导出的边。
4.  消除所有边的箭头，因为所有的边都应该是指向上方的。

Definition: maximal/minimal elements

设 $(A,\preccurlyeq)$ 是一个偏序集，称 $a$ 是一个**最大元素(maximal element)** 当且仅当 $A$ 中不存在元素 $b$ 满足 $a \prec b$。称 $a$ 是一个**最小元素(minimal element)** 当且仅当 $A$ 中不存在元素 $b$ 满足 $b\prec a$。

显然，最小元素和最大元素可能不止一个。进一步地，在任意有限偏序集中，其最大元素和最小元素一定存在。体现在 Hasse 图中，则最大元素是位于其顶端的点，最小元素是位于其底端的点。正确性显然。

Definition: greatest/least element

设 $(A,\preccurlyeq)$ 是一个偏序集，称 $a$ 是其**最大值(greatest element)** 当且仅当对于每个 $A$ 中的元素 $b$ 都有 $b \preccurlyeq a$；称 $a$ 是其**最小值(least element)** 当且仅当对于每个 $A$ 中的元素 $b$ 都有 $a \preccurlyeq b$。

偏序集的最大值和最小值不一定存在，且如果存在则一定是唯一的。

Definition: upper/lower bounds

设 $(S,\preccurlyeq)$ 是一个偏序集，$A \subset S$。若存在一个 $S$ 中的元素 $a$ 满足对于 $A$ 中的所有元素 $b$ 都有 $b\preccurlyeq a$，则称 $a$ 是 $A$ 的一个**上界(upper bound)**。若存在一个 $S$ 中的元素 $a$ 满足对于所有 $A$ 中的元素 $b$ 都有 $a\preccurlyeq b$，则称 $a$ 是 $A$ 的一个**下界(lower bound)**。

类似的，上下界可能不止一个，也可能不存在。

可以通过 Hasse 图帮助我们找到子集的上下界。

![Hasse 图示例](../../../assets/notes/ad58ffefa09f99bd0192.png)Hasse 图示例

Definition: least upper bound / greatest lower bound

如果 $a$ 是子集 $A$ 的上界中最小的，则称其是 $A$ 的**最小上界(least upper bound)**，记为 $\text{lub}(A)$。如果 $a$ 是子集 $A$ 的下界中最大的，则称其是 $A$ 的**最大下界(greatest lower bound)**。

### 5.4. 链 Chain {#54-链-chain}

Definition: comparable / incomparable

The elements $a$ and $b$ of a poset $(S,\preccurlyeq)$ are **可比较的(comparable)** if either $a\preccurlyeq b$ or $b\preccurlyeq a$. When $a$ and $b$ are elements of $S$ so that neither $a\preccurlyeq b$ nor $b\preccurlyeq a$, then $a$ and $b$ are called **不可比较的(incomparable)**.

对于偏序集 $(S,R)$ 如果集合 $S$ 中的元素两两都是可比较的，那么认为 $S$ 是**全序的(total ordered)** 或者说**线性关系(linear order)**。

Definition: Chain

$(A,\preccurlyeq)$ 是一个偏序集，$B\subseteq A$。如果 $(B,\preccurlyeq)$ 是全序的，则称 $B$ 是 $A$ 的一条**链(chain)**。

Definition: Antichain

$(A,\preccurlyeq)$ 是一个偏序集，$B\subseteq A$。如果 $\forall a, b ,\in B(a \neq b),\space (a, b)\not\in R, (b, a)\not\in R$，则称 $B$ 是 $A$ 的一条**反链(antichain)**。

### 5.5. 良序集 Well-ordered Sets {#55-良序集-well-ordered-sets}

Definition: Well-ordered set

一个偏序集 $(A,R)$ 是**良序集(well-ordered set)** 当且仅当其每一个非空子集都有一个最小值。

一个良序集一定是一个**全序集(totally ordered set)**。

### 5.6. 格 Lattices {#56-格-lattices}

Definition: Lattices ★

一个偏序集被称为**格(lattice)** 当且仅当其每一对元素都有一个最小上界和最大下界。

如 $(\mathbb Z^+, \mid)$ 是一个格，对于其任意一对元素 $(x,y)$，他们的 lub 为他们的**最小公倍数(least common multiple)**，记为 $\text{lcm}(x,y)$；他们的 glb 为他们的**最大公因数(great common divisor)**，记为 $\gcd(x,y)$。
