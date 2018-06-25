from unicef_snapshot.serializers import SnapshotModelSerializer

from demo.sample.models import Author


class AuthorSerializer(SnapshotModelSerializer):
    class Meta:
        model = Author
        fields = ("__all__")
