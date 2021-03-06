# third party
import pytest
import torch as th

# syft absolute
import syft as sy


def test_searchable_pointable() -> None:
    bob = sy.VirtualMachine(name="Bob")
    root_client = bob.get_root_client()

    with pytest.deprecated_call():
        x_ptr = th.Tensor([1, 2, 3]).send(root_client, searchable=True)

    assert x_ptr.pointable is True

    with pytest.deprecated_call():
        assert x_ptr.searchable is True

    with pytest.deprecated_call():
        x_ptr.searchable = False
        assert x_ptr.searchable is False
