---
title: Lecture4 提升CNN的准确性
---
# Lecture4 提升CNN的准确性 {#lecture4-提升cnn的准确性}

## 数据增强 {#数据增强}


!!! note "为什么需要数据增强"
    我们可以通过对数据合理的变换，模拟真实的数据分布，将已有的先验知识注入模型，使模型的训练更有效率。但并非所有的变换都合理，如6和9的上下翻转，因为发生变化后答案也变了。

    本文我们主要讨论二维图像的数据增强。图像是三维场景的一个二维投射，一个场景的每一张图片都是这个随机变量的一个采样，它们共同构成了它的样本空间



### 有监督的样本数据增强 {#有监督的样本数据增强}
- 几何变化类：旋转、翻转、裁剪、变形、缩放...
- 颜色变换类：噪声、模糊、擦除、填充、颜色扰动、亮度、通道偏移...

### 无监督样本数据增强 {#无监督样本数据增强}
通过模型学习数据的分布，随机生成与训练集分布一致的图片，如GAN、DCGAN(这些会在lecture7中详细介绍)



$$
z\sim p(z),\qquad x'=G(z)
$$



模型从随机噪声 $z$ 出发，直接生成一张新图片。它需要先从大量真实图片中学习近似的数据分布



$$
p_G(x)\approx p_{\text{data}}(x)
$$



## 归一化 Normalization {#归一化-normalization}

归一化的目的是使数据和特征准确表达、便于处理
![](../../assets/notes/5ceb58b842c6aece8cf8.png)

### 批量归一化 Batch Normalization {#批量归一化-batch-normalization}

!!! note
    训练神经网络时，前面的层参数发生变化会导致每层输入的分布在训练过程中会发生变化，导致模型需要较低的学习率和非常谨慎的参数初始化策略，这种现象叫`内部协变量转移(Internal Covariate Shift)`，BN就是用来解决这个问题


 ![](../../assets/notes/b9551f1892e7b6143e3f.png)

- 有助于激活函数进行非线性化
- 均值为0，方差为1，加快收敛速度
- 防止过拟合，将一个batch的数据关联在一起
- 防止梯度爆炸和梯度消失


## 正则化 Regularization {#正则化-regularization}



### Dropout {#dropout}
Dropout 是一种防止神经网络过拟合的正则化方法，通过关闭部分神经元来迫使网络不过渡依赖某几个特征。训练时开启，预测时关闭。（特殊的Monte Carlo Dropout使用预测的Dropout来估计模型的不确定性）



$$y=\frac{m\odot x}{1-p}$$


p为神经元被关闭的概率，除以1-p是为了保持期望不变
m是Dropout产生的掩码


!!! tip "Dropout位置"

    ```text
    Conv → BatchNorm → ReLU → Dropout2d → Pool
    ```
    ```text
    Linear → ReLU → Dropout → Linear
    ```
    前者关闭通道；后者关闭神经元，更常见。总之都在激活层之后
