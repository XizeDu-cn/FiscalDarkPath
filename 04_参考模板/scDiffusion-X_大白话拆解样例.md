sdx 看完本质缝合之后，大白活拆解

故事总结

# 摘要

单细胞多组学技术牛逼，能够看一个细胞的多个层面；为了克服这个测序技术的规模，成本，覆盖度，计算方法需要被提出；为此我们提出了我们的模型 for 整合、生成、翻译；核心贡献是 DCA that 捕获不同模态之间的底层联系，提供了一个灵活可解释的框架；我们的模型很牛逼，benchmark 展示了我们模型可以生成牛逼的拟合数据；beyond拟合牛逼，模型还可以准确的模态翻译；furthermore，还设计了一个为 DCA 模块提供可解释性的功能，用来发现 GRN ； by 整合现在的生成式建模与生物学解释性，我们的模型 serve as 一个牛逼的解释调控关系，预测扰动的多组学框架



# Introduction

## 第一段：多组学技术牛逼

单细胞多组学技术让我们对于一个细胞的理解更加深入，比如 10x 让我们同时看 rna 和 atac、citeseq 让我们同时看 rna 和蛋白质；这些技术让我们可以comprehensive and systematic 去看细胞状态，发育轨迹，细胞之间的交流

## 第二段：多组学数据获取有难度

尽管单细胞多组学技术已经进步了，但是还是获取大规模、高质量的数据集还是存在问题 due to 大规模的成本和实验条件；当前的模拟算法存在着分辨率的覆盖率的平衡；所以，当前能够获取规模化的数据很难，阻碍了相关的应用

## 第三段：当前生成模型拉

为了解决这些问题，目前已经有一堆计算模型发明出来了；multivi 使用 vae 的框架将两者并入一个空间，while effective，vae 的模型可能会生成过于平滑的数据；CFGen 使用流模型来生成，however，流模型的生成会被限制；scdesign3 是统计模型是提供模拟数据来测评计算方法的，并不用于生产真实数据

## 第四段：我们的方法提出了，很厉害

为了解决这些局限性，我们提出了我们的方法：一个基于深度生成模型 specifically for single cell muti-omics data；通过使用当前最优秀的扩算模型框架，模型展示了强大的扩展性和灵活性，他的迭代生成不但捕获了复杂的模态，同时适合对高维度的复杂模态之间的关系进行建模

## 第五段：方法的核心框架是 DCA，跟传统比很厉害

X 的关键创新是 DCA 模块，designed for 自适应可解释的模态解释；跟传统的整合策略（比如直接拼接 vector），DCA 提供了一个更加灵活并且整合的方式来建模不同模态的内部联系；为了增强解释性，还设计了一个基于梯度的解释性框架 with DCA 来鉴别细胞类型特异的 GRN，提供了一个生物学的理解

## 第六段：翻译功能

不像已有的模型专注于生成，X 还可以用来进行不同模态之间的翻译；更重要的是，我们的方法整合了不确定性量化，允许对 data 进行概率建模，与之前的点估计方法不同

## 第七段：讲一下我们的实验设计，为啥牛逼

为了严格考察 X 的能力，我们设计了一系列的实验，包括：条件多组学生成、模态翻译；结果阐释了 X 稳定的比其他方法强大 by generating high-quality multi-omics data across diverse conditions and scale；furthermore，引入的基于梯度的解释框架可以发掘 gene 和 peak 之间的关系；总之，X 是一个有力的工具用来生成多组学数据，捕获复杂的调控关系，预测扰动反应，鉴别潜在的生物学模式



# Results

## 1.overview of X model

### 第一段：整体的组件介绍

X 是一个多模态的潜在去噪生成框架，结构有两个主要组件：一个多模态的自编码器还有一个多模态的降噪网络；多模态的自编码器将多模态的数据放到一个低维的空间里面，用来适配 diffusion 的学习；降噪网络在潜在空间里面进行操作，反复重构数据的分布从而捕获数据的生物学意义；核心的 DCA 模块以一个可解释的方式整合不同的模态；细胞类型等条件信息融入到训练的过程中，来让生成变得可控

### 第二段：训练方式+下游应用

训练阶段，首先自编码器学习潜在的嵌入，然后降噪网络学习如何从随机噪声拟合这些嵌入；推理阶段从高斯噪声开始对这些噪声进行生成；最后将这个模型投入了一堆应用；总之通过这些组件，X 提供了一个新颖并且可解释的框架用于生成并且分析多组学的数据

