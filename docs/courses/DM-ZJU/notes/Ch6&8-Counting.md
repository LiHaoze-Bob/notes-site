---
title: Ch6&8-Counting
---
Ch6&8 Counting

2024 年 4 月 2 日

> 本篇笔记涵盖了计数原理的基本概念，包括加法原理、乘法原理、容斥原理和树形图等。接着介绍了鸽笼原理及其广义形式，排列组合的定义和计算方法，以及如何处理重复元素的排列和组合。还探讨了将对象分配到盒子中的不同情况，组合恒等式的应用，以及递推关系的定义和解法。最后，生成函数的概念及其在计数问题和递推关系中的应用也得到了阐述。<small>（由 gpt-4o-mini 生成摘要）</small>

## 1\. 计数原理 Counting Principles {#1-计数原理-counting-principles}

### 1.1. 加法原理 The Sum Rule {#11-加法原理-the-sum-rule}

**加法原理(the sum rule)**：If $S$ and $T$ are **不相交的(disjoint)** finite sets, then

$|S\cup T| = |S| +|T|$

### 1.2. 乘法原理 The Product Rule {#12-乘法原理-the-product-rule}

**乘法原理(the product rule)**：If $S$ and $T$ are finite sets, then

$|S \times T| = |S| \times |T|$

Here $S \times T$ denotes the Cartesian product of sets $S$ and $T$.

### 1.3. 容斥原理 The Inclusion-Exclusion principle {#13-容斥原理-the-inclusion-exclusion-principle}

**容斥原理(the inclusion-exclusion principle = subtraction rule)**：If $S$ and $T$ are finite sets, then

$|S\cup T| = |S| + |T| - |S\cap T|$

### 1.4. 树形图 Tree Diagrams {#14-树形图-tree-diagrams}

一种用**树形图(tree diagram)** 来计数的思想：To use trees in counting, we use a branch to represent each possible choice. We represent the possible outcomes by the leaves.

Chapter 6.1 - Example 9

How many bit strings of length four do not have two consecutive 1s?

Solution

![](../../../assets/notes/9beed1d4ebb6030b53d4.png) There are $8$ bit strings of length four without two consecutive 1s.

## 2\. 鸽笼原理 The Pigeonhole Principle {#2-鸽笼原理-the-pigeonhole-principle}

**鸽笼原理(the pigeonhole principle)**

If $k$ is a positive integer and $k+1$ or more objects are placed into $k$ boxes, then there is at least one box containing two or more of the objects.

**广义鸽笼原理(the generalized pigeonhole principle)**

If $n$ objects are placed into $k$ boxes, then there is at least one box containing at least $\lceil n/k \rceil$ objects.

Chapter 6.2 - Example 6

Every sequence of $n^2+1$ distinct integers contains a subsequence of length $n + 1$ that is either strictly increasing or strictly decreasing.

Solution by myself

Dilworth 定理指出，对于任意有限偏序集，其最长反链长度必等于最小链划分中链的数目。故命题“最长上升子序列的长度为 $n$” 的对偶命题为“非升子序列的最小划分数为 $n$”。

对于原数列，若其最长上升子序列的大于等于 $n+1$，则问题解决；否则存在一组 $n$ 个下降子序列的划分。根据鸽笼原理，其中至少有一个的长度大于 $n$，即可找到一个长度大于等于 $n+1$ 的下降子序列。

Solution by teacher

反证法：用 $(x_i,y_i)$ 表示第 $i$ 个位置开始的最长上升子序列长度和最长下降子序列长度，根据鸽笼原理，必存在 $i,j$ 满足 $(x_i,y_i) = (x_j,y_j)$，而 $a_i \neq  a_j$，故矛盾。

![](../../../assets/notes/efa223aff2ad4c7a7a07.png)

![](../../../assets/notes/d2d2f0e575ed8cadad33.png)

## 3\. 排列组合 Permutations and Combinations {#3-排列组合-permutations-and-combinations}

### 3.1. Introduction {#31-introduction}

Definition: Permutation

A **排列(permutation)** of a set of _distinct_ objects is an _ordered_ arrangement of these objects.

