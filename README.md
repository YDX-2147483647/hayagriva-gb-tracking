# Hayagriva对GB/T 7714—2015的支持情况

测试结果见[网页][gh-pages]。

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fydx-2147483647.github.io%2Fhayagriva-gb-tracking%2F)][gh-pages]

[gh-pages]: https://ydx-2147483647.github.io/hayagriva-gb-tracking/

## 历史记录策略

历史测试结果存于[`history.toml`](./history.toml)，按Hayagriva版本顺序（不同于实际测试顺序）排列。

由于测试结果已较稳定，以后只记录正式发布版Hayagriva的测试结果，但既有结果仍保留。

## 开发

本项目包含三部分，其中编译、测试Hayagriva两部分需要共用python虚拟环境。以下使用[uv](https://docs.astral.sh/uv/)管理虚拟环境，但使用`python -m venv/pip`自行管理亦可。

### 编译Hayagriva

`maturin develop`会将rust库`hayagriva`编译成python包，供后续步骤调用。

此步需要rust工具链；如无条件，可跳过此步，转而[从 GitHub Actions 下载编译好的`hayagriva-py-wheels-*`](https://github.com/YDX-2147483647/hayagriva-gb-tracking/actions/workflows/build.yaml)，解压，然后`uv pip install path/to/hayagriva_py-*.whl`。

开发本项目用的maturin通过`uv tool install maturin`安装，版本为1.10.2。[其它安装方法](https://www.maturin.rs/installation.html)、其它版本的maturin应该也可使用。

```shell
uv venv
maturin develop --release
```

本仓库`Cargo.toml`设置的Hayagriva是其主分支最新版。如欲测试其它版本，可用如下命令切换。具体请参考 [Specifying dependencies from `git` repositories - The Cargo Book](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-dependencies-from-git-repositories)。注意切换时可能需要同步更新后续步骤需要的日期信息，详见[`history_data.ts`](./website/plugins/history_data.ts)中的注释。

```shell
cargo add --git https://github.com/typst/hayagriva [--branch main] / [--tag vX.Y.Z] / …
```

### 测试Hayagriva

`uv run -m tracking`会运行python模块`tracking`，调用上一步编译好的Hayagriva，生成参考文献，并与对照组比较。

```shell
uv run -m tracking --show-details
```

默认不会把结果记录进`history.toml`。如需更新历史，请如下指定`--update-history`。

```shell
uv run -m tracking --update-history history.toml
```

此步有缓存，位于``target/tracking-cache/`。

### 展示测试结果

`pnpm dev`会读取上一步生成的`history.toml`，在网页上展示出来。

此步需要node.js工具链。

```shell
cd website
pnpm install
pnpm dev --open
```

如果运行过上一步（并且未指定`--no-save-output`），那么当时缓存的`{expected,actual}-output.txt`还会被当作`history.toml`最后一个版本的输出，显示到网页上。
