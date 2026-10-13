# 工程工具

## first-run.py

用于安装后自动检查 NEMU 内置镜像和 Verilator C++ 示例。日常交互实验使用 [日常实验](../docs/日常实验.md) 中的 Shell 入口。必须通过 YSYX 的 WSL 隔离入口调用。

```powershell
& ..\..\Tools\wsl-sandbox\sandbox.ps1 -Action Run -Command @('python3', '-B', 'tools/first-run.py')
```

以上命令在 YSYX/Main 目录执行；从 Workspace 根执行时，入口为 .\Tools\wsl-sandbox\sandbox.ps1。

- 默认检查两个组件；--component nemu 或 --component verilator 可只检查一个。
- 没有 NEMU 配置时，使用官方 Kconfig 默认值生成配置；已有配置不会重置。
- NEMU 通过 help、c、q 运行内置四指令镜像，以 GOOD TRAP、指令数和退出状态共同判定。
- Verilator 使用登记的 5.052 工具，复制随安装提供的 make_hello_c 官方源码到 YSYX/cache/first-run/verilator，以 -j1 构建并运行，检查 Hello World 输出。
- 工具不会实现课程中尚未完成的 CPU 或操作系统功能。

依赖、初始化与日志索引见 [开发环境](../docs/开发环境.md)。
## nvboard-startup.py

构建 NVBoard 上游 example，通过 WSLg 启动并观察 5 秒后终止进程。窗口关闭由检查工具发起，不是示例程序自行结束。此检查覆盖示例的编译和有限时启动，不验证拨码、键盘、VGA 等全部功能。

从 Workspace 根目录运行：

```powershell
& .\Tools\wsl-sandbox\sandbox.ps1 -Action Run -Gui -Command @('python3', '-B', 'tools/nvboard-startup.py')
```

普通运行不加 -Gui 时使用 SDL dummy 驱动；这个图形检查显式启用 WSLg X11 和软件渲染。
