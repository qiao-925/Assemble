## Redis大事件(8.0回归开源)

#### **2009年：Redis诞生**
Salvatore Sanfilippo [antirez](https://github.com/antirez) 创建Redis，用于开发实时网络日志分析器。Redis的意思是"远程词典服务器"（Remote Dictionary Server）。antirez试图提高其意大利初创公司的可扩展性，在使用传统数据库系统扩展某些类型的工作负载时遇到重大问题后，开始用Tcl制作Redis的第一个概念验证版本原型，后来翻译成C语言并实现了第一个数据类型（列表）。在内部使用该项目几周并取得成功后，antirez决定开源，并在Hacker News上宣布了该项目。该项目开始受到关注，尤其是在Ruby社区中，GitHub和Instagram是首批采用它的公司之一。

#### **2010年3月：antirez被VMware聘用**
Salvatore Sanfilippo被VMware聘用，这是Redis发展的重要里程碑，标志着Redis开始获得企业级支持。

#### **2013年5月：获得Pivotal Software赞助**
Redis获得Pivotal Software（VMware的衍生公司）的赞助，进一步推动了项目的发展。

#### **2015年6月：开发由Redis Ltd.赞助**
Redis开发由Redis Ltd.赞助，这是Redis商业化的开始，标志着Redis从个人项目转向企业级服务。

#### **2018年8月：首次协议变更**
Redis Ltd.宣布将可选的Redis模块从GNU Affero通用公共许可证(AGPL)重新授权为Apache许可证，但需遵守"Commons Clause"附录，该附录限制了Redis模块的商业使用。这意味着这些模块将以源代码形式提供，不再是免费软件。核心Redis软件仍采用BSD许可证，Redis Ltd.承诺维护这些条款。

#### **2018年10月：Redis 5.0发布**
Redis 5.0发布，引入了Redis Stream——一种新的数据结构，允许在单个键上以基于时间的自动序列存储多个字段和字符串值。

#### **2019年2月：协议进一步收紧**
由于许可条款存在混淆，Redis模块的Apache公共条款许可证被替换为"Redis源代码可用许可证"（RSAL），该许可证明确禁止将模块作为"数据库、缓存引擎、流处理引擎、搜索引擎、索引引擎或ML/DL/AI服务引擎"的一部分进行商业使用。社区成员在免费开源许可证下对模块进行了最后的修订，并将其分叉为GoodFORM项目。

#### **2020年6月：创始人离职**
Salvatore Sanfilippo辞去Redis唯一维护者职务。Yossi Gottlieb和Oran Agra接任了Sanfilippo的职位。这标志着Redis从个人项目彻底转向商业项目。[The end of the Redis adventure](http://antirez.com/news/133)

#### **2024年3月：核心软件协议变更**
Redis Ltd.宣布从7.4版开始，核心Redis软件将重新采用RSAL和服务器端公共许可证(SSPL)进行授权，这两个许可证均提供源代码且非免费。这一重大决策的背后有着深层的商业逻辑和战略考量。

**协议变更的核心动机**：
- **云服务商"搭便车"问题**：AWS、阿里云、腾讯云等云服务商大量使用Redis构建商业服务，获得巨大商业价值但技术贡献有限。Redis Ltd.认为这种"价值分配不均"需要重新平衡。
- **商业可持续性压力**：Redis作为开源项目，维护成本持续增长，但传统"免费软件+付费支持"模式难以支撑企业级发展需求。
- **差异化竞争策略**：通过协议变更，Redis Ltd.希望将开源版本与商业版本进行明确区分，为付费服务创造更多价值空间。

**协议变更的具体影响**：
- **对云服务商**：AWS、阿里云等需要重新评估Redis的使用策略，可能面临商业限制
- **对开发者社区**：引发激烈争议，担心这会破坏开源生态的开放性
- **对Redis生态**：标志着Redis从"完全开源"转向"源代码可用但商业受限"的新模式

**Linux基金会的直接反击**：
Linux基金会随后宣布，将把最后一个BSD许可版本的Redis分叉为Valkey项目。这一举措实际上是对Redis协议变更的直接回应，为社区提供了真正的开源替代方案。

**社区反应的深层含义**：
这一事件揭示了开源项目在现代商业环境中的根本矛盾：如何在保持开源精神的同时实现商业可持续性？Redis的选择实际上是在"完全自由"和"适度控制"之间寻找平衡点，但这种平衡往往难以把握。

- <a href='https://www.infoq.cn/article/ee6dyubdjdvsr369zune'>开源 Redis 的生命将就此终结？Redis 之父回应分叉浪潮：未来谁能领先，各凭本事！</a>

- <a href='https://www.infoq.cn/article/cyh0hqiNW99Eh61mEaY3'>从 Redis 开源协议变更看开源软件与云计算巨头之间的竞争博弈</a>

- <a href='https://www.businesswirechina.com/zh/news/57686.html'>再授权风波让Valkey成为Redis的领先开源替代方案</a>

- <a href='https://blog.csdn.net/baidu_41642080/article/details/136913195'>Redis 又双叒叕改开源协议了，微软提前推出高性能替代方案 Garnet</a>
- <a href='https://36kr.com/p/2700542716409992'>新版 Redis 将不再“开源”引争议：本想避免云厂商“白嫖”，却让开发者遭到“背刺”</a>

- <a href='https://www.infoq.cn/article/ppo8vzpth59mqj8np0hn'>微软开抢年收入上亿美元的 Redis 饭碗？开源性能遥遥领先的 Garnet：无需修改，Redis 客户端可直接接入</a>

- <a href='https://fanjingbo.com/post/tan-tan-redisxiu-gai-licenseshi-jian'>谈谈 Redis 修改 License 事件</a>

- <a href='https://huangz.blog/2024/post-redis-era.html'>欢迎进入后Redis时代——关于Redis修改许可之后的问题、现状和未来</a>


#### **2025年5月：回归AGPL许可证**
Redis Ltd.宣布将从8.0版开始再次将许可证更改为AGPL。这一决策的背后有几个关键因素：

**创始人antirez的回归**：根据[InfoQ的报道](https://www.infoq.cn/article/ev7mdrxasucv8wrjmb2c)，Redis之父antirez在2025年宣布"Redis再次开源"。antirez作为Redis的创始人和开源精神的代表，他的回归对Redis回归开源起到了关键的推动作用。这标志着Redis重新回到了开源文化的根源。

**社区压力的直接回应**：Linux基金会在2024年3月宣布将最后一个BSD许可版本的Redis分叉为Valkey项目，这是对Redis协议变更的直接反击。开源社区的不满和生态震动迫使Redis重新考虑其策略。

**商业策略的重新评估**：由于Valkey分叉项目的存在，Redis的协议变更实际上失去了意义——用户已经有了开源替代方案。继续坚持闭源策略反而可能加速用户流失。

**回归AGPL的战略意义**：
- **应对竞争威胁**：Valkey分叉项目已经成熟，Redis需要重新获得竞争优势
- **重新拥抱开源生态**：antirez本身就是开源精神的代表，Redis的成功很大程度上归功于开源社区的支持，没有必要放弃这块"肥肉"
- **创始人的价值观回归**：antirez的回归象征着Redis重新回到"开源优先"的价值观，这对社区和用户来说是一个重要的信任重建信号

- <a href='https://www.showapi.com/news/article/683a9eb24ddd79013c010b1d'>Redis 8.0版本更新：AGPLv3许可证转变的时机是否成熟？</a>

- <a href='https://www.infoq.cn/article/ev7mdrxasucv8wrjmb2c'>Redis 之父宣布“Redis 再次开源”！网友：骗我一次，算你狠；骗我两次，是我蠢</a>

- <a href='https://redis.ac.cn/docs/latest/develop/whats-new/8-0/'>Redis 开源版 Redis 8 中的最新动态</a>

- <a href='https://www.oschina.net/news/348326/redis-8-ga'>Redis 8 正式 GA</a>

---

### **协议演变总结与未来展望**

#### **Redis协议变更的完整轨迹**
从2009年到2025年，Redis的开源协议经历了从**完全开放**到**适度控制**再到**重新平衡**的完整演变：

**第一阶段（2009-2018年8月）**：完全开源时代
- 核心Redis：BSD许可证（最自由）
- Redis模块：AGPL许可证
- 策略：完全开放，依靠社区和商业服务盈利

**第二阶段（2018年8月-2024年3月）**：逐步收紧时代
- 2018年8月：模块改为Apache+Commons Clause
- 2019年2月：模块改为RSAL（更严格的商业限制）
- 核心Redis：仍保持BSD许可证
- 策略：模块商业化，核心保持开源

**第三阶段（2024年3月-2025年5月）**：全面闭源时代
- 核心Redis：改为SSPL+RSAL
- 策略：全面控制，应对云服务商"搭便车"

**第四阶段（2025年5月至今）**：重新平衡时代
- 核心Redis：回归AGPL许可证
- 策略：在开源精神与商业利益之间找到平衡点

#### **对开源生态的启示**
Redis的协议演变历程揭示了开源项目在现代商业环境中的生存智慧：

1. **平衡的艺术**：完全开放可能导致价值分配不均，过度控制可能破坏生态
2. **策略的灵活性**：不同发展阶段需要不同的协议策略
3. **社区的重要性**：最终Redis选择回归开源，体现了社区力量的不可忽视

#### **未来发展趋势**
- **协议标准化**：开源协议体系将更加完善，平衡各方利益
- **商业模式创新**：开源项目将探索更多可持续的盈利模式
- **社区治理优化**：开源项目的治理结构将更加民主和透明

Redis的回归开源不仅是一个技术决策，更是对整个开源生态健康发展的积极贡献。
