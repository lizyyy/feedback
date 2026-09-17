# feedback — Code Sense 评测题只读仓库

每道 Code Sense 题的**模型可见只读仓库**各放一个分支（分支名 = 题号小写）。这里只有 `environment/workspace/repo` 的内容；题包的 solution/ 与 tests/ 不在本仓库。

| 分支 | 题号 | 题目 | 底座 | 许可证 |
|---|---|---|---|---|
| [cs-001](https://github.com/lizyyy/feedback/tree/cs-001) | CS-001 v1.1.0 | 内部 Scrapy 分支：dpipe 超时解析接口迁移复核 | scrapy/scrapy main 2026-09-17 快照 + 自撰 dpipe/（含上游 downloadtimeout.py / retry.py 两处补丁） | BSD-3-Clause |

| [cs-002](https://github.com/lizyyy/feedback/tree/cs-002) | CS-002 | 内部 Sphinx 分支：docmill 增量缓存跨进程失效排查 | sphinx-doc/sphinx main 2026-09-17 快照 + 自撰 docmill/（含上游 builders/html 一处补丁） | BSD-2-Clause |

| [cs-003](https://github.com/lizyyy/feedback/tree/cs-003) | CS-003 | 内部 zarr 分支：chunkforge 折叠后读到错版本数据 | zarr-developers/zarr-python main 2026-09-17 快照 + 自撰 chunkforge/（上游一行未改） | MIT |

取用：`git clone --depth 1 --branch cs-001 https://github.com/lizyyy/feedback.git`
