from typing import TYPE_CHECKING

from cozepy.auth import Auth
from cozepy.request import Requester

if TYPE_CHECKING:
    from .runs import WorkflowClient as WorkflowClientRuns


class WorkflowClient(object):
    def __init__(self, base_url: str, auth: Auth, requester: Requester):
        self._base_url = base_url
        self._auth = auth
        self._requester = requester
        self._runs = None

    @property
    def runs(self) -> "WorkflowClientRuns":
        if not self._runs:
            from .runs import WorkflowClient

            self._runs = WorkflowClient(self._base_url, self._auth, self._requester)
        return self._runs