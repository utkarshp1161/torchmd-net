import pytest
from pytest import mark
import torch
import pytorch_lightning as pl
from torchmdnet import models
from torchmdnet.models.model import create_model
from torchmdnet.priors import Atomref, D2
from torch_scatter import scatter
from utils import load_example_args, create_example_batch, DummyDataset


@mark.parametrize("model_name", models.__all__)
def test_atomref(model_name):
    dataset = DummyDataset(has_atomref=True)
    atomref = Atomref(max_z=100, dataset=dataset)
    z, pos, batch = create_example_batch()

    # create model with atomref
    pl.seed_everything(1234)
    model_atomref = create_model(
        load_example_args(model_name, prior_model="Atomref"), prior_model=atomref
    )
    # create model without atomref
    pl.seed_everything(1234)
    model_no_atomref = create_model(load_example_args(model_name, remove_prior=True))

    # get output from both models
    x_atomref, _ = model_atomref(z, pos, batch)
    x_no_atomref, _ = model_no_atomref(z, pos, batch)

    # check if the output of both models differs by the expected atomref contribution
    expected_offset = scatter(dataset.get_atomref().squeeze()[z], batch).unsqueeze(1)
    torch.testing.assert_allclose(x_atomref, x_no_atomref + expected_offset)


def test_d2():

    prior = D2()

    y1 = torch.tensor([0.0, 0.0, 0.0])
    z = torch.tensor([1, 8, 8, 1, 1, 8, 1])
    pos = torch.tensor(
        [
            [0.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 4.0, 0.0],
            [2.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, 0.0, 2.0],
        ]
    )
    batch = torch.tensor([0, 0, 1, 1, 2, 2, 2])

    y2 = prior.post_reduce(y1, z, pos, batch)
    assert torch.isclose(y2[0], y[1])
