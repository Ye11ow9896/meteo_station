from pydantic import BaseModel


class MeteoStation(BaseModel):
    id: int
    id_user: int
    name: str
    lat: float
    lon: float
    has_video_server: bool
    video_server_ip: str
    video_server_port: str
    video_server_stream_path: str
    has_timelapse: bool
    video_server_snapshot_path: str
    os_login: str
    os_password_hash: str