## 2.X generates realistic single-cell multi-omics data

### 第一段（说明这个子任务的重要性）

分析工具越来越多 → 需要 benchmark → benchmark 最好有 ground truth → 真实数据 ground truth 不完整 → 所以需要 realistic simulator → 因此我们 scDiffusion-X 很有价值。

### 第二段（为了评价我们的能力，用了啥数据集，用了谁作为对比）

为了评价 X 的能力，我们用 openproblem 和 10x 来训练模型，使用细胞类型作为标签，我们将会评测 X 是否准确学到了潜在的分布信号；作为对比，选择了 abcd 作为对比

### 第三段（展示一）

我们使用了多种指标来评测 X 的质量；UMAP 展示了 X 清晰展示了不同细胞的聚类结构，捕获到了伪时间信息，其他的方法则表现了模糊；进一步，定量的评估指标：SCC，MMD，LISI，AUC 用于评估，更明亮的颜色代表更优秀的性能，可以从 fig2c 看出，rna 层面 X 一直做到了 top 性能，MMD 提升了 33.3%，LISI 提升了 15.5%，atac 层面同样表现了卓越的性能

### 第四段（展示二）

除了生成整体的分布，我们评估 X 能否生成真实的细胞类型特异的多组学数据，我们使用 CFGen 和 multivi 作为 baseline，我们给定细胞类型生成数据，检测他的 AUC；fig2e 可以看到，X 产生的细胞很像 real cell，实现了更低的 AUC，specifically，rna0.864-0.747，atac0.802-0.640；为了进一步论证生成数据的生物学保真度，还专门把生成的向量里面的关键 marker 基因挑出来，跟原始细胞做对比，看看KL 散度的差距，也是 ok 的

### 第五段（展示三）

探索 X 的应用价值，我们检测了生成的罕见的细胞类型是否能够增强下游的计算分析。

思路：

原始 OpenProblem 里 cDC2、plasma 这些稀有类样本少
→ Random Forest 几乎学不会这些类，某些 rare-cell F1 甚至是 0
→ 用 scDiffusion-X 按 cell-type condition 生成一批 cDC2 / plasma
→ 把这些 synthetic rare cells 塞回训练集
→ 重新训练 Random Forest
→ rare-class F1 从 0 拉到 80%+

我们将两种细胞类型加入到原始的数据集当中，并且训练了一个随机森林用于分类检测，结果显示 F1 分数从 0-80%，说明了 X 可以作为一个有效的数据增强工具，使得对数据集进行更好的表示。同时做了一个免责声明，表示实验并不严谨。

### 第六段（展示四）

X 的一个核心优势在于他的扩展性，尤其是处理大数据集的能力，根据 fig2f 可以看出我们用不同的数据规模对这些方法进行测试；c 在 10000 以上的细胞量级上表现的无法训练，但是 X 在不同数据规模下都保持了性能稳定；此为，X 使用保持了 best LISI，对比其他的 deep learning 方法，展示了 X 的鲁棒性；总之 X 是一个能够生成真实数据同时保持数据分布，还能够维持性能的一个模型

### 第七段（展示五）

为了让模型能够利用，我们还在一个 130000 个细胞的量级的图谱上进行测试，性能也很好，并且开放了权重

## 3.X enables modality translation and in-silico perturbation

### 第一段

多组学测序的成本远远高于单模态的测序技术，模态翻译的定义是给定一个模态给另一个模态的数据，这提供了一个强大的计算方案来解决多组学的成本问题；不像已经有的方法，他们只做生成，X 可以直接做翻译在训练之后；specifically，每个时间步，将已有的模态的信息插入进去，然后生成另一个模态的信息从高斯噪声，直到模型产生另一个模态的数据

### 第二段

为了测量有效性，跟 BABEL 进行对比；将一个数据集聚类，挑一个类出来作为测试集，同时挑一个外部测试集作为测试集，然后其他部分用来训练，最后发现 LISI 提升了；pseudo bulk 也是更加准确；同时把 marker 基因拿出来，检测了一下分布，也是更好；说明捕获了交叉模态之间的关系，允许模态翻译

### 第三段

`正常 RNA`
→ scDiffusion-X
→ `预测正常 ATAC`

然后人为把某个 RNA gene 设成 0：

`RNA，但是 ZAP70/CD3E/CD4 = 0`
→ scDiffusion-X
→ `预测“扰动后” ATAC`

最后比较：

`预测 ATAC 的变化方向`
vs
`真实 CRISPR/perturbation experiment 中 ATAC 的变化方向`

