from demo.sample.models import Author

from unicef_snapshot.serializers import SnapshotModelSerializer


class AuthorSerializer(SnapshotModelSerializer):
    class Meta:
        model = Author
        fields = ("__all__")
