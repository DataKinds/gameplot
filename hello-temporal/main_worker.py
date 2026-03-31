from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

@activity.defn
async def my_epic_activity(n: int) -> str:
    o = ""
    for i in range(n):
        o += f"DA COUNTDOWN: {n-i}...\n"
    return o

@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, n: int) -> str:
        return await workflow.execute_activity(
            my_epic_activity, n
        )


async def main():
    client = await Client.connect("temporal:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="hello-task-queue", workflows=[HelloWorkflow], activities=[my_epic_activity]
    )
    await worker.run()
    print("Hello from hello-temporal!")


if __name__ == "__main__":
    asyncio.run(main())