为了进一步评估 X 能否捕获到功能性的关系，我们做了一个交叉多模态的扰动实验，按理说如果我们敲除了一部分基因，那么对应的 scatac 的翻译应该展示出相应的变化；找了一个自己制作的数据集，进行扰动，跟现实中 变化强烈的 peak 做对比，最后结果好

### 第四段

`diffusion 有随机性`
→ `同一个 ATAC 可以生成很多个可能 RNA`
→ `这些样本构成 predictive distribution`
→ `我可以造 95% prediction interval`
→ `真实值约 94% 落进去`
→ **“模型的不确定性校准得很好”**
→ **“相比 BABEL 这种 point estimate，我提供 richer information”**

### 第五段

`真实 gene SD 大`
↓
`模型 PI width 也大`
↓
PCC ≈ 0.95
↓
**“captures inherent gene-specific uncertainty”**
↓
生成的几个高表达 gene 分布也像真数据
↓
**“learned a full generative distribution”**



## 4.scDiffusion-X uncovers gene regulation mechanisms from DCA

找到内在的关联和基因调控的架构很重要，他们为此对 DCA 进行了分析，然后得到了如下的结果

得到的 atac*rna注意力矩阵，按照 atac 列归一化，然后每一行 rna 求和，得到一些重要的 rna，最后做一个 go 分析，还有做一些乱七八糟的东西，感觉不是很好，直接过了

### 第一段：为什么要解释 DCA

多组学最重要的问题之一：

> RNA 和 ATAC 到底有什么关系？

作者说：

DCA attention matrix 本身就编码了跨模态 interaction。

于是提出：

> gradient-based interpretability。

对于某个高 attention latent pair：

```
$$M_{ij}=f(x_R,x_A)$$
```

直接计算：

```
$$\partial M_{ij}/\partial x_R,\quad
\partial M_{ij}/\partial x_A.$$
```

gradient 越大：

> 这个 gene/peak 对这个 attention element 越重要。

于是：

`attention`
负责选 latent interaction；

`gradient`
负责把 latent interaction 映回真实 gene/peak。

------

### 第二段：先证明这些 latent element 有 biological meaning

拿第二个 DCA 举例。

先在同一个 cell type 中：

`ATAC→RNA attention map`
→ 对 cells 平均
→ 再沿 ATAC axis 平均
→ 得到每个 RNA latent element 的 attention importance。

比如：

> 第 38 个 RNA latent element 在 CD4 T 中很重要。

然后对这个 latent element：

```
backward → 所有 genes gradient
```

取 top100 genes。

做 GO enrichment。

得到：

- T cell selection；
- TCR complex；
- immune process。

于是说：

> 这个 latent dimension 确实包含 cell-type-specific biological information。

------

### 第三段：避免只挑一个漂亮案例，再做全局 marker 验证

对每个 cell type：

取 top-5 high-attention RNA latent elements。

每个 element：

算所有 genes 的 gradient magnitude。

然后看已知 marker genes 的排名是不是比普通 gene 靠前。

最后：

> 22 个 cell types 里 18 个显著。

于是 claim：

> gradient-based interpretation 可以找到 biologically relevant genes。

------

### 第四段：从 gene/peak importance 升级成“regulatory relationship”

构建 dual attention：

```
$$M_{\rm dual}
=
M_{A\to R}
+
M_{R\to A}^{T}.$$
```

选 RNA latent 和 ATAC latent 中互相 attention 高的 pair。

然后：

`RNA latent`
通过 gradient 找对应 genes；

`ATAC latent`
通过 gradient 找对应 peaks。

于是得到：

`gene`
→ `RNA latent`
↔ `ATAC latent`
← `peak`

作者把能够通过这条路径连起来的 gene–peak 认为是潜在 regulatory pair。

------

### 第五段：用已有生物数据给这个关系镀合法性

先看选出来的 key peaks：

是不是落在：

- promoter；
- enhancer；
- H3K27ac regions；
- TSS 附近。

结果比 random peaks 更容易重叠。

然后举例：

CD5 附近三个 key peaks 正好位于 potential promoter/enhancer。

于是故事变成：

> 这些不是随机 peak，而是可能真有 regulatory function。

------

### 第六段：把局部关系扩展成 heterogeneous GRN

正式构造四类 node：

- gene；
- RNA latent element；
- ATAC latent element；
- peak。

边来自：

- gene↔RNA element：gradient；
- RNA↔ATAC element：DCA attention；
- ATAC element↔peak：gradient。

