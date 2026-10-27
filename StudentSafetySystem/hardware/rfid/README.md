# RFID Hardware Adapter
Connect the actual RFID reader here. The adapter should POST verified tag reads to the backend with:
POST /api/events/
Example payload: {"kind":"RFID","title":"RFID detected","detail":"RFID-A01","severity":"INFO"}