An r-permutation is an _ordered_ arrangement of $r$ elements of a set, denoted by $P(n,r)$.

$P(n,r) = {n\times (n-1)\times \cdots \times (n-r+1)}$

Definition: Combination

A r-**组合(combination)** of elements of a set is an _unordered_ selection of $r$ elements from the set, denoted by $C(n,r) = \displaystyle\binom n r$.

$C(n,r) = \frac{P(n,r)}{P(r,r)} = \frac{n\times (n-1)\times \cdots \times (n-r+1)}{r\times (r-1)\times \cdots \times 1}$

### 3.2. Permutation and Combination with Repetition {#32-permutation-and-combination-with-repetition}

**$r$\-permutation with repetition**：The number of $r$\-permutations of a set of $n$ objects with repetition allowed is

$n^r$

**$n$\-permutation with limited repetition**：The number of different permutations of $n$ objects, where there are $n_1$ indistinguishable objects of type1, …, and $n_k$ indistinguishable objects of type $k$, is

$\frac{n!}{n_1!n_2!\cdots n_k!}$

**$r$\-circle permutation**：The number of $r$\-circle permutations of a set of $n$ objects is

$\frac{P(n,r)}{r}$

![](../../../assets/notes/081e55519d2e2a46fe0d.png)

**$r$\-combination with repetition**：The number of $r$\-combination from a set with $n$ elements when repetition of elements is allowed is

$\binom{n+r-1}{r}$

这个就是隔板法大家懂的都懂。

### 3.3. Distributing Objects into Boxes {#33-distributing-objects-into-boxes}

**Distinguishable objects and distinguishable boxes**：The number of ways to distribute $n$ distinguishable objects into $k$ distinguishable boxes so that $n_i$ objects are place into box $i$, $i=1,2,\cdots,k$, equals

$\frac{n!}{n_1! n_2! \cdots n_k!}$

**Distinguishable objects and indistinguishable boxes**：The number of ways to distribute $n$ distinguishable objects into $k$ indistinguishable boxes is

$\sum_{j=1}^k S(n,j) = \sum_{j=1}^k \left( \sum_{i=0}^{j-1} \binom{i}{j} \frac{(-1)^i (j-i)^n}{j!}  \right)$

需要引入第二类斯特林数。但一般来说，不搞斯特林数那一套，手动枚举一下可能的隔板情况，并利用组合数进行统计的做法更为高效。

**Indistinguishable objects and distinguishable boxes**：The number of ways to distribute $n$ indistinguishable objects into $k$ distinguishable boxes is

$\binom{n-1}{k-1}$

还是使用隔板法。

**Indistinguishable objects and indistinguishable boxes**：The number of ways to distribute $n$ indistinguishable objects into $k$ indistinguishable boxes is

### 3.4. 组合恒等式 Combinatorial Indentities {#34-组合恒等式-combinatorial-indentities}

Theorem 1: **二项式定理(the binomial theorem)**

Let $x$ and $y$ be variables, and let $n$ be a nonegative integer. Then

$(x+y)^n = \sum_{j=0}^n \binom{n}{j} x^{n-j} y^j$

可以得到以下推论：

$\sum_{k=0}^n \binom{n}{k} = 2^n$

$\sum_{k=0}^n (-1)^k \binom {n}{k} = 0$

