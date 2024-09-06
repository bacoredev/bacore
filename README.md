# bacore
Bacore is a business analysis and test automation framework. It is written in Python and is available through
[pypi.org](https://pypi.org/project/bacore/).

Documentation is available at [bacore.dev](https://bacore.dev).

It is *very* early days for bacore, and the developers would ask you to let it "cook" for a bit longer before trying it
out.


## Maturin Builds

- Mac: `maturin build --release`
- Linux ARM: `docker run --rm -v $(pwd):/io ghcr.io/pyo3/maturin build --release --manylinux 2014`
- Linux AMD: `maturin build --release --manylinux 2014`
- Windows AMD: `maturin build --release --target x86_64-pc-windows-msvc -i python3.12`