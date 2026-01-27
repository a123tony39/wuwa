# Score 計算說明

這是為了實現聲骸副詞條分數計算的應用，並用於遊戲/產品的評分系統。

## 詞條分數 StatScore

每個副詞條分數(StatScore)都有一個基礎分數（base score），和一個額外加分 (quality)。

額外加分受該數值浮動所影響。

分數公式如下：

$$
\text{StatScore}(s) = B_s \times (\alpha + \beta \cdot Q(s))
$$

其中：

- $B_s$ : 副詞條 $s$ 的基礎分數 (base score)
- $Q(s)$ : 副詞條 $s$ 的浮動百分比 (quality)
- $\alpha$ : 基本比例，預設 0.7
- $\beta$ : 依品質額外加分比例，預設 0.3

---

## 副詞條品質 $Q(s)$ -- 離散 CDF

$Q(s)$ 是把分布表中所有小於等於該副詞條實際數值 $v_s$ 的可能數值 $v_i$ 的機率 $p_i$ 累加起來，得到該數值的累積機率百分比，也就是副詞條的品質。

$$
Q(s) = \text{CDF}_\text{discrete}(v_s) = \sum_{v_i \le v_s} p_i
$$

其中：

- $v_s$ : 該副詞條的實際數值  
- $v_i$ : 該副詞條的可能數值  
- $p_i$ : 對應數值的機率  
- $\text{CDF}_\text{discrete}(v_s)$ : 該數值的累積的機率百分比，範圍 0-1

---
## 聲骸分數
單一聲骸的總分數計算方式如下：

$$
\text{EchoScore} = \sum_{s \in \text{valid stats}} \text{StatScore}(s)
$$

最終單一聲骸的完成度（Echo Completion）計算公式為：

$$
\text{EchoCompletion} = \frac{\text{EchoScore}}{\text{ScoreCeiling}} \times 20
$$

其中：

- $\text{EchoScore}$ : 有效副詞條分數累加總和
- $\text{valid stats}$ : 該角色有效副詞條
- $\text{StatScore}$ : 詞條分數計算公式（詳見 [詞條分數 StatScore](#詞條分數-statscore)）
- $\text{ScoreCeiling}$ : 該聲骸理論最大總分（所有副詞條均為最大浮動值時）  
- $\text{EchoCompletion}$ : 單一聲骸分數，範圍 0–20

---

## 角色評分
角色評分為五個聲骸分數的和：
$$
\text{CharacterScore} = \sum_{x=1}^{5} \text{EchoScore}(x)
$$

其中：
- $x$: 第 $x$ 個聲骸
- $\text{EchoScore}(x)$: 第 $x$ 個聲骸的分數
- $\text{CharacterScore}$: 角色評分