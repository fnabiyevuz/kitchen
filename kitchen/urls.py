from django.contrib import admin
from django.urls import path, include
from api.routers import router
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='API | kitchen')),
    path('schema/', get_schema_view(title="API", description="API for 5-street",), name="openapi-schema")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)