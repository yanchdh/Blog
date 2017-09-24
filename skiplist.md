# SkipList

*	作者: [William Pugh](https://en.wikipedia.org/wiki/William_Pugh)

*	论文: [skiplists.pdf](http://uosis.mif.vu.lt/~ragaisis/ADS2006/skiplists.pdf)

*	维基百科: [Skip list](https://en.wikipedia.org/wiki/Skip_list)

SkipList，缘起leveldb源码，一见钟情。它是如此的简单，高效。又名跳跃表, 动态结构图如下（来自维基百科）。

![](https://i.imgur.com/4FKSEjP.gif)
<center>图1</center>

**SkipList由多层有序单向链表组成。搜索，插入，删除的平均复杂度是O(log<sub>n</sub>)。It's amazing! 接下来我们通过Pugh的论文一起来分析学习一下（如有错误之处，敬请指出，谢谢！）。**

Search Algorithm
--
>We search for an element by traversing forward pointers that do not overshoot the node containing the element being searched for. When no more progress can be made at the current level of forward pointers, the search moves down to the next level. When we can make no more progress at level 1, we must be immediately in front of the node that contains the desired element (if it is in the list).

我们通过遍历forward指针来搜索元素，不会超出包含要搜索元素的节点。如果在当前层不能取得进展时，搜索将向下移动一层。如果在第一层也不能取得进展，我们必须立即在包含所需元素的节点前面（如果它在列表中）。

##Choosing a Random Level
>Initially, we discussed a probability distribution where half of the nodes that have level i pointers also have level i+1 pointers. To get away from magic constants, we say that a fraction p of the nodes with level i pointers also have level i+1 pointers. (for our original discussion, p = 1/2).

如果一个点在第i层，那么有1/2的概率也在第i+1层, 用一个分数p来表示，p=1/2。

	randomLevel()
		lvl := 1
		-- random() that returns a random value in [0...1)
		while random() < p and lvl < MaxLevel do
			lvl := lvl + 1
		return lvl

**通过随机使每个结点出现在不同的层级，从而加快搜索速度。MaxLevel是设定的一个最大层级。**

##	At what level do we start a search? Defining L(n)
>In a skip list of 16 elements generated with p = 1/2, we might happen to have 9 elements of level 1, 3 elements of level 2, 3 elements of level 3 and 1 element of level 14 (this would be very unlikely, but it could happen). How should we handle this? If we use the standard algorithm and start our search at level 14, we will do a lot of useless work.

假如有16个元素，p=1/2, 我们可能出现有9个元素在第1层，3个元素在第2层，3个元素在第3层，1个元素在第14层。我们如果用标准的算法从第14层开始搜索，将会做很多无用功。（是不是觉得和MaxLevel有点关系？）

>Where should we start the search? Our analysis suggests that ideally we would start a search at the level L where we expect 1/p nodes. This happens when L = log<sub>1/p</sub> n. Since we will be referring frequently to this formula, we will use L(n) to denote log<sub>1/p</sub> n.

通过分析我们建议，理想的情况下应该从期望有1/p (2) 个结点的第L层开始搜索。当且仅当L = log<sub>1/p</sub> n 时, 这些才会发生。因为我们会经常用到这个公式，所以用L（n）来表示 log<sub>1/p</sub> n 。 Why ? 我们来分析一下，n表示SkipList中有n个元素，也就是说当有n个元素, 第L层元素个数的期望值是1/p(2)个。

**首先，第L层元素的个数的期望值是1/p(2)个。现在有n个元素，每个元素出现在L层的概率是p<sup>L-1</sup>, 那第L层元素个数的期望值为: n * p<sup>L-1</sup>。**

推导过程如下：

1/p = n*p<sup>L-1</sup>

n = (1/p)<sup>L</sup>

L = log<sub>1/p</sub> n

定义：***L*(n) = log<sub>1/p</sub> n**

##	Determining MaxLevel
>Since we can safely cap levels at L(n), we should choose MaxLevel = L(N) (where N is an upper bound on the number of elements in a skip list). If p = 1/2, using MaxLevel = 16 is appropriate for data structures containing up to 2<sup>16</sup> elements.

我们选择用 **MaxLevel = L(N)**（N是skip list中元素个数的上限值）。如果p=1/2, 那么MaxLevel=16适用于高达2<sup>16</sup>个元素的skip list。 

##Analysis of expected search cost
>We analyze the search path backwards, travelling up and to the left. Although the levels of nodes in the list are known and fixed when the search is performed, we act as if the level of a node is being determined only when it is observed while backtracking the search path.

我们对搜索路径进行反向分析，向上和向左移动（如图1，搜索过程是向下和向右）。虽然当搜索执行时，列表中的节点是已知的并且是固定的，但只有在回溯路径时观察到，我们的行为就好像结点的层级是确定的。

>At any particular point in the climb, we are at a situation similar to situation a in Figure 6 – we are at the i<sup>th</sup> forward pointer of a node x and we have no knowledge about the levels of nodes to the left of x or about the level of x, other than that the level of x must be at least i. Assume the x is not the header (the is equivalent to assuming the list extends infinitely to the left). If the level of x is equal to i, then we are in situation b. If the level of x is greater than i, then we are in situation c. The probability that we are in situation c is p. Each time we are in situation c, we climb up a level. Let C(k) = the expected cost (i.e, length) of a search path that climbs up k levels in an infinite list:

>C(0) = 0

>C(k) = (1–p) (cost in situation b) + p (cost in situation c)

>By substituting and simplifying, we get:

>C(k) = (1–p) (1 + C(k)) + p (1 + C(k–1))

>C(k) = 1/p + C(k–1)

>C(k) = k/p

![](https://i.imgur.com/IgdGMKB.png)

在向上climb的任意点，我们的situation类似于图6的situation a。我们现在在第i层结点x的forward指针处，我们不知道结点x左边的结点或结点x的层级，但是结点x的层级至少是i。假定结点x不是头结点（这相当于假设列表无限延伸到左边）。如果结点x的层级等于i，我们在situation b。如果x的层级比i大，那么我们就在situation c。我们在situation c的概率是p（原因见Choosing a Random Level）。每一次我们在situation c，我们向上climb一层。让C(k)等于搜索路径向上climb k层的期望值。

**(cost in situation b) = (1 + C(k)) 是因为从x左边的结点到x需要1步再加上需要向上climb k层，其余的推导过程，请手动推导一下，不再赘述。**


>Our assumption that the list is infinite is a pessimistic assumption. When we bump into the header in our backwards climb, we simply climb up it, without performing any leftward movements. This gives us an upper bound of (L(n)–1)/p on the expected length of the path that climbs from level 1 to level L(n) in a list of n elements.

我们假设这个列表是无限的，这是一个悲观的假设。当我们碰到头在我们的反向climb，我们就向上climb，不执行任何向左运动。这给出了在n个元素列表中从第1层到第L(n)层路径的期望长度的上界
(L(n)–1)/p。

由于MaxLevel = L(n)， C(k) = k / p，因此期望值为：(L(n) – 1) / p

将L(n) = log<sub>1/p</sub> n 代入可得：(log<sub>1/p</sub> n - 1) / p

将p = 1 / 2 代入可得：2 * log<sub>2</sub> n - 2，即O(log<sub>n</sub>)的时间复杂度。

我们观察反向路径，通过分析计算得到从第1层到第L(n)层路径的期望长度为(log<sub>1/p</sub> n - 1) / p，p是一个分数，因此搜索的期望值的时间复杂度是O(log<sub>n</sub>)。

至此我们已经得到搜索的时间复杂度，那对于插入和删除来说，其实是一样的，我们就不再赘述。我们只是做了一个简单的分析，有兴趣可以再研读一下[Pugh的论文](http://uosis.mif.vu.lt/~ragaisis/ADS2006/skiplists.pdf)。

**总结：**

**1）如果一个点在第 i 层，那么有1/2的概率也在第 i+1 层, 用一个分数p来表示，p=1/2；**

**2）理想的情况下应该从期望有1/p个结点的第L层开始搜索。**

**这两点是搜索期望值推导出来的核心。**