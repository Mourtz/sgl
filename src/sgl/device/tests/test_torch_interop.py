# SPDX-License-Identifier: Apache-2.0

import sgl
import sys
import pytest
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).parent))
import sglhelpers as helpers


@pytest.mark.parametrize("device_type", helpers.DEFAULT_DEVICE_TYPES)
def test_torch_interop(device_type):
    try:
        import torch
    except ImportError:
        pytest.skip("torch is not installed")

    device = sgl.Device(
        type=device_type,
        enable_debug_layers=True,
        enable_cuda_interop=True,
        compiler_options={"include_paths": [Path(__file__).parent]},
    )

    if not device.supports_cuda_interop:
        pytest.skip(f"CUDA interop is not supported on this device type {device_type}")

    program = device.load_program("test_torch_interop.slang", ["main"])
    kernel = device.create_compute_kernel(program)

    # Create a torch CUDA device
    torch_device = torch.device("cuda:0")

    # Create some torch CUDA tensors
    a = torch.linspace(0, 1023, 1024, device=torch_device, dtype=torch.float32)
    b = torch.linspace(1024, 1, 1024, device=torch_device, dtype=torch.float32)
    c = torch.zeros(1024, device=torch_device, dtype=torch.float32)

    # Dispatch compute kernel
    # (CUDA tensors are internally copied to/from sgl buffers)
    kernel.dispatch([1024, 1, 1], vars={"a": a, "b": b, "c": c})

    # Check result
    assert torch.all(c == a + b)


@pytest.mark.parametrize("device_type", helpers.DEFAULT_DEVICE_TYPES)
def test_buffer_to_torch(device_type):
    try:
        import torch
    except ImportError:
        pytest.skip("torch is not installed")

    device = sgl.Device(
        type=device_type,
        enable_debug_layers=True,
        enable_cuda_interop=True,
        compiler_options={"include_paths": [Path(__file__).parent]},
    )

    if not device.supports_cuda_interop:
        pytest.skip(f"CUDA interop is not supported on this device type {device_type}")

    data = np.linspace(0, 15, 16, dtype=np.float32)
    buffer = device.create_buffer(
        size=4 * 16,
        usage=sgl.ResourceUsage.shared,
        data=data,
    )
    tensor1 = buffer.to_torch(type=sgl.DataType.float32)
    assert tensor1.shape == (16,)
    assert torch.all(
        tensor1 == torch.tensor(data, dtype=torch.float32, device="cuda:0")
    )

    tensor2 = buffer.to_torch(type=sgl.DataType.float32, shape=[4, 4])
    assert tensor2.shape == (4, 4)
    assert torch.all(
        tensor2
        == torch.tensor(np.reshape(data, [4, 4]), dtype=torch.float32, device="cuda:0")
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
