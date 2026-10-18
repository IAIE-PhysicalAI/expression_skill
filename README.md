# 语言表达 · Chinese Expression

一份面向中文写作与润色的 Agent Skill。围绕作者的核心想法选择信息、组织论证，在同一份文档上分阶段修改，让重点讲清楚、句间逻辑成立，并保留作者的语言风格。

**想法驱动，信息支撑。想法决定需要表达什么，逻辑决定如何组织与表达信息。**

适用于中文文章、技术说明、方案、汇报和基于材料的文档写作。技能主体、规则和使用提示均为中文，技术标识为 `chinese-expression`。

[阅读完整技能](skills/chinese-expression/SKILL.md) · [下载发布包](https://github.com/IAIE-PhysicalAI/expression_skill/releases/latest) · [反馈问题](https://github.com/IAIE-PhysicalAI/expression_skill/issues)

## 安装

### 使用 skills CLI

需要能够运行 `npx` 的 Node.js 环境。执行以下命令，再按提示选择使用的 agent：

```bash
npx skills add IAIE-PhysicalAI/expression_skill --skill chinese-expression
```

仅安装到当前项目的 Codex：

```bash
npx skills add IAIE-PhysicalAI/expression_skill --skill chinese-expression --agent codex
```

如需跨项目使用，在命令末尾添加 `--global`。安装位置由安装工具和目标 agent 决定。

安装前可以只查看仓库中可用的技能：

```bash
npx skills add IAIE-PhysicalAI/expression_skill --list
```

### 手动下载

从 [Releases](https://github.com/IAIE-PhysicalAI/expression_skill/releases/latest) 下载 `chinese-expression.zip`，解压后将整个 `chinese-expression` 文件夹放入目标 agent 的技能目录，保留其中的 `SKILL.md` 和 `agents/`。

也可以点击 GitHub 的 **Code → Download ZIP** 下载仓库，技能位于 `skills/chinese-expression/`。不同工具的技能目录和刷新方式可能不同，请以对应工具的说明为准。

## 使用

安装后，在支持技能调用的 agent 中指定 `chinese-expression`。Codex 中可以使用 `$chinese-expression`；其他工具按各自的技能调用方式使用。

### 润色已有文档

```text
请使用 $chinese-expression 润色 article.md。
目标读者是第一次接触这个主题的同事，重点讲清方案的判断依据。
保留我的立场与语言风格，先保存大纲，再分阶段修改。
生成 article-polished.md，并保留原文件。
可以补充公开资料；无法核实的信息请单独说明。
```

### 基于固定材料成稿

```text
请使用 $chinese-expression，根据 notes.md 写一份项目复盘。
读者是项目组成员，重点解释失败原因及下一次如何避免。
只使用输入材料，不新增外部事实、数据或真实案例。
按流程保存大纲和正文；材料不足以支撑的判断请指出。
```

### 开放式写作

```text
请使用 $chinese-expression 写一篇关于团队知识库维护的中文文章。
核心想法是：知识库需要明确维护责任和更新时机。
先确认问题并保存大纲，重点解释维护机制如何落地。
根据大纲搜集可靠依据，在同一份工作文档上完成起草、校验和风格调整。
语言直接、具体，适合中小团队负责人阅读。
```

提供原稿、目标读者、核心想法、材料边界和风格参考，有助于 agent 判断重点与详略。完整的说明性示例见 [润色示例](examples/润色示例.md)。

## 工作流程

七个步骤按五个执行阶段组织，合并边界由技能明确规定：

| 阶段 | 对应步骤 | 需要完成的工作 |
| --- | --- | --- |
| 准备 | 一至三步合并 | 确认核心问题，理解已有材料，保存具有层级和详略安排的大纲 |
| 补充信息 | 第四步独立 | 根据大纲中的重点观点再次检索与核实，记录依据、出处和缺口 |
| 内容成稿 | 第五步独立 | 确定每段核心，选择并组织信息，写入同一份工作文档 |
| 校验与修复 | 第六步独立 | 回读已保存正文，逐句检查逻辑与支撑，定向回退并复查 |
| 个性化风格 | 第七步独立 | 调整作者特有的语气、节奏和表达方式，保存并复查 |

大纲明确同级标题的并列关系、子标题的从属关系，并标出需要详细介绍的内容。后续改变结构或重点时，大纲也要同步更新。

每轮修改针对具体问题。依据不足就补充材料，核心信息孤立就补足解释与关联，句间推理不成立就重新组织。已符合要求的内容保留，不为增加轮次而强行修改。

## 中文表达规则

- 优先使用准确、熟悉的词汇；必要术语保留，并按读者需要解释。
- 删除重复与空泛内容，为重要但抽象的判断补足具体解释。
- 根据实际逻辑决定是否使用关联词，避免把相关、先后发生或用词相近写成因果与递进。
- 正面陈述优先，避免反复使用“不是……而是……”等防备性表达；必要的反面说明集中后置。
- 核实新增的事实、数据、引用与真实案例，保留原意、适用条件和确定性程度。
- 在全文、段落和句子三个层面检查信息是否支撑观点，避免关键概念、数据或判断孤立出现。

这些规则贯穿全程；最后的风格阶段处理作者个性化的表达特点。

## 环境与适用范围

技能使用通用的 [Agent Skills 格式](https://agentskills.io/)，核心指令位于 `SKILL.md`。`agents/openai.yaml` 提供 Codex 的展示信息；其他工具可能忽略该文件。

完整执行需要 agent 能读写文档；开放式写作和外部核验还需要搜索、读取来源的能力。技能本身不附带搜索服务、模型或文档编辑软件。仅有聊天输出的环境可以参考表达规则，但无法完整执行文件保存与回读流程。

格式兼容不等于各模型执行效果相同。分阶段修改依赖 agent 遵循指令，本仓库不包含强制调度各阶段的运行程序。涉及事实的最终稿仍需结合原始来源审阅。

## 文件与更新

```text
expression_skill/
├── README.md
├── examples/
│   └── 润色示例.md
└── skills/
    └── chinese-expression/
        ├── SKILL.md
        ├── LICENSE
        └── agents/
            └── openai.yaml
```

技能规则以 `skills/chinese-expression/SKILL.md` 为准。更新记录与下载包见 [Releases](https://github.com/IAIE-PhysicalAI/expression_skill/releases)。

通过 skills CLI 安装后，可以使用该工具的更新功能；手动安装时，下载新版本并替换对应技能文件夹，替换前保留自己的定制内容。

## 反馈与改进

欢迎通过 [Issues](https://github.com/IAIE-PhysicalAI/expression_skill/issues) 提交实际使用中遇到的问题。建议附上技能版本、使用的 agent、脱敏后的输入与输出，以及期望改善的具体地方。

规则调整优先解决可复现的问题，并保持流程清楚、篇幅适当。

## 许可证

本项目采用 [MIT 许可证](LICENSE)，允许修改、再分发和商业使用，需保留版权与许可声明。
