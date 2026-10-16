# System Architecture

Users -> Web UI (HTML/CSS/JavaScript/Bootstrap) -> Django Backend -> MySQL

Django Backend integrates with:
- Log/Event ingestion and preprocessing
- ML module: Isolation Forest anomaly detection + Random Forest classification
- Severity assessment and defensive recommendations
- Incident and alert management
- Reports
- AI Security Assistant using stored incident data

For the academic prototype, network/device data can be simulated from the supplied synthetic dataset. The system does not perform offensive actions.
