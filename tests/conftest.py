import os
import tempfile

import pytest

# Force the offline engine and a throwaway database before the app is imported.
os.environ["MODEL_API_KEY"] = ""
os.environ["OPERATOR_ID"] = ""
os.environ["OPERATOR_KEY"] = ""
os.environ["DATABASE_PATH"] = os.path.join(tempfile.mkdtemp(), "app.db")


@pytest.fixture
def settings(tmp_path):
    from verichainx.config import Settings

    return Settings(model_api_key=None, operator_id=None, operator_key=None,
                    database_path=str(tmp_path / "test.db"))


@pytest.fixture
def service(settings):
    from verichainx.engine import MockEngine
    from verichainx.provenance import NullAnchorer
    from verichainx.service import VeriChainX
    from verichainx.store import Store

    return VeriChainX(settings, MockEngine(), Store(settings.database_path), NullAnchorer())


@pytest.fixture
def demo_items():
    from verichainx.demo import _inline_static_images, load_demo_listings

    return [(_inline_static_images(listing), seller) for listing, seller in load_demo_listings()]
