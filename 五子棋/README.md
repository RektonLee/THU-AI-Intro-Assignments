  # 人工智能导论第一次作业-搜索实践

## 介绍

“[五子棋]((https://en.wikipedia.org/wiki/Gomoku))”是一款大家耳熟能详的游戏，本次作业需要结合课上学习的搜索相关知识，逐步实现一个无禁手五子棋Intelligent Agent :)

本次作业目标：
- 实现二人零和博弈最基本的minimax搜索
- 实现alpha-beta search等剪枝方法
- 设计评估函数并实现基于评估的截断搜索
- 实现蒙特卡洛搜索树（MCTS）搜索方法
- 了解AlphaZero的原理并进行基本尝试


## 文件结构

需要编辑的文件：

- ```minimax.py```: 基于minimax的搜索方法实现。
- ```evaluation.py```: 评估函数的实现。
- ```mcts.py```: 基于mcts的搜索方法实现。
- ```alphazero.py```: alphazero思想的实现。

需要阅读的文件：

- ```game.py```: ```State```类、```Board```类、```Player```类的定义和接口。


## 使用说明

进入目录，输入以下命令运行五子棋游戏：

```
python play.py
```

![](assets/demo.png)

游戏规则：通过键盘输入坐标 `A,B` 表示在第A行第B列落子，五子连珠即可获得胜利。

通过在指令中加入不同的参数，可以得到不同的棋盘大小以及获胜所需子数，具体地：
```
python play.py --width w --height h --n_in_row n
```
表示在 w$\times$h 的棋盘上以n子连珠为胜利。

代码中已经实现了一个最简单的```DummyPlayer```，它永远只会下在棋盘从下到上、从左到右第一个可以落子的位置。想要与AI进行对战，运行指令：
```
python play.py --player_1 Human --player_2 DummyPlayer
python play.py --player_1 DummyPlayer --player_2 Human
```
分别表示执先、后手与AI进行对战。

查看更详细的参数说明：
```
python play.py --help
```

### 问题一（5pt）

首先我们考虑一个简化版的问题：$w=h=n=3$，也就是我们常玩的井字棋。此时状态数比较小，因此可以通过完全搜索解决，其中约定获胜得分+1，失败得分-1，平局得分0。你需要实现二人零和博弈中最基本的minimax搜索方法来寻找最优策略。

#### 任务
- 阅读```minimax.py```文件中的```MinimaxSearchPlayer```类，我们已经提供了部分框架及相应的注释，你需要<u>实现核心部分代码内容</u>。
- 实现后，运行以下命令进行人机对战测试，并<u>汇报AI是否找到一组必不输策略</u>：
```
python play.py --width 3 --height 3 --n_in_row 3 --player_1 Human --player_2 MinimaxSearchPlayer
python play.py --width 3 --height 3 --n_in_row 3 --player_1 MinimaxSearchPlayer --player_2 Human
```

#### 提示

- 请仔细阅读注释，并尽可能调用state对象的接口，你可以在game.py的State类找到相应接口。
- **建议统一将```MinimaxSearchPlayer```对应的玩家（```self._player```）作为最大值玩家（max player），而非将一号玩家作为最大值玩家**，这不仅是为了代码实现方便，更是为了与后续问题相照应。由于进入搜索时一定是该玩家的回合，因此这等价于从最大值玩家开始搜索。
- 搜索程序（尤其是不加剪枝的搜索程序）通常运行缓慢，若AI无响应，未必是死循环，可能需要耐心等待。
- 井字棋的必不输策略不是唯一的，你的AI可能找到了一组策略，但未必与标准策略（例如开局下在中心）相同。

### 问题二（5pt）

尝试扩大问题规模：$w=4,h=n=3$，容易发现存在先手必胜策略。然而如果直接将朴素的minimax搜索应用其中，可能运行很久也没有搜索完毕。我们尝试用alpha-beta搜索进行剪枝。

#### 任务
- 阅读```minimax.py```文件中的```AlphaBetaSearchPlayer```类，并<u>实现核心部分代码内容</u>。
- 运行以下命令，在$4\times 3$的棋盘上分别测试有无剪枝的搜索，<u>对比以及第一步大致的运行时间，并汇报alpha-beta搜索是否找到一组先手必胜策略</u>：
```
python play.py --width 4 --height 3 --n_in_row 3 --player_1 MinimaxSearchPlayer --player_2 Human
python play.py --width 4 --height 3 --n_in_row 3 --player_1 AlphaBetaSearchPlayer --player_2 Human
```

#### 提示
- 必胜策略不是唯一的。

### 问题三（15pt）

现在考虑更实际的情况，比如 $w=h=9,n=5$。此时棋盘相对很大，并且没有平凡的必胜策略。若尝试直接调用问题一、二得到的AI：
```
python play.py --player_1 MinimaxSearchPlayer --player_2 Human
python play.py --player_1 AlphaBetaSearchPlayer --player_2 Human
```
则由于搜索树太深，AI甚至无法做出第一步落子！因此必须做出一些“让步”：当深度较浅时，可以通过搜索充分考虑对手的行为逻辑；但是当深度较大时，受时间限制，不能继续搜索。为了体现出不同后继的差异，需要对状态进行**评估**，并进行截断搜索（cutting off search）。

这里的评估需要基于五子棋的先验知识，比如：
- 落棋应当尽量落在正中间附近，防止被阻挡；
- 活三、冲四等棋型可以强迫对手进行一步防守;
- 活四等棋型对手无法防守，几乎已经获得胜利。

我们在```game.py```的```Board```类里**已经提供了**部分先验知识的提取，包括：
- 活四、冲四、活三、眠三、活二的数目
- 最远棋子距离棋盘中心的相对距离（最小为0，最大为1）

**你不需要复现或改进这部分代码，而是需要基于已经提取好的信息，设计一个合适的评估函数，并实现带评估函数的截断搜索**。代码中提供了```dummy_evaluation_func```和```distance_evaluation_func```作为参考。

你也可以基于评估函数进行其他剪枝，比如：对状态按照评估函数排序等等。

#### 任务
- 阅读```evaluation.py```中```Board```类的```get_info```函数，了解该函数的返回值，在```evaluation.py```中基于该函数设计评估函数，实现```detailed_evaluation_func```函数。这个函数输入一个棋盘状态，输出**即将行动的玩家**对这个状态的评估。可以参考同文件下的```dummy_evaluation_func```和```distance_evaluation_func```。<u>汇报你的评估函数及其设计动机</u>。
- 阅读```minimax.py```中的```CuttingOffAlphaBetaSearchPlayer```类，并基于```detailed_evaluation_func```评估函数，<u>实现核心部分代码内容</u>。
  - 你也可以尝试在方法中加入其他剪枝技巧，以获得更高效的搜索。
- 实现后，运行以下命令与AI进行对战，并<u>汇报AI展现出的棋力</u>：
```
python play.py --player_1 CuttingOffAlphaBetaSearchPlayer --player_2 Human --max_depth 1 --evaluation_func detailed_evaluation_func
```

#### 提示
- 建议将评估函数的取值固定到 $[-1,1]$ 之间，因为通常获胜得分为 $1$ 而失败得分为 $-1$ 。
- ```detailed_evaluation_func```的一种可能实现为：为每种棋型设置一个得分，用当前玩家的总得分减去对手的得分；你和对手的计分方法可以是非对称的，比如：你的冲四可以立即变为五连从而胜利，但是对手的冲四却可以被封堵等等。
- 按照课件约定，```depth```为两人各走一步的轮数（而非双方下棋的次数），即```depth=1```时，表示当前玩家下一步，对手下一步，当前玩家评估目前状态。
- 若实现正确，展现出的“棋力”应当包括但不限于：会对活三、冲四进行封堵，会主动进攻等等。

### 问题四（20pt）

AlphaZero是继AlphaGo之后的又一力作，相比于AlphaGo需要基于大量人类棋谱进行训练，AlphaZero则是完全从零开始训练，仅仅通过自我对抗（self-play）的训练方式，就能够学习到超出人类的棋力水平。AlphaZero适用于种种不同的棋类游戏，成为了AI发展的重要标志。

在前三道题中，你或许已经体会到了传统基于minimax搜索的AI的局限性：搜索深度多大，复杂度爆炸，因此必须设计合适的评估函数，而这往往就成为了算法的瓶颈；相比之下，AlphaZero所使用的是**蒙特卡洛搜索树（MCTS）** 与强化学习相结合的方法。这一方法逐渐加大深度，可以平衡探索与利用，相比于minimax搜索更加灵活，适合与深度学习方法相结合。

在此，你需要实现一个基础版本的MCTS，并感受其与minimax搜索的不同。

#### 任务
- 阅读```mcts.py```中的```TreeNode```、```MCTS```和```MCTSPlayer```三个类，<u>实现核心部分代码内容</u>。
  - 其中，```TreeNode```类记录了搜索树中每个节点的信息，需要完成节点UCB的计算（```get_ucb```）、基于UCB的选择（```select```）以及权值的更新（```update```）；```MCTS```类记录了整棵树的信息，需要完成基于随机策略的评估（```get_left_value```）；```MCTSPlayer```定义了一个agent，需要完成MCTS的调用和决策（```get_action```）。每个函数和变量的具体功能可以参考代码注释。
- 实现完成后，尝试让两个AI进行对战，<u>汇报对战结果，并简要分析MCTS产生这种表现的原因</u>：
```
python play.py --player_1 MCTSPlayer --player_2 CuttingOffAlphaBetaSearchPlayer --evaluation_func detailed_evaluation_func
python play.py --player_1 CuttingOffAlphaBetaSearchPlayer --player_2 MCTSPlayer --evaluation_func detailed_evaluation_func
```

#### 提示
- 需要注意，代码中有两处地方与课件上不同：
  - 代码中胜、负、平对应的权值为1、-1或0，而非课件上的1、0、0.5；
  - 代码中根据UCB选择节点时会**固定选UCB最大的节点**，而非课件上的根据UCB进行采样。
- 建议将节点权值定义为**当前玩家（即将行棋的玩家）的权值**，这样叶子结点的权值即为该玩家是否胜利；在```select```时，由于要讨论的是父亲节点（对应另一名玩家）的选择，因此权值应该取负号（在代码中已经完成）。你也可以尝试其他定义，但需要注意正负号与最大最小值的问题。
- 若算法运行时间过长，你可以适当减小`n_sample`的值，比如`--n_sample 2000`。

### 问题五（5pt）

你可能已经发现，朴素的MCTS效果并不好，且行棋较慢。作为改善，AlphaZero使用深度网络来学习当前局面的评估函数（以及行棋的概率先验）。出于简化，我们并不使用深度学习，而是尝试将问题三得到的人工评估函数引入到MCTS中。

#### 任务
- 阅读```alphazero.py```中的```AlphaZero```类，<u>实现核心部分代码内容</u>。
  - 这个类继承自```MCTS```，你只需要将```get_leaf_value```函数中的随机游戏改成根据评估函数进行评估。
- 实现完成后，运行以下代码让问题四和问题五的AI进行对战，并<u>汇报引入评估函数后是否行棋更加合理</u>：
```
python play.py --player_1 MCTSPlayer --player_2 AlphaZeroPlayer --evaluation_func detailed_evaluation_func
python play.py --player_1 AlphaZeroPlayer --player_2 MCTSPlayer --evaluation_func detailed_evaluation_func
```

#### 提示
- 如果效果始终不佳，你可以尝试较小的c值，比如`--c 0.1`
- 你也可以通过`AlphaZeroPlayer`和`CuttingOffAlphaBetaSearchPlayer`的对战情况观察实现效果。
  - 不必过分执着于二者的对战结果，只需观察行棋的合理性即可。

## 最终提交

- 代码部分：提交**全部代码**，包括补全后的```minimax.py```, ```evaluation.py```, ```mcts.py```, ```alphazero.py```及其他文件。
- 文档部分：提交实验报告，包括以上问题的汇报部分，以及你认为有必要展示的代码片段。**其中AI的表现分析部分可以结合对战结果进行展示**。

在项目中遇到任何问题，欢迎在课程微信群中讨论。
