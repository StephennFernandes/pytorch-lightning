import pickle

import tests.models.utils as tutils
from pytorch_lightning import Trainer
from tests.models import LightningTestModel


def test_testtube_logger(tmpdir):
    """Verify that basic functionality of test tube logger works."""
    tutils.reset_seed()
    hparams = tutils.get_hparams()
    model = LightningTestModel(hparams)

    logger = tutils.get_test_tube_logger(tmpdir, False)

    assert logger.name == 'lightning_logs'

    trainer_options = dict(
        default_save_path=tmpdir,
        max_epochs=1,
        train_percent_check=0.05,
        logger=logger
    )

    trainer = Trainer(**trainer_options)
    result = trainer.fit(model)

    assert result == 1, 'Training failed'


def test_testtube_pickle(tmpdir):
    """Verify that pickling a trainer containing a test tube logger works."""
    tutils.reset_seed()

    hparams = tutils.get_hparams()

    logger = tutils.get_test_tube_logger(tmpdir, False)
    logger.log_hyperparams(hparams)
    logger.save()

    trainer_options = dict(
        default_save_path=tmpdir,
        max_epochs=1,
        train_percent_check=0.05,
        logger=logger
    )

    trainer = Trainer(**trainer_options)
    pkl_bytes = pickle.dumps(trainer)
    trainer2 = pickle.loads(pkl_bytes)
    trainer2.logger.log_metrics({'acc': 1.0})
