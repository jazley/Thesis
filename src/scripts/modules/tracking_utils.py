import numpy as np
from typing import List
from supervision.tools.detections import Detections
from yolox.tracker.byte_tracker import STrack
from onemetric.cv.utils.iou import box_iou_batch

class TrackingUtils():

    def __init__(self) -> None:
        pass

    # converts Detections into format that can be consumed by match_detections_with_tracks function
    def detections2boxes(self, detections: Detections) -> np.ndarray:
        return np.hstack((
            detections.xyxy,
            detections.confidence[:, np.newaxis]
        ))

    # converts List[STrack] into format that can be consumed by match_detections_with_tracks function
    def tracks2boxes(self, tracks: List[STrack]) -> np.ndarray:
        return np.array([
            track.tlbr
            for track
            in tracks
        ], dtype=float)

    # matches our bounding boxes with predictions
    def match_detections_with_tracks(
        self,
        detections: Detections,
        tracks: List[STrack]
    ) -> Detections:
        if not np.any(detections.xyxy) or len(tracks) == 0:
            return np.empty((0,))

        tracks_boxes = self.tracks2boxes(tracks=tracks)
        iou = box_iou_batch(tracks_boxes, detections.xyxy)
        track2detection = np.argmax(iou, axis=1)

        tracker_ids = [None] * len(detections)

        for tracker_index, detection_index in enumerate(track2detection):
            if iou[tracker_index, detection_index] != 0:
                tracker_ids[detection_index] = tracks[tracker_index].track_id

        return tracker_ids