class AsyncMixin:
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create_coro(*args, **kwargs):
            return await model_class.objects.acreate(*args, **kwargs)

        return create_coro(*args, **kwargs)