于是形成：

```
gene — RNA latent — ATAC latent — peak
```

四层 heterogeneous regulatory network。

再做 GO，发现网络里的 genes 符合对应 cell-type biology。

作用：

> 从“解释一个 attention element”升级成“构建完整 cell-type-specific GRN”。

------

### 第七段：把 latent graph 映射成直接 gene–peak pair，再和 GRN baseline 对打

如果：

`gene`
和
`peak`

可以通过：

```
gene → RNA element → ATAC element → peak
```

连起来，

就认为是 candidate gene–peak regulatory pair。

再加限制：

- same chromosome；
- distance ≤120 kb。

CD4 activated T 中得到：

> 366 gene–peak pairs。

然后用 HiChIP loop 当 ground truth。

再比较：

- random；
- nearest peak；
- MultiVI/correlation；
- SCENIC+ 等。

scDiffusion-X reported precision：

> 0.64。

于是完成最终 claim：

> **我们的 DCA 不只是帮助生成，它还学到了可以恢复 gene–chromatin regulatory associations 的 latent structure。**



## 5.DCA模块有用



### 第一段：先重新定义问题——普通 concat 不够

作者先说：

多组学 integration 传统方式：

- early concat；
- late concat；

把两个模态简单拼起来，不能显式建模复杂 dependency。

DCA 则每个 denoising step 都让两模态交互。

所以这一节的总目标：

> 验证 DCA 比普通融合更有价值。

------

### 第二段：DCA 越多是不是越好

训练：

- 1 个 DCA；
- 3 个 DCA；
- 5 个 DCA。

结果：

> DCA 越多，translation performance 越好。

但更多 DCA 增加计算量。

最后选：

> 3 DCA。

故事：

> “跨模态交互次数增加确实有收益，但考虑效率，三层是折中。”

------

### 第三段：DCA vs 简单 concat + linear

把 3 个 DCA 全部替换成：

`RNA latent || ATAC latent`
→ fully connected linear layer。

结果 linear fusion 比 DCA 差。

于是作者说：

> attention 比简单拼接更加有效地捕获复杂的跨模态关系。

作用：

> 给 DCA 相对于最普通 fusion baseline 的优势背书。

------

### 第四段：有 DCA vs 完全没有 DCA

再做更直接的 sanity check。

去掉 cell-type condition，避免 condition 本身泄露过多信息。

比较：

```
with DCA
```

vs

`without DCA`。

指标：

- MMD；
- LISI；
- AUC。

RNA、ATAC 都是 with DCA 更好。

于是作者说：

> 当前模态生成确实能从另一模态得到有用的信息。

这一实验真正证明的是：

> **有跨模态通信 > 完全无跨模态通信。**

然后作者把它继续包装成：

> DCA 有效利用了 cross-modal dependency。

------

### 第五段：不同 DCA / timestep 里面“信息量”不一样

模型有：

- 多个 DCA；
- 1000 个 diffusion steps。

作者问：

> 到底哪个 DCA、哪个 timestep 最有信息？

于是对 attention map 算两个东西：

### Information Entropy (IE)

用来描述 attention map 的“information richness”。

### MSE

当前 attention map
vs
100 steps 以前的 attention map。

表示 attention 随时间变化了多少。

然后发现：

- IE 随 diffusion 过程变化；
- 第一、第二 DCA 的 MSE 比第三个明显；
- 某些 timestep 变化最大。

于是说：

> 不同层、不同 timestep 学到的信息丰富程度不同。

------

### 第六段：用这个分析给前面的 GRN 解释选择位置

根据 entropy / MSE，

最后挑：

- 第二个 DCA，t=1000；
- 第一个 DCA，t=900；

作为比较“informative”的 attention maps。

然后前面 Fig.4 那套：

`attention`
→ `gradient`
→ `gene/peak`
→ `GRN`

就主要从这些位置取。

这一步的论文功能是：

> 给“为什么偏偏解释这个 DCA / 这个 timestep”提供一个看似数据驱动的理由。

------

### 第七段：整个 DCA section 的最终结论

最后总结：

DCA 不仅：

1. 比 linear concat 性能好；
2. 比 no-DCA 性能好；
3. 多插几个还能继续提高性能；

而且：

1. attention 随 diffusion timestep 具有动态结构；
2. attention 可以拿来做 gene/peak interpretation。

所以作者把 DCA 定义成：

> **既提高 generation/translation performance，又提供 biological interpretability 的核心模块。**

也就是把整篇前面所有故事重新归功于 DCA。