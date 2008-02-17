from image_repository import ImageRepo
from stream_name_cache import StreamNameCache
from sequences_cache import SequencesCache
from peers_cache import PeersCache

image_repo = ImageRepo()

g_last_stream_name_search = StreamNameCache()

g_stream_name_cache = StreamNameCache()

g_sequences_cache = SequencesCache()

g_peers_cache = PeersCache()