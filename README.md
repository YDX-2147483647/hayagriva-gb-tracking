# Hayagriva对GB/T 7714—2015的支持情况

测试结果见网页。

## 开发

```shell
uv tool install maturin

uv venv
maturin develop --release

uv run -m tracking --show-details
```

`maturin develop`会编译hayagriva供python调用。此步需要rust工具链；如无条件，可[从 GitHub Actions 下载编译好的`hayagriva-py-wheels-*`](https://github.com/YDX-2147483647/hayagriva-gb-tracking/actions/workflows/build.yaml)，解压，然后`uv pip install path/to/hayagriva_py-*.whl`。