Theorem 2: **帕斯卡恒等式(PASCAL's identity)**

Let $n$ and $k$ be positive integers with $k\le n$. Then

$\binom{n+1}{k}=\binom{n}{k-1}+\binom{n}{k}$

Theorem 3: **范德蒙德恒等式(Vandermonde's indentity)** ★

Let $m,n$ and $r$ be nonnegative integer with $r$ not exceeding either $m$ or $n$. Then

$\binom{m+n}{r} = \sum_{k=0}^r \binom{m}{r-k}\binom{n}{k}$

可以得到以下推论：

$\binom{2n}{n} = \sum_{k=0}^n \binom{n}{k}^2$

Theorem 4

Let $n$ and $r$ be nonnegative integer with $r \le n$. Then

$\binom{n+1}{r+1} = \sum_{j=r}^n\binom{j}{r}$

## 4\. 组合证明 Combinatorial Proofs {#4-组合证明-combinatorial-proofs}

A **数两次的证明方法(double counting proof)** uses counting arguments to prove that both sides of an identity count the same objects, but in different ways.

A **基于双射的证明方法(bijective proof)** shows that there is a bijection between the sets of objects counted by the two sides of the identity.

利用组合方法证明：$C(n,r)=C(n,n-r)$

![](../../../assets/notes/9bfb31a1934a99adff90.png)

## 5\. 递推关系 Recurrence Relations {#5-递推关系-recurrence-relations}

### 5.1. 递推关系 Recurrence Relations {#51-递推关系-recurrence-relations}

Definition: Recurrence Relations

A **递推关系(recurrence relation)** for the sequence $\{a_n\}$ is an equation that expresses $a_n$ in terms of one or more orf the previous terms of the sequence, namely, $a_0,a_1,\ldots,a_{n-1}$ or all integers $n$ with $n\ge n_0$, where $n_0$ is a nonnegative integer.

$a_n= f(a_0,a_1,a_2,\ldots,a_{n-1}),\quad  n\ge n_0$

满足同一组递推关系的数列可能有很多，我们用**初始条件(initial conditon)** 区分他们。

### 5.2. 线性递推 Linear Recurrence Relations {#52-线性递推-linear-recurrence-relations}

Definition: Linear Homogeneous Recurrence Relation of Degree $k$ with Constant Coefficients

It refers to a recurrence relation in the form

$a_n=c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}$

where $c_1,c_2,\ldots,c_k$ are real numbers, and $c_k\neq 0$.

-   **线性(linear)**：linear combination of previous terms
-   **常系数(constant coefficient)**：the coefficients of $a_i$s are constants
-   **阶(degree)** $k$：$a_n$ 可以看做一个之和_前_ $k$ 项有关的函数。 $a_n$ is a function of the previous $k$ terms of the sequence
-   **齐次(homogeneous)**：等式右边没有非零的常数项。If we put all the $a_i$s on the left side of the equation and everything else on the right side, then the right side is $0$. Otherwise **非齐次(nonhomogeneous)**

Some Examples

![](../../../assets/notes/5fc11935b9ae64a77ae5.png)

我们可以从常系数 $k$ 阶线性齐次递推的递推式中得到他的**特征方程(characteristic equation)**：

$r^k - c_1 r^{k-1} - c_2 r^{k-2} - \cdots - c_k = 0$

和**特征根(characteristic root)**：

$r_1,r_2,\ldots,r_k$

#### 5.2.1. 解常系数线性齐次递推 Solve Linear Homogeneous Recurrence Relation With Constant Coefficients {#521-解常系数线性齐次递推-solve-linear-homogeneous-recurrence-relation-with-constant-coefficients}

Theorem

设 $c_1,c_2,\cdots,c_k$ 为实系数。假设递推关系的特征方程 $r^k-c_1 r^{k-1} - \cdots - c_k=0$ 有 $t$ 个不同的特征根 $r_1,r_2,\cdots,r_t$ 且重复次数分别为 $m_1,m_2,\cdots,m_t$。那么常系数线性齐次递推数列 $\{a_n\}$ 的一个**通解(general solution)** 是

$\begin{aligned} a_n = & \,(\alpha_{1,0} +\alpha_{1,1} n+\cdots+\alpha_{1,m_1-1} n^{m_1-1}) r_1^n\\ + & \,(\alpha_{2,0} + \alpha_{2,1} n + \cdots + \alpha_{2,m_2-1} n^{m_2-1}) r_2^n  \\ + &\, \cdots\\ + & \,(\alpha_{t,0} + \alpha_{t,1} n + \cdots +\alpha_{t,m_t-1} n^{m_t-1}) r_t^n \end{aligned}$

这里通解的系数 $\alpha_{i, j} \,(1\le i\le t,\,1\le j\le m_i)$ 一般采用插值（或者说解线性方程组）的方式求得。

#### 5.2.2. 解常系数线性非齐次递推 Solve Linear Nonhomogeneous Recurrence Relation With Constant Coefficients {#522-解常系数线性非齐次递推-solve-linear-nonhomogeneous-recurrence-relation-with-constant-coefficients}

这一节中我们解决的是形如这样的递推关系（这里 $c_i\,(1\le i\le k)$ 是常实数，$F(n)$ 是一个非恒为零且只与 $n$ 有关的函数）：

$a_n = c_1 a_{n-1} +c_2 a_{n-2} +\cdots + c_k a_{n-k} +F(n)$

Theorem 1

设 $\{a_n^{(p)}\}$ 是常系数线性非齐次递推 $a_n=c_1 a_{n-1} +c_2 a_{n-2}+\cdots c_k a_{n-k}+ F(n)$ 的一个**特解(particular solution)**，那么他的通解可以被表示为 $\{a_n^{(p)}+a_n^{(h)}\}$，这里 $\{a_n^{(h)}\}$ 是常系数线性齐次递推 $a_n=c_1 a_{n-1} +c_2 a_{n-2} +\cdots + c_k a_{n-k}$ 的一个通解。

Proof

![](../../../assets/notes/64c4272b865ce9cff6b4.png)

Theorem 2 ★

假设常系数线性非齐次递推的非齐次部分可以表示为

$F(n)=(b_t n^t + b_{t-1} n^{t-1} + \cdots + b_1 n + b_0) s^n$

那么该非齐次递推的特解遵循以下形式

$n^m (p_t n^t + p_{t-1} n^{t-1} + \cdots + p_1 n + p_0) s^n$

这里 $m$ 表示 $s$ 作为特征方程的解的重数，如果 $s$ 不是特征根则 $m=0$。

一般来说要解的 $F(n)$ 都符合 Theorem 2 的形式，这种情况下先把特解的形式代入递推式，即可求特一组特解 $\{a_n^{(p)}\}$。随后若给了原数列的初始条件，则将其减去 $\{a_n^{(p)}\}$ 中的对应项，从而解得 $\{a_n^{(h)}\}$。

## 6\. 生成函数 Generating Functions {#6-生成函数-generating-functions}

Some Mathematical Terms

-   **$x$ 的 $k$ 次方($x$ to the power of $k$)**：$x^k$
-   **分式分解(partial fraction decomposition)**
-   **一阶导数(the first derivative)**、**二阶导数(the second derivvative)**：“$f(x)$ 的一阶导”用英语说是“the first derivative of $f(x)$”。
-   **卷积(convolution)**

Definition: (Original) Generating Function

The **生成函数(generating function)** for the sequence $a_0,a_1,a_2,\ldots a_k,\ldots$ of read numbers is the infinite series

$G(x) = a_0 + a_1 x + a_2 x^2 + \cdots + a_k x^k + \cdots = \sum_{k=0}^{\infty} a_k x^k$

-   在使用生成函数时，我们不关心其定义域，也不关心其的敛散性。
-   本课程中，我们不学习指数生成函数，狄利克雷生成函数等其他类型的生成函数，故直接用“生成函数”一词默认指代 OGF。

Theorem 1

Let $f(x) = \sum\limits_{k=0}^{\infty} a_k x^k$，$g(x) = \sum\limits_{k=0}^{\infty} b_k x^k$. Then

-   $f(x) + g(x) = \sum\limits_{k=0}^\infty (a_k + b_k) x^k$；
-   $\alpha \cdot f(x) = \sum\limits_{k=0}^\infty \alpha \cdot a_k x^k$；
-   $x \cdot f'(x) = \sum\limits_{k=0}^\infty k \cdot a_k x^k$；
-   $f(\alpha x) = \sum\limits_{k=0}^\infty a_k \alpha^k x^k$；
-   $f(x)g(x) = \sum\limits_{k=0}^\infty \sum\limits_{i=0}^\infty a_k b_i x^{k+i}$。

### 6.1. 广义二项式定理 The Extended Binomial Theorem {#61-广义二项式定理-the-extended-binomial-theorem}

Definition: **广义二项式(extended binomial coefficient)**

Let $u$ be a real number and $k$ a nonnegative integer. Then the extended binomial coefficient is defined by

$\binom{u}{k} = \begin{cases} u(u-1)\cdots (u-k+1)/k! \quad &\text{if } k>0\\ 1\quad&\text{if }k=0 \end{cases}$

Theorem: **广义二项式定理(the extended binomial theorem)** ★

Let $x$ be a real number with $|x|<1$ and let $u$ be a real number. Then

$(1+x)^u  = \sum_{k=0}^\infty \binom{u}{k} x^k$

### 6.2. Some Common Used Generating Functions {#62-some-common-used-generating-functions}

|Sequence|Generating Function|
|---|---|
|$C(n,k)$|$(1+x)^n$|
|$C(n,k) a^k$|$(1+ax)^n$|
|$[k<n]$|$1+x+x^2+\cdots+x^{n-1}=\dfrac{1-x^n}{1-x}$|
|$1$|$\dfrac{1}{1-x}$|
|$a^k$|$\dfrac{1}{1-ax}$|
|$k+1$|$\dfrac{1}{(1-x)^2}$|
|$C(n+k-1,k)$|$(1-x)^{-n}$|
|$(-1)^k C(n+k-1,k)$|$(1+x)^{-n}$|
|$C(n+k-1,k) a^k$|$(1-ax)^{-n}$|
|$\dfrac{1}{k!}$|$e^x$|
|$\dfrac{(-1)^{k+1}}{k}$|$\ln (1+x)$|

### 6.3. 生成函数的应用 Applications of Generating Function {#63-生成函数的应用-applications-of-generating-function}

Example: Solve Counting Problems with Generating Function

Suppose that there are $2r$ red balls, $2r$ blue balls, and $2r$ white balls. How many ways to select $3r$ balls from these balls?

Combinational Solution

容斥原理+隔板法。先不加限制任取，然后减掉某种颜色选超过 $2r$ 个的情况，按理来说还要加上有两个选超但是这已经超过 $3r$ 了故不需要考虑。所以答案是：

$\binom{3r+3-1}{3-1} - 3 \binom{3r-(r-1)+3-1}{3-1}$

Solution by Generating Function

$[x^{3r}] \left( \frac{1-x^{2r+1}}{1-x} \right)^3 = \binom{3r+2}{2}- 3\binom{r+1}{2}$

Example: Solve Recurrence Relations with Generating Function

Use generating functions to solve the recurrence relation $a_n=2a_{n-1} + 3 a_{n-2} + 4^n + 6$ with initial conditions $a_0=20,\,a_1=60$.

Solution

![ydMpu3C0.png](../../../assets/notes/bcfe78ebbbab7e0ada64.png)

![sgMGeqvD.png](../../../assets/notes/4128257ff7f72fed28f2.png)

## 7\. 容斥原理 The Principle of Inclusion-Exclusion {#7-容斥原理-the-principle-of-inclusion-exclusion}

Theorem: The Principle of Inclusion-Exclusion

$\mid A_{1}\cup A_{2}\cup\cdots\cup A_{n}\mid=\sum_{i=1}^{n}|A_{i}|-\sum_{1\leq i<j\leq n}| A_{i}\cap A_{j}|+\sum_{1\leq i<j<k\leq n}| A_{i}\cap A_{j}\cap A_{k}|+\cdots+(-1)^{n+1} | A_{1}\cap A_{2}\cap\cdots\cap A_{n}|$

and an alternative form:

$N(P_1^{\prime}P_2^{\prime}\cdots P_n^{\prime})=N-\left|A_1\cup A_2\cdots\cup A_n\right|=N-\sum_{1\leq i\leq n}N(P_i)+\sum_{1\leq i<j\leq n}N(P_iP_j)+\cdots+(-1)^nN(P_1P_2\cdots P_n)$

### 7.1. Examples {#71-examples}

#### 7.1.1. 埃氏筛 The Sieve of Eratoshenes {#711-埃氏筛-the-sieve-of-eratoshenes}

Example: The sieve of Eratoshenes

![](../../../assets/notes/50eb772569f473efb879.png)

Example: Derangement

Count the permutations for n objects that leave no objects in their original positions.

Theorem

The number of derangements of a set with $n$ elements is

$D_n=n! \left(1-\frac{1}{1!}+\frac{1}{2!}-\frac{1}{3!}+\cdots+(-1)^n \frac{1}{n!} \right)$
