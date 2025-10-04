# Eye2Eye Patient Data MCP Server

MCP (Model Context Protocol) server for accessing Eye2Eye optometry/ophthalmology patient data, prescriptions, appointments, inventory, and imaging through REST API endpoints.

## Features

- **Read-only access** to Eye2Eye backend API
- **23 MCP tools** covering:
  - Patient management (6 tools)
  - Prescriptions (2 tools)
  - Inventory (3 tools)
  - Retinal imaging (4 tools)
  - Appointments (2 tools)
  - Activities tracking (3 tools)
  - System diagnostics (3 tools)
- **Dual API support**: Separate configurable URLs for main API and appointments API
- **No authentication required** (simplified for internal use)
- Built with FastMCP and async httpx

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your API endpoints:
```env
EYE2EYE_API_BASE_URL=http://192.168.1.100:5005
EYE2EYE_APPOINTMENTS_API_BASE_URL=http://192.168.1.100:5006
```

## Usage

### Running the Server

```bash
python -m src.server
```

Or using mcp:
```bash
mcp run src/server.py
```

### Configuration

Set these environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `EYE2EYE_API_BASE_URL` | Main API base URL | `http://localhost:5005` |
| `EYE2EYE_APPOINTMENTS_API_BASE_URL` | Appointments API base URL | `http://localhost:5006` |
| `API_TIMEOUT` | Request timeout in seconds | `30` |

## Available Tools

### Patient Tools
- `get_all_patients()` - Retrieve all patient profiles
- `get_patient_by_id(patient_id)` - Get patient by ID
- `get_patient_by_name(first_name, last_name)` - Search by name
- `get_patients_by_birthday_month(month)` - Patients with birthdays in month (1-12)
- `get_patients_by_insurance_type(insurance_type)` - Filter by insurance
- `get_insurance_types()` - List all insurance types

### Prescription Tools
- `get_contact_prescriptions(patient_id)` - Contact lens prescriptions
- `get_frame_prescriptions(patient_id)` - Eyeglass frame prescriptions

### Inventory Tools
- `get_inventory()` - All frames and contacts inventory
- `get_frame_by_id(frame_id)` - Specific frame details
- `get_contact_by_id(contact_id)` - Specific contact lens details

### Imaging Tools
- `get_retinal_scans(customer_id)` - Retinal scan metadata
- `get_retinal_scan_image(filename)` - Retinal scan image file
- `get_patient_image(filename)` - Patient photo
- `get_frame_image(filename)` - Frame product image

### Appointments Tools (Separate API)
- `get_appointments(start_date, end_date)` - Appointments in date range (ISO 8601)
- `get_appointment_by_id(appointment_id)` - Single appointment details

### Activities Tools
- `get_recent_activities(limit)` - Recent activities (default: 4)
- `get_all_activities(limit)` - All activities with pagination (default: 50)
- `get_today_activities_count()` - Count of today's activities

### System Tools
- `get_system_health()` - Backend and database health check
- `get_system_version()` - System version information
- `get_connection_config()` - Database connection retry settings

## Project Structure

```
patients-api/
├── src/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── .env.example           # Environment variable template
├── pyproject.toml         # Project configuration
├── requirements.txt       # Python dependencies
├── CLAUDE.md             # Product requirements document
└── README.md             # This file
```

## Requirements

- Python >= 3.10
- mcp >= 0.9.0
- httpx >= 0.27.0
- python-dotenv >= 1.0.0

## Error Handling

All tools return structured error responses:

```json
{
  "error": "Error message",
  "status_code": 404,
  "type": "connection_error"
}
```

Error types:
- `validation_error` - Invalid parameters
- `connection_error` - Network/connection issues
- `unknown_error` - Unexpected errors

## Development

### Install dev dependencies:
```bash
pip install -e ".[dev]"
```

### Code formatting:
```bash
black src/
ruff check src/
```

## License

Internal use only - Eye2Eye Optometry System
