import hashlib

import json
import asyncio
import datetime

import django_rq

from rq_scheduler import Scheduler

from django.core.management.base import BaseCommand
from django.conf import settings

from ... import service as management_sv


TARGET_JOBS = [
    {
        'func': management_sv.ping_domain,
        'args': (settings.SERVICE_HOST,),
        'kwargs': {},
        'interval': 10,
        'result_ttl': 10,
    }
]

rq_scheduler = Scheduler(
    connection=django_rq.get_connection(), queue_name="default", interval=5
)


def generate_job_id(job_definition: dict) -> str:
    metadata = job_definition.copy()
    metadata["func"] = metadata["func"].__name__
    print(metadata)
    return hashlib.sha1(json.dumps(metadata, sort_keys=True).encode()).hexdigest()


def schedule(kwargs):
    rq_scheduler.schedule(
        scheduled_time=datetime.datetime.now(), id=generate_job_id(kwargs), **kwargs
    )


class Command(BaseCommand):
    help = 'schedule'

    def handle(self, *args, **options):
        asyncio.run(self._main())

    async def _main(self, *args):
        scheduler = rq_scheduler
        registered_jobs = {job.id: job for job in scheduler.get_jobs()}
        defined_jobs = {generate_job_id(job): job for job in TARGET_JOBS}
        jobs_to_cleanup_ids = set(registered_jobs.keys()) - set(defined_jobs.keys())
        jobs_to_register_ids = set(defined_jobs.keys()) - set(registered_jobs.keys())
        all_jobs = {}
        all_jobs.update(registered_jobs)
        all_jobs.update(defined_jobs)

        for job_id in jobs_to_cleanup_ids:
            job = all_jobs[job_id]
            print(f'{job_id=} delete')
            scheduler.cancel(job)
            job.delete()

        for job_id in jobs_to_register_ids:
            job = all_jobs[job_id]
            print(f'{job_id=} {job["func"]} register')
            schedule(job)



