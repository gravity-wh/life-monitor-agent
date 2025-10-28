import json, time
from typing import Any, Dict, Tuple

MQTT_TOPIC_PREFIX = 'observations'

def topic_for(source_id: str) -> str:
    return f"{MQTT_TOPIC_PREFIX}/{source_id}"

class Serializer:
    def __init__(self) -> None:
        try:
            from life_monitor.proto import observation_pb2  # type: ignore
            self.pb = observation_pb2  # type: ignore
        except Exception:
            self.pb = None
    def build(self, source_id: str, kind: str, payload: Dict[str, Any], ts_ms: int | None = None, schema: str = 'v1'):
        ts = ts_ms if ts_ms is not None else int(time.time() * 1000)
        if self.pb is None:
            return { 'source_id': source_id, 'ts_ms': ts, 'schema': schema, 'kind': kind, 'payload': payload }
        obs = self.pb.Observation(); obs.source_id = source_id; obs.ts_ms = ts; obs.schema = schema
        if kind == 'image': obs.image.CopyFrom(self.pb.ImageObservation(**payload))
        elif kind == 'audio': obs.audio.CopyFrom(self.pb.AudioObservation(**payload))
        elif kind == 'wearable': obs.wearable.CopyFrom(self.pb.WearableObservation(**payload))
        elif kind == 'pc': obs.pc.CopyFrom(self.pb.PCObservation(**payload))
        elif kind == 'kv':
            msg = self.pb.KeyValue(); [msg.fields.__setitem__(str(k), str(v)) for k,v in (payload or {}).items()]; obs.kv.CopyFrom(msg)
        else: raise ValueError(f'Unknown kind: {kind}')
        return obs
    def dumps(self, obj) -> Tuple[bytes, str]:
        if self.pb is None: return (json.dumps(obj).encode('utf-8'), 'application/json')
        return (obj.SerializeToString(), 'application/x-protobuf')
    def loads(self, data: bytes) -> Dict[str, Any]:
        if self.pb is None: return json.loads(data.decode('utf-8'))
        obs = self.pb.Observation(); obs.ParseFromString(data)
        out: Dict[str, Any] = { 'source_id': obs.source_id, 'ts_ms': obs.ts_ms, 'schema': obs.schema }
        which = obs.WhichOneof('payload'); out['kind'] = which or 'unknown'
        if which == 'image': out['payload'] = { 'activity': obs.image.activity, 'confidence': obs.image.confidence }
        elif which == 'audio': out['payload'] = { 'transcript': obs.audio.transcript, 'guitar_detected': obs.audio.guitar_detected, 'speech_confidence': obs.audio.speech_confidence }
        elif which == 'wearable': out['payload'] = { 'heart_rate': obs.wearable.heart_rate, 'steps': obs.wearable.steps, 'stress': obs.wearable.stress }
        elif which == 'pc': out['payload'] = { 'active_app': obs.pc.active_app, 'active_window': obs.pc.active_window }
        elif which == 'kv': out['payload'] = dict(obs.kv.fields)
        else: out['payload'] = {}
        return out
