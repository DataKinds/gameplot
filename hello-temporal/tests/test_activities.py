import uuid

import pytest

from temporalio import activity
from temporalio.worker import Worker
from temporalio.testing import WorkflowEnvironment

from main_worker import my_epic_activity, HelloWorkflow

@pytest.mark.asyncio
async def test_execute_workflow():
    task_queue_name = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[HelloWorkflow],
            activities=[my_epic_activity],
        ):
            assert "Hello, World!" == await env.client.execute_workflow(
                HelloWorkflow.run,
                15,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )